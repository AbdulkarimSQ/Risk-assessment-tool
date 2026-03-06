"""
Tests for Risk Calculator
=========================
Unit tests for the risk calculation engine.
"""

import pytest
from src.asset import Asset
from src.risk_calculator import RiskCalculator


class TestThreatScoring:
    """Tests for threat score calculation."""

    def test_calculate_threat_score_single_threat(self, risk_calculator):
        """Test threat score with a single known threat."""
        threats = ["Cyber Attack"]
        score = risk_calculator.calculate_threat_score(threats)
        assert score == 8  # Cyber Attack = 8

    def test_calculate_threat_score_multiple_threats(self, risk_calculator):
        """Test threat score with multiple threats (average)."""
        threats = ["Cyber Attack", "Ransomware"]  # 8 + 9 = 17, avg = 8.5
        score = risk_calculator.calculate_threat_score(threats)
        assert score == 8.5

    def test_calculate_threat_score_empty_list(self, risk_calculator):
        """Test threat score with no threats returns minimum."""
        score = risk_calculator.calculate_threat_score([])
        assert score == 1.0

    def test_calculate_threat_score_unknown_threat(self, risk_calculator):
        """Test threat score with unknown threat defaults to 5."""
        threats = ["Unknown Threat Type"]
        score = risk_calculator.calculate_threat_score(threats)
        assert score == 5  # Default for unknown

    def test_calculate_threat_score_all_threats(self, risk_calculator):
        """Test threat score with all known threat types."""
        all_threats = list(risk_calculator.threat_scores.keys())
        score = risk_calculator.calculate_threat_score(all_threats)
        expected = sum(risk_calculator.threat_scores.values()) / len(all_threats)
        assert score == expected


class TestVulnerabilityScoring:
    """Tests for vulnerability score calculation."""

    def test_calculate_vuln_score_critical(self, risk_calculator):
        """Test vulnerability score with critical severity."""
        vulns = ["Critical - Unpatched system"]
        score = risk_calculator.calculate_vulnerability_score(vulns)
        assert score == 10

    def test_calculate_vuln_score_high(self, risk_calculator):
        """Test vulnerability score with high severity."""
        vulns = ["High - Weak authentication"]
        score = risk_calculator.calculate_vulnerability_score(vulns)
        assert score == 8

    def test_calculate_vuln_score_medium(self, risk_calculator):
        """Test vulnerability score with medium severity."""
        vulns = ["Medium - Missing segmentation"]
        score = risk_calculator.calculate_vulnerability_score(vulns)
        assert score == 5

    def test_calculate_vuln_score_low(self, risk_calculator):
        """Test vulnerability score with low severity."""
        vulns = ["Low - Minor configuration issue"]
        score = risk_calculator.calculate_vulnerability_score(vulns)
        assert score == 3

    def test_calculate_vuln_score_mixed_takes_max(self, risk_calculator):
        """Test that mixed severities return the maximum (worst-case)."""
        vulns = ["Low - Minor issue", "Critical - Major flaw", "Medium - Some problem"]
        score = risk_calculator.calculate_vulnerability_score(vulns)
        assert score == 10  # Critical is highest

    def test_calculate_vuln_score_empty_list(self, risk_calculator):
        """Test vulnerability score with no vulnerabilities."""
        score = risk_calculator.calculate_vulnerability_score([])
        assert score == 1.0

    def test_calculate_vuln_score_no_severity_prefix(self, risk_calculator):
        """Test vulnerability without severity prefix defaults to Medium."""
        vulns = ["Some vulnerability without severity"]
        score = risk_calculator.calculate_vulnerability_score(vulns)
        assert score == 5  # Medium default


class TestExtractSeverity:
    """Tests for severity extraction from vulnerability strings."""

    def test_extract_severity_critical(self, risk_calculator):
        """Test extracting Critical severity."""
        severity = risk_calculator._extract_severity("Critical - Test")
        assert severity == "Critical"

    def test_extract_severity_high(self, risk_calculator):
        """Test extracting High severity."""
        severity = risk_calculator._extract_severity("High - Test")
        assert severity == "High"

    def test_extract_severity_case_insensitive(self, risk_calculator):
        """Test that severity extraction is case insensitive."""
        severity = risk_calculator._extract_severity("CRITICAL - Test")
        assert severity == "Critical"

    def test_extract_severity_default(self, risk_calculator):
        """Test default severity for unrecognized strings."""
        severity = risk_calculator._extract_severity("Unknown format")
        assert severity == "Medium"

    def test_extract_severity_none_input(self, risk_calculator):
        """Test handling of None input."""
        severity = risk_calculator._extract_severity(None)
        assert severity == "Medium"

    def test_extract_severity_empty_string(self, risk_calculator):
        """Test handling of empty string."""
        severity = risk_calculator._extract_severity("")
        assert severity == "Medium"


class TestCriticalityWeight:
    """Tests for criticality weight retrieval."""

    def test_mission_critical_weight(self, risk_calculator):
        """Test Mission Critical weight."""
        weight = risk_calculator.get_criticality_weight("Mission Critical")
        assert weight == 10

    def test_high_criticality_weight(self, risk_calculator):
        """Test High criticality weight."""
        weight = risk_calculator.get_criticality_weight("High")
        assert weight == 8

    def test_medium_criticality_weight(self, risk_calculator):
        """Test Medium criticality weight."""
        weight = risk_calculator.get_criticality_weight("Medium")
        assert weight == 5

    def test_low_criticality_weight(self, risk_calculator):
        """Test Low criticality weight."""
        weight = risk_calculator.get_criticality_weight("Low")
        assert weight == 3

    def test_unknown_criticality_defaults(self, risk_calculator):
        """Test unknown criticality defaults to 5."""
        weight = risk_calculator.get_criticality_weight("Unknown")
        assert weight == 5


class TestControlMultiplier:
    """Tests for control effectiveness multiplier."""

    def test_strong_controls(self, risk_calculator):
        """Test Strong control effectiveness (70% reduction)."""
        multiplier = risk_calculator.get_control_multiplier("Strong")
        assert multiplier == 0.3

    def test_adequate_controls(self, risk_calculator):
        """Test Adequate control effectiveness (50% reduction)."""
        multiplier = risk_calculator.get_control_multiplier("Adequate")
        assert multiplier == 0.5

    def test_weak_controls(self, risk_calculator):
        """Test Weak control effectiveness (30% reduction)."""
        multiplier = risk_calculator.get_control_multiplier("Weak")
        assert multiplier == 0.7

    def test_no_controls(self, risk_calculator):
        """Test no controls (no reduction)."""
        multiplier = risk_calculator.get_control_multiplier("None")
        assert multiplier == 1.0

    def test_unknown_controls_default(self, risk_calculator):
        """Test unknown control effectiveness defaults to 1.0."""
        multiplier = risk_calculator.get_control_multiplier("Unknown")
        assert multiplier == 1.0


class TestInherentRiskCalculation:
    """Tests for inherent risk calculation."""

    def test_inherent_risk_mission_critical(self, risk_calculator, sample_asset):
        """Test inherent risk for mission critical asset."""
        risk = risk_calculator.calculate_inherent_risk(sample_asset)
        # Threat avg: (8+9)/2 = 8.5, Vuln max: 10, Crit: 10
        # Base: (8.5+10)/2 = 9.25, Weighted: 9.25*10/10 = 9.25
        assert 8 <= risk <= 10
        assert isinstance(risk, float)

    def test_inherent_risk_low_criticality(self, risk_calculator, minimal_asset):
        """Test inherent risk for low criticality asset."""
        risk = risk_calculator.calculate_inherent_risk(minimal_asset)
        # Low threats, low vulns, low criticality = low risk
        assert risk < 5

    def test_inherent_risk_clamped_to_range(self, risk_calculator, high_risk_asset):
        """Test that inherent risk is clamped to 1-10."""
        risk = risk_calculator.calculate_inherent_risk(high_risk_asset)
        assert 1.0 <= risk <= 10.0

    def test_inherent_risk_no_vulns(self, risk_calculator, no_vuln_asset):
        """Test inherent risk with no vulnerabilities."""
        risk = risk_calculator.calculate_inherent_risk(no_vuln_asset)
        # Should be lower due to minimal vulnerability score
        assert risk < 5


