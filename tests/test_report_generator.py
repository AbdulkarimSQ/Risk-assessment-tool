"""
Tests for Report Generator
==========================
Unit tests for report generation functionality.
"""

import pytest
import json
import csv
import os
from pathlib import Path
from colorama import Fore
from src.report_generator import ReportGenerator


class TestReportGeneratorInit:
    """Tests for ReportGenerator initialization."""

    def test_init_creates_report_date(self, report_generator):
        """Test that initialization sets report date."""
        assert hasattr(report_generator, 'report_date')
        assert report_generator.report_date is not None

    def test_report_date_format(self, report_generator):
        """Test report date format."""
        # Expected format: YYYY-MM-DD HH:MM:SS
        parts = report_generator.report_date.split(' ')
        assert len(parts) == 2
        assert len(parts[0].split('-')) == 3  # Date
        assert len(parts[1].split(':')) == 3  # Time


class TestSeverityColor:
    """Tests for severity color mapping."""

    def test_critical_color(self, report_generator):
        """Test CRITICAL severity color."""
        color = report_generator._get_severity_color('CRITICAL')
        assert color == Fore.RED

    def test_high_color(self, report_generator):
        """Test HIGH severity color."""
        color = report_generator._get_severity_color('HIGH')
        assert color == Fore.YELLOW

    def test_medium_color(self, report_generator):
        """Test MEDIUM severity color."""
        color = report_generator._get_severity_color('MEDIUM')
        assert color == Fore.CYAN

    def test_low_color(self, report_generator):
        """Test LOW severity color."""
        color = report_generator._get_severity_color('LOW')
        assert color == Fore.GREEN

    def test_unknown_severity_color(self, report_generator):
        """Test unknown severity defaults to white."""
        color = report_generator._get_severity_color('UNKNOWN')
        assert color == Fore.WHITE


class TestJSONExport:
    """Tests for JSON export functionality."""

    def test_export_to_json_creates_file(self, report_generator, multiple_assessments, sample_statistics, tmp_path):
        """Test that export_to_json creates a file."""
        filename = str(tmp_path / "test_report.json")
        report_generator.export_to_json(multiple_assessments, sample_statistics, filename)

        assert os.path.exists(filename)

    def test_export_to_json_valid_json(self, report_generator, multiple_assessments, sample_statistics, tmp_path):
        """Test that exported file contains valid JSON."""
        filename = str(tmp_path / "test_report.json")
        report_generator.export_to_json(multiple_assessments, sample_statistics, filename)

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert isinstance(data, dict)

    def test_export_to_json_structure(self, report_generator, multiple_assessments, sample_statistics, tmp_path):
        """Test JSON export contains required fields."""
        filename = str(tmp_path / "test_report.json")
        report_generator.export_to_json(multiple_assessments, sample_statistics, filename)

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert 'report_date' in data
        assert 'summary_statistics' in data
        assert 'asset_assessments' in data

    def test_export_to_json_assessments_count(self, report_generator, multiple_assessments, sample_statistics, tmp_path):
        """Test that all assessments are exported."""
        filename = str(tmp_path / "test_report.json")
        report_generator.export_to_json(multiple_assessments, sample_statistics, filename)

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data['asset_assessments']) == len(multiple_assessments)

    def test_export_to_json_statistics(self, report_generator, multiple_assessments, sample_statistics, tmp_path):
        """Test that statistics are exported correctly."""
        filename = str(tmp_path / "test_report.json")
        report_generator.export_to_json(multiple_assessments, sample_statistics, filename)

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data['summary_statistics']['total_assets'] == sample_statistics['total_assets']


class TestCSVExport:
    """Tests for CSV export functionality."""

    def test_export_to_csv_creates_file(self, report_generator, multiple_assessments, tmp_path):
        """Test that export_to_csv creates a file."""
        filename = str(tmp_path / "test_report.csv")
        report_generator.export_to_csv(multiple_assessments, filename)

        assert os.path.exists(filename)

    def test_export_to_csv_has_header(self, report_generator, multiple_assessments, tmp_path):
        """Test that CSV file has header row."""
        filename = str(tmp_path / "test_report.csv")
        report_generator.export_to_csv(multiple_assessments, filename)

        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)

        expected_headers = [
            'Asset ID', 'Asset Name', 'Type', 'Criticality',
            'Inherent Risk', 'Residual Risk', 'Risk Reduction %',
            'Severity', 'Recommended Action',
            'Threats', 'Vulnerabilities', 'Controls', 'Control Effectiveness'
        ]

        assert header == expected_headers

    def test_export_to_csv_row_count(self, report_generator, multiple_assessments, tmp_path):
        """Test that CSV has correct number of rows."""
        filename = str(tmp_path / "test_report.csv")
        report_generator.export_to_csv(multiple_assessments, filename)

        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Header + data rows
        assert len(rows) == len(multiple_assessments) + 1

    def test_export_to_csv_data_integrity(self, report_generator, multiple_assessments, tmp_path):
        """Test that CSV data matches source assessments."""
        filename = str(tmp_path / "test_report.csv")
        report_generator.export_to_csv(multiple_assessments, filename)

        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for i, row in enumerate(rows):
            assert row['Asset ID'] == multiple_assessments[i]['asset_id']
            assert row['Asset Name'] == multiple_assessments[i]['asset_name']
            assert row['Severity'] == multiple_assessments[i]['severity']

    def test_export_to_csv_empty_list(self, report_generator, tmp_path, capsys):
        """Test exporting empty assessment list."""
        filename = str(tmp_path / "empty_report.csv")
        report_generator.export_to_csv([], filename)

        # Should print warning
        captured = capsys.readouterr()
        assert "No assessments to export" in captured.out

    def test_export_to_csv_numeric_values(self, report_generator, multiple_assessments, tmp_path):
        """Test that numeric values are exported correctly."""
        filename = str(tmp_path / "test_report.csv")
        report_generator.export_to_csv(multiple_assessments, filename)

        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for i, row in enumerate(rows):
            # Should be able to convert to float
            assert float(row['Inherent Risk']) == multiple_assessments[i]['inherent_risk']
            assert float(row['Residual Risk']) == multiple_assessments[i]['residual_risk']


