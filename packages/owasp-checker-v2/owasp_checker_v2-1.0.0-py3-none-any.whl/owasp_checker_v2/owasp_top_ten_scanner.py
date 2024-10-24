import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import re
from urllib.parse import urlparse

class OWASPTopTenScanner:
    def __init__(self, zap_proxy_address: str):
        self.zap_proxy_address = zap_proxy_address
        self.cache = {}
        self.cache_duration = timedelta(hours=24)
        self.test_mode = False

    def enable_test_mode(self):
        """Enable test mode for mock responses"""
        self.test_mode = True

    def scan_url(self, url: str, vulnerability_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Scan a URL for OWASP Top Ten vulnerabilities"""
        if not url:
            raise ValueError("URL cannot be empty")

        if not isinstance(url, str):
            raise ValueError("URL must be a string")

        if not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format. Must start with http:// or https://")

        if self.test_mode:
            return self._get_mock_results()

        try:
            # Check cache first
            cache_key = f"{url}-{'-'.join(vulnerability_types or [])}"
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]

            # Validate URL format and accessibility
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                raise ValueError("Invalid URL format")

            # Initialize scan
            scan_id = self._start_scan(url)
            if not scan_id:
                return []

            # Wait for scan to complete
            self._wait_for_scan_completion(scan_id)

            # Get scan results
            results = self._get_scan_results(scan_id, vulnerability_types)

            # Filter results if specific vulnerability types are requested
            if vulnerability_types:
                results = [r for r in results if any(vt.lower() in r['name'].lower() 
                                                   for vt in vulnerability_types)]

            # Cache the results
            self._update_cache(cache_key, results)
            return results

        except requests.exceptions.RequestException as e:
            print(f"Network error during scan: {str(e)}")
            raise
        except Exception as e:
            print(f"Error during scan: {str(e)}")
            raise

    def _start_scan(self, url: str) -> Optional[str]:
        """Start a new scan"""
        try:
            response = requests.get(
                f"{self.zap_proxy_address}/JSON/spider/action/scan/",
                params={'url': url},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data.get('scan')
        except Exception as e:
            print(f"Error starting scan: {str(e)}")
            return None

    def _wait_for_scan_completion(self, scan_id: str) -> None:
        """Wait for scan to complete"""
        try:
            while True:
                response = requests.get(
                    f"{self.zap_proxy_address}/JSON/spider/view/status/",
                    params={'scanId': scan_id},
                    timeout=30
                )
                response.raise_for_status()
                status = response.json().get('status', '0')
                if status == '100':  # Scan completed
                    break
                time.sleep(5)  # Wait before checking again
        except Exception as e:
            print(f"Error checking scan status: {str(e)}")

    def _get_scan_results(self, scan_id: str, vulnerability_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Get scan results"""
        try:
            response = requests.get(
                f"{self.zap_proxy_address}/JSON/core/view/alerts/",
                params={'scanId': scan_id},
                timeout=30
            )
            response.raise_for_status()
            alerts = response.json().get('alerts', [])

            # Process and format results
            results = []
            for alert in alerts:
                result = {
                    'name': alert.get('name', 'Unknown'),
                    'risk': alert.get('risk', 'Info'),
                    'confidence': alert.get('confidence', 'Low'),
                    'description': alert.get('description', ''),
                    'solution': alert.get('solution', ''),
                    'url': alert.get('url', ''),
                    'param': alert.get('param', ''),
                    'evidence': alert.get('evidence', ''),
                    'cvss_score': alert.get('cvssScore', '0.0')
                }
                results.append(result)

            return results
        except Exception as e:
            print(f"Error getting scan results: {str(e)}")
            return []

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
        """Return mock scan results for testing"""
        return [
            {
                'name': 'SQL Injection',
                'risk': 'High',
                'confidence': 'Medium',
                'description': 'SQL injection vulnerability found',
                'solution': 'Use parameterized queries',
                'url': 'http://example.com/test',
                'param': 'id',
                'evidence': "' OR '1'='1",
                'cvss_score': 8.5
            },
            {
                'name': 'XSS',
                'risk': 'Medium',
                'confidence': 'High',
                'description': 'Cross-site scripting vulnerability',
                'solution': 'Sanitize user input',
                'url': 'http://example.com/test',
                'param': 'comment',
                'evidence': '<script>alert(1)</script>',
                'cvss_score': 6.5
            }
        ]
