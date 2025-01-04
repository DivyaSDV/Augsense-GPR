import os
import re
import matplotlib.pyplot as plt
from tools.plot_Bscan import get_output_data, mpl_plot
from tqdm import tqdm



# used to generate png files from the output files
file_list = []
dir_path = '/content/Interns/dataset_generated/bscan_output_files/'

for filename in os.listdir(dir_path):
    if filename.endswith('.out'):
        file_path = os.path.join(dir_path, filename)
        file_list.append(file_path)



def save_plots(file_list):
    output_dir = '/content/Interns/dataset_generated/B_scan_images/'
    
    for i, input_filename in enumerate(tqdm(file_list, desc="Saving plots")):
        rxnumber = 1
        rxcomponent = 'Ez'
        outputdata, dt = get_output_data(input_filename, rxnumber, rxcomponent)
        plt = mpl_plot(input_filename, outputdata, dt, rxnumber, rxcomponent)
        plt.set_cmap('gray')
        plt.grid(False)

        # Extract diameter and depth from input filename using regex
        match = re.search(r'(\d+)mm_dia_(\d+)mm_depth_merged.out', input_filename)
        diameter = int(match.group(1))
        depth = int(match.group(2))

        # Construct output filename
        output_filename = f"{diameter}mm_dia_{depth}mm_depth_image.png"

        # Save the plot
        output_path = os.path.join(output_dir, output_filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

























