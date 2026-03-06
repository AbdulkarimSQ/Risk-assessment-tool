"""
Pytest Configuration and Fixtures
=================================
Shared fixtures for risk assessment tool tests.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.asset import Asset
from src.risk_calculator import RiskCalculator
from src.report_generator import ReportGenerator


@pytest.fixture
def sample_asset():
    """Create a sample asset for testing."""
    return Asset(
        asset_id="TEST-001",
        name="Test SCADA System",
        asset_type="SCADA/ICS",
        criticality="Mission Critical",
        location="Test Facility",
        owner="Security Team",
        vulnerabilities=["Critical - Unpatched system", "High - Weak authentication"],
        threats=["Cyber Attack", "Ransomware"],
        existing_controls=["Firewall", "Access logging"],
        control_effectiveness="Adequate"
    )


@pytest.fixture
def minimal_asset():
    """Create a minimal asset with few vulnerabilities."""
    return Asset(
        asset_id="MIN-001",
        name="Minimal Test Asset",
        asset_type="Workstation",
        criticality="Low",
        location="Office",
        owner="IT",
        vulnerabilities=["Low - Minor issue"],
        threats=["Phishing"],
        existing_controls=["Antivirus", "Training", "EDR"],
        control_effectiveness="Strong"
    )


@pytest.fixture
def high_risk_asset():
    """Create a high-risk asset for testing."""
    return Asset(
        asset_id="HIGH-001",
        name="High Risk HMI",
        asset_type="HMI System",
        criticality="Mission Critical",
        location="Control Room",
        owner="Operations",
        vulnerabilities=[
            "Critical - Running Windows 7 (EOL)",
            "Critical - No antivirus installed",
            "High - Direct internet connectivity"
        ],
        threats=["Ransomware", "Malware", "Cyber Attack", "System Failure"],
        existing_controls=["Physical access control"],
        control_effectiveness="None"
    )


@pytest.fixture
def no_vuln_asset():
    """Create an asset with no vulnerabilities."""
    return Asset(
        asset_id="SAFE-001",
        name="Well Protected Asset",
        asset_type="Server",
        criticality="Medium",
        location="Data Center",
        owner="IT",
        vulnerabilities=[],
        threats=["Cyber Attack"],
        existing_controls=["Firewall", "IDS", "Encryption"],
        control_effectiveness="Strong"
    )


@pytest.fixture
def risk_calculator():
    """Create a RiskCalculator instance."""
    return RiskCalculator()


@pytest.fixture
def report_generator():
    """Create a ReportGenerator instance."""
    return ReportGenerator()


@pytest.fixture
def sample_assessment(sample_asset, risk_calculator):
    """Create a sample assessment result."""
    return risk_calculator.assess_asset(sample_asset)


@pytest.fixture
def multiple_assets(sample_asset, minimal_asset, high_risk_asset):
    """Create a list of multiple assets."""
    return [sample_asset, minimal_asset, high_risk_asset]


@pytest.fixture
def multiple_assessments(multiple_assets, risk_calculator):
    """Create assessments for multiple assets."""
    return risk_calculator.assess_multiple_assets(multiple_assets)


@pytest.fixture
def sample_statistics(multiple_assessments, risk_calculator):
    """Create sample statistics."""
    return risk_calculator.get_summary_statistics(multiple_assessments)
