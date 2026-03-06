# Risk Assessment Methodology

## Overview

This document describes the risk assessment methodology implemented in the Cybersecurity Risk Assessment Tool. The methodology is designed for critical infrastructure environments, particularly Oil & Gas and Industrial Control Systems (ICS/OT).

## Risk Assessment Framework

### Standards Alignment

This methodology aligns with industry-recognized frameworks:

| Framework | Application |
|-----------|-------------|
| **ISO 27001** | Information Security Management System |
| **NIST CSF** | Cybersecurity Framework (Identify, Protect, Detect, Respond, Recover) |
| **IEC 62443** | Industrial Automation and Control Systems Security |
| **NERC CIP** | Critical Infrastructure Protection (Energy Sector) |
| **NCA ECC** | Saudi National Cybersecurity Authority Essential Controls |

---

## Risk Calculation Process

### Step 1: Threat Assessment

Threats are evaluated based on a predefined taxonomy with associated likelihood scores (1-10):

| Threat Category | Base Score | Description |
|-----------------|------------|-------------|
| Ransomware | 9 | Encryption-based extortion attacks |
| Data Breach | 9 | Unauthorized data exfiltration |
| Cyber Attack | 8 | General targeted cyber attacks |
| Insider Threat | 7 | Malicious or negligent insiders |
| Supply Chain | 7 | Third-party compromise |
| Malware | 7 | Malicious software infections |
| DDoS | 6 | Distributed denial of service |
| Phishing | 6 | Social engineering attacks |
| Physical Breach | 6 | Physical security compromise |
| System Failure | 5 | Technical failures and outages |

**Calculation**: Average of all applicable threat scores

```
Threat Score = Σ(Applicable Threat Scores) / Number of Threats
```

### Step 2: Vulnerability Evaluation

Vulnerabilities are assessed based on severity levels:

| Severity | Score | Examples |
|----------|-------|----------|
| **Critical** | 10 | Unpatched systems, RCE vulnerabilities, no authentication |
| **High** | 8 | Weak authentication, outdated firmware, SQL injection |
| **Medium** | 5 | Missing segmentation, outdated encryption, weak passwords |
| **Low** | 3 | Minor misconfigurations, informational findings |
| **None** | 1 | No identified vulnerabilities |

**Calculation**: Maximum (worst-case) vulnerability score

```
Vulnerability Score = MAX(All Vulnerability Severities)
```

> **Rationale**: Using the maximum score ensures that critical vulnerabilities are not diluted by lower-severity findings.

### Step 3: Asset Criticality Weighting

Asset criticality reflects business and operational importance:

| Criticality Level | Weight | Examples |
|-------------------|--------|----------|
| **Mission Critical** | 10 | SCADA systems, HMI, core network infrastructure |
| **High** | 8 | Production databases, backup systems, VPN gateways |
| **Medium** | 5 | Office workstations, development servers |
| **Low** | 3 | Test environments, non-production systems |

### Step 4: Control Effectiveness Assessment

Security controls are evaluated for their effectiveness in reducing risk:

| Effectiveness | Multiplier | Risk Reduction | Description |
|---------------|------------|----------------|-------------|
| **Strong** | 0.3 | 70% | Comprehensive, well-maintained controls |
| **Adequate** | 0.5 | 50% | Reasonable controls with some gaps |
| **Weak** | 0.7 | 30% | Minimal or poorly implemented controls |
| **None** | 1.0 | 0% | No controls in place |

---

## Risk Scoring Formulas

### Inherent Risk (Before Controls)

Inherent risk represents the risk level without considering security controls:

```
Base Risk = (Threat Score + Vulnerability Score) / 2
Inherent Risk = (Base Risk × Criticality Weight) / 10
```

The result is normalized to a 1-10 scale.

### Residual Risk (After Controls)

Residual risk represents the remaining risk after applying security controls:

```
Residual Risk = Inherent Risk × Control Effectiveness Multiplier
```

The result is clamped to a minimum of 1.0 and maximum of 10.0.

### Risk Reduction

