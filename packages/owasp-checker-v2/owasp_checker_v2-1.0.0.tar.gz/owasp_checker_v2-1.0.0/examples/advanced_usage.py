#!/usr/bin/env python3
"""
Advanced usage examples for the OWASP Checker V2 library.
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from owasp_checker_v2 import OWASPChecker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SecurityScanner:
    """Advanced security scanner implementation"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        """Initialize scanner with optional API keys"""
        self.checker = OWASPChecker(
            nvd_api_key=api_keys.get('nvd_api_key') if api_keys else None,
            vt_api_key=api_keys.get('vt_api_key') if api_keys else None
        )
        self.results_dir = 'scan_results'
        os.makedirs(self.results_dir, exist_ok=True)
    
    def scan_microservices(
        self,
        services: Dict[str, str],
        dependencies: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Scan multiple microservices and their dependencies.
        
        Args:
            services: Dictionary mapping service names to URLs
            dependencies: Dictionary mapping service names to dependency files
        
        Returns:
            Dictionary containing scan results for all services
        """
        logger.info("Starting microservices security scan")
        results = {}
        
        with ThreadPoolExecutor() as executor:
            # Scan services in parallel
            future_to_service = {
                executor.submit(self._scan_service, name, url, dependencies.get(name)):
                name for name, url in services.items()
            }
            
            for future in future_to_service:
                service_name = future_to_service[future]
                try:
                    results[service_name] = future.result()
                except Exception as e:
                    logger.error(f"Error scanning {service_name}: {str(e)}")
                    results[service_name] = {'error': str(e)}
        
        return results
    
    def _scan_service(
        self,
        name: str,
        url: str,
        dependency_file: str = None
    ) -> Dict[str, Any]:
        """Scan a single service"""
        logger.info(f"Scanning service: {name}")
        
        # Run full security check
        results = self.checker.run_full_check(
            url=url,
            dependency_file=dependency_file,
            vulnerability_types=[
                'sql_injection',
                'xss',
                'csrf',
                'authentication_bypass',
                'insecure_deserialization'
            ]
        )
        
        # Enrich with threat intelligence
        if results.get('vulnerabilities'):
            results['vulnerabilities'] = (
                self.checker.threat_intelligence.enrich_vulnerability_data(
                    results['vulnerabilities']
                )
            )
        
        return results
    
    def analyze_security_posture(
        self,
        scan_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze overall security posture from scan results.
        
        Args:
            scan_results: Results from security scans
        
        Returns:
            Dictionary containing security analysis
        """
        logger.info("Analyzing security posture")
        
        analysis = {
            'total_services': len(scan_results),
            'total_vulnerabilities': 0,
            'risk_levels': {},
            'high_risk_services': [],
            'vulnerability_types': {},
            'active_exploits': 0
        }
        
        # Analyze each service
        for service_name, results in scan_results.items():
            if 'error' in results:
                continue
            
            vulns = results.get('vulnerabilities', [])
            analysis['total_vulnerabilities'] += len(vulns)
            
            # Calculate service risk score
            service_risk = self._calculate_service_risk(vulns)
            if service_risk >= 7.0:
                analysis['high_risk_services'].append({
                    'name': service_name,
                    'risk_score': service_risk,
                    'critical_vulnerabilities': len([
                        v for v in vulns
                        if v.get('risk', '').lower() == 'critical'
                    ])
                })
            
            # Count vulnerability types
            for vuln in vulns:
                vuln_type = vuln.get('name', '').lower()
                analysis['vulnerability_types'][vuln_type] = (
                    analysis['vulnerability_types'].get(vuln_type, 0) + 1
                )
                
                # Count risk levels
                risk_level = vuln.get('risk', 'Unknown')
                analysis['risk_levels'][risk_level] = (
                    analysis['risk_levels'].get(risk_level, 0) + 1
                )
                
                # Count active exploits
                if vuln.get('active_exploits'):
                    analysis['active_exploits'] += 1
        
        return analysis
    
    def _calculate_service_risk(self, vulnerabilities: List[Dict[str, Any]]) -> float:
        """Calculate risk score for a service"""
        if not vulnerabilities:
            return 0.0
        
        # Use risk prioritizer for accurate scoring
        prioritized = self.checker.risk_prioritizer.prioritize_vulnerabilities(
            vulnerabilities
        )
        metrics = self.checker.risk_prioritizer.get_risk_metrics(prioritized)
        
        return metrics['highest_risk_score']
    
    def generate_security_report(
        self,
        scan_results: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> str:
        """
        Generate a comprehensive security report.
        
        Args:
            scan_results: Results from security scans
            analysis: Security posture analysis
        
        Returns:
            Path to the generated report file
        """
        logger.info("Generating security report")
        
        # Prepare report data
        report = {
            'scan_time': datetime.now().isoformat(),
            'summary': {
                'total_services': analysis['total_services'],
                'total_vulnerabilities': analysis['total_vulnerabilities'],
                'high_risk_services': len(analysis['high_risk_services']),
                'active_exploits': analysis['active_exploits']
            },
            'risk_analysis': {
                'risk_levels': analysis['risk_levels'],
                'high_risk_services': analysis['high_risk_services'],
                'vulnerability_types': analysis['vulnerability_types']
            },
            'service_details': scan_results,
            'remediation_guidelines': self._get_remediation_guidelines(scan_results)
        }
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(
            self.results_dir,
            f'security_report_{timestamp}.json'
        )
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    def _get_remediation_guidelines(
        self,
        scan_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get remediation guidelines for all vulnerabilities"""
        guidelines = {}
        
        for service_name, results in scan_results.items():
            if 'error' in results:
                continue
            
            service_guidelines = []
            for vuln in results.get('vulnerabilities', []):
                remediation = self.checker.get_remediation_steps(vuln)
                service_guidelines.append({
                    'vulnerability': vuln['name'],
                    'risk_level': vuln.get('risk', 'Unknown'),
                    'steps': remediation['steps'],
                    'references': remediation['references']
                })
            
            guidelines[service_name] = service_guidelines
        
        return guidelines

def main():
    """Run advanced usage examples"""
    # Sample microservices setup
    services = {
        'auth_service': 'http://auth.example.com',
        'user_service': 'http://users.example.com',
        'payment_service': 'http://payments.example.com'
    }
    
    dependencies = {
        'auth_service': 'auth/requirements.txt',
        'user_service': 'users/package.json',
        'payment_service': 'payments/pom.xml'
    }
    
    try:
        # Create mock dependency files
        os.makedirs('auth', exist_ok=True)
        os.makedirs('users', exist_ok=True)
        os.makedirs('payments', exist_ok=True)
        
        with open('auth/requirements.txt', 'w') as f:
            f.write('django==3.1.0\nrequests==2.25.0\n')
        
        with open('users/package.json', 'w') as f:
            json.dump({
                'dependencies': {
                    'express': '4.17.1',
                    'mongoose': '5.12.3'
                }
            }, f)
        
        with open('payments/pom.xml', 'w') as f:
            f.write('''
                <project>
                    <dependencies>
                        <dependency>
                            <groupId>org.springframework.boot</groupId>
                            <artifactId>spring-boot-starter-web</artifactId>
                            <version>2.4.4</version>
                        </dependency>
                    </dependencies>
                </project>
            ''')
        
        # Initialize scanner
        scanner = SecurityScanner()
        scanner.checker.enable_test_mode()  # For demonstration purposes
        
        # Scan microservices
        scan_results = scanner.scan_microservices(services, dependencies)
        
        # Analyze results
        analysis = scanner.analyze_security_posture(scan_results)
        
        # Generate report
        report_file = scanner.generate_security_report(scan_results, analysis)
        
        logger.info(f"Security scan completed. Report saved to: {report_file}")
        
        # Print summary
        print("\nSecurity Scan Summary:")
        print(f"Total Services: {analysis['total_services']}")
        print(f"Total Vulnerabilities: {analysis['total_vulnerabilities']}")
        print(f"Active Exploits: {analysis['active_exploits']}")
        print("\nRisk Levels:")
        for level, count in analysis['risk_levels'].items():
            print(f"  {level}: {count}")
        print("\nHigh Risk Services:")
        for service in analysis['high_risk_services']:
            print(f"  {service['name']} (Risk Score: {service['risk_score']:.2f})")
    
    finally:
        # Clean up
        import shutil
        for dir_name in ['auth', 'users', 'payments', 'scan_results']:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)

if __name__ == '__main__':
    main()
