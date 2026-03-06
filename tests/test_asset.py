"""
Tests for Asset Class
=====================
Unit tests for the Asset data model.
"""

import pytest
from datetime import datetime
from src.asset import Asset


class TestAssetCreation:
    """Tests for Asset instantiation."""

    def test_create_valid_asset(self, sample_asset):
        """Test creating a valid asset."""
        assert sample_asset.asset_id == "TEST-001"
        assert sample_asset.name == "Test SCADA System"
        assert sample_asset.asset_type == "SCADA/ICS"
        assert sample_asset.criticality == "Mission Critical"

    def test_create_asset_with_all_fields(self):
        """Test creating an asset with all fields specified."""
        asset = Asset(
            asset_id="FULL-001",
            name="Full Test Asset",
            asset_type="Server",
            criticality="High",
            location="Data Center",
            owner="IT Team",
            vulnerabilities=["High - Test vuln"],
            threats=["Cyber Attack"],
            existing_controls=["Firewall"],
            control_effectiveness="Adequate",
            last_assessment="2024-01-15"
        )
        assert asset.last_assessment == "2024-01-15"

    def test_default_assessment_date(self):
        """Test that last_assessment defaults to today's date."""
        asset = Asset(
            asset_id="DATE-001",
            name="Date Test",
            asset_type="Server",
            criticality="Low",
            location="Office",
            owner="IT",
            vulnerabilities=[],
            threats=[],
            existing_controls=[],
            control_effectiveness="None"
        )
        today = datetime.now().strftime("%Y-%m-%d")
        assert asset.last_assessment == today


class TestAssetValidation:
    """Tests for Asset validation."""

    def test_missing_asset_id_raises_error(self):
        """Test that missing asset_id raises ValueError."""
        with pytest.raises(ValueError, match="Asset ID is required"):
            Asset(
                asset_id="",
                name="Test",
                asset_type="Server",
                criticality="Low",
                location="Office",
                owner="IT",
                vulnerabilities=[],
                threats=[],
                existing_controls=[],
                control_effectiveness="None"
            )

    def test_missing_name_raises_error(self):
        """Test that missing name raises ValueError."""
        with pytest.raises(ValueError, match="Asset name is required"):
            Asset(
                asset_id="TEST-001",
                name="",
                asset_type="Server",
                criticality="Low",
                location="Office",
                owner="IT",
                vulnerabilities=[],
                threats=[],
                existing_controls=[],
                control_effectiveness="None"
            )

    def test_none_asset_id_raises_error(self):
        """Test that None asset_id raises ValueError."""
        with pytest.raises((ValueError, TypeError)):
            Asset(
                asset_id=None,
                name="Test",
                asset_type="Server",
                criticality="Low",
                location="Office",
                owner="IT",
                vulnerabilities=[],
                threats=[],
                existing_controls=[],
                control_effectiveness="None"
            )


class TestAssetSerialization:
    """Tests for Asset serialization methods."""

    def test_to_dict(self, sample_asset):
        """Test converting asset to dictionary."""
        data = sample_asset.to_dict()

        assert isinstance(data, dict)
        assert data['asset_id'] == "TEST-001"
        assert data['name'] == "Test SCADA System"
        assert data['asset_type'] == "SCADA/ICS"
        assert data['criticality'] == "Mission Critical"
        assert data['location'] == "Test Facility"
        assert data['owner'] == "Security Team"
        assert len(data['vulnerabilities']) == 2
        assert len(data['threats']) == 2
        assert len(data['existing_controls']) == 2
        assert data['control_effectiveness'] == "Adequate"

    def test_from_dict(self):
        """Test creating asset from dictionary."""
        data = {
            'asset_id': 'DICT-001',
            'name': 'Dict Test Asset',
            'asset_type': 'Database Server',
            'criticality': 'High',
            'location': 'Data Center',
            'owner': 'DBA Team',
            'vulnerabilities': ['High - SQL injection'],
            'threats': ['Data Breach'],
            'existing_controls': ['Encryption'],
            'control_effectiveness': 'Strong',
            'last_assessment': '2024-02-01'
        }

        asset = Asset.from_dict(data)

        assert asset.asset_id == 'DICT-001'
        assert asset.name == 'Dict Test Asset'
        assert asset.criticality == 'High'
        assert asset.last_assessment == '2024-02-01'

    def test_from_dict_with_defaults(self):
        """Test creating asset from dictionary with missing optional fields."""
        data = {
            'asset_id': 'MIN-DICT-001',
            'name': 'Minimal Dict Asset',
            'asset_type': 'Server',
            'criticality': 'Low',
            'location': 'Office',
            'owner': 'IT'
        }

        asset = Asset.from_dict(data)

        assert asset.vulnerabilities == []
        assert asset.threats == []
        assert asset.existing_controls == []
        assert asset.control_effectiveness == 'None'

    def test_roundtrip_serialization(self, sample_asset):
        """Test that to_dict and from_dict are inverse operations."""
        data = sample_asset.to_dict()
        restored_asset = Asset.from_dict(data)

        assert restored_asset.asset_id == sample_asset.asset_id
        assert restored_asset.name == sample_asset.name
        assert restored_asset.vulnerabilities == sample_asset.vulnerabilities
        assert restored_asset.threats == sample_asset.threats


class TestAssetSummary:
    """Tests for Asset summary method."""

    def test_get_summary(self, sample_asset):
        """Test getting asset summary string."""
        summary = sample_asset.get_summary()

        assert "TEST-001" in summary
        assert "Test SCADA System" in summary
        assert "SCADA/ICS" in summary
        assert "Mission Critical" in summary
        assert "Vulnerabilities: 2" in summary
        assert "Threats: 2" in summary
        assert "Controls: 2" in summary

    def test_summary_format(self, minimal_asset):
        """Test that summary is properly formatted."""
        summary = minimal_asset.get_summary()

        assert "Asset:" in summary
        assert "Type:" in summary
        assert "Criticality:" in summary
        assert "Location:" in summary
        assert "Owner:" in summary
