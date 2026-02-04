"""
Asset Class Definition
======================
Represents IT/OT assets in critical infrastructure environments.
Used for risk assessment and security control evaluation.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Asset:
    """
    Represents a technology asset in the infrastructure.

    Attributes:
        asset_id: Unique identifier for the asset
        name: Human-readable name
        asset_type: Type of asset (Server, SCADA, Network Device, etc.)
        criticality: Business/operational criticality level
        location: Physical or logical location
        owner: Responsible person/department
        vulnerabilities: List of known vulnerabilities
        threats: List of applicable threats
        existing_controls: List of security controls in place
        control_effectiveness: Overall control effectiveness rating
    """

    asset_id: str
    name: str
    asset_type: str
    criticality: str
    location: str
    owner: str
    vulnerabilities: List[str]
    threats: List[str]
    existing_controls: List[str]
    control_effectiveness: str
    last_assessment: Optional[str] = None

    def __post_init__(self):
        """Validate asset data after initialization"""
        if not self.asset_id:
            raise ValueError("Asset ID is required")
        if not self.name:
            raise ValueError("Asset name is required")

        # Set default assessment date if not provided
        if self.last_assessment is None:
            self.last_assessment = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        """Convert asset to dictionary for JSON serialization"""
        return {
            'asset_id': self.asset_id,
            'name': self.name,
            'asset_type': self.asset_type,
            'criticality': self.criticality,
            'location': self.location,
            'owner': self.owner,
            'vulnerabilities': self.vulnerabilities,
            'threats': self.threats,
            'existing_controls': self.existing_controls,
            'control_effectiveness': self.control_effectiveness,
            'last_assessment': self.last_assessment
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Asset':
        """Create Asset instance from dictionary"""
        return cls(
            asset_id=data['asset_id'],
            name=data['name'],
            asset_type=data['asset_type'],
            criticality=data['criticality'],
            location=data['location'],
            owner=data['owner'],
            vulnerabilities=data.get('vulnerabilities', []),
            threats=data.get('threats', []),
            existing_controls=data.get('existing_controls', []),
            control_effectiveness=data.get('control_effectiveness', 'None'),
            last_assessment=data.get('last_assessment')
        )

    def get_summary(self) -> str:
        """Return a formatted summary of the asset"""
        return f"""
Asset: {self.name} ({self.asset_id})
Type: {self.asset_type}
Criticality: {self.criticality}
Location: {self.location}
Owner: {self.owner}
Vulnerabilities: {len(self.vulnerabilities)}
Threats: {len(self.threats)}
Controls: {len(self.existing_controls)} ({self.control_effectiveness})
Last Assessment: {self.last_assessment}
"""