import subprocess
import os

# Define the list of input files assuming filenames are concrete_01.in, concrete_02.in...etc
input_folder = os.path.dirname(os.path.abspath(__file__))
input_folder = input_folder  + "\gpr_in_files"

input_files = [f'{input_folder}\gprMax_in_file_{i}.in' for i in range(20,35) ]

# Define the output directory
output_dir = 'output_Ascans'

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
print(output_dir)
# Loop through each input file and run gprMax
for input_file in input_files:
    print(input_file)
    # Define the output file name
    output_file = os.path.join(output_dir, input_file.replace('.in', '.out'))

    # Run gprMax for the current input file
    command = f'python -m gprMax {input_file}' #, '-o', output_file]
    subprocess.run(command)

    print(f'Generated A-scan for {input_file} as {output_file}')
