#!/usr/bin/env python3
"""
Integration tests for the OWASP Checker V2 library.
"""

import os
import pytest
from unittest.mock import Mock, patch

from owasp_checker_v2 import (
    OWASPChecker,
    OWASPTopTenScanner,
    DependencyChecker,
    ThreatIntelligenceChecker,
    RiskPrioritizer,
    OWASPScraper
)

@pytest.fixture
def checker():
    """Create a test instance of OWASPChecker with all components"""
    checker = OWASPChecker(
        zap_proxy_address='http://localhost:8080',
        nvd_api_key='test-nvd-key',
        vt_api_key='test-vt-key'
    )
    checker.enable_test_mode()
    return checker

def test_full_security_check(checker):
    """Test comprehensive security check workflow"""
    # Create test requirements file
    with open('test_requirements.txt', 'w') as f:
        f.write('requests==2.25.0\ndjango==3.1.0')
    
    try:
        # Run full security check
        results = checker.run_full_check(
            url='http://example.com',
            dependency_file='test_requirements.txt',
            vulnerability_types=['sql_injection', 'xss']
        )
        
        # Verify results structure
        assert isinstance(results, dict)
        assert 'scan_time' in results
        assert 'vulnerabilities' in results
        assert 'guidelines' in results
        
        # Verify vulnerabilities
        vulns = results['vulnerabilities']
        assert isinstance(vulns, list)
        assert len(vulns) > 0
        
        # Verify each vulnerability has required fields
        for vuln in vulns:
            assert 'name' in vuln
            assert 'risk' in vuln
            assert 'confidence' in vuln
            assert 'cvss_score' in vuln
            assert 'description' in vuln
            assert 'solution' in vuln
            assert 'exploitation_risk' in vuln
            assert 'active_exploits' in vuln
            assert 'priority' in vuln
        
        # Verify guidelines
        guidelines = results['guidelines']
        assert isinstance(guidelines, dict)
        assert 'OWASP Top Ten' in guidelines
        assert 'Cheat Sheets' in guidelines
        
    finally:
        # Clean up
        if os.path.exists('test_requirements.txt'):
            os.remove('test_requirements.txt')

def test_component_interaction(checker):
    """Test interaction between different components"""
    # 1. Scanner finds vulnerabilities
    scan_results = checker.scanner.scan_url('http://example.com')
    assert isinstance(scan_results, list)
    assert len(scan_results) > 0
    
    # 2. Threat intelligence enriches data
    enriched_results = checker.threat_intelligence.enrich_vulnerability_data(
        scan_results
    )
    assert len(enriched_results) == len(scan_results)
    assert all('exploitation_risk' in vuln for vuln in enriched_results)
    
    # 3. Risk prioritizer ranks vulnerabilities
    prioritized_results = checker.risk_prioritizer.prioritize_vulnerabilities(
        enriched_results
    )
    assert len(prioritized_results) == len(enriched_results)
    assert all('priority' in vuln for vuln in prioritized_results)
    
    # 4. OWASP scraper provides guidelines
    guidelines = checker.owasp_scraper.fetch_owasp_guidelines()
    assert isinstance(guidelines, dict)
    assert 'OWASP Top Ten' in guidelines

def test_dependency_scanning_workflow(checker):
    """Test dependency scanning workflow"""
    # Create test files for different ecosystems
    files = {
        'requirements.txt': 'requests==2.25.0\ndjango==3.1.0',
        'package.json': '{"dependencies":{"express":"^4.17.1"}}',
        'pom.xml': '''
            <project>
                <dependencies>
                    <dependency>
                        <groupId>org.springframework</groupId>
                        <artifactId>spring-core</artifactId>
                        <version>5.3.5</version>
                    </dependency>
                </dependencies>
            </project>
        '''
    }
    
    try:
        # Create test files
        for filename, content in files.items():
            with open(filename, 'w') as f:
                f.write(content)
        
        # Test each ecosystem
        for filename in files:
            results = checker.check_dependencies(filename)
            assert isinstance(results, list)
            assert len(results) > 0
            
            # Verify vulnerability enrichment
            for vuln in results:
                assert 'exploitation_risk' in vuln
                assert 'active_exploits' in vuln
                assert 'priority' in vuln
    
    finally:
        # Clean up
        for filename in files:
            if os.path.exists(filename):
                os.remove(filename)

def test_cache_coordination(checker):
    """Test cache coordination between components"""
    # Initial scan
    results1 = checker.run_full_check(url='http://example.com')
    
    # Should use cached results
    results2 = checker.run_full_check(url='http://example.com')
    assert results1 == results2
    
    # Clear all caches
    checker.clear_cache()
    assert len(checker.scanner.cache) == 0
    assert len(checker.dependency_checker.cache) == 0
    assert len(checker.threat_intelligence.cache) == 0
    assert len(checker.owasp_scraper.cache) == 0
    
    # Should perform new scan
    results3 = checker.run_full_check(url='http://example.com')
    assert results3 is not None

def test_error_propagation(checker):
    """Test error handling and propagation between components"""
    # Test with invalid URL
    with pytest.raises(ValueError):
        checker.run_full_check(url='invalid-url')
    
    # Test with non-existent dependency file
    with pytest.raises(FileNotFoundError):
        checker.run_full_check(dependency_file='nonexistent.txt')
    
    # Test with API errors
    with patch.object(checker.threat_intelligence, '_get_threat_intelligence',
                     side_effect=Exception('API Error')):
        # Should still complete with default threat data
        results = checker.run_full_check(url='http://example.com')
        assert results is not None
        assert len(results['vulnerabilities']) > 0

def test_remediation_workflow(checker):
    """Test vulnerability remediation workflow"""
    # Run initial scan
    results = checker.run_full_check(url='http://example.com')
    assert len(results['vulnerabilities']) > 0
    
    # Get remediation steps for each vulnerability
    for vuln in results['vulnerabilities']:
        remediation = checker.get_remediation_steps(vuln)
        assert isinstance(remediation, dict)
        assert 'vulnerability' in remediation
        assert 'steps' in remediation
        assert 'references' in remediation
        assert 'guidelines' in remediation

if __name__ == '__main__':
    pytest.main([__file__])