```
Risk Reduction = Inherent Risk - Residual Risk
Reduction Percentage = (Risk Reduction / Inherent Risk) × 100
```

---

## Risk Severity Classification

Risk scores are classified into severity levels with associated actions:

| Severity | Score Range | Color | Recommended Action |
|----------|-------------|-------|-------------------|
| **CRITICAL** | 9.0 - 10.0 | 🔴 Red | Immediate action required |
| **HIGH** | 7.0 - 8.9 | 🟠 Orange | Escalate and plan mitigation |
| **MEDIUM** | 4.0 - 6.9 | 🟡 Yellow | Review and schedule remediation |
| **LOW** | 1.0 - 3.9 | 🟢 Green | Monitor and maintain controls |

---

## Example Calculation

### Asset: Primary SCADA System

**Input Parameters:**
- Threats: Cyber Attack (8), Ransomware (9), Insider Threat (7)
- Vulnerabilities: Critical (10), High (8), Medium (5)
- Criticality: Mission Critical (10)
- Control Effectiveness: Adequate (0.5)

**Calculations:**

1. **Threat Score**: (8 + 9 + 7) / 3 = **8.0**

2. **Vulnerability Score**: MAX(10, 8, 5) = **10**

3. **Base Risk**: (8.0 + 10) / 2 = **9.0**

4. **Inherent Risk**: (9.0 × 10) / 10 = **9.0**

5. **Residual Risk**: 9.0 × 0.5 = **4.5**

6. **Risk Reduction**: 9.0 - 4.5 = **4.5 (50%)**

7. **Severity**: 4.5 → **MEDIUM**

8. **Recommended Action**: **Review and Plan**

---

## Risk Matrix Visualization

```
                    IMPACT
           Low    Medium    High    Critical
         ┌────────┬────────┬────────┬────────┐
Almost   │ MEDIUM │  HIGH  │CRITICAL│CRITICAL│
Certain  │  4-6   │  7-8   │  9-10  │  9-10  │
         ├────────┼────────┼────────┼────────┤
L  Likely│  LOW   │ MEDIUM │  HIGH  │CRITICAL│
I        │  2-3   │  4-6   │  7-8   │  9-10  │
K        ├────────┼────────┼────────┼────────┤
E Possible│  LOW  │ MEDIUM │ MEDIUM │  HIGH  │
L        │  1-2   │  4-5   │  5-6   │  7-8   │
I        ├────────┼────────┼────────┼────────┤
H Unlikely│  LOW  │  LOW   │ MEDIUM │ MEDIUM │
O        │  1-2   │  2-3   │  4-5   │  5-6   │
O        ├────────┼────────┼────────┼────────┤
D  Rare  │  LOW   │  LOW   │  LOW   │ MEDIUM │
         │  1-2   │  1-2   │  2-3   │  4-5   │
         └────────┴────────┴────────┴────────┘
```

---

## Limitations and Considerations

### Methodology Limitations

1. **Qualitative Inputs**: Threat and vulnerability scores are based on predefined values that may not reflect organization-specific context.

2. **Point-in-Time Assessment**: Risk scores represent a snapshot and should be reassessed periodically.

3. **Control Effectiveness**: Subjective assessment of control effectiveness may vary between assessors.

### Recommendations

1. **Regular Reviews**: Conduct risk assessments quarterly or after significant changes.

2. **Calibration**: Adjust scoring parameters based on organizational risk appetite.

3. **Validation**: Compare results with external assessments and penetration tests.

4. **Documentation**: Maintain audit trails for compliance and tracking.

---

## References

1. ISO/IEC 27001:2022 - Information Security Management Systems
2. NIST Cybersecurity Framework v2.0
3. IEC 62443 - Industrial Communication Networks
4. NIST SP 800-30 - Guide for Conducting Risk Assessments
5. FAIR (Factor Analysis of Information Risk)

---

## Document Information

| Property | Value |
|----------|-------|
| Version | 1.0 |
| Last Updated | February 2025 |
| Author | Abdulkarim Alqahtani |
| Review Cycle | Annual |
