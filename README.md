 Cybersecurity Risk Assessment Tool
Python-based cybersecurity risk assessment tool for critical infrastructure (IT/OT).

[![Tests](https://github.com/AbdulkarimSQ/Risk-assessment-tool/actions/workflows/tests.yml/badge.svg)](https://github.com/AbdulkarimSQ/Risk-assessment-tool/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/AbdulkarimSQ/Risk-assessment-tool/branch/main/graph/badge.svg)](https://codecov.io/gh/AbdulkarimSQ/Risk-assessment-tool)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Automated risk assessment framework for critical infrastructure cybersecurity, with a focus on Oil & Gas and Industrial Control Systems (ICS/OT).**

Developed by **Abdulkarim Alqahtani** as part of MSc Computer Science coursework and portfolio work at Queen Mary University of London, leveraging real-world experience from Saudi Aramco operations.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

---

## 
 Overview

This tool provides a **structured, quantitative approach** to cybersecurity risk assessment for critical infrastructure environments. It evaluates IT/OT assets based on:

- **Threat likelihood** (from cyber attacks to system failures)
- **Vulnerability severity** (Critical, High, Medium, Low)
- **Asset criticality** (Mission Critical, High, Medium, Low)
- **Control effectiveness** (Strong, Adequate, Weak, None)

The tool calculates both **inherent risk** (before controls) and **residual risk** (after controls), providing actionable insights for security decision-making.

### Outputs

- Console summary + risk matrix
- JSON export (machine-readable)
- CSV export (risk register friendly)

### Why This Tool?

Traditional risk assessment methods are often:
- ❌ Manual and time-consuming
- ❌ Subjective and inconsistent
- ❌ Difficult to audit and track
- ❌ Not tailored to industrial environments

This tool addresses these challenges by:
- ✅ Automating risk calculations with consistent methodology
- ✅ Providing quantitative risk scores (1-10 scale)
- ✅ Supporting audit trails and traceability
- ✅ Focusing on critical infrastructure (OT/ICS) security

---

## 
 Features

### Core Capabilities

- **🎯 Automated Risk Scoring**: Calculate inherent and residual risk scores using industry-standard methodology
- **📊 Risk Categorization**: Classify risks as LOW, MEDIUM, HIGH, or CRITICAL
- **🔄 Multiple Asset Assessment**: Batch process hundreds of assets efficiently
- **📈 Summary Statistics**: Get overview of risk distribution across your infrastructure
- **📝 Detailed Reporting**: Generate comprehensive reports in console, JSON, or CSV formats
- **🎨 Visual Risk Matrix**: Text-based risk matrix for quick overview
- **⚙️ Configurable Thresholds**: Customize risk calculations for your organization
- **🏭 Industry-Specific**: Tailored for Oil & Gas, manufacturing, and critical infrastructure

### Risk Assessment Methodology

The tool implements a robust risk calculation formula:

```
Inherent Risk = ((Threat Score + Vulnerability Score) / 2) × (Criticality / 10)
Residual Risk = Inherent Risk × Control Effectiveness Multiplier
```

Risk scores are normalized to a **1-10 scale** for consistency.

---

##  Installation

### Prerequisites

- Python 3.11+
- pip package manager
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/AbdulkarimSQ/Risk-assessment-tool.git
cd Risk-assessment-tool
```

### Step 2: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

**Dependencies:**
- `pandas` - Data manipulation and analysis
- `matplotlib` - Data visualization
- `reportlab` - PDF report generation
- `colorama` - Colored terminal output

### Step 3: Verify Installation

```bash
python main.py
```

You should see the tool load sample assets and display a summary report.

---

##  Usage

### Basic Usage

Run the main application:

```bash
python main.py
```

This will:
1. Load sample assets from `data/sample_assets.json`
2. Perform risk assessments on all assets
3. Display an interactive menu with report options

Exports are saved to the current working directory by default (e.g., `risk_assessment.json`, `risk_assessment.csv`). You can change the output location in `main.py` or extend the tool with a CLI flag.

### Interactive Menu Options

After running the tool, you'll see:

```
Report Options:
1. View detailed report (all assets)
2. View individual asset assessment
3. View risk matrix
4. Export to JSON
5. Export to CSV
6. Exit
```

### Command Line Examples

**Assess sample assets:**
```bash
python main.py
```

**Single asset demo:**
```python
# Edit main.py and uncomment:
# demo_single_asset()
```

### Using the Tool Programmatically

```python
# Run from the repo root (Risk-assessment-tool/)
from src.asset import Asset
from src.risk_calculator import RiskCalculator
from src.report_generator import ReportGenerator

# Create an asset
asset = Asset(
    asset_id="SCADA-001",
    name="Primary SCADA System",
    asset_type="SCADA/ICS",
    criticality="Mission Critical",
    location="Control Room A",
    owner="Operations",
    vulnerabilities=["Critical - Unpatched system"],
    threats=["Cyber Attack", "Ransomware"],
    existing_controls=["Firewall", "IDS"],
    control_effectiveness="Adequate"
)

# Assess the asset
calculator = RiskCalculator()
assessment = calculator.assess_asset(asset)

# Generate report
reporter = ReportGenerator()
reporter.print_asset_assessment(assessment)
```

---

##  Methodology

### Risk Calculation Process

#### 1. Threat Assessment
Evaluates applicable threats from a predefined taxonomy:
- Cyber Attack (8/10)
- Ransomware (9/10)
- Data Breach (9/10)
- Insider Threat (7/10)
- DDoS (6/10)
- And more...

**Calculation**: Average of all applicable threat scores

#### 2. Vulnerability Evaluation
Assesses vulnerability severity:
- **Critical**: 10/10 (e.g., unpatched critical systems)
- **High**: 8/10 (e.g., weak authentication)
- **Medium**: 5/10 (e.g., missing segmentation)
- **Low**: 3/10 (e.g., minor misconfigurations)
- **None**: 1/10

**Calculation**: Maximum (worst-case) vulnerability score

#### 3. Asset Criticality Weighting
Factors in business/operational criticality:
- **Mission Critical**: 10/10 (SCADA, HMI, core network)
- **High**: 8/10 (production databases, backup systems)
- **Medium**: 5/10 (office systems, workstations)
- **Low**: 3/10 (test environments, dev systems)

#### 4. Control Effectiveness
Evaluates existing security controls:
- **Strong**: Reduces risk by 70% (multiplier: 0.3)
- **Adequate**: Reduces risk by 50% (multiplier: 0.5)
- **Weak**: Reduces risk by 30% (multiplier: 0.7)
- **None**: No reduction (multiplier: 1.0)

#### 5. Risk Scoring
```
Inherent Risk = (Avg Threat + Max Vulnerability) / 2 × Criticality / 10
Residual Risk = Inherent Risk × Control Multiplier
```

#### 6. Severity Classification
- **CRITICAL**: 9-10 → Immediate action required
- **HIGH**: 7-8 → Escalate and plan mitigation
- **MEDIUM**: 4-6 → Review and schedule remediation
- **LOW**: 1-3 → Monitor and maintain controls

---

## 📁 Project Structure

```
Risk-assessment-tool/
│
├── src/                          # Source code
│   ├── __init__.py
│   ├── asset.py                  # Asset data model
│   ├── risk_calculator.py        # Risk assessment engine
│   └── report_generator.py       # Report generation
│
├── tests/                        # Unit tests (97 tests, 99% coverage)
│   ├── conftest.py               # Pytest fixtures
│   ├── test_asset.py             # Asset class tests
│   ├── test_risk_calculator.py   # Risk calculator tests
│   └── test_report_generator.py  # Report generator tests
│
├── data/                         # Sample data
│   └── sample_assets.json        # 10 example assets (Oil & Gas)
│
├── .github/workflows/            # CI/CD
│   └── tests.yml                 # GitHub Actions workflow
│
├── config.py                     # Configuration settings
├── main.py                       # Main application
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .gitignore                    # Git ignore rules
└── LICENSE                       # MIT License
```

---

## ⚙️ Configuration

Customize the tool by editing `config.py`:

### Risk Thresholds
```python
SEVERITY_LEVELS = {
    'LOW': {'range': (1, 3), 'action': 'Monitor'},
    'MEDIUM': {'range': (4, 6), 'action': 'Review and Plan'},
    'HIGH': {'range': (7, 8), 'action': 'Escalate'},
    'CRITICAL': {'range': (9, 10), 'action': 'Immediate Action'}
}
```

### Threat Categories
Add or modify threat types and their base scores:
```python
THREAT_CATEGORIES = {
    'Custom Threat': 7,
    # Add more...
}
```

### Control Effectiveness
Adjust control effectiveness multipliers:
```python
CONTROL_EFFECTIVENESS = {
    'Strong': 0.3,    # 70% risk reduction
    'Adequate': 0.5,  # 50% risk reduction
    # Customize...
}
```

---

## 💡 Examples

### Example 1: SCADA System Assessment

**Input Asset:**
- SCADA System (Mission Critical)
- Vulnerabilities: Critical unpatched system, weak auth
- Threats: Cyber Attack, Ransomware
- Controls: Firewall, access logging (Adequate)

Sample output:
```
Inherent Risk:  8.5/10
Residual Risk:  4.25/10 (MEDIUM)
Risk Reduction: 4.25 (50%)
Recommended Action: Review and Plan
```

### Example 2: Office Workstation

**Input Asset:**
- Workstation (Medium criticality)
- Vulnerabilities: Missing updates, no encryption
- Threats: Phishing, Malware
- Controls: Antivirus, EDR, training (Adequate)

Sample output:
```
Inherent Risk:  3.5/10
Residual Risk:  1.75/10 (LOW)
Risk Reduction: 1.75 (50%)
Recommended Action: Monitor
```

---

##  Use Cases

This tool is designed for:

- **Security Analysts**: Conducting periodic risk assessments
- **Compliance Officers**: Documenting security posture for audits
- **IT Managers**: Prioritizing security investments
- **Risk Managers**: Quantifying and tracking residual risk
- **CISO/Security Leadership**: Executive reporting and dashboards
- **Students/Researchers**: Learning risk assessment methodologies

---

##  Compliance Frameworks

The tool's methodology aligns with:

- **ISO 27001** (Information Security Management)
- **NIST Cybersecurity Framework** (Identify, Protect, Detect, Respond, Recover)
- **IEC 62443** (Industrial Automation and Control Systems Security)
- **NERC CIP** (Critical Infrastructure Protection for energy sector)
- **NCA ECC** (Saudi National Cybersecurity Authority Essential Controls)

---

##  Future Enhancements

Planned features for future versions:

- [ ] PDF report generation with charts
- [ ] Database backend (PostgreSQL) for asset management
- [ ] REST API for integration with other tools
- [ ] Web-based dashboard
- [ ] Optional anomaly scoring / trend analytics (future)
- [ ] Integration with vulnerability scanners
- [ ] Multi-language support (Arabic, English)
- [ ] Risk trend analysis over time

---

##  Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Abdulkarim Alqahtani**
- 🎓 MSc Computer Science - Queen Mary University of London
- 🛡️ MA National Security - King's College London
- 💼 Oil Plant Operations - Saudi Aramco Total (SATORP)
- 🔗 LinkedIn: [linkedin.com/in/abdulkarim-saad-7a8b05214](https://www.linkedin.com/in/abdulkarim-saad-7a8b05214/)
- 📧 Email: a.qh20@outlook.com

---

## 🙏 Acknowledgments

- Inspired by real-world risk assessment needs in critical infrastructure
- Built on industry best practices from ISO 27001, NIST, and IEC 62443
- Thanks to the cybersecurity community for open-source tools and frameworks

---

## 📊 Project Status

**Current Version**: 1.0.0  
**Status**: Active Development  
**Last Updated**: February 2026

---

<div align="center">

### 🔒 *"Building secure systems through risk-informed design"*

**Star this repository if you find it useful!** ⭐

</div>
