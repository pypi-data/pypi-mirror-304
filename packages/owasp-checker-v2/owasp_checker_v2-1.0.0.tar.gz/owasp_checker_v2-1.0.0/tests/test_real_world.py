#!/usr/bin/env python3
"""
Real-world scenario tests for the OWASP Checker V2 library.
"""

import os
import json
import pytest
from unittest.mock import Mock, patch
from datetime import datetime

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

def test_wordpress_vulnerabilities(checker):
    """Test scanning WordPress site vulnerabilities"""
    # Common WordPress vulnerabilities
    results = checker.scan_url(
        'http://example-wordpress.com',
        vulnerability_types=[
            'sql_injection',
            'xss',
            'csrf',
            'file_inclusion',
            'authentication_bypass'
        ]
    )
    
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Verify WordPress-specific checks
    vuln_names = [v['name'].lower() for v in results]
    assert any('wordpress' in name for name in vuln_names)
    assert any('plugin' in name for name in vuln_names)
    assert any('theme' in name for name in vuln_names)

def test_node_dependencies(checker):
    """Test checking Node.js project dependencies"""
    # Create package.json with common dependencies
    package_json = {
        "dependencies": {
            "express": "^4.17.1",
            "mongoose": "^5.12.3",
            "jsonwebtoken": "^8.5.1",
            "bcrypt": "^5.0.1",
            "axios": "^0.21.1"
        },
        "devDependencies": {
            "jest": "^26.6.3",
            "eslint": "^7.23.0",
            "typescript": "^4.2.4"
        }
    }
    
    with open('package.json', 'w') as f:
        json.dump(package_json, f)
    
    try:
        results = checker.check_dependencies('package.json')
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Verify Node.js ecosystem checks
        assert all(v['ecosystem'] == 'npm' for v in results)
        
        # Check for common Node.js vulnerabilities
        vuln_names = [v['name'].lower() for v in results]
        assert any('prototype pollution' in name for name in vuln_names)
        assert any('command injection' in name for name in vuln_names)
        assert any('authentication bypass' in name for name in vuln_names)
    
    finally:
        os.remove('package.json')

