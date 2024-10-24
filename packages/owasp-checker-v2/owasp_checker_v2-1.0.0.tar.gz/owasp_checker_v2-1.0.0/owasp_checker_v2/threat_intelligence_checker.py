import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

class ThreatIntelligenceChecker:
    def __init__(self, vt_api_key: Optional[str] = None):
        self.vt_api_key = vt_api_key
        self.vt_api_url = "https://www.virustotal.com/api/v3"
        self.cache = {}
        self.cache_duration = timedelta(hours=24)
        self.test_mode = False

    def enable_test_mode(self):
        """Enable test mode for mock responses"""
        self.test_mode = True

    def enrich_vulnerability_data(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich vulnerability data with threat intelligence"""
        if not vulnerabilities:
            return []

        if self.test_mode:
            return self._get_mock_enriched_data(vulnerabilities)

        try:
            enriched_vulns = []
            for vuln in vulnerabilities:
                enriched_vuln = vuln.copy()
                
                # Check cache first
                cache_key = f"{vuln.get('name', '')}-{vuln.get('cve_id', '')}"
                if self._is_cache_valid(cache_key):
                    enriched_vulns.append(self.cache[cache_key])
                    continue

                # Enrich with threat intelligence data
                threat_data = self._get_threat_intelligence(vuln)
                enriched_vuln.update(threat_data)

                # Cache the results
                self._update_cache(cache_key, enriched_vuln)
                enriched_vulns.append(enriched_vuln)

            return enriched_vulns
        except Exception as e:
            print(f"Error enriching vulnerability data: {str(e)}")
            return vulnerabilities

    def _get_threat_intelligence(self, vulnerability: Dict[str, Any]) -> Dict[str, Any]:
        """Get threat intelligence data for a vulnerability"""
        try:
            if not self.vt_api_key:
                return self._get_default_threat_data()

            # Prepare search terms
            search_terms = []
            if 'cve_id' in vulnerability:
                search_terms.append(vulnerability['cve_id'])
            if 'name' in vulnerability:
                search_terms.append(vulnerability['name'])

            threat_data = {
                'exploitation_risk': 'Unknown',
                'active_exploits': False,
                'last_seen': None,
                'detection_ratio': '0/0'
            }

            for term in search_terms:
                # Query VirusTotal API
                headers = {
                    'x-apikey': self.vt_api_key,
                    'Accept': 'application/json'
                }
                response = requests.get(
                    f"{self.vt_api_url}/search?query={term}",
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                # Process threat intelligence data
                if 'data' in data and data['data']:
                    item = data['data'][0]
                    stats = item.get('attributes', {}).get('last_analysis_stats', {})
                    
                    # Update threat data
                    malicious = stats.get('malicious', 0)
                    total = sum(stats.values()) if stats else 0
                    
                    if malicious > 0:
                        threat_data['active_exploits'] = True
                        threat_data['exploitation_risk'] = self._calculate_risk_level(malicious, total)
                    
                    threat_data['detection_ratio'] = f"{malicious}/{total}"
                    
                    last_seen = item.get('attributes', {}).get('last_submission_date')
                    if last_seen:
                        threat_data['last_seen'] = datetime.fromtimestamp(last_seen).strftime('%Y-%m-%d')

            return threat_data
        except Exception as e:
            print(f"Error getting threat intelligence: {str(e)}")
            return self._get_default_threat_data()

    def _calculate_risk_level(self, malicious: int, total: int) -> str:
        """Calculate risk level based on detection ratio"""
        if total == 0:
            return 'Unknown'
        
        ratio = malicious / total
        if ratio >= 0.7:
            return 'Critical'
        elif ratio >= 0.4:
            return 'High'
        elif ratio >= 0.2:
            return 'Medium'
        else:
            return 'Low'

    def _get_default_threat_data(self) -> Dict[str, Any]:
        """Return default threat data when API key is not available"""
        return {
            'exploitation_risk': 'Unknown',
            'active_exploits': False,
            'last_seen': None,
            'detection_ratio': '0/0'
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

    def _get_mock_enriched_data(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return mock enriched data for testing"""
        enriched = []
        for vuln in vulnerabilities:
            enriched_vuln = vuln.copy()
            enriched_vuln.update({
                'exploitation_risk': 'High',
                'active_exploits': True,
                'last_seen': '2024-01-24',
                'detection_ratio': '10/55'
            })
            enriched.append(enriched_vuln)
        return enriched
