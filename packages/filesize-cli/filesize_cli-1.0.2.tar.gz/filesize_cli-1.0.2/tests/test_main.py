# Import pytest for testing
import pytest

# Import os for file handling
import os

# Import mock for mocking functions and objects during tests
from unittest import mock

# Import Namespace to simulate command-line arguments
from argparse import Namespace

# Import the main function from the 'filesize_cli' module to test it
from filesize_cli.main import main


# Fixture to create a temporary file for testing purposes
@pytest.fixture
def temp_file(tmp_path):
	"""
	Fixture to create a temporary file for testing.

	Args:
		tmp_path (Path): Temporary directory path provided by pytest.

	Returns:
		str: Path to the temporary file.
	"""
	# Create a file path in the temporary directory
	file = tmp_path / "testfile.txt"
	# Write text to the file for testing
	file.write_text("This is a test file.")
	# Return the file path as a string
	return str(file)


# Test to display file size in megabytes with pretty print enabled
def test_file_size_in_mb_pretty(monkeypatch, capsys, temp_file):
	"""
	Test case for displaying file size in megabytes with pretty print enabled.

	Args:
		monkeypatch (MonkeyPatch): Pytest fixture for monkeypatching.
		capsys (CaptureFixture): Pytest fixture to capture stdout and stderr.
		temp_file (str): Path to the temporary file.
	"""
	# Mock ArgumentParser.parse_args to simulate input arguments
	monkeypatch.setattr('filesize_cli.main.ArgumentParser.parse_args', lambda self: Namespace(
		file=temp_file,
		unit='mb',
		rate=1000,
		pretty=True
	))

	# Run the main function with the mocked arguments
	main()

	# Capture stdout and stderr outputs
	captured = capsys.readouterr()
	# Get the actual file size in bytes
	actual_size_bytes = os.path.getsize(temp_file)
	# Calculate expected file size in MB using conversion rate 1000
	expected_size_mb = actual_size_bytes / (1000 ** 2)
	# Format the expected output with two decimal places and unit label
	expected_output = f"{expected_size_mb:.2f} MB"

	# Assert the printed output matches the expected output
	assert captured.out.strip() == expected_output


# Test to handle a non-existent file
def test_non_existent_file(monkeypatch, caplog):
	"""
	Test case for handling a non-existent file.

	Args:
		monkeypatch (MonkeyPatch): Pytest fixture for monkeypatching.
		caplog (LogCaptureFixture): Pytest fixture to capture log messages.
	"""
	# Mock ArgumentParser.parse_args to use arguments with a non-existent file
	monkeypatch.setattr('filesize_cli.main.ArgumentParser.parse_args', lambda self: Namespace(
		file='nonexistentfile.txt',
		unit='mb',
		rate=1000,
		pretty=True
	))

	# Run main in a way that it raises SystemExit on failure
	with pytest.raises(SystemExit) as exc_info:
		main()

	# Check that the program exited with status code 1
	assert exc_info.value.code == 1

	# Verify that the appropriate error message was logged
	assert 'File "nonexistentfile.txt" could not be found.' in caplog.text


# Test to display file size in kilobytes without pretty print
def test_file_size_in_kb(monkeypatch, capsys, temp_file):
	"""
	Test case for displaying file size in kilobytes without pretty print.

	Args:
		monkeypatch (MonkeyPatch): Pytest fixture for monkeypatching.
		capsys (CaptureFixture): Pytest fixture to capture stdout and stderr.
		temp_file (str): Path to the temporary file.
	"""
	# Mock ArgumentParser.parse_args to simulate input arguments
	monkeypatch.setattr('filesize_cli.main.ArgumentParser.parse_args', lambda self: Namespace(
		file=temp_file,
		unit='kb',
		rate=1000,
		pretty=False
	))

	# Run the main function with the mocked arguments
	main()

	# Capture the output printed to stdout
	captured = capsys.readouterr()
	# Calculate the expected file size in kilobytes
	actual_size_bytes = os.path.getsize(temp_file)
	expected_size_kb = actual_size_bytes / 1000
	# Format the expected output with two decimal places
	expected_output = f"{expected_size_kb:.2f}"

	# Assert the printed output matches the expected output
	assert captured.out.strip() == expected_output


# Test case to check file size calculation using a custom conversion rate
def test_custom_conversion_rate(monkeypatch, capsys, temp_file):
	"""
	Test case for using a custom conversion rate.

	Args:
		monkeypatch (MonkeyPatch): Pytest fixture for monkeypatching.
		capsys (CaptureFixture): Pytest fixture to capture stdout and stderr.
		temp_file (str): Path to the temporary file.
	"""
	# Mock ArgumentParser.parse_args to simulate input arguments
	monkeypatch.setattr('filesize_cli.main.ArgumentParser.parse_args', lambda self: Namespace(
		file=temp_file,
		unit='mb',
		rate=1024,
		pretty=True
	))

	# Run the main function with the mocked arguments
	main()

	# Capture the output printed to stdout
	captured = capsys.readouterr()
	# Calculate expected file size in MB using the custom rate of 1024
	actual_size_bytes = os.path.getsize(temp_file)
	expected_size_mb = actual_size_bytes / (1024 ** 2)
	# Format the expected output with two decimal places and unit label
	expected_output = f"{expected_size_mb:.2f} MB"

	# Assert the printed output matches the expected output
	assert captured.out.strip() == expected_output


# Integration test with an actual example file
@pytest.mark.integration
def test_integration_real_file(capsys):
	"""
	Integration test using a real example file.

	Args:
		capsys (CaptureFixture): Pytest fixture to capture stdout and stderr.
	"""
	# Define the path to a real example file
	example_file = os.path.join('examples', 'image.jpg')  # Ensure this file exists

	# Skip test if the file does not exist
	if not os.path.isfile(example_file):
		pytest.skip(f"Example file {example_file} does not exist.")

	# Mock ArgumentParser.parse_args to simulate input arguments
	with mock.patch('filesize_cli.main.ArgumentParser.parse_args', return_value=Namespace(
		file=example_file,
		unit='mb',
		rate=1000,
		pretty=True
	)):
		main()

	# Capture the output printed to stdout
	captured = capsys.readouterr()
	# Calculate expected file size in MB with the standard rate of 1000
	actual_size_bytes = os.path.getsize(example_file)
	expected_size_mb = actual_size_bytes / (1000 ** 2)
	# Format the expected output with two decimal places and unit label
	expected_output = f"{expected_size_mb:.2f} MB"

	# Assert the printed output matches the expected output
	assert captured.out.strip() == expected_output
