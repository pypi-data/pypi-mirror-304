#!/usr/bin/env python3
"""
Dependency vulnerability checker using NVD API.

This module provides functionality to check dependencies for known vulnerabilities
using the National Vulnerability Database (NVD) API.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import requests
import packaging.version

class DependencyChecker:
    """
    Checks dependencies for known vulnerabilities using NVD API.
    """

    def __init__(self, nvd_api_key: Optional[str] = None):
        """
        Initialize DependencyChecker.

        Args:
            nvd_api_key: Optional NVD API key for higher rate limits
        """
        self.nvd_api_key = nvd_api_key
        self.nvd_api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.cache = {}
        self.cache_duration = timedelta(hours=24)
        self.test_mode = False

    def enable_test_mode(self):
        """Enable test mode for mock responses"""
        self.test_mode = True

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
            List of vulnerabilities found in dependencies
        """
        if self.test_mode:
            return self._get_mock_results()

        try:
            # Parse dependencies
            dependencies = self._parse_dependencies(dependency_file, file_type)
            vulnerabilities = []

            # Check each dependency
            for dep in dependencies:
                # Check cache first
                cache_key = f"{dep['name']}-{dep['version']}"
                if self._is_cache_valid(cache_key):
                    vulns = self.cache[cache_key]
                else:
                    vulns = self._check_dependency(dep)
                    self._update_cache(cache_key, vulns)
                
                vulnerabilities.extend(vulns)

            return vulnerabilities

        except Exception as e:
            print(f"Error checking dependencies: {str(e)}")
            return []

    def _parse_dependencies(
        self,
        dependency_file: str,
        file_type: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Parse dependency file to extract package information.

        Args:
            dependency_file: Path to dependency file
            file_type: Type of dependency file

        Returns:
            List of dictionaries containing package information
        """
        if not os.path.exists(dependency_file):
            raise FileNotFoundError(f"Dependency file not found: {dependency_file}")

        # Determine file type if not provided
        if not file_type:
            file_type = self._detect_file_type(dependency_file)

        with open(dependency_file, 'r') as f:
            content = f.read()

        if file_type == 'requirements':
            return self._parse_requirements(content)
        elif file_type == 'package.json':
            return self._parse_package_json(content)
        elif file_type == 'pom.xml':
            return self._parse_pom_xml(content)
        else:
            raise ValueError(f"Unsupported dependency file type: {file_type}")

    def _detect_file_type(self, file_path: str) -> str:
        """Detect dependency file type from file name"""
        if file_path.endswith('requirements.txt'):
            return 'requirements'
        elif file_path.endswith('package.json'):
            return 'package.json'
        elif file_path.endswith('pom.xml'):
            return 'pom.xml'
        else:
            raise ValueError("Unable to detect dependency file type")

    def _parse_requirements(self, content: str) -> List[Dict[str, str]]:
        """Parse Python requirements.txt file"""
        dependencies = []
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                # Parse package name and version
                match = re.match(r'^([a-zA-Z0-9-_.]+)([=<>!~]+)([a-zA-Z0-9-_.]+)', line)
                if match:
                    dependencies.append({
                        'name': match.group(1),
                        'version': match.group(3),
                        'ecosystem': 'pypi'
                    })
        return dependencies

    def _parse_package_json(self, content: str) -> List[Dict[str, str]]:
        """Parse Node.js package.json file"""
        data = json.loads(content)
        dependencies = []
        
        # Parse both dependencies and devDependencies
        for dep_type in ['dependencies', 'devDependencies']:
            if dep_type in data:
                for name, version in data[dep_type].items():
                    # Remove version prefix characters
                    version = re.sub(r'^[^0-9]*', '', version)
                    dependencies.append({
                        'name': name,
                        'version': version,
                        'ecosystem': 'npm'
                    })
        return dependencies

    def _parse_pom_xml(self, content: str) -> List[Dict[str, str]]:
        """Parse Maven pom.xml file"""
        dependencies = []
        # Basic XML parsing - for production use a proper XML parser
        matches = re.finditer(
            r'<dependency>.*?<groupId>(.*?)</groupId>.*?<artifactId>(.*?)</artifactId>.*?<version>(.*?)</version>.*?</dependency>',
            content,
            re.DOTALL
        )
        for match in matches:
            dependencies.append({
                'name': f"{match.group(1)}:{match.group(2)}",
                'version': match.group(3),
                'ecosystem': 'maven'
            })
        return dependencies

    def _check_dependency(self, dependency: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Check a single dependency for vulnerabilities.

        Args:
            dependency: Dictionary containing package information

        Returns:
            List of vulnerabilities found for the dependency
        """
        try:
            # Prepare API request
            headers = {
                'Accept': 'application/json'
            }
            if self.nvd_api_key:
                headers['apiKey'] = self.nvd_api_key

            # Search for vulnerabilities
            params = {
                'keywordSearch': f"{dependency['name']} {dependency['version']}"
            }
            response = requests.get(
                self.nvd_api_url,
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            # Process vulnerabilities
            vulnerabilities = []
            for vuln in data.get('vulnerabilities', []):
                cve = vuln.get('cve', {})
                if self._is_version_affected(
                    dependency['version'],
                    cve.get('configurations', [])
                ):
                    vulnerabilities.append(self._format_vulnerability(
                        cve,
                        dependency
                    ))

            return vulnerabilities

        except Exception as e:
            print(f"Error checking dependency {dependency['name']}: {str(e)}")
            return []

    def _is_version_affected(
        self,
        version: str,
        configurations: List[Dict[str, Any]]
    ) -> bool:
        """Check if version is affected by vulnerability"""
        try:
            pkg_version = packaging.version.parse(version)
            for config in configurations:
                for node in config.get('nodes', []):
                    for match in node.get('cpeMatch', []):
                        if match.get('vulnerable', False):
                            version_range = match.get('versionRange', '')
                            if self._version_in_range(pkg_version, version_range):
                                return True
            return False
        except Exception:
            return False

    def _version_in_range(
        self,
        version: packaging.version.Version,
        version_range: str
    ) -> bool:
        """Check if version is in specified range"""
        try:
            # Parse version range (basic implementation)
            if '<=' in version_range:
                max_version = packaging.version.parse(version_range.split('<=')[1])
                return version <= max_version
            elif '>=' in version_range:
                min_version = packaging.version.parse(version_range.split('>=')[1])
                return version >= min_version
            elif '<' in version_range:
                max_version = packaging.version.parse(version_range.split('<')[1])
                return version < max_version
            elif '>' in version_range:
                min_version = packaging.version.parse(version_range.split('>')[1])
                return version > min_version
            elif '=' in version_range:
                exact_version = packaging.version.parse(version_range.split('=')[1])
                return version == exact_version
            return False
        except Exception:
            return False

    def _format_vulnerability(
        self,
        cve: Dict[str, Any],
        dependency: Dict[str, str]
    ) -> Dict[str, Any]:
        """Format vulnerability data"""
        metrics = cve.get('metrics', {}).get('cvssMetricV31', [{}])[0]
        cvss = metrics.get('cvssData', {})

        return {
            'name': f"Vulnerable Dependency: {dependency['name']}",
            'cve_id': cve.get('id', 'Unknown'),
            'version': dependency['version'],
            'ecosystem': dependency['ecosystem'],
            'description': cve.get('descriptions', [{}])[0].get('value', ''),
            'cvss_score': cvss.get('baseScore', 0.0),
            'cvss_vector': cvss.get('vectorString', ''),
            'severity': cvss.get('baseSeverity', 'Unknown'),
            'published': cve.get('published', ''),
            'references': [ref.get('url') for ref in cve.get('references', [])],
            'solution': 'Update to a non-vulnerable version.'
        }

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

    def _get_mock_results(self) -> List[Dict[str, Any]]:
        """Return mock vulnerability results for testing"""
        return [
            {
                'name': 'Vulnerable Dependency: requests',
                'cve_id': 'CVE-2023-12345',
                'version': '2.25.0',
                'ecosystem': 'pypi',
                'description': 'Security vulnerability in requests library',
                'cvss_score': 7.5,
                'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
                'severity': 'High',
                'published': '2023-01-15T10:00:00Z',
                'references': ['https://example.com/CVE-2023-12345'],
                'solution': 'Update to version 2.26.0 or later.'
            },
            {
                'name': 'Vulnerable Dependency: django',
                'cve_id': 'CVE-2023-67890',
                'version': '3.1.0',
                'ecosystem': 'pypi',
                'description': 'SQL injection vulnerability in Django ORM',
                'cvss_score': 8.5,
                'cvss_vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
                'severity': 'Critical',
                'published': '2023-02-20T15:30:00Z',
                'references': ['https://example.com/CVE-2023-67890'],
                'solution': 'Update to version 3.1.1 or later.'
            }
        ]
