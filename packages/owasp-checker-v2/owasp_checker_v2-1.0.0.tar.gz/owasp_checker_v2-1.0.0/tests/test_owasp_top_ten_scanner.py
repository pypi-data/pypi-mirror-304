#!/usr/bin/env python3
"""
Tests for the OWASPTopTenScanner class.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from urllib.parse import urlparse

from owasp_checker_v2.owasp_top_ten_scanner import OWASPTopTenScanner

@pytest.fixture
def scanner():
    """Create a test instance of OWASPTopTenScanner"""
    return OWASPTopTenScanner('http://localhost:8080')

@pytest.fixture
def mock_zap_response():
    """Create mock ZAP API response"""
    return {
        'scan': '1',
        'alerts': [
            {
                'name': 'SQL Injection',
                'risk': 'High',
                'confidence': 'Medium',
                'description': 'SQL injection vulnerability found',
                'solution': 'Use parameterized queries',
                'url': 'http://example.com/test',
                'param': 'id',
                'evidence': "' OR '1'='1",
                'cvssScore': '8.5'
            },
            {
                'name': 'Cross Site Scripting (XSS)',
                'risk': 'Medium',
                'confidence': 'High',
                'description': 'XSS vulnerability found',
                'solution': 'Sanitize user input',
                'url': 'http://example.com/test',
                'param': 'comment',
                'evidence': '<script>alert(1)</script>',
                'cvssScore': '6.5'
            }
        ]
    }

def test_initialization(scanner):
    """Test OWASPTopTenScanner initialization"""
    assert scanner.zap_proxy_address == 'http://localhost:8080'
    assert not scanner.test_mode

def test_enable_test_mode(scanner):
    """Test enabling test mode"""
    scanner.enable_test_mode()
    assert scanner.test_mode

def test_scan_url_test_mode(scanner):
    """Test URL scanning in test mode"""
    scanner.enable_test_mode()
    results = scanner.scan_url('http://example.com')
    
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Verify vulnerability structure
    vuln = results[0]
    assert 'name' in vuln
    assert 'risk' in vuln
    assert 'confidence' in vuln
    assert 'description' in vuln
    assert 'solution' in vuln
    assert 'url' in vuln
    assert 'cvss_score' in vuln

def test_scan_url_with_types(scanner):
    """Test URL scanning with specific vulnerability types"""
    scanner.enable_test_mode()
    results = scanner.scan_url(
        'http://example.com',
        vulnerability_types=['sql_injection', 'xss']
    )
    
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Verify vulnerabilities match requested types
    for vuln in results:
        assert any(vtype in vuln['name'].lower() 
                  for vtype in ['sql injection', 'xss'])

@patch('requests.get')
def test_start_scan(mock_get, scanner):
    """Test starting a new scan"""
    # Mock ZAP API response
    mock_response = Mock()
    mock_response.json.return_value = {'scan': '1'}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    scan_id = scanner._start_scan('http://example.com')
    assert scan_id == '1'

@patch('requests.get')
def test_wait_for_scan_completion(mock_get, scanner):
    """Test waiting for scan completion"""
    # Mock ZAP API responses
    responses = [
        {'status': '50'},   # 50% complete
        {'status': '75'},   # 75% complete
        {'status': '100'}   # 100% complete
    ]
    mock_get.side_effect = [
        Mock(json=lambda: resp, raise_for_status=Mock())
        for resp in responses
    ]
    
    # Should complete without raising exceptions
    scanner._wait_for_scan_completion('1')

@patch('requests.get')
def test_get_scan_results(mock_get, scanner, mock_zap_response):
    """Test getting scan results"""
    # Mock ZAP API response
    mock_response = Mock()
    mock_response.json.return_value = mock_zap_response
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    results = scanner._get_scan_results('1')
    assert isinstance(results, list)
    assert len(results) == 2
    
    # Verify result structure
    result = results[0]
    assert result['name'] == 'SQL Injection'
    assert result['risk'] == 'High'
    assert result['cvss_score'] == '8.5'

def test_url_validation(scanner):
    """Test URL validation"""
    # Test with invalid URLs
    with pytest.raises(ValueError):
        scanner.scan_url('')
    
    with pytest.raises(ValueError):
        scanner.scan_url('invalid-url')
    
    with pytest.raises(ValueError):
        scanner.scan_url('ftp://example.com')  # Non-HTTP protocol
    
    # Test with valid URLs
    scanner.enable_test_mode()
    assert scanner.scan_url('http://example.com') is not None
    assert scanner.scan_url('https://example.com') is not None

def test_cache_management(scanner):
    """Test cache management functionality"""
    scanner.enable_test_mode()
    
    # Initial scan
    results1 = scanner.scan_url('http://example.com')
    
    # Should use cached results
    results2 = scanner.scan_url('http://example.com')
    assert results1 == results2
    
    # Clear cache
    scanner.clear_cache()
    assert len(scanner.cache) == 0
    
    # Should perform new scan
    results3 = scanner.scan_url('http://example.com')
    assert results3 is not None

@patch('requests.get')
def test_error_handling(mock_get, scanner):
    """Test error handling"""
    # Mock network error
    mock_get.side_effect = Exception('Network error')
    
    # Should handle error gracefully
    results = scanner.scan_url('http://example.com')
    assert isinstance(results, list)
    assert len(results) == 0

def test_mock_results(scanner):
    """Test mock results structure"""
    scanner.enable_test_mode()
    results = scanner._get_mock_results()
    
    assert isinstance(results, list)
    assert len(results) == 2
    
    # Verify mock vulnerability structure
    vuln = results[0]
    assert all(key in vuln for key in [
        'name', 'risk', 'confidence', 'description', 'solution',
        'url', 'param', 'evidence', 'cvss_score'
    ])

def test_vulnerability_filtering(scanner):
    """Test vulnerability type filtering"""
    scanner.enable_test_mode()
    
    # Test with single vulnerability type
    results = scanner.scan_url(
        'http://example.com',
        vulnerability_types=['sql_injection']
    )
    assert all('sql injection' in vuln['name'].lower() for vuln in results)
    
    # Test with multiple vulnerability types
    results = scanner.scan_url(
        'http://example.com',
        vulnerability_types=['sql_injection', 'xss']
    )
    assert all(any(vtype in vuln['name'].lower() 
                  for vtype in ['sql injection', 'xss'])
              for vuln in results)
    
    # Test with invalid vulnerability type
    results = scanner.scan_url(
        'http://example.com',
        vulnerability_types=['invalid_type']
    )
    assert len(results) == 0

if __name__ == '__main__':
    pytest.main([__file__])
