# tests/test_main.py

import pytest
import os
from unittest import mock
from argparse import Namespace
from filesize_cli.main import main


# Fixture for creating a temporary file
@pytest.fixture
def temp_file(tmp_path):
	file = tmp_path / "testfile.txt"
	file.write_text("This is a test file.")
	return str(file)


# Test displaying file size in megabytes (default)
def test_file_size_in_mb_pretty(monkeypatch, capsys, temp_file):
	# Mock ArgumentParser.parse_args to return predefined arguments
	monkeypatch.setattr('filesize_cli.main.ArgumentParser.parse_args', lambda self: Namespace(
		file=temp_file,
		unit='mb',
		rate=1000,
		pretty=True
	))

	main()

	captured = capsys.readouterr()
	# Calculate expected size in MB
	actual_size_bytes = os.path.getsize(temp_file)
	expected_size_mb = actual_size_bytes / (1000 ** 2)
	expected_output = f"{expected_size_mb:.2f} MB"

	assert captured.out.strip() == expected_output


# Test handling non-existent file
def test_non_existent_file(monkeypatch, caplog):
	# Mock ArgumentParser.parse_args to return predefined arguments with a non-existent file
	monkeypatch.setattr('filesize_cli.main.ArgumentParser.parse_args', lambda self: Namespace(
		file='nonexistentfile.txt',
		unit='mb',
		rate=1000,
		pretty=True
	))

	with pytest.raises(SystemExit) as exc_info:
		main()

	assert exc_info.value.code == 1  # Ensure the script exited with status code 1

	# Check that the error message was logged
	assert 'File "nonexistentfile.txt" could not be found.' in caplog.text


# Test displaying file size in kilobytes without pretty print
def test_file_size_in_kb(monkeypatch, capsys, temp_file):
	# Mock ArgumentParser.parse_args to return predefined arguments
	monkeypatch.setattr('filesize_cli.main.ArgumentParser.parse_args', lambda self: Namespace(
		file=temp_file,
		unit='kb',
		rate=1000,
		pretty=False
	))

	main()

	captured = capsys.readouterr()
	# Calculate expected size in KB
	actual_size_bytes = os.path.getsize(temp_file)
	expected_size_kb = actual_size_bytes / 1000
	expected_output = f"{expected_size_kb:.2f}"

	assert captured.out.strip() == expected_output


# Test using a custom conversion rate
def test_custom_conversion_rate(monkeypatch, capsys, temp_file):
	# Mock ArgumentParser.parse_args to return predefined arguments
	monkeypatch.setattr('filesize_cli.main.ArgumentParser.parse_args', lambda self: Namespace(
		file=temp_file,
		unit='mb',
		rate=1024,
		pretty=True
	))

	main()

	captured = capsys.readouterr()
	# Calculate expected size in MB with custom rate
	actual_size_bytes = os.path.getsize(temp_file)
	expected_size_mb = actual_size_bytes / (1024 ** 2)
	expected_output = f"{expected_size_mb:.2f} MB"

	assert captured.out.strip() == expected_output


# Integration test using a real example file
@pytest.mark.integration
def test_integration_real_file(capsys):
	example_file = os.path.join('examples', 'image.jpg')  # Ensure this file exists
	if not os.path.isfile(example_file):
		pytest.skip(f"Example file {example_file} does not exist.")

	# Mock ArgumentParser.parse_args to return predefined arguments
	with mock.patch('filesize_cli.main.ArgumentParser.parse_args', return_value=Namespace(
		file=example_file,
		unit='mb',
		rate=1000,
		pretty=True
	)):
		main()

	captured = capsys.readouterr()
	# Calculate expected size in MB
	actual_size_bytes = os.path.getsize(example_file)
	expected_size_mb = actual_size_bytes / (1000 ** 2)
	expected_output = f"{expected_size_mb:.2f} MB"

	assert captured.out.strip() == expected_output
