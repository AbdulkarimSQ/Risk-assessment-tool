"""
Risk Assessment Tool - Configuration File
==========================================
Defines risk scoring parameters, thresholds, and severity levels
for cybersecurity risk assessment in critical infrastructure.
"""

# Risk Scoring Scale (1-10)
RISK_SCALE = {
    'min': 1,
    'max': 10
}

# Risk Severity Levels
SEVERITY_LEVELS = {
    'LOW': {'range': (1.0, 3.9), 'color': 'green', 'action': 'Monitor'},
    'MEDIUM': {'range': (4.0, 6.9), 'color': 'yellow', 'action': 'Review and Plan'},
    'HIGH': {'range': (7.0, 8.9), 'color': 'orange', 'action': 'Escalate'},
    'CRITICAL': {'range': (9.0, 10.0), 'color': 'red', 'action': 'Immediate Action Required'}
}

# Threat Categories and Base Scores
THREAT_CATEGORIES = {
    'Cyber Attack': 8,
    'Insider Threat': 7,
    'Physical Breach': 6,
    'System Failure': 5,
    'Data Breach': 9,
    'Malware': 7,
    'Phishing': 6,
    'DDoS': 6,
    'Ransomware': 9,
    'Supply Chain': 7
}

# Vulnerability Severity Scores
VULNERABILITY_SCORES = {
    'Critical': 10,
    'High': 8,
    'Medium': 5,
    'Low': 3,
    'None': 1
}

# Asset Criticality Levels
ASSET_CRITICALITY = {
    'Mission Critical': 10,  # e.g., SCADA systems in oil plants
    'High': 8,               # e.g., Production databases
    'Medium': 5,             # e.g., Office systems
    'Low': 3                 # e.g., Test environments
}

# Control Effectiveness Multipliers
CONTROL_EFFECTIVENESS = {
    'Strong': 0.3,      # Reduces risk by 70%
    'Adequate': 0.5,    # Reduces risk by 50%
    'Weak': 0.7,        # Reduces risk by 30%
    'None': 1.0         # No reduction
}

# Industry-Specific Settings (Oil & Gas / Critical Infrastructure)
INDUSTRY_CONFIG = {
    'sector': 'Oil & Gas',
    'compliance_frameworks': ['ISO 27001', 'NIST CSF', 'IEC 62443'],
    'regulatory_requirements': ['NCA ECC', 'NERC CIP'],
    'audit_retention_days': 2555  # 7 years
}

# Risk Matrix Thresholds (Likelihood × Impact)
RISK_MATRIX = {
    'likelihood': {
        'Rare': 1,
        'Unlikely': 2,
        'Possible': 3,
        'Likely': 4,
        'Almost Certain': 5
    },
    'impact': {
        'Negligible': 1,
        'Minor': 2,
        'Moderate': 3,
        'Major': 4,
        'Catastrophic': 5
    }
}

# Decision Thresholds for Access Control (from MSc project)
ACCESS_DECISION_THRESHOLDS = {
    'ALLOW': 3,      # Risk score ≤ 3
    'ESCALATE': 7,   # Risk score 4-7
    'DENY': 8        # Risk score ≥ 8
}

# Report Settings
REPORT_CONFIG = {
    'company_name': 'Risk Assessment Framework',
    'report_author': 'Abdulkarim Alqahtani',
    'output_format': 'PDF',
    'include_charts': True,
    'include_recommendations': True
}