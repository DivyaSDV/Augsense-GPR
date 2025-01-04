# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:42:38 2024
Based on the video  https://www.youtube.com/watch?v=ACe_wmGp2LI
@author: divya
"""

import scipy.interpolate
import numpy as np
from random import random as rd
import os

# Define constants
m = np.array([12, 9.3, 6.2, 5.5, 2.8, 0.2]) #Percentage of water content
#Experimentally derived Debye Properties of concrete
e_stat = np.array([12.84, 11.19, 9.14, 8.63, 6.75, 4.814]) # epsilon - static permittivity corresponding to above water content %
e_inf = np.array([7.42, 7.2, 5.93, 6.023, 5.503, 4.507]) #epsilon - infinty permittivity (more details in the ref papers)
t = np.array([0.611, 0.73, 0.8, 1, 2.28, 0.82]) * 10**-9 # relaxation time
sigma = np.array([20.6, 23, 6.7, 5.15, 2.03, 0.606]) * 10**-3 # conductivity

# Interpolations
# Interpolating e_stat with respect to water content, and for other parameters
es = scipy.interpolate.interp1d(m, e_stat)
ei = scipy.interpolate.interp1d(m, e_inf)
t0 = scipy.interpolate.interp1d(m, t)
si = scipy.interpolate.interp1d(m, sigma)



total_files = 2000
# Get the directory where the script is located
folder_path = os.path.dirname(os.path.abspath(__file__))
folder_path = folder_path +"\gpr_in_files"

for i in range(total_files):
    # Open file for appending data
    in_filename = "\gprMax_in_file_" + str(i) + ".in"
    filename = folder_path + in_filename
    print(filename)
    with open(filename, 'w') as f:
        
        f.write("#title: GPR input file \n")
        f.write("#domain: 0.5 0.3 0.4 \n")
        f.write("#dx_dy_dz: 0.001 0.001 0.001 \n")
        f.write("#time_window: 3000 \n")
        mv = 0.2 + (12.0 - 0.21) * rd()  # Adjust lower bound to 0.2
        
        # Print material properties with unique ID
        material_id = f"Concrete_{i}"
        # print(f"#material: {ei(mv)} {si(mv)} 1 0 {material_id} \n")
        # print(f"#add_dispersion_debye: 1 {es(mv) - ei(mv)} {t0(mv)} {material_id} \n")
        # print(f"#box: 0 0 0 0.5 0.3 0.3 {material_id} \n")

        f.write(f"#material: {ei(mv)} {si(mv)} 1 0 {material_id} \n")
        f.write(f"#add_dispersion_debye: 1 {es(mv) - ei(mv)} {t0(mv)} {material_id} \n")
        f.write(f"#box: 0 0 0 0.5 0.3 0.3 {material_id} \n")
        # Cylinder properties
        # Radius should vary from 5 mm to 2.5 cm
        # Rebar should be within concrete. Therefore 0.3 - r. 
        # 0.3 is the height of the rebar.
        r = 0.005 + 0.0245 * rd()
        z = (0.3 - r) * rd()
        
        f.write(f"#cylinder: 0.25 0 {z} 0.25 0.3 {z} {r} pec \n")

        
        f.write("#python: \n")
        f.write("from user_libs.antennas import GSSI \n")
        f.write("GSSI.antenna_like_GSSI_1500(0.25, 0.15, 0.3, resolution=0.001) \n")
        f.write("#end_python:")
        
        # To save the parameters for machine learning
        # Save currently run model full name, Parameters: Radius, Depth, Water content (r, z, mv)
        # Append data to file
        # Open file for appending data
        label_filename = "\Concrete_labels" + ".txt"
        label_filename = folder_path + label_filename
        print(label_filename)
        with open(label_filename, 'a') as f_label:
            f_label.write(f"{in_filename}: {r} {z} {mv}\n")
        f_label.close()
f.close()

