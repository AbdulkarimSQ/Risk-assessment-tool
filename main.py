#!/usr/bin/env python3
"""
Risk Assessment Tool - Main Application
========================================
Cybersecurity risk assessment framework for critical infrastructure.

Author: Abdulkarim Alqahtani
Purpose: Automated risk evaluation for IT/OT assets in Oil & Gas environments
"""

import json
import sys
from pathlib import Path
from colorama import Fore, Style

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.asset import Asset
from src.risk_calculator import RiskCalculator
from src.report_generator import ReportGenerator


def load_sample_assets(filename: str = 'data/sample_assets.json'):
    """
    Load sample assets from JSON file.

    Args:
        filename: Path to JSON file containing asset data

    Returns:
        List of Asset objects
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assets = [Asset.from_dict(asset_data) for asset_data in data]
        print(f"{Fore.GREEN}✓ Loaded {len(assets)} assets from {filename}")
        return assets

    except FileNotFoundError:
        print(f"{Fore.RED}✗ Error: File '{filename}' not found")
        return []
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}✗ Error: Invalid JSON in '{filename}': {e}")
        return []
    except Exception as e:
        print(f"{Fore.RED}✗ Error loading assets: {e}")
        return []


def main():
    """Main application entry point"""

    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
    print(f"{'CYBERSECURITY RISK ASSESSMENT TOOL'.center(80)}")
    print(f"{'Critical Infrastructure Security Framework'.center(80)}")
    print(f"{'=' * 80}\n")

    # Load sample assets
    assets = load_sample_assets()

    if not assets:
        print(f"{Fore.RED}No assets loaded. Exiting.")
        return

    # Initialize risk calculator
    calculator = RiskCalculator()
    print(f"{Fore.GREEN}✓ Risk calculator initialized")

    # Perform risk assessments
    print(f"{Fore.CYAN}\nPerforming risk assessments...")
    assessments = calculator.assess_multiple_assets(assets)
    print(f"{Fore.GREEN}✓ Assessed {len(assessments)} assets")

    # Calculate summary statistics
    statistics = calculator.get_summary_statistics(assessments)
    print(f"{Fore.GREEN}✓ Summary statistics calculated")

    # Generate reports
    reporter = ReportGenerator()

    # Display summary report
    reporter.print_summary_report(assessments, statistics)

    # Interactive menu
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Report Options:")
        print(f"{Fore.WHITE}1. View detailed report (all assets)")
        print(f"{Fore.WHITE}2. View individual asset assessment")
        print(f"{Fore.WHITE}3. View risk matrix")
        print(f"{Fore.WHITE}4. Export to JSON")
        print(f"{Fore.WHITE}5. Export to CSV")
        print(f"{Fore.WHITE}6. Exit")

        choice = input(f"\n{Fore.YELLOW}Select option (1-6): {Fore.WHITE}").strip()

        if choice == '1':
            # Detailed report
            reporter.print_detailed_report(assessments, statistics)

        elif choice == '2':
            # Individual asset
            print(f"\n{Fore.CYAN}Available Assets:")
            for idx, assessment in enumerate(assessments, 1):
                severity_color = reporter._get_severity_color(assessment['severity'])
                print(f"{idx}. {assessment['asset_name']} - "
                      f"{severity_color}{assessment['severity']} "
                      f"{Fore.WHITE}(Risk: {assessment['residual_risk']:.2f})")

            try:
                asset_num = int(input(f"\n{Fore.YELLOW}Select asset number: {Fore.WHITE}").strip())
                if 1 <= asset_num <= len(assessments):
                    reporter.print_asset_assessment(assessments[asset_num - 1])
                else:
                    print(f"{Fore.RED}Invalid asset number")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number")

        elif choice == '3':
            # Risk matrix
            reporter.generate_risk_matrix_text(assessments)

        elif choice == '4':
            # Export JSON
            filename = input(f"{Fore.YELLOW}Enter filename (default: risk_assessment.json): {Fore.WHITE}").strip()
            if not filename:
                filename = 'risk_assessment.json'
            if not filename.endswith('.json'):
                filename += '.json'
            reporter.export_to_json(assessments, statistics, filename)

        elif choice == '5':
            # Export CSV
            filename = input(f"{Fore.YELLOW}Enter filename (default: risk_assessment.csv): {Fore.WHITE}").strip()
            if not filename:
                filename = 'risk_assessment.csv'
            if not filename.endswith('.csv'):
                filename += '.csv'
            reporter.export_to_csv(assessments, filename)

        elif choice == '6':
            # Exit
            print(f"\n{Fore.CYAN}Thank you for using the Risk Assessment Tool!")
            print(f"{Fore.GREEN}Stay secure! 🔒\n")
            break

        else:
            print(f"{Fore.RED}Invalid option. Please select 1-6.")


def demo_single_asset():
    """
    Demonstration of assessing a single asset.
    Useful for testing and understanding the tool.
    """
    # Create a sample asset programmatically
    test_asset = Asset(
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

    # Assess the asset
    calculator = RiskCalculator()
    assessment = calculator.assess_asset(test_asset)

    # Generate report
    reporter = ReportGenerator()
    reporter.print_header("SINGLE ASSET ASSESSMENT DEMO")
    reporter.print_asset_assessment(assessment)


if __name__ == "__main__":
    try:
        main()
        # Uncomment below to run single asset demo instead:
        # demo_single_asset()

    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠ Assessment interrupted by user")
        print(f"{Fore.WHITE}Exiting safely...\n")
        sys.exit(0)

    except Exception as e:
        print(f"\n{Fore.RED}✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)