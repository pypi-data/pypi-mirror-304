#!/usr/bin/env python3
"""
Tests for the RiskPrioritizer class.
"""

import pytest
from owasp_checker_v2.risk_prioritizer import RiskPrioritizer, RiskFactors

@pytest.fixture
def prioritizer():
    """Create a test instance of RiskPrioritizer"""
    return RiskPrioritizer()

@pytest.fixture
def sample_vulnerabilities():
    """Create sample vulnerability data for testing"""
    return [
        {
            'name': 'SQL Injection',
            'cvss_score': 8.5,
            'exploitation_risk': 'High',
            'active_exploits': True,
            'confidence': 'High',
            'description': 'SQL injection vulnerability',
            'solution': 'Use parameterized queries'
        },
        {
            'name': 'XSS',
            'cvss_score': 6.5,
            'exploitation_risk': 'Medium',
            'active_exploits': False,
            'confidence': 'Medium',
            'description': 'Cross-site scripting vulnerability',
            'solution': 'Sanitize user input'
        },
        {
            'name': 'Information Disclosure',
            'cvss_score': 4.0,
            'exploitation_risk': 'Low',
            'active_exploits': False,
            'confidence': 'High',
            'description': 'Information disclosure vulnerability',
            'solution': 'Configure proper access controls'
        }
    ]

def test_initialization(prioritizer):
    """Test RiskPrioritizer initialization"""
    assert prioritizer.risk_levels == ['Critical', 'High', 'Medium', 'Low', 'Info']
    assert prioritizer.confidence_levels == ['High', 'Medium', 'Low']
    assert prioritizer.exploitation_levels == ['Critical', 'High', 'Medium', 'Low', 'Unknown']

def test_prioritize_vulnerabilities(prioritizer, sample_vulnerabilities):
    """Test vulnerability prioritization"""
    results = prioritizer.prioritize_vulnerabilities(sample_vulnerabilities)
    
    assert isinstance(results, list)
    assert len(results) == len(sample_vulnerabilities)
    
    # Verify prioritization order (highest risk first)
    assert results[0]['name'] == 'SQL Injection'
    assert results[1]['name'] == 'XSS'
    assert results[2]['name'] == 'Information Disclosure'
    
    # Verify risk scores and priority levels are added
    for result in results:
        assert 'risk_score' in result
        assert 'priority' in result
        assert result['risk_score'] >= 0.0
        assert result['risk_score'] <= 10.0
        assert result['priority'] in prioritizer.risk_levels

def test_calculate_risk_score(prioritizer):
    """Test risk score calculation"""
    vulnerability = {
        'cvss_score': 8.5,
        'exploitation_risk': 'High',
        'active_exploits': True,
        'confidence': 'High'
    }
    
    score = prioritizer._calculate_risk_score(vulnerability)
    assert isinstance(score, float)
    assert score >= 0.0
    assert score <= 10.0

def test_risk_factors_dataclass():
    """Test RiskFactors dataclass"""
    factors = RiskFactors(
        cvss_score=8.5,
        exploitation_risk='High',
        active_exploits=True,
        detection_confidence='High',
        asset_criticality='High'
    )
    
    assert factors.cvss_score == 8.5
    assert factors.exploitation_risk == 'High'
    assert factors.active_exploits is True
    assert factors.detection_confidence == 'High'
    assert factors.asset_criticality == 'High'

def test_get_exploitation_multiplier(prioritizer):
    """Test exploitation risk multiplier calculation"""
    assert prioritizer._get_exploitation_multiplier('Critical') == 1.3
    assert prioritizer._get_exploitation_multiplier('High') == 1.2
    assert prioritizer._get_exploitation_multiplier('Medium') == 1.1
    assert prioritizer._get_exploitation_multiplier('Low') == 1.0
    assert prioritizer._get_exploitation_multiplier('Unknown') == 1.0
    assert prioritizer._get_exploitation_multiplier('Invalid') == 1.0

def test_get_confidence_multiplier(prioritizer):
    """Test confidence multiplier calculation"""
    assert prioritizer._get_confidence_multiplier('High') == 1.2
    assert prioritizer._get_confidence_multiplier('Medium') == 1.1
    assert prioritizer._get_confidence_multiplier('Low') == 1.0
    assert prioritizer._get_confidence_multiplier('Invalid') == 1.0

def test_get_criticality_multiplier(prioritizer):
    """Test asset criticality multiplier calculation"""
    assert prioritizer._get_criticality_multiplier('Critical') == 1.4
    assert prioritizer._get_criticality_multiplier('High') == 1.3
    assert prioritizer._get_criticality_multiplier('Medium') == 1.2
    assert prioritizer._get_criticality_multiplier('Low') == 1.1
    assert prioritizer._get_criticality_multiplier('Invalid') == 1.0

def test_assign_priority_levels(prioritizer):
    """Test priority level assignment"""
    scored_vulns = [
        {'risk_score': 9.5, 'name': 'Critical Vuln'},
        {'risk_score': 7.5, 'name': 'High Vuln'},
        {'risk_score': 5.5, 'name': 'Medium Vuln'},
        {'risk_score': 3.5, 'name': 'Low Vuln'},
        {'risk_score': 0.0, 'name': 'Info Vuln'}
    ]
    
    results = prioritizer._assign_priority_levels(scored_vulns)
    
    assert results[0]['priority'] == 'Critical'
    assert results[1]['priority'] == 'High'
    assert results[2]['priority'] == 'Medium'
    assert results[3]['priority'] == 'Low'
    assert results[4]['priority'] == 'Info'

def test_get_risk_metrics(prioritizer, sample_vulnerabilities):
    """Test risk metrics calculation"""
    # First prioritize vulnerabilities to add risk scores
    prioritized = prioritizer.prioritize_vulnerabilities(sample_vulnerabilities)
    
    metrics = prioritizer.get_risk_metrics(prioritized)
    
    assert isinstance(metrics, dict)
    assert 'total_vulnerabilities' in metrics
    assert 'risk_levels' in metrics
    assert 'average_risk_score' in metrics
    assert 'highest_risk_score' in metrics
    assert 'active_exploits_count' in metrics
    
    assert metrics['total_vulnerabilities'] == len(sample_vulnerabilities)
    assert isinstance(metrics['risk_levels'], dict)
    assert metrics['average_risk_score'] > 0.0
    assert metrics['highest_risk_score'] > 0.0
    assert metrics['active_exploits_count'] == 1

def test_empty_input(prioritizer):
    """Test handling of empty input"""
    assert prioritizer.prioritize_vulnerabilities([]) == []
    
    metrics = prioritizer.get_risk_metrics([])
    assert metrics['total_vulnerabilities'] == 0
    assert metrics['average_risk_score'] == 0.0
    assert metrics['highest_risk_score'] == 0.0
    assert metrics['active_exploits_count'] == 0

def test_missing_fields(prioritizer):
    """Test handling of vulnerabilities with missing fields"""
    vulnerabilities = [
        {'name': 'Incomplete Vuln'},  # Missing most fields
        {'name': 'Partial Vuln', 'cvss_score': 5.0}  # Missing some fields
    ]
    
    results = prioritizer.prioritize_vulnerabilities(vulnerabilities)
    assert len(results) == 2
    for result in results:
        assert 'risk_score' in result
        assert 'priority' in result

if __name__ == '__main__':
    pytest.main([__file__])
