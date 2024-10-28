# Import the os module to interact with the operating system, e.g., to check if a file exists
import os

# Import the sys module to interact with the Python interpreter, e.g., to exit the program
import sys

# Import the logging module to log error messages if needed
import logging

# Import ArgumentParser from argparse to parse command-line arguments
from argparse import ArgumentParser

# Configure logging to output only ERROR level messages to stderr in a simple format
logging.basicConfig(level=logging.ERROR, format='%(message)s')


# Define the main function to handle command-line arguments and display the file size
def main():
	"""
	Main function to handle command-line arguments and display the size of a file
	in the specified unit.
	"""

	# Initialize the variable 'size' to hold the file size (in bytes initially)
	size: float = 0

	# Create an ArgumentParser object with a description for the program's purpose
	parser = ArgumentParser(
		description='Displays the size of a file in B, KB, MB (default), GB, or TB.'
	)

	# Add an argument for the unit of file size, with 'mb' as the default
	parser.add_argument(
		'-u', '--unit',
		default='mb',
		help='Unit to display the file size in',
		choices=['b', 'kb', 'mb', 'gb', 'tb']
	)

	# Add an argument for the conversion rate, with 1000 as the default
	parser.add_argument(
		'-r',
		'--rate',
		type=int,
		default=1000,
		help='Conversion rate'
	)

	# Add an argument for pretty-printing the output, which includes unit labels if enabled
	parser.add_argument(
		'-p',
		'--pretty',
		action='store_const',
		const=True,
		default=False,
		help='Pretty print the output (includes unit labels)'
	)

	# Add a positional argument for the file path
	parser.add_argument(
		'file',
		help='Path to the file'
	)

	# Parse the command-line arguments into the 'args' object
	args = parser.parse_args()

	# Check if the provided file path exists and is a file
	if not os.path.isfile(args.file):
		# Log an error message if the file is not found
		logging.error(f'File "{args.file}" could not be found.')

		# Exit the program with a non-zero status code to indicate an error
		sys.exit(1)

	# Get the size of the file in bytes using the file path provided
	size_bytes = os.path.getsize(args.file)

	# Convert the file size to the specified unit based on the conversion rate provided
	if args.unit == 'b':
		size = size_bytes
	elif args.unit == 'kb':
		size = size_bytes / args.rate
	elif args.unit == 'mb':
		size = size_bytes / (args.rate ** 2)
	elif args.unit == 'gb':
		size = size_bytes / (args.rate ** 3)
	elif args.unit == 'tb':
		size = size_bytes / (args.rate ** 4)

	# Format the output to 2 decimal places for readability
	output = f'{size:.2f}'

	# Add the unit to the output if pretty printing is enabled
	if args.pretty:
		output = f'{size:.2f} {args.unit.upper()}'

	# Print the final formatted output
	print(output)


# Check if this script is being run as the main program
if __name__ == '__main__':
	# Call the main function to execute the program
	main()
