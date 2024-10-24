#!/usr/bin/env python3
"""
Tests for the OWASPChecker class.
"""

import os
import json
from datetime import datetime
import pytest
from unittest.mock import Mock, patch

from owasp_checker_v2 import OWASPChecker

@pytest.fixture
def checker():
    """Create a test instance of OWASPChecker"""
    checker = OWASPChecker(
        zap_proxy_address='http://localhost:8080',
        nvd_api_key='test-nvd-key',
        vt_api_key='test-vt-key'
    )
    checker.enable_test_mode()
    return checker

def test_initialization():
    """Test OWASPChecker initialization"""
    checker = OWASPChecker()
    assert checker.zap_proxy_address == 'http://localhost:8080'
    assert checker.nvd_api_key is None
    assert checker.vt_api_key is None
    assert not checker.test_mode

def test_enable_test_mode(checker):
    """Test enabling test mode"""
    assert checker.test_mode
    assert checker.scanner.test_mode
    assert checker.dependency_checker.test_mode
    assert checker.threat_intelligence.test_mode

def test_scan_url(checker):
    """Test URL scanning functionality"""
    results = checker.scan_url('http://example.com')
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Verify vulnerability structure
    vuln = results[0]
    assert 'name' in vuln
    assert 'risk' in vuln
    assert 'confidence' in vuln
    assert 'description' in vuln
    assert 'solution' in vuln
    assert 'cvss_score' in vuln

def test_scan_url_with_types(checker):
    """Test URL scanning with specific vulnerability types"""
    results = checker.scan_url(
        'http://example.com',
        vulnerability_types=['sql_injection', 'xss']
    )
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Verify vulnerabilities match requested types
    for vuln in results:
        assert any(vtype in vuln['name'].lower() 
                  for vtype in ['sql injection', 'xss'])

def test_check_dependencies(checker):
    """Test dependency checking functionality"""
    # Create a temporary requirements file
    with open('test_requirements.txt', 'w') as f:
        f.write('requests==2.25.0\ndjango==3.1.0')

    try:
        results = checker.check_dependencies('test_requirements.txt')
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Verify vulnerability structure
        vuln = results[0]
        assert 'name' in vuln
        assert 'cve_id' in vuln
        assert 'version' in vuln
        assert 'ecosystem' in vuln
        assert 'cvss_score' in vuln
        assert 'severity' in vuln

    finally:
        # Clean up
        os.remove('test_requirements.txt')

def test_run_full_check(checker):
    """Test comprehensive security check"""
    # Create a temporary requirements file
    with open('test_requirements.txt', 'w') as f:
        f.write('requests==2.25.0\ndjango==3.1.0')

    try:
        results = checker.run_full_check(
            url='http://example.com',
            dependency_file='test_requirements.txt',
            vulnerability_types=['sql_injection', 'xss']
        )
        
        assert isinstance(results, dict)
        assert 'scan_time' in results
        assert 'vulnerabilities' in results
        assert 'guidelines' in results
        
        # Verify scan time format
        datetime.fromisoformat(results['scan_time'])
        
        # Verify vulnerabilities
        assert isinstance(results['vulnerabilities'], list)
        assert len(results['vulnerabilities']) > 0
        
        # Verify guidelines
        assert isinstance(results['guidelines'], dict)
        assert 'OWASP Top Ten' in results['guidelines']

    finally:
        # Clean up
        os.remove('test_requirements.txt')

def test_get_remediation_steps(checker):
    """Test remediation steps retrieval"""
    vulnerability = {
        'name': 'SQL Injection',
        'risk': 'High',
        'confidence': 'Medium',
        'description': 'SQL injection vulnerability found',
        'solution': 'Use parameterized queries',
        'references': ['https://example.com/sql-injection']
    }
    
    remediation = checker.get_remediation_steps(vulnerability)
    assert isinstance(remediation, dict)
    assert 'vulnerability' in remediation
    assert 'steps' in remediation
    assert 'references' in remediation
    assert 'guidelines' in remediation

def test_cache_management(checker):
    """Test cache management functionality"""
    # Initial scan
    results1 = checker.scan_url('http://example.com')
    
    # Should use cached results
    results2 = checker.scan_url('http://example.com')
    assert results1 == results2
    
    # Clear cache
    checker.clear_cache()
    
    # Should perform new scan
    results3 = checker.scan_url('http://example.com')
    assert results3 is not None

def test_error_handling(checker):
    """Test error handling"""
    # Test with invalid URL
    with pytest.raises(ValueError):
        checker.scan_url('invalid-url')
    
    # Test with non-existent dependency file
    with pytest.raises(FileNotFoundError):
        checker.check_dependencies('nonexistent.txt')

@patch('requests.get')
def test_api_error_handling(mock_get, checker):
    """Test API error handling"""
    # Mock API error
    mock_get.side_effect = Exception('API Error')
    
    # Should handle error gracefully
    results = checker.scan_url('http://example.com')
    assert isinstance(results, list)
    assert len(results) == 0

def test_input_validation(checker):
    """Test input validation"""
    # Test with empty URL
    with pytest.raises(ValueError):
        checker.scan_url('')
    
    # Test with None URL
    with pytest.raises(ValueError):
        checker.scan_url(None)
    
    # Test with invalid vulnerability types
    results = checker.scan_url(
        'http://example.com',
        vulnerability_types=['invalid_type']
    )
    assert isinstance(results, list)
    assert len(results) == 0

def test_performance(checker):
    """Test performance with multiple scans"""
    urls = [
        'http://example1.com',
        'http://example2.com',
        'http://example3.com'
    ]
    
    start_time = datetime.now()
    
    for url in urls:
        results = checker.scan_url(url)
        assert isinstance(results, list)
    
    duration = datetime.now() - start_time
    assert duration.total_seconds() < 10  # Should complete within 10 seconds

if __name__ == '__main__':
    pytest.main([__file__])
