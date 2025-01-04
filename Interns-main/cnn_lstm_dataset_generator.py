import os
import re
import numpy as np
import matplotlib.pyplot as plt
from tools.plot_Bscan import get_output_data, mpl_plot



# create a list of path to output files
file_list = []
dir_path = '/content/Interns/dataset_generated/bscan_output_files/'

for filename in os.listdir(dir_path):
    if filename.endswith('.out'):
        file_path = os.path.join(dir_path, filename)
        file_list.append(file_path)



def cnn_lstm_numpy_files(file_list):
    cnn_dir = '/content/Interns/dataset_generated/cnn_dataset/'
    lstm_dir = '/content/Interns/dataset_generated/lstm_dataset/'

    for i, input_filename in enumerate(file_list):
        print(f"Processing file {i} in file_list: {input_filename}")
        rxnumber = 1
        rxcomponent = 'Ez'
        fieldstrength, dt = get_output_data(input_filename, rxnumber, rxcomponent)

        mean_trace = np.mean(fieldstrength, axis=1)

        clutter_removed = fieldstrength - mean_trace[:, np.newaxis]
        print(f"Clutter removed for file {i} in file file_lsit")

        normalized_cnn = (clutter_removed - clutter_removed.min()) / (clutter_removed.max() - clutter_removed.min())
        print(f"Normalized CNN data for file {i} in file_list")

        # Extract diameter and depth from input filename using regex
        match = re.search(r'(\d+)mm_dia_(\d+)mm_depth_merged.out', input_filename)
        diameter = int(match.group(1))
        depth = int(match.group(2))

        # Construct output filename
        cnn_filename = f"{diameter}mm_dia_{depth}mm_depth_cnn.npy"

        # Save the plot
        cnn_path = os.path.join(cnn_dir, cnn_filename)
        np.save(cnn_path, normalized_cnn)
        print(f"Saved CNN file corresponding to index {i} in file_list : {cnn_filename}")

        normalized_lstm = (fieldstrength - fieldstrength.min()) / (fieldstrength.max() - fieldstrength.min())
        lstm_data = normalized_lstm.T
        print(f"Created LSTM data for file {i} in file_list")

        lstm_filename = f"{diameter}mm_dia_{depth}mm_depth_lstm.npy"
        lstm_path = os.path.join(lstm_dir, lstm_filename)
        np.save(lstm_path, lstm_data)
        print(f"Saved LSTM file corresponding to index {i} in file_list : {lstm_filename}")



cnn_lstm_numpy_files(file_list)








