def test_python_web_framework(checker):
    """Test scanning Python web framework vulnerabilities"""
    # Create requirements.txt with web framework dependencies
    requirements = """
Django==3.1.0
Flask==1.1.2
SQLAlchemy==1.3.23
requests==2.25.0
Jinja2==2.11.2
PyYAML==5.3.1
cryptography==3.3.1
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    try:
        # Check dependencies
        dep_results = checker.check_dependencies('requirements.txt')
        assert isinstance(dep_results, list)
        assert len(dep_results) > 0
        
        # Scan framework-specific vulnerabilities
        scan_results = checker.scan_url(
            'http://example-flask-app.com',
            vulnerability_types=[
                'sql_injection',
                'xss',
                'template_injection',
                'open_redirect',
                'csrf'
            ]
        )
        
        assert isinstance(scan_results, list)
        assert len(scan_results) > 0
        
        # Verify Python-specific vulnerabilities
        all_results = dep_results + scan_results
        vuln_names = [v['name'].lower() for v in all_results]
        assert any('template injection' in name for name in vuln_names)
        assert any('deserialization' in name for name in vuln_names)
        assert any('sql injection' in name for name in vuln_names)
    
    finally:
        os.remove('requirements.txt')

def test_api_security(checker):
    """Test API security scanning"""
    # Test RESTful API endpoints
    api_endpoints = [
        'http://api.example.com/v1/users',
        'http://api.example.com/v1/auth/login',
        'http://api.example.com/v1/products',
        'http://api.example.com/v1/orders'
    ]
    
    all_results = []
    for endpoint in api_endpoints:
        results = checker.scan_url(
            endpoint,
            vulnerability_types=[
                'injection',
                'broken_authentication',
                'data_exposure',
                'xxe',
                'broken_access_control',
                'rate_limiting'
            ]
        )
        all_results.extend(results)
    
    assert len(all_results) > 0
    
    # Verify API-specific vulnerabilities
    vuln_names = [v['name'].lower() for v in all_results]
    assert any('authentication' in name for name in vuln_names)
    assert any('authorization' in name for name in vuln_names)
    assert any('rate limit' in name for name in vuln_names)
    assert any('injection' in name for name in vuln_names)

def test_microservices_architecture(checker):
    """Test microservices security scanning"""
    # Test multiple service endpoints
    services = {
        'auth': 'http://auth.example.com',
        'users': 'http://users.example.com',
        'products': 'http://products.example.com',
        'orders': 'http://orders.example.com',
        'payment': 'http://payment.example.com'
    }
    
    # Service dependencies
    dependencies = {
        'auth': 'auth-service/requirements.txt',
        'users': 'user-service/package.json',
        'products': 'product-service/pom.xml',
        'orders': 'order-service/requirements.txt',
        'payment': 'payment-service/package.json'
    }
    
    # Create mock dependency files
    try:
        os.makedirs('auth-service', exist_ok=True)
        os.makedirs('user-service', exist_ok=True)
        os.makedirs('product-service', exist_ok=True)
        os.makedirs('order-service', exist_ok=True)
        os.makedirs('payment-service', exist_ok=True)
        
        # Create sample dependency files
        with open('auth-service/requirements.txt', 'w') as f:
            f.write('flask==1.1.2\njwt==1.0.0\n')
        
        with open('user-service/package.json', 'w') as f:
            json.dump({"dependencies": {"express": "4.17.1"}}, f)
        
        with open('product-service/pom.xml', 'w') as f:
            f.write('<project><dependencies><dependency><groupId>org.springframework.boot</groupId></dependency></dependencies></project>')
        
        with open('order-service/requirements.txt', 'w') as f:
            f.write('django==3.1.0\ncelery==5.0.0\n')
        
        with open('payment-service/package.json', 'w') as f:
            json.dump({"dependencies": {"stripe": "8.137.0"}}, f)
        
        # Test each service
        all_results = []
        for service_name, url in services.items():
            # Scan service endpoint
            scan_results = checker.scan_url(
                url,
                vulnerability_types=[
                    'injection',
                    'broken_authentication',
                    'data_exposure',
                    'broken_access_control'
                ]
            )
            
            # Check service dependencies
            dep_results = checker.check_dependencies(dependencies[service_name])
            
            all_results.extend(scan_results)
            all_results.extend(dep_results)
        
        assert len(all_results) > 0
        
        # Verify microservices-specific vulnerabilities
        vuln_names = [v['name'].lower() for v in all_results]
        assert any('authentication' in name for name in vuln_names)
        assert any('authorization' in name for name in vuln_names)
        assert any('communication' in name for name in vuln_names)
        assert any('configuration' in name for name in vuln_names)
    
    finally:
        # Clean up
        import shutil
        for service in ['auth-service', 'user-service', 'product-service', 'order-service', 'payment-service']:
            if os.path.exists(service):
                shutil.rmtree(service)

def test_cloud_native_application(checker):
    """Test cloud-native application security scanning"""
    # Test cloud service endpoints
    cloud_endpoints = {
        'api_gateway': 'http://api.cloud.example.com',
        'auth_service': 'http://auth.cloud.example.com',
        'storage_service': 'http://storage.cloud.example.com',
        'compute_service': 'http://compute.cloud.example.com'
    }
    
    # Cloud-specific vulnerability types
    cloud_vulnerabilities = [
        'misconfiguration',
        'data_exposure',
        'broken_authentication',
        'insecure_api',
        'insufficient_monitoring'
    ]
    
    all_results = []
    for service_name, url in cloud_endpoints.items():
        results = checker.scan_url(url, vulnerability_types=cloud_vulnerabilities)
        all_results.extend(results)
    
    assert len(all_results) > 0
    
    # Verify cloud-specific vulnerabilities
    vuln_names = [v['name'].lower() for v in all_results]
    assert any('configuration' in name for name in vuln_names)
    assert any('exposure' in name for name in vuln_names)
    assert any('authentication' in name for name in vuln_names)
    assert any('monitoring' in name for name in vuln_names)

if __name__ == '__main__':
    pytest.main([__file__])
