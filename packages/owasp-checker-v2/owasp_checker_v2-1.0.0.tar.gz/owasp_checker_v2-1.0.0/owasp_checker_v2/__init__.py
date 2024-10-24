"""
OWASP Top Ten Compliance Checker Library

This library provides automated detection of web application, API, and dependency
vulnerabilities based on OWASP Top Ten guidelines. It integrates with various
security tools and data sources to provide comprehensive security checks and
actionable remediation guidance.

Main Components:
- OWASPChecker: Main interface for running security checks
- OWASPTopTenScanner: Web vulnerability scanner using OWASP ZAP
- DependencyChecker: Dependency vulnerability checker using NVD API
- ThreatIntelligenceChecker: Threat intelligence data enrichment
- RiskPrioritizer: Risk-based vulnerability prioritization
- OWASPScraper: OWASP guidelines and cheat sheets scraper
"""

from .owasp_checker import OWASPChecker
from .owasp_top_ten_scanner import OWASPTopTenScanner
from .dependency_checker import DependencyChecker
from .threat_intelligence_checker import ThreatIntelligenceChecker
from .risk_prioritizer import RiskPrioritizer
from .owasp_scraper import OWASPScraper

__version__ = '0.1.0'
__author__ = 'Cline'
__email__ = 'cline@example.com'

__all__ = [
    'OWASPChecker',
    'OWASPTopTenScanner',
    'DependencyChecker',
    'ThreatIntelligenceChecker',
    'RiskPrioritizer',
    'OWASPScraper'
]
