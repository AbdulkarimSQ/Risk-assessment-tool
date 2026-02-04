"""
Report Generator
================
Generate formatted reports for risk assessment results.
Supports console output, CSV export, and summary dashboards.
"""

from typing import List, Dict
from datetime import datetime
from colorama import Fore, Style, init
import json

# Initialize colorama for colored terminal output
init(autoreset=True)


class ReportGenerator:
    """
    Generate and format risk assessment reports.
    """

    def __init__(self):
        self.report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _get_severity_color(self, severity: str) -> str:
        """Get appropriate color for severity level"""
        colors = {
            'CRITICAL': Fore.RED,
            'HIGH': Fore.YELLOW,
            'MEDIUM': Fore.CYAN,
            'LOW': Fore.GREEN
        }
        return colors.get(severity, Fore.WHITE)

    def print_header(self, title: str):
        """Print formatted report header"""
        print("\n" + "=" * 80)
        print(f"{Fore.CYAN}{Style.BRIGHT}{title.center(80)}")
        print("=" * 80)
        print(f"Generated: {self.report_date}")
        print("=" * 80 + "\n")

    def print_asset_assessment(self, assessment: Dict):
        """
        Print detailed assessment for a single asset.

        Args:
            assessment: Assessment result dictionary
        """
        severity = assessment['severity']
        color = self._get_severity_color(severity)

        print(f"\n{Fore.WHITE}{Style.BRIGHT}Asset: {assessment['asset_name']} ({assessment['asset_id']})")
        print(f"{Fore.WHITE}Type: {assessment['asset_type']} | Criticality: {assessment['criticality']}")
        print("-" * 80)

        print(f"\n{Fore.WHITE}Risk Assessment:")
        print(f"  Inherent Risk:  {Fore.YELLOW}{assessment['inherent_risk']:.2f}/10")
        print(f"  Residual Risk:  {color}{assessment['residual_risk']:.2f}/10 ({severity})")
        print(
            f"  Risk Reduction: {Fore.GREEN}{assessment['risk_reduction']:.2f} ({assessment['reduction_percentage']:.1f}%)")

        print(f"\n{Fore.WHITE}Security Posture:")
        print(f"  Threats:         {assessment['threat_count']}")
        print(f"  Vulnerabilities: {assessment['vulnerability_count']}")
        print(f"  Controls:        {assessment['control_count']} ({assessment['control_effectiveness']})")

        print(f"\n{color}{Style.BRIGHT}Recommended Action: {assessment['recommended_action']}")
        print("-" * 80)

    def print_summary_report(self, assessments: List[Dict], statistics: Dict):
        """
        Print executive summary report.

        Args:
            assessments: List of assessment results
            statistics: Summary statistics dictionary
        """
        self.print_header("RISK ASSESSMENT SUMMARY REPORT")

        print(f"{Fore.WHITE}{Style.BRIGHT}Overview:")
        print(f"  Total Assets Assessed: {statistics['total_assets']}")
        print(f"  Average Inherent Risk: {Fore.YELLOW}{statistics['average_inherent_risk']:.2f}/10")
        print(f"  Average Residual Risk: {Fore.CYAN}{statistics['average_residual_risk']:.2f}/10")
        print(f"  Average Risk Reduction: {Fore.GREEN}{statistics['average_risk_reduction']:.1f}%")

        print(f"\n{Fore.WHITE}{Style.BRIGHT}Risk Distribution:")
        dist = statistics['severity_distribution']
        total = statistics['total_assets']

        print(f"  {Fore.RED}CRITICAL: {dist['CRITICAL']} ({dist['CRITICAL'] / total * 100:.1f}%)")
        print(f"  {Fore.YELLOW}HIGH:     {dist['HIGH']} ({dist['HIGH'] / total * 100:.1f}%)")
        print(f"  {Fore.CYAN}MEDIUM:   {dist['MEDIUM']} ({dist['MEDIUM'] / total * 100:.1f}%)")
        print(f"  {Fore.GREEN}LOW:      {dist['LOW']} ({dist['LOW'] / total * 100:.1f}%)")

        print(f"\n{Fore.RED}{Style.BRIGHT}Highest Risk Asset:")
        print(f"  {statistics['highest_risk_asset']}")
        print(f"  Risk Score: {statistics['highest_risk_score']:.2f}/10")

        # Top 5 risks
        print(f"\n{Fore.WHITE}{Style.BRIGHT}Top 5 Highest Risk Assets:")
        print(f"{'Rank':<6} {'Asset Name':<30} {'Risk':<8} {'Severity':<12} {'Action'}")
        print("-" * 80)

        for idx, assessment in enumerate(assessments[:5], 1):
            color = self._get_severity_color(assessment['severity'])
            print(f"{idx:<6} "
                  f"{assessment['asset_name']:<30} "
                  f"{color}{assessment['residual_risk']:<8.2f} "
                  f"{assessment['severity']:<12} "
                  f"{Fore.WHITE}{assessment['recommended_action']}")

        print("\n" + "=" * 80 + "\n")

    def print_detailed_report(self, assessments: List[Dict], statistics: Dict):
        """
        Print complete detailed report with all assessments.

        Args:
            assessments: List of assessment results
            statistics: Summary statistics dictionary
        """
        self.print_summary_report(assessments, statistics)

        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'DETAILED ASSET ASSESSMENTS'.center(80)}")
        print("=" * 80)

        for assessment in assessments:
            self.print_asset_assessment(assessment)

    def export_to_json(self, assessments: List[Dict], statistics: Dict, filename: str):
        """
        Export assessment results to JSON file.

        Args:
            assessments: List of assessment results
            statistics: Summary statistics
            filename: Output filename
        """
        output = {
            'report_date': self.report_date,
            'summary_statistics': statistics,
            'asset_assessments': assessments
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"{Fore.GREEN}✓ Report exported to: {filename}")

    def export_to_csv(self, assessments: List[Dict], filename: str):
        """
        Export assessment results to CSV file.

        Args:
            assessments: List of assessment results
            filename: Output filename
        """
        import csv

        if not assessments:
            print(f"{Fore.YELLOW}⚠ No assessments to export")
            return

        # Define CSV headers
        headers = [
            'Asset ID', 'Asset Name', 'Type', 'Criticality',
            'Inherent Risk', 'Residual Risk', 'Risk Reduction %',
            'Severity', 'Recommended Action',
            'Threats', 'Vulnerabilities', 'Controls', 'Control Effectiveness'
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for a in assessments:
                writer.writerow([
                    a['asset_id'],
                    a['asset_name'],
                    a['asset_type'],
                    a['criticality'],
                    a['inherent_risk'],
                    a['residual_risk'],
                    a['reduction_percentage'],
                    a['severity'],
                    a['recommended_action'],
                    a['threat_count'],
                    a['vulnerability_count'],
                    a['control_count'],
                    a['control_effectiveness']
                ])

        print(f"{Fore.GREEN}✓ Report exported to: {filename}")

    def generate_risk_matrix_text(self, assessments: List[Dict]):
        """
        Generate a text-based risk matrix visualization.

        Args:
            assessments: List of assessment results
        """
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Risk Matrix Distribution:")
        print("=" * 50)

        # Simple matrix representation
        matrix = {
            'CRITICAL': [],
            'HIGH': [],
            'MEDIUM': [],
            'LOW': []
        }

        for a in assessments:
            matrix[a['severity']].append(a['asset_name'][:20])

        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            color = self._get_severity_color(severity)
            count = len(matrix[severity])
            bar = '█' * count
            print(f"{color}{severity:<10} [{count:2}] {bar}")

        print("=" * 50 + "\n")