"""Risk Calculator Engine
======================
Core risk assessment logic for cybersecurity risk evaluation.
Implements risk scoring based on threat likelihood, vulnerability severity,
asset criticality, and control effectiveness.

Risk Formula:
    Base Risk = (Threat Score + Vulnerability Score) × Asset Criticality Weight
    Residual Risk = Base Risk × Control Effectiveness Multiplier
"""

from typing import List, Dict

import config
from src.asset import Asset


class RiskCalculator:
    """Calculate cybersecurity risk scores for assets."""

    def __init__(self):
        self.threat_scores = config.THREAT_CATEGORIES
        self.vuln_scores = config.VULNERABILITY_SCORES
        self.criticality_weights = config.ASSET_CRITICALITY
        self.control_multipliers = config.CONTROL_EFFECTIVENESS
        self.severity_levels = config.SEVERITY_LEVELS

    def calculate_threat_score(self, threats: List[str]) -> float:
        """Calculate average threat score for an asset."""
        if not threats:
            return 1.0

        threat_values = [self.threat_scores.get(t, 5) for t in threats]
        return sum(threat_values) / len(threat_values)

    def calculate_vulnerability_score(self, vulnerabilities: List[str]) -> float:
        """Calculate maximum vulnerability severity score (worst-case)."""
        if not vulnerabilities:
            return 1.0

        vuln_values = []
        for vuln in vulnerabilities:
            severity = self._extract_severity(vuln)
            vuln_values.append(self.vuln_scores.get(severity, 5))

        return max(vuln_values)

    def _extract_severity(self, vulnerability: str) -> str:
        """Extract severity level from vulnerability description."""
        vuln_upper = (vulnerability or "").upper()
        for severity in self.vuln_scores.keys():
            if severity.upper() in vuln_upper:
                return severity
        return "Medium"

    def get_criticality_weight(self, criticality: str) -> float:
        """Get asset criticality weight."""
        return self.criticality_weights.get(criticality, 5)

    def get_control_multiplier(self, control_effectiveness: str) -> float:
        """Get control effectiveness multiplier."""
        return self.control_multipliers.get(control_effectiveness, 1.0)

    def calculate_inherent_risk(self, asset: Asset) -> float:
        """Calculate inherent risk (risk before controls), normalized to 1-10."""
        threat_score = self.calculate_threat_score(asset.threats)
        vuln_score = self.calculate_vulnerability_score(asset.vulnerabilities)
        criticality_weight = self.get_criticality_weight(asset.criticality)

        base_risk = (threat_score + vuln_score) / 2
        weighted_risk = (base_risk * criticality_weight) / 10

        inherent_risk = min(max(weighted_risk, 1.0), 10.0)
        return round(inherent_risk, 2)

    def calculate_residual_risk(self, asset: Asset) -> float:
        """Calculate residual risk (risk after controls), clamped to 1-10."""
        inherent_risk = self.calculate_inherent_risk(asset)
        control_multiplier = self.get_control_multiplier(asset.control_effectiveness)

        residual_risk = inherent_risk * control_multiplier
        residual_risk = max(1.0, min(10.0, residual_risk))
        return round(residual_risk, 2)

    def get_risk_severity(self, risk_score: float) -> str:
        """Determine risk severity level based on score."""
        for level, details in self.severity_levels.items():
            min_score, max_score = details["range"]
            if min_score <= risk_score <= max_score:
                return level
        return "MEDIUM"

    def get_recommended_action(self, risk_score: float) -> str:
        """Get recommended action based on risk score."""
        severity = self.get_risk_severity(risk_score)
        return self.severity_levels.get(severity, {"action": "Review and Plan"})["action"]

    def assess_asset(self, asset: Asset) -> Dict:
        """Perform complete risk assessment on an asset."""
        inherent_risk = self.calculate_inherent_risk(asset)
        residual_risk = self.calculate_residual_risk(asset)
        severity = self.get_risk_severity(residual_risk)
        action = self.get_recommended_action(residual_risk)

        risk_reduction = max(0.0, inherent_risk - residual_risk)
        reduction_percentage = (risk_reduction / inherent_risk * 100) if inherent_risk > 0 else 0

        return {
            "asset_id": asset.asset_id,
            "asset_name": asset.name,
            "asset_type": asset.asset_type,
            "criticality": asset.criticality,
            "inherent_risk": inherent_risk,
            "residual_risk": residual_risk,
            "risk_reduction": round(risk_reduction, 2),
            "reduction_percentage": round(reduction_percentage, 1),
            "severity": severity,
            "recommended_action": action,
            "threat_count": len(asset.threats),
            "vulnerability_count": len(asset.vulnerabilities),
            "control_count": len(asset.existing_controls),
            "control_effectiveness": asset.control_effectiveness,
        }

    def assess_multiple_assets(self, assets: List[Asset]) -> List[Dict]:
        """Assess multiple assets and return sorted results."""
        results = [self.assess_asset(a) for a in assets]
        results.sort(key=lambda x: x["residual_risk"], reverse=True)
        return results

    def get_summary_statistics(self, assessment_results: List[Dict]) -> Dict:
        """Calculate summary statistics for a set of assessments."""
        if not assessment_results:
            return {}

        total_assets = len(assessment_results)
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for r in assessment_results:
            sev = r.get("severity", "MEDIUM")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        avg_inherent = sum(r["inherent_risk"] for r in assessment_results) / total_assets
        avg_residual = sum(r["residual_risk"] for r in assessment_results) / total_assets
        avg_reduction = sum(r["reduction_percentage"] for r in assessment_results) / total_assets

        return {
            "total_assets": total_assets,
            "severity_distribution": severity_counts,
            "average_inherent_risk": round(avg_inherent, 2),
            "average_residual_risk": round(avg_residual, 2),
            "average_risk_reduction": round(avg_reduction, 1),
            "highest_risk_asset": assessment_results[0]["asset_name"],
            "highest_risk_score": assessment_results[0]["residual_risk"],
        }