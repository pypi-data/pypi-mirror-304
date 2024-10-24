#!/usr/bin/env python3
"""
Main OWASP Checker class that integrates all components for comprehensive security scanning.
"""

from typing import List, Dict, Any, Optional
import os
from datetime import datetime

from .owasp_top_ten_scanner import OWASPTopTenScanner
from .dependency_checker import DependencyChecker
from .threat_intelligence_checker import ThreatIntelligenceChecker
from .risk_prioritizer import RiskPrioritizer
from .owasp_scraper import OWASPScraper

class OWASPChecker:
    """
    Main class for OWASP security checking functionality.
    Integrates vulnerability scanning, dependency checking, and threat intelligence.
    """

    def __init__(
        self,
        zap_proxy_address: str = 'http://localhost:8080',
        nvd_api_key: Optional[str] = None,
        vt_api_key: Optional[str] = None
    ):
        """
        Initialize OWASP Checker with optional API keys.

        Args:
            zap_proxy_address: OWASP ZAP proxy address
            nvd_api_key: NVD API key for dependency checking
            vt_api_key: VirusTotal API key for threat intelligence
        """
        self.zap_proxy_address = zap_proxy_address
        self.nvd_api_key = nvd_api_key
        self.vt_api_key = vt_api_key

        # Initialize components
        self.scanner = OWASPTopTenScanner(zap_proxy_address)
        self.dependency_checker = DependencyChecker(nvd_api_key)
        self.threat_intelligence = ThreatIntelligenceChecker(vt_api_key)
        self.risk_prioritizer = RiskPrioritizer()
        self.owasp_scraper = OWASPScraper()

        self.test_mode = False

    def enable_test_mode(self) -> None:
        """Enable test mode for all components"""
        self.test_mode = True
        self.scanner.enable_test_mode()
        self.dependency_checker.enable_test_mode()
        self.threat_intelligence.enable_test_mode()

    def scan_url(
        self,
        url: str,
        vulnerability_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Scan a URL for vulnerabilities.

        Args:
            url: Target URL to scan
            vulnerability_types: List of specific vulnerability types to scan for

        Returns:
            List of detected vulnerabilities with enriched data
        """
        # Scan for vulnerabilities
        vulnerabilities = self.scanner.scan_url(url, vulnerability_types)

        # Enrich with threat intelligence
        enriched_vulns = self.threat_intelligence.enrich_vulnerability_data(vulnerabilities)

        # Prioritize vulnerabilities
        prioritized_vulns = self.risk_prioritizer.prioritize_vulnerabilities(enriched_vulns)

        return prioritized_vulns

    def check_dependencies(
        self,
        dependency_file: str,
        file_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Check dependencies for known vulnerabilities.

        Args:
            dependency_file: Path to dependency file
            file_type: Type of dependency file (requirements, package.json, pom.xml)

        Returns:
            List of detected vulnerabilities in dependencies
        """
        # Check dependencies
        vulnerabilities = self.dependency_checker.check_dependencies(
            dependency_file,
            file_type
        )

        # Enrich with threat intelligence
        enriched_vulns = self.threat_intelligence.enrich_vulnerability_data(vulnerabilities)

        # Prioritize vulnerabilities
        prioritized_vulns = self.risk_prioritizer.prioritize_vulnerabilities(enriched_vulns)

        return prioritized_vulns

    def run_full_check(
        self,
        url: Optional[str] = None,
        dependency_file: Optional[str] = None,
        vulnerability_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run a comprehensive security check.

        Args:
            url: Target URL to scan
            dependency_file: Path to dependency file
            vulnerability_types: List of specific vulnerability types to scan for

        Returns:
            Dictionary containing all scan results and guidelines
        """
        results = {
            'scan_time': datetime.now().isoformat(),
            'vulnerabilities': [],
            'guidelines': {}
        }

        # Scan URL if provided
        if url:
            url_vulns = self.scan_url(url, vulnerability_types)
            results['vulnerabilities'].extend(url_vulns)

        # Check dependencies if provided
        if dependency_file:
            dep_vulns = self.check_dependencies(dependency_file)
            results['vulnerabilities'].extend(dep_vulns)

        # Fetch latest OWASP guidelines
        results['guidelines'] = self.owasp_scraper.fetch_owasp_guidelines()

        # Prioritize all vulnerabilities together
        results['vulnerabilities'] = self.risk_prioritizer.prioritize_vulnerabilities(
            results['vulnerabilities']
        )

        return results

    def get_remediation_steps(
        self,
        vulnerability: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get detailed remediation steps for a vulnerability.

        Args:
            vulnerability: Vulnerability dictionary

        Returns:
            Dictionary containing remediation steps and guidelines
        """
        vuln_type = vulnerability.get('name', '').lower()
        guidelines = self.owasp_scraper.fetch_owasp_guidelines()

        remediation = {
            'vulnerability': vulnerability,
            'steps': [],
            'references': [],
            'guidelines': {}
        }

        # Get relevant OWASP guidelines
        for category, guide in guidelines.get('OWASP Top Ten', {}).items():
            if vuln_type in category.lower():
                remediation['guidelines'][category] = guide

        # Add remediation steps from vulnerability data
        if 'solution' in vulnerability:
            remediation['steps'].append(vulnerability['solution'])

        # Add references
        if 'references' in vulnerability:
            remediation['references'].extend(vulnerability['references'])

        return remediation

    def clear_cache(self) -> None:
        """Clear cache in all components"""
        self.scanner.clear_cache()
        self.dependency_checker.clear_cache()
        self.threat_intelligence.clear_cache()
        self.owasp_scraper.clear_cache()

    def update_cache_duration(self, hours: int) -> None:
        """Update cache duration in all components"""
        self.scanner.update_cache_duration(hours)
        self.dependency_checker.update_cache_duration(hours)
        self.threat_intelligence.update_cache_duration(hours)
        self.owasp_scraper.update_cache_duration(hours)
