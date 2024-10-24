#!/usr/bin/env python3
"""
OWASP guidelines and cheat sheets scraper.

This module provides functionality to fetch and parse the latest OWASP guidelines,
cheat sheets, and security recommendations from the OWASP website.
"""

import requests
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import re

class OWASPScraper:
    """
    Scrapes and parses OWASP guidelines and security recommendations.
    """

    def __init__(self):
        """Initialize the OWASPScraper"""
        self.base_url = "https://owasp.org"
        self.top_ten_url = f"{self.base_url}/Top10"
        self.cheat_sheets_url = f"{self.base_url}/www-project-cheat-sheets"
        
        self.cache = {}
        self.cache_duration = timedelta(hours=24)
        self.test_mode = False

    def enable_test_mode(self):
        """Enable test mode for mock responses"""
        self.test_mode = True

    def fetch_owasp_guidelines(self) -> Dict[str, Any]:
        """
        Fetch the latest OWASP guidelines and recommendations.

        Returns:
            Dictionary containing OWASP guidelines and recommendations
        """
        if self.test_mode:
            return self._get_mock_guidelines()

        # Check cache first
        if self._is_cache_valid('guidelines'):
            return self.cache['guidelines']

        try:
            guidelines = {
                'OWASP Top Ten': self._fetch_top_ten(),
                'Cheat Sheets': self._fetch_cheat_sheets(),
                'last_updated': datetime.now().isoformat()
            }

            # Cache the results
            self._update_cache('guidelines', guidelines)
            return guidelines

        except Exception as e:
            print(f"Error fetching OWASP guidelines: {str(e)}")
            return self._get_mock_guidelines()

    def _fetch_top_ten(self) -> Dict[str, str]:
        """
        Fetch OWASP Top Ten vulnerabilities and descriptions.

        Returns:
            Dictionary mapping vulnerability categories to descriptions
        """
        try:
            response = requests.get(self.top_ten_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            top_ten = {}
            
            # Parse the Top Ten categories and descriptions
            for category in soup.find_all(class_=re.compile(r'top-?10-?item')):
                title = category.find(class_=re.compile(r'title|heading'))
                description = category.find(class_=re.compile(r'description|content'))
                
                if title and description:
                    title_text = self._clean_text(title.get_text())
                    desc_text = self._clean_text(description.get_text())
                    top_ten[title_text] = desc_text

            return top_ten

        except Exception as e:
            print(f"Error fetching OWASP Top Ten: {str(e)}")
            return self._get_mock_top_ten()

    def _fetch_cheat_sheets(self) -> Dict[str, str]:
        """
        Fetch OWASP cheat sheets and security recommendations.

        Returns:
            Dictionary mapping cheat sheet titles to content
        """
        try:
            response = requests.get(self.cheat_sheets_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            cheat_sheets = {}
            
            # Parse the cheat sheets
            for sheet in soup.find_all(class_=re.compile(r'cheat-?sheet')):
                title = sheet.find(class_=re.compile(r'title|heading'))
                content = sheet.find(class_=re.compile(r'content|body'))
                
                if title and content:
                    title_text = self._clean_text(title.get_text())
                    content_text = self._clean_text(content.get_text())
                    cheat_sheets[title_text] = content_text

            return cheat_sheets

        except Exception as e:
            print(f"Error fetching OWASP cheat sheets: {str(e)}")
            return self._get_mock_cheat_sheets()

    def _clean_text(self, text: str) -> str:
        """Clean and format scraped text"""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove special characters
        text = re.sub(r'[\xa0\u200b]', '', text)
        return text

    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        
        cache_time = self.cache.get(f"{key}_time")
        if not cache_time:
            return False
        
        return datetime.now() - cache_time < self.cache_duration

    def _update_cache(self, key: str, data: Any) -> None:
        """Update cache with new data"""
        self.cache[key] = data
        self.cache[f"{key}_time"] = datetime.now()

    def clear_cache(self) -> None:
        """Clear the cache"""
        self.cache.clear()

    def update_cache_duration(self, hours: int) -> None:
        """Update cache duration"""
        self.cache_duration = timedelta(hours=hours)

    def _get_mock_guidelines(self) -> Dict[str, Any]:
        """Return mock guidelines for testing"""
        return {
            'OWASP Top Ten': self._get_mock_top_ten(),
            'Cheat Sheets': self._get_mock_cheat_sheets(),
            'last_updated': datetime.now().isoformat()
        }

    def _get_mock_top_ten(self) -> Dict[str, str]:
        """Return mock OWASP Top Ten data"""
        return {
            'A01:2021 - Broken Access Control': 
                'Access control enforces policy such that users cannot act outside of their intended permissions.',
            'A02:2021 - Cryptographic Failures':
                'Failures related to cryptography which often lead to sensitive data exposure or system compromise.',
            'A03:2021 - Injection':
                'Injection flaws, such as SQL, NoSQL, OS, and LDAP injection, occur when untrusted data is sent to an interpreter.',
            'A04:2021 - Insecure Design':
                'Insecure design is a broad category representing different weaknesses expressed as "missing or ineffective control design."',
            'A05:2021 - Security Misconfiguration':
                'Security misconfiguration is the most commonly seen issue, due to insecure default configurations, incomplete configurations, and verbose error messages.',
            'A06:2021 - Vulnerable and Outdated Components':
                'Components, such as libraries, frameworks, and other software modules, run with the same privileges as the application.',
            'A07:2021 - Identification and Authentication Failures':
                'Authentication related attacks that target user's identity, authentication, and session management.',
            'A08:2021 - Software and Data Integrity Failures':
                'Software and data integrity failures relate to code and infrastructure that does not protect against integrity violations.',
            'A09:2021 - Security Logging and Monitoring Failures':
                'This category helps detect, escalate, and respond to active breaches. Without logging and monitoring, breaches cannot be detected.',
            'A10:2021 - Server-Side Request Forgery':
                'SSRF flaws occur whenever a web application is fetching a remote resource without validating the user-supplied URL.'
        }

    def _get_mock_cheat_sheets(self) -> Dict[str, str]:
        """Return mock cheat sheets data"""
        return {
            'Authentication Cheat Sheet':
                'Implement proper authentication using secure protocols, password policies, and MFA.',
            'Authorization Cheat Sheet':
                'Implement proper authorization using role-based access control and principle of least privilege.',
            'Input Validation Cheat Sheet':
                'Validate and sanitize all input data to prevent injection attacks.',
            'Session Management Cheat Sheet':
                'Implement secure session management using secure cookies and proper timeout policies.',
            'REST Security Cheat Sheet':
                'Secure REST APIs using proper authentication, authorization, and input validation.'
        }
