#!/usr/bin/env python3
"""
Tests for the DependencyChecker class.
"""

import os
import json
import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from owasp_checker_v2.dependency_checker import DependencyChecker

@pytest.fixture
def checker():
    """Create a test instance of DependencyChecker"""
    return DependencyChecker(nvd_api_key='test-api-key')

@pytest.fixture
def sample_requirements():
    """Create sample requirements.txt content"""
    return """
requests>=2.25.0
django==3.1.0
beautifulsoup4~=4.9.3
urllib3<=1.26.7
"""

@pytest.fixture
def sample_package_json():
    """Create sample package.json content"""
    return json.dumps({
        "dependencies": {
            "express": "^4.17.1",
            "axios": "0.21.1"
        },
        "devDependencies": {
            "jest": "^26.6.3",
            "typescript": "4.2.4"
        }
    })

@pytest.fixture
def sample_pom_xml():
    """Create sample pom.xml content"""
    return """
    <project>
        <dependencies>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-core</artifactId>
                <version>5.3.5</version>
            </dependency>
            <dependency>
                <groupId>org.apache.logging.log4j</groupId>
                <artifactId>log4j-core</artifactId>
                <version>2.14.1</version>
            </dependency>
        </dependencies>
    </project>
    """

def test_initialization(checker):
    """Test DependencyChecker initialization"""
    assert checker.nvd_api_key == 'test-api-key'
    assert checker.nvd_api_url == "https://services.nvd.nist.gov/rest/json/cves/2.0"
    assert not checker.test_mode

def test_enable_test_mode(checker):
    """Test enabling test mode"""
    checker.enable_test_mode()
    assert checker.test_mode

def test_check_dependencies_test_mode(checker):
    """Test dependency checking in test mode"""
    checker.enable_test_mode()
    results = checker.check_dependencies('requirements.txt')
    
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

def test_parse_requirements(checker, sample_requirements):
    """Test parsing requirements.txt"""
    dependencies = checker._parse_requirements(sample_requirements)
    
    assert isinstance(dependencies, list)
    assert len(dependencies) == 4
    
    # Verify dependency structure
    dep = dependencies[0]
    assert dep['name'] == 'requests'
    assert dep['version'] == '2.25.0'
    assert dep['ecosystem'] == 'pypi'

def test_parse_package_json(checker, sample_package_json):
    """Test parsing package.json"""
    dependencies = checker._parse_package_json(sample_package_json)
    
    assert isinstance(dependencies, list)
    assert len(dependencies) == 4
    
    # Verify dependency structure
    dep = next(d for d in dependencies if d['name'] == 'express')
    assert dep['version'] == '4.17.1'
    assert dep['ecosystem'] == 'npm'

def test_parse_pom_xml(checker, sample_pom_xml):
    """Test parsing pom.xml"""
    dependencies = checker._parse_pom_xml(sample_pom_xml)
    
    assert isinstance(dependencies, list)
    assert len(dependencies) == 2
    
    # Verify dependency structure
    dep = dependencies[0]
    assert 'org.springframework:spring-core' in dep['name']
    assert dep['version'] == '5.3.5'
    assert dep['ecosystem'] == 'maven'

def test_detect_file_type(checker):
    """Test dependency file type detection"""
    assert checker._detect_file_type('requirements.txt') == 'requirements'
    assert checker._detect_file_type('package.json') == 'package.json'
    assert checker._detect_file_type('pom.xml') == 'pom.xml'
    
    with pytest.raises(ValueError):
        checker._detect_file_type('unknown.txt')

@patch('requests.get')
def test_check_dependency(mock_get, checker):
    """Test checking a single dependency"""
    # Mock NVD API response
    mock_response = Mock()
    mock_response.json.return_value = {
        'vulnerabilities': [
            {
                'cve': {
                    'id': 'CVE-2023-12345',
                    'descriptions': [{'value': 'Test vulnerability'}],
                    'metrics': {
                        'cvssMetricV31': [{
                            'cvssData': {
                                'baseScore': 7.5,
                                'vectorString': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
                                'baseSeverity': 'High'
                            }
                        }]
                    },
                    'published': '2023-01-01T00:00:00Z',
                    'references': [{'url': 'https://example.com/CVE-2023-12345'}]
                }
            }
        ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    dependency = {
        'name': 'test-package',
        'version': '1.0.0',
        'ecosystem': 'pypi'
    }
    
    results = checker._check_dependency(dependency)
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Verify vulnerability details
    vuln = results[0]
    assert vuln['cve_id'] == 'CVE-2023-12345'
    assert vuln['cvss_score'] == 7.5
    assert vuln['severity'] == 'High'

def test_version_comparison(checker):
    """Test version comparison functionality"""
    assert checker._version_in_range(
        packaging.version.parse('2.0.0'),
        '>=1.0.0'
    )
    assert not checker._version_in_range(
        packaging.version.parse('1.0.0'),
        '>1.0.0'
    )
    assert checker._version_in_range(
        packaging.version.parse('1.0.0'),
        '=1.0.0'
    )

def test_cache_management(checker):
    """Test cache management functionality"""
    checker.enable_test_mode()
    
    # Initial check
    results1 = checker.check_dependencies('requirements.txt')
    
    # Should use cached results
    results2 = checker.check_dependencies('requirements.txt')
    assert results1 == results2
    
    # Clear cache
    checker.clear_cache()
    assert len(checker.cache) == 0
    
    # Should perform new check
    results3 = checker.check_dependencies('requirements.txt')
    assert results3 is not None

def test_error_handling(checker):
    """Test error handling"""
    # Test with non-existent file
    with pytest.raises(FileNotFoundError):
        checker.check_dependencies('nonexistent.txt')
    
    # Test with invalid file type
    with pytest.raises(ValueError):
        checker.check_dependencies('invalid.xyz')

@patch('requests.get')
def test_api_error_handling(mock_get, checker):
    """Test API error handling"""
    # Mock API error
    mock_get.side_effect = Exception('API Error')
    
    dependency = {
        'name': 'test-package',
        'version': '1.0.0',
        'ecosystem': 'pypi'
    }
    
    # Should handle error gracefully
    results = checker._check_dependency(dependency)
    assert isinstance(results, list)
    assert len(results) == 0

def test_mock_results(checker):
    """Test mock results structure"""
    checker.enable_test_mode()
    results = checker._get_mock_results()
    
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Verify mock vulnerability structure
    vuln = results[0]
    assert all(key in vuln for key in [
        'name', 'cve_id', 'version', 'ecosystem', 'description',
        'cvss_score', 'cvss_vector', 'severity', 'published',
        'references', 'solution'
    ])

if __name__ == '__main__':
    pytest.main([__file__])
