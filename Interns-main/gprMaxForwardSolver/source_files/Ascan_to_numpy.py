'''
Author: Rahul

'''
import h5py
import numpy as np
import os
from scipy.io import savemat

def process_ascan(file_path, dataset_path):
    with h5py.File(file_path, 'r') as f:
        data = f[dataset_path][:]
    data_transposed = np.transpose(data)
    return data_transposed

def main(input_dir, dataset_path, output_file):
    all_ascans = []

    # Process each .out file in the directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".out"):
            file_path = os.path.join(input_dir, file_name)
            ascan_data = process_ascan(file_path, dataset_path)
            all_ascans.append(ascan_data)

    # Stack all the A-scans into a single matrix
    combined_matrix = np.stack(all_ascans, axis=-1)

    # Save the matrix to a .mat file
    savemat(output_file, {"combined_matrix": combined_matrix})
    np.save("combined_matrix.npy", combined_matrix)
    print(f"Saved combined matrix to {output_file}")

if __name__ == "__main__":
    input_dir = "C:/Work/output_Ascans"  # Directory containing .out 
    dataset_path = '/rxs/rx1/Ex'  # Dataset path in the .out files
    output_file = "combined_ascans.mat"  # Output .mat file

    main(input_dir, dataset_path, output_file)
