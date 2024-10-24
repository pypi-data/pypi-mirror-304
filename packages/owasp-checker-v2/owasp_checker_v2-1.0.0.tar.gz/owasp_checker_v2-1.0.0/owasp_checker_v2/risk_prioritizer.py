#!/usr/bin/env python3
"""
Risk-based vulnerability prioritization module.

This module provides functionality to prioritize vulnerabilities based on multiple
risk factors including CVSS score, threat intelligence data, and asset importance.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RiskFactors:
    """Risk factors used for vulnerability prioritization"""
    cvss_score: float = 0.0
    exploitation_risk: str = 'Unknown'
    active_exploits: bool = False
    detection_confidence: str = 'Low'
    asset_criticality: str = 'Low'

class RiskPrioritizer:
    """
    Handles risk-based prioritization of vulnerabilities.
    """

    def __init__(self):
        """Initialize the RiskPrioritizer"""
        self.risk_levels = ['Critical', 'High', 'Medium', 'Low', 'Info']
        self.confidence_levels = ['High', 'Medium', 'Low']
        self.exploitation_levels = ['Critical', 'High', 'Medium', 'Low', 'Unknown']

    def prioritize_vulnerabilities(
        self,
        vulnerabilities: List[Dict[str, Any]],
        asset_criticality: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Prioritize vulnerabilities based on risk factors.

        Args:
            vulnerabilities: List of vulnerability dictionaries
            asset_criticality: Optional criticality level of the scanned asset

        Returns:
            List of vulnerabilities sorted by risk priority
        """
        if not vulnerabilities:
            return []

        # Calculate risk scores
        scored_vulns = []
        for vuln in vulnerabilities:
            risk_score = self._calculate_risk_score(vuln, asset_criticality)
            scored_vuln = vuln.copy()
            scored_vuln['risk_score'] = risk_score
            scored_vulns.append(scored_vuln)

        # Sort by risk score (descending)
        prioritized_vulns = sorted(
            scored_vulns,
            key=lambda x: x['risk_score'],
            reverse=True
        )

        # Add priority levels
        return self._assign_priority_levels(prioritized_vulns)

    def _calculate_risk_score(
        self,
        vulnerability: Dict[str, Any],
        asset_criticality: Optional[str] = None
    ) -> float:
        """
        Calculate a risk score for a vulnerability.

        Args:
            vulnerability: Vulnerability dictionary
            asset_criticality: Optional criticality level of the scanned asset

        Returns:
            Risk score between 0 and 10
        """
        # Extract risk factors
        risk_factors = RiskFactors(
            cvss_score=float(vulnerability.get('cvss_score', 0.0)),
            exploitation_risk=vulnerability.get('exploitation_risk', 'Unknown'),
            active_exploits=vulnerability.get('active_exploits', False),
            detection_confidence=vulnerability.get('confidence', 'Low'),
            asset_criticality=asset_criticality or 'Low'
        )

        # Base score from CVSS
        base_score = risk_factors.cvss_score

        # Adjust for exploitation risk
        exploitation_multiplier = self._get_exploitation_multiplier(
            risk_factors.exploitation_risk
        )
        base_score *= exploitation_multiplier

        # Adjust for active exploits
        if risk_factors.active_exploits:
            base_score *= 1.2  # 20% increase for active exploits

        # Adjust for detection confidence
        confidence_multiplier = self._get_confidence_multiplier(
            risk_factors.detection_confidence
        )
        base_score *= confidence_multiplier

        # Adjust for asset criticality
        criticality_multiplier = self._get_criticality_multiplier(
            risk_factors.asset_criticality
        )
        base_score *= criticality_multiplier

        # Ensure score is between 0 and 10
        return min(max(base_score, 0.0), 10.0)

    def _get_exploitation_multiplier(self, exploitation_risk: str) -> float:
        """Get multiplier based on exploitation risk level"""
        multipliers = {
            'Critical': 1.3,
            'High': 1.2,
            'Medium': 1.1,
            'Low': 1.0,
            'Unknown': 1.0
        }
        return multipliers.get(exploitation_risk, 1.0)

    def _get_confidence_multiplier(self, confidence: str) -> float:
        """Get multiplier based on detection confidence"""
        multipliers = {
            'High': 1.2,
            'Medium': 1.1,
            'Low': 1.0
        }
        return multipliers.get(confidence, 1.0)

    def _get_criticality_multiplier(self, criticality: str) -> float:
        """Get multiplier based on asset criticality"""
        multipliers = {
            'Critical': 1.4,
            'High': 1.3,
            'Medium': 1.2,
            'Low': 1.1
        }
        return multipliers.get(criticality, 1.0)

    def _assign_priority_levels(
        self,
        scored_vulns: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Assign priority levels based on risk scores.

        Args:
            scored_vulns: List of vulnerabilities with risk scores

        Returns:
            List of vulnerabilities with priority levels
        """
        prioritized = []
        for vuln in scored_vulns:
            priority_vuln = vuln.copy()
            score = vuln['risk_score']

            # Assign priority level based on score
            if score >= 9.0:
                priority_vuln['priority'] = 'Critical'
            elif score >= 7.0:
                priority_vuln['priority'] = 'High'
            elif score >= 4.0:
                priority_vuln['priority'] = 'Medium'
            elif score >= 0.1:
                priority_vuln['priority'] = 'Low'
            else:
                priority_vuln['priority'] = 'Info'

            prioritized.append(priority_vuln)

        return prioritized

    def get_risk_metrics(
        self,
        vulnerabilities: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate risk metrics for a set of vulnerabilities.

        Args:
            vulnerabilities: List of vulnerability dictionaries

        Returns:
            Dictionary containing risk metrics
        """
        if not vulnerabilities:
            return {
                'total_vulnerabilities': 0,
                'risk_levels': {},
                'average_risk_score': 0.0,
                'highest_risk_score': 0.0,
                'active_exploits_count': 0
            }

        # Calculate metrics
        risk_levels = {level: 0 for level in self.risk_levels}
        total_score = 0.0
        highest_score = 0.0
        active_exploits = 0

        for vuln in vulnerabilities:
            # Count risk levels
            risk_levels[vuln.get('priority', 'Info')] += 1

            # Track scores
            score = vuln.get('risk_score', 0.0)
            total_score += score
            highest_score = max(highest_score, score)

            # Count active exploits
            if vuln.get('active_exploits', False):
                active_exploits += 1

        return {
            'total_vulnerabilities': len(vulnerabilities),
            'risk_levels': risk_levels,
            'average_risk_score': total_score / len(vulnerabilities),
            'highest_risk_score': highest_score,
            'active_exploits_count': active_exploits
        }
