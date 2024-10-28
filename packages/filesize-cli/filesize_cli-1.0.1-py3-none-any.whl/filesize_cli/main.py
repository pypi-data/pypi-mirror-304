import os
import sys
import logging
from argparse import ArgumentParser

# Configure logging to output ERROR level messages to stderr with a simple format
logging.basicConfig(level=logging.ERROR, format='%(message)s')


def main():
	# Initialize output variables
	output: str = ''

	# Initial filesize, in bytes
	size: float = 0

	# Create an ArgumentParser object to handle command-line arguments
	parser = ArgumentParser(
		description='Displays the size of a file in B, KB, MB (default), GB, or TB.'
	)

	# Add argument for unit of file size
	parser.add_argument(
		'-u', '--unit',
		default='mb',
		help='Unit to display the file size in',
		choices=['b', 'kb', 'mb', 'gb', 'tb']
	)

	# Add argument for conversion rate
	parser.add_argument(
		'-r',
		'--rate',
		type=int,
		default=1000,
		help='Conversion rate'
	)

	# Add argument for pretty print option
	parser.add_argument(
		'-p',
		'--pretty',
		action='store_true',
		default=True,
		help='Pretty print the output (includes unit labels)'
	)

	# Add argument for file path
	parser.add_argument(
		'file',
		help='Path to the file'
	)

	# Parse the command-line arguments
	args = parser.parse_args()

	# Check if the provided file path is valid
	if not os.path.isfile(args.file):
		# Log an error message
		logging.error(f' File "{args.file}" could not be found.')

		# Exit the script with a non-zero status
		sys.exit(1)

	# Get the size of the file in bytes
	size_bytes = os.path.getsize(args.file)

	# Convert the file size to the specified unit using the set conversion rate
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

	# Format output with a maximum of 2 decimal places
	output = f'{size:.2f}'

	# Add unit to the output if pretty print is enabled
	if args.pretty:
		output = f'{size:.2f} {args.unit.upper()}'

	# Print the output
	print(output)


if __name__ == '__main__':
	main()
