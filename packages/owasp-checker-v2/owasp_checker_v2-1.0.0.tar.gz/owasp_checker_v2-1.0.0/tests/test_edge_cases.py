#!/usr/bin/env python3
"""
Edge case and boundary condition tests for the OWASP Checker V2 library.
"""

import os
import json
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

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
    """Create a test instance of OWASPChecker"""
    checker = OWASPChecker(
        zap_proxy_address='http://localhost:8080',
        nvd_api_key='test-nvd-key',
        vt_api_key='test-vt-key'
    )
    checker.enable_test_mode()
    return checker

def test_empty_inputs():
    """Test handling of empty inputs"""
    checker = OWASPChecker()
    
    # Empty URL
    with pytest.raises(ValueError):
        checker.scan_url('')
    
    # Empty dependency file
    with pytest.raises(ValueError):
        checker.check_dependencies('')
    
    # Empty vulnerability types
    results = checker.scan_url('http://example.com', vulnerability_types=[])
    assert isinstance(results, list)

def test_invalid_inputs():
    """Test handling of invalid inputs"""
    checker = OWASPChecker()
    
    # Invalid URL formats
    invalid_urls = [
        'not-a-url',
        'ftp://example.com',
        'http:/example.com',
        'https://',
        123,  # Non-string
        None,
        True,
        ['http://example.com'],
        {'url': 'http://example.com'}
    ]
    
    for url in invalid_urls:
        with pytest.raises((ValueError, TypeError)):
            checker.scan_url(url)
    
    # Invalid vulnerability types
    invalid_types = [
        123,
        None,
        True,
        'sql_injection',  # Should be list
        {'type': 'sql_injection'}
    ]
    
    for vuln_type in invalid_types:
        with pytest.raises((ValueError, TypeError)):
            checker.scan_url('http://example.com', vulnerability_types=vuln_type)

def test_large_inputs():
    """Test handling of large inputs"""
    checker = OWASPChecker()
    checker.enable_test_mode()
    
    # Large URL
    long_url = 'http://example.com/' + 'a' * 10000
    results = checker.scan_url(long_url)
    assert isinstance(results, list)
    
    # Large dependency file
    with open('large_requirements.txt', 'w') as f:
        for i in range(1000):
            f.write(f'package{i}==1.0.0\n')
    
    try:
        results = checker.check_dependencies('large_requirements.txt')
        assert isinstance(results, list)
    finally:
        os.remove('large_requirements.txt')

def test_malformed_dependency_files():
    """Test handling of malformed dependency files"""
    checker = OWASPChecker()
    checker.enable_test_mode()
    
    # Malformed requirements.txt
    with open('bad_requirements.txt', 'w') as f:
        f.write('malformed==package==version\n')
    
    # Malformed package.json
    with open('bad_package.json', 'w') as f:
        f.write('{invalid json}')
    
    # Malformed pom.xml
    with open('bad_pom.xml', 'w') as f:
        f.write('<invalid>xml</invalid')
    
    try:
        # Should handle errors gracefully
        for file in ['bad_requirements.txt', 'bad_package.json', 'bad_pom.xml']:
            results = checker.check_dependencies(file)
            assert isinstance(results, list)
    finally:
        # Clean up
        for file in ['bad_requirements.txt', 'bad_package.json', 'bad_pom.xml']:
            if os.path.exists(file):
                os.remove(file)

def test_api_rate_limits():
    """Test handling of API rate limits"""
    checker = OWASPChecker()
    
    # Mock rate limit responses
    rate_limit_response = Mock()
    rate_limit_response.raise_for_status.side_effect = Exception('Rate limit exceeded')
    
    # Test NVD API rate limit
    with patch('requests.get', return_value=rate_limit_response):
        results = checker.check_dependencies('requirements.txt')
        assert isinstance(results, list)
    
    # Test VirusTotal API rate limit
    with patch('requests.get', return_value=rate_limit_response):
        results = checker.scan_url('http://example.com')
        assert isinstance(results, list)

def test_concurrent_requests():
    """Test handling of concurrent requests"""
    checker = OWASPChecker()
    checker.enable_test_mode()
    
    # Simulate concurrent scans
    import threading
    results = []
    
    def scan():
        result = checker.scan_url('http://example.com')
        results.append(result)
    
    threads = [threading.Thread(target=scan) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    assert len(results) == 10
    assert all(isinstance(r, list) for r in results)

def test_cache_edge_cases():
    """Test cache edge cases"""
    checker = OWASPChecker()
    checker.enable_test_mode()
    
    # Cache expiration exactly at boundary
    checker.scanner.cache_duration = timedelta(seconds=0)
    results1 = checker.scan_url('http://example.com')
    results2 = checker.scan_url('http://example.com')
    assert results1 != results2  # Should not use cache
    
    # Very large cache duration
    checker.scanner.cache_duration = timedelta(days=36500)  # 100 years
    results = checker.scan_url('http://example.com')
    assert isinstance(results, list)
    
    # Negative cache duration
    with pytest.raises(ValueError):
        checker.scanner.update_cache_duration(-1)

def test_unicode_handling():
    """Test handling of Unicode characters"""
    checker = OWASPChecker()
    checker.enable_test_mode()
    
    # Unicode in URL
    url = 'http://例子.com'
    results = checker.scan_url(url)
    assert isinstance(results, list)
    
    # Unicode in dependency names
    with open('unicode_requirements.txt', 'w', encoding='utf-8') as f:
        f.write('パッケージ==1.0.0\n')
    
    try:
        results = checker.check_dependencies('unicode_requirements.txt')
        assert isinstance(results, list)
    finally:
        os.remove('unicode_requirements.txt')

def test_memory_usage():
    """Test memory usage with large datasets"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    checker = OWASPChecker()
    checker.enable_test_mode()
    
    # Generate large test data
    large_vulns = []
    for i in range(10000):
        large_vulns.append({
            'name': f'Vulnerability {i}',
            'description': 'x' * 1000,
            'solution': 'x' * 1000
        })
    
    # Process large dataset
    results = checker.threat_intelligence.enrich_vulnerability_data(large_vulns)
    assert isinstance(results, list)
    
    # Check memory usage
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Should not increase memory usage by more than 100MB
    assert memory_increase < 100 * 1024 * 1024

if __name__ == '__main__':
    pytest.main([__file__])
