#!/usr/bin/env python3
"""
Tests for the ThreatIntelligenceChecker class.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from owasp_checker_v2.threat_intelligence_checker import ThreatIntelligenceChecker

@pytest.fixture
def checker():
    """Create a test instance of ThreatIntelligenceChecker"""
    return ThreatIntelligenceChecker(vt_api_key='test-api-key')

@pytest.fixture
def sample_vulnerabilities():
    """Create sample vulnerability data for testing"""
    return [
        {
            'name': 'SQL Injection',
            'cve_id': 'CVE-2023-12345',
            'description': 'SQL injection vulnerability',
            'solution': 'Use parameterized queries'
        },
        {
            'name': 'XSS',
            'cve_id': 'CVE-2023-67890',
            'description': 'Cross-site scripting vulnerability',
            'solution': 'Sanitize user input'
        }
    ]

@pytest.fixture
def mock_vt_response():
    """Create mock VirusTotal API response"""
    return {
        'data': [
            {
                'attributes': {
                    'last_analysis_stats': {
                        'malicious': 10,
                        'suspicious': 5,
                        'undetected': 40
                    },
                    'last_submission_date': 1706140800  # 2024-01-25
                }
            }
        ]
    }

def test_initialization(checker):
    """Test ThreatIntelligenceChecker initialization"""
    assert checker.vt_api_key == 'test-api-key'
    assert checker.vt_api_url == "https://www.virustotal.com/api/v3"
    assert not checker.test_mode

def test_enable_test_mode(checker):
    """Test enabling test mode"""
    checker.enable_test_mode()
    assert checker.test_mode

def test_enrich_vulnerability_data_test_mode(checker, sample_vulnerabilities):
    """Test vulnerability data enrichment in test mode"""
    checker.enable_test_mode()
    results = checker.enrich_vulnerability_data(sample_vulnerabilities)
    
    assert isinstance(results, list)
    assert len(results) == len(sample_vulnerabilities)
    
    # Verify enriched data structure
    enriched = results[0]
    assert 'exploitation_risk' in enriched
    assert 'active_exploits' in enriched
    assert 'last_seen' in enriched
    assert 'detection_ratio' in enriched

@patch('requests.get')
def test_get_threat_intelligence(mock_get, checker, mock_vt_response):
    """Test getting threat intelligence data"""
    # Mock VirusTotal API response
    mock_response = Mock()
    mock_response.json.return_value = mock_vt_response
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    vulnerability = {
        'name': 'Test Vulnerability',
        'cve_id': 'CVE-2023-12345'
    }
    
    threat_data = checker._get_threat_intelligence(vulnerability)
    assert isinstance(threat_data, dict)
    assert threat_data['exploitation_risk'] == 'High'  # Based on detection ratio
    assert threat_data['active_exploits'] is True
    assert threat_data['detection_ratio'] == '10/55'
    assert threat_data['last_seen'] == '2024-01-25'

def test_calculate_risk_level(checker):
    """Test risk level calculation"""
    assert checker._calculate_risk_level(35, 50) == 'Critical'  # 70%
    assert checker._calculate_risk_level(20, 50) == 'High'      # 40%
    assert checker._calculate_risk_level(10, 50) == 'Medium'    # 20%
    assert checker._calculate_risk_level(5, 50) == 'Low'        # 10%
    assert checker._calculate_risk_level(0, 0) == 'Unknown'     # No data

def test_get_default_threat_data(checker):
    """Test default threat data"""
    data = checker._get_default_threat_data()
    assert data['exploitation_risk'] == 'Unknown'
    assert data['active_exploits'] is False
    assert data['last_seen'] is None
    assert data['detection_ratio'] == '0/0'

def test_cache_management(checker):
    """Test cache management functionality"""
    checker.enable_test_mode()
    
    # Initial enrichment
    results1 = checker.enrich_vulnerability_data([{
        'name': 'Test Vulnerability',
        'cve_id': 'CVE-2023-12345'
    }])
    
    # Should use cached results
    results2 = checker.enrich_vulnerability_data([{
        'name': 'Test Vulnerability',
        'cve_id': 'CVE-2023-12345'
    }])
    assert results1 == results2
    
    # Clear cache
    checker.clear_cache()
    assert len(checker.cache) == 0
    
    # Should perform new enrichment
    results3 = checker.enrich_vulnerability_data([{
        'name': 'Test Vulnerability',
        'cve_id': 'CVE-2023-12345'
    }])
    assert results3 is not None

@patch('requests.get')
def test_error_handling(mock_get, checker):
    """Test error handling"""
    # Mock API error
    mock_get.side_effect = Exception('API Error')
    
    vulnerability = {
        'name': 'Test Vulnerability',
        'cve_id': 'CVE-2023-12345'
    }
    
    # Should return default data on error
    threat_data = checker._get_threat_intelligence(vulnerability)
    assert threat_data['exploitation_risk'] == 'Unknown'
    assert threat_data['active_exploits'] is False

def test_mock_enriched_data(checker):
    """Test mock enriched data structure"""
    checker.enable_test_mode()
    vulnerabilities = [{
        'name': 'Test Vulnerability',
        'cve_id': 'CVE-2023-12345'
    }]
    
    results = checker._get_mock_enriched_data(vulnerabilities)
    assert isinstance(results, list)
    assert len(results) == 1
    
    # Verify mock data structure
    enriched = results[0]
    assert enriched['exploitation_risk'] == 'High'
    assert enriched['active_exploits'] is True
    assert enriched['last_seen'] == '2024-01-24'
    assert enriched['detection_ratio'] == '10/55'

def test_empty_input(checker):
    """Test handling of empty input"""
    assert checker.enrich_vulnerability_data([]) == []

def test_missing_fields(checker):
    """Test handling of vulnerabilities with missing fields"""
    vulnerabilities = [
        {'name': 'Incomplete Vuln'},  # Missing CVE ID
        {'cve_id': 'CVE-2023-12345'}  # Missing name
    ]
    
    checker.enable_test_mode()
    results = checker.enrich_vulnerability_data(vulnerabilities)
    assert len(results) == 2
    for result in results:
        assert 'exploitation_risk' in result
        assert 'active_exploits' in result
        assert 'last_seen' in result
        assert 'detection_ratio' in result

if __name__ == '__main__':
    pytest.main([__file__])