class TestPrintFunctions:
    """Tests for print/display functions."""

    def test_print_header(self, report_generator, capsys):
        """Test print_header output."""
        report_generator.print_header("TEST HEADER")
        captured = capsys.readouterr()

        assert "TEST HEADER" in captured.out
        assert "=" in captured.out  # Separator lines
        assert "Generated:" in captured.out

    def test_print_asset_assessment(self, report_generator, sample_assessment, capsys):
        """Test print_asset_assessment output."""
        report_generator.print_asset_assessment(sample_assessment)
        captured = capsys.readouterr()

        assert sample_assessment['asset_name'] in captured.out
        assert sample_assessment['asset_id'] in captured.out
        assert "Inherent Risk:" in captured.out
        assert "Residual Risk:" in captured.out
        assert "Recommended Action:" in captured.out

    def test_print_summary_report(self, report_generator, multiple_assessments, sample_statistics, capsys):
        """Test print_summary_report output."""
        report_generator.print_summary_report(multiple_assessments, sample_statistics)
        captured = capsys.readouterr()

        assert "RISK ASSESSMENT SUMMARY REPORT" in captured.out
        assert "Total Assets Assessed:" in captured.out
        assert "Risk Distribution:" in captured.out
        assert "CRITICAL:" in captured.out
        assert "HIGH:" in captured.out
        assert "MEDIUM:" in captured.out
        assert "LOW:" in captured.out
        assert "Highest Risk Asset:" in captured.out
        assert "Top 5 Highest Risk Assets:" in captured.out

    def test_print_detailed_report(self, report_generator, multiple_assessments, sample_statistics, capsys):
        """Test print_detailed_report output."""
        report_generator.print_detailed_report(multiple_assessments, sample_statistics)
        captured = capsys.readouterr()

        # Should include summary
        assert "RISK ASSESSMENT SUMMARY REPORT" in captured.out
        # Should include detailed assessments
        assert "DETAILED ASSET ASSESSMENTS" in captured.out

    def test_generate_risk_matrix_text(self, report_generator, multiple_assessments, capsys):
        """Test generate_risk_matrix_text output."""
        report_generator.generate_risk_matrix_text(multiple_assessments)
        captured = capsys.readouterr()

        assert "Risk Matrix Distribution:" in captured.out
        assert "CRITICAL" in captured.out
        assert "HIGH" in captured.out
        assert "MEDIUM" in captured.out
        assert "LOW" in captured.out


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_export_with_special_characters(self, report_generator, risk_calculator, tmp_path):
        """Test export with special characters in asset names."""
        from src.asset import Asset

        asset = Asset(
            asset_id="SPEC-001",
            name="Test Asset with 'quotes' and \"double quotes\"",
            asset_type="Server",
            criticality="Medium",
            location="Location with, comma",
            owner="Owner & Team",
            vulnerabilities=["Medium - Test"],
            threats=["Cyber Attack"],
            existing_controls=["Firewall"],
            control_effectiveness="Adequate"
        )

        assessment = risk_calculator.assess_asset(asset)
        assessments = [assessment]
        stats = risk_calculator.get_summary_statistics(assessments)

        # Test JSON export
        json_file = str(tmp_path / "special_chars.json")
        report_generator.export_to_json(assessments, stats, json_file)

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data['asset_assessments'][0]['asset_name'] == asset.name

        # Test CSV export
        csv_file = str(tmp_path / "special_chars.csv")
        report_generator.export_to_csv(assessments, csv_file)

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            row = next(reader)
        assert row['Asset Name'] == asset.name

    def test_export_with_unicode(self, report_generator, risk_calculator, tmp_path):
        """Test export with unicode characters."""
        from src.asset import Asset

        asset = Asset(
            asset_id="UNI-001",
            name="خادم اختبار",  # Arabic text
            asset_type="Server",
            criticality="High",
            location="مركز البيانات",
            owner="فريق تقنية المعلومات",
            vulnerabilities=["High - ثغرة أمنية"],
            threats=["Cyber Attack"],
            existing_controls=["جدار حماية"],
            control_effectiveness="Adequate"
        )

        assessment = risk_calculator.assess_asset(asset)
        assessments = [assessment]
        stats = risk_calculator.get_summary_statistics(assessments)

        # Test JSON export
        json_file = str(tmp_path / "unicode.json")
        report_generator.export_to_json(assessments, stats, json_file)

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data['asset_assessments'][0]['asset_name'] == asset.name

    def test_single_assessment_statistics(self, report_generator, sample_assessment, risk_calculator, tmp_path):
        """Test with single assessment."""
        assessments = [sample_assessment]
        stats = risk_calculator.get_summary_statistics(assessments)

        json_file = str(tmp_path / "single.json")
        report_generator.export_to_json(assessments, stats, json_file)

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data['summary_statistics']['total_assets'] == 1