class TestResidualRiskCalculation:
    """Tests for residual risk calculation."""

    def test_residual_risk_with_adequate_controls(self, risk_calculator, sample_asset):
        """Test residual risk with adequate controls (50% reduction)."""
        inherent = risk_calculator.calculate_inherent_risk(sample_asset)
        residual = risk_calculator.calculate_residual_risk(sample_asset)
        # Adequate = 0.5 multiplier
        assert residual == pytest.approx(inherent * 0.5, rel=0.01)

    def test_residual_risk_with_strong_controls(self, risk_calculator, minimal_asset):
        """Test residual risk with strong controls (70% reduction)."""
        inherent = risk_calculator.calculate_inherent_risk(minimal_asset)
        residual = risk_calculator.calculate_residual_risk(minimal_asset)
        # Strong = 0.3 multiplier
        expected = max(1.0, inherent * 0.3)
        assert residual == pytest.approx(expected, rel=0.01)

    def test_residual_risk_with_no_controls(self, risk_calculator, high_risk_asset):
        """Test residual risk with no controls."""
        inherent = risk_calculator.calculate_inherent_risk(high_risk_asset)
        residual = risk_calculator.calculate_residual_risk(high_risk_asset)
        # None = 1.0 multiplier, so residual equals inherent
        assert residual == inherent

    def test_residual_risk_minimum_is_one(self, risk_calculator, minimal_asset):
        """Test that residual risk minimum is 1.0."""
        residual = risk_calculator.calculate_residual_risk(minimal_asset)
        assert residual >= 1.0

    def test_residual_less_than_or_equal_inherent(self, risk_calculator, sample_asset):
        """Test that residual risk is never higher than inherent risk."""
        inherent = risk_calculator.calculate_inherent_risk(sample_asset)
        residual = risk_calculator.calculate_residual_risk(sample_asset)
        assert residual <= inherent


class TestRiskSeverity:
    """Tests for risk severity classification."""

    def test_low_severity(self, risk_calculator):
        """Test LOW severity classification."""
        assert risk_calculator.get_risk_severity(1.0) == "LOW"
        assert risk_calculator.get_risk_severity(2.5) == "LOW"
        assert risk_calculator.get_risk_severity(3.9) == "LOW"

    def test_medium_severity(self, risk_calculator):
        """Test MEDIUM severity classification."""
        assert risk_calculator.get_risk_severity(4.0) == "MEDIUM"
        assert risk_calculator.get_risk_severity(5.5) == "MEDIUM"
        assert risk_calculator.get_risk_severity(6.9) == "MEDIUM"

    def test_high_severity(self, risk_calculator):
        """Test HIGH severity classification."""
        assert risk_calculator.get_risk_severity(7.0) == "HIGH"
        assert risk_calculator.get_risk_severity(8.0) == "HIGH"
        assert risk_calculator.get_risk_severity(8.9) == "HIGH"

    def test_critical_severity(self, risk_calculator):
        """Test CRITICAL severity classification."""
        assert risk_calculator.get_risk_severity(9.0) == "CRITICAL"
        assert risk_calculator.get_risk_severity(9.5) == "CRITICAL"
        assert risk_calculator.get_risk_severity(10.0) == "CRITICAL"


class TestRecommendedAction:
    """Tests for recommended action retrieval."""

    def test_low_risk_action(self, risk_calculator):
        """Test recommended action for low risk."""
        action = risk_calculator.get_recommended_action(2.0)
        assert action == "Monitor"

    def test_medium_risk_action(self, risk_calculator):
        """Test recommended action for medium risk."""
        action = risk_calculator.get_recommended_action(5.0)
        assert action == "Review and Plan"

    def test_high_risk_action(self, risk_calculator):
        """Test recommended action for high risk."""
        action = risk_calculator.get_recommended_action(7.5)
        assert action == "Escalate"

    def test_critical_risk_action(self, risk_calculator):
        """Test recommended action for critical risk."""
        action = risk_calculator.get_recommended_action(9.5)
        assert action == "Immediate Action Required"


class TestAssetAssessment:
    """Tests for complete asset assessment."""

    def test_assess_asset_returns_dict(self, risk_calculator, sample_asset):
        """Test that assess_asset returns a dictionary."""
        assessment = risk_calculator.assess_asset(sample_asset)
        assert isinstance(assessment, dict)

    def test_assess_asset_contains_required_fields(self, risk_calculator, sample_asset):
        """Test that assessment contains all required fields."""
        assessment = risk_calculator.assess_asset(sample_asset)

        required_fields = [
            'asset_id', 'asset_name', 'asset_type', 'criticality',
            'inherent_risk', 'residual_risk', 'risk_reduction',
            'reduction_percentage', 'severity', 'recommended_action',
            'threat_count', 'vulnerability_count', 'control_count',
            'control_effectiveness'
        ]

        for field in required_fields:
            assert field in assessment, f"Missing field: {field}"

    def test_assess_asset_values(self, risk_calculator, sample_asset):
        """Test assessment values are correct."""
        assessment = risk_calculator.assess_asset(sample_asset)

        assert assessment['asset_id'] == "TEST-001"
        assert assessment['asset_name'] == "Test SCADA System"
        assert assessment['threat_count'] == 2
        assert assessment['vulnerability_count'] == 2
        assert assessment['control_count'] == 2
        assert assessment['control_effectiveness'] == "Adequate"

    def test_assess_asset_risk_reduction(self, risk_calculator, sample_asset):
        """Test that risk reduction is calculated correctly."""
        assessment = risk_calculator.assess_asset(sample_asset)

        expected_reduction = assessment['inherent_risk'] - assessment['residual_risk']
        assert assessment['risk_reduction'] == pytest.approx(expected_reduction, rel=0.01)

    def test_assess_asset_reduction_percentage(self, risk_calculator, sample_asset):
        """Test that reduction percentage is calculated correctly."""
        assessment = risk_calculator.assess_asset(sample_asset)

        expected_pct = (assessment['risk_reduction'] / assessment['inherent_risk']) * 100
        assert assessment['reduction_percentage'] == pytest.approx(expected_pct, rel=0.1)


class TestMultipleAssetAssessment:
    """Tests for multiple asset assessment."""

    def test_assess_multiple_returns_list(self, risk_calculator, multiple_assets):
        """Test that assess_multiple_assets returns a list."""
        results = risk_calculator.assess_multiple_assets(multiple_assets)
        assert isinstance(results, list)
        assert len(results) == len(multiple_assets)

    def test_assess_multiple_sorted_by_risk(self, risk_calculator, multiple_assets):
        """Test that results are sorted by residual risk (descending)."""
        results = risk_calculator.assess_multiple_assets(multiple_assets)

        for i in range(len(results) - 1):
            assert results[i]['residual_risk'] >= results[i + 1]['residual_risk']

    def test_assess_multiple_empty_list(self, risk_calculator):
        """Test assessing empty asset list."""
        results = risk_calculator.assess_multiple_assets([])
        assert results == []


class TestSummaryStatistics:
    """Tests for summary statistics calculation."""

    def test_summary_statistics_structure(self, risk_calculator, multiple_assessments):
        """Test summary statistics contains required fields."""
        stats = risk_calculator.get_summary_statistics(multiple_assessments)

        required_fields = [
            'total_assets', 'severity_distribution', 'average_inherent_risk',
            'average_residual_risk', 'average_risk_reduction',
            'highest_risk_asset', 'highest_risk_score'
        ]

        for field in required_fields:
            assert field in stats, f"Missing field: {field}"

    def test_summary_statistics_total_assets(self, risk_calculator, multiple_assessments):
        """Test total assets count is correct."""
        stats = risk_calculator.get_summary_statistics(multiple_assessments)
        assert stats['total_assets'] == len(multiple_assessments)

    def test_summary_statistics_severity_distribution(self, risk_calculator, multiple_assessments):
        """Test severity distribution contains all levels."""
        stats = risk_calculator.get_summary_statistics(multiple_assessments)
        dist = stats['severity_distribution']

        assert 'CRITICAL' in dist
        assert 'HIGH' in dist
        assert 'MEDIUM' in dist
        assert 'LOW' in dist

        # Total should equal number of assets
        total = sum(dist.values())
        assert total == stats['total_assets']

    def test_summary_statistics_highest_risk(self, risk_calculator, multiple_assessments):
        """Test highest risk asset is identified correctly."""
        stats = risk_calculator.get_summary_statistics(multiple_assessments)

        # First item in sorted list should be highest risk
        assert stats['highest_risk_asset'] == multiple_assessments[0]['asset_name']
        assert stats['highest_risk_score'] == multiple_assessments[0]['residual_risk']

    def test_summary_statistics_empty_list(self, risk_calculator):
        """Test summary statistics with empty list."""
        stats = risk_calculator.get_summary_statistics([])
        assert stats == {}

    def test_summary_statistics_averages(self, risk_calculator, multiple_assessments):
        """Test average calculations are correct."""
        stats = risk_calculator.get_summary_statistics(multiple_assessments)

        expected_avg_inherent = sum(a['inherent_risk'] for a in multiple_assessments) / len(multiple_assessments)
        expected_avg_residual = sum(a['residual_risk'] for a in multiple_assessments) / len(multiple_assessments)

        assert stats['average_inherent_risk'] == pytest.approx(expected_avg_inherent, rel=0.01)
        assert stats['average_residual_risk'] == pytest.approx(expected_avg_residual, rel=0.01)
