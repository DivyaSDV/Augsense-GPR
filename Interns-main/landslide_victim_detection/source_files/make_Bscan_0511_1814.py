# change sample file name in code and actual
# python code to make n A-scan input files

# from 0111_1758.py
# 05/11/2024 6:14pm: 
# changed sample_number to 20 (according to chatgpt, if we want 20 A-scans, sample_number should be 20 
import os.path
import numpy as np

# ensure A-scan format file is in same folder as this file
def create_file(file_path=str, current_dir=str, n=int):
    sample_file = f"{current_dir}/format_Bscan_file_0511_1814.txt" # contains basic details of input file
    
    r1 = 0.03 # change to the values mentioned in the paper
    r2 = 0.05 # change to the values mentioned in the paper
    
    # to use different inhale and exhale radii

    # print("Enter the cylinder radii for when human is breathing")
    # r1_input = float(input("Larger radius in meters (inhaling): "))
    # r2_input = float(input("Smaller radius in meters (exhaling): "))

    # r1 = "{:.3f}".format(r1_input)
    # r2 = "{:.3f}".format(r2_input)

    radius_values = generate_radii(r1, r2)
    m = len(radius_values)
    
    for i in range (1, n+1):
        name = f"{file_path}{str(i)}.in"
        radius = radius_values[i % m]

        with open (name, 'w') as f: # to make individual files
            
            with open (sample_file, 'r') as sample: # to write basic details into file
                details = sample.read()
            
            f.write(details)
            f.write(f"\n#cylinder: 0.250 0.500 0 0.250 0.500 0.002 {radius:.3f} BoneCancellous")
    print(f"{n} A-scans generated successfully in {file_path}\nNow generate .out files using \"source_files/run_in_files.py\"")


def generate_radii (r1, r2):
    freq = 0.25  # Frequency in Hz
    time_period = 1 / freq  # Total time to run the simulation (seconds)
    #sampling_rate = 0.25  # Sampling rate (Hz)
    
    # Calculate the number of samples
    #sample_number = int(time_period * sampling_rate) # number of samples
    sample_number = 20
    t = np.linspace(0, time_period, sample_number) # time array

    radius_values = r1 + (r2 - r1) * 0.5 * (1 + np.sin(2 * np.pi * freq * t))
    return radius_values


if __name__ == "__main__":
    file_name = input("Enter file name (file will be created in current folder as <file_name>50.in): ")
    current_dir = os.getcwd()
    os.system("mkdir {file}_folder".format(file = file_name)) # to make folder with A-scans
    
    file_path = f"{current_dir}/{file_name}_folder/{file_name}"
    
    n = int(input("Enter number of A scans to generate: "))
    create_file(file_path, current_dir, n)
