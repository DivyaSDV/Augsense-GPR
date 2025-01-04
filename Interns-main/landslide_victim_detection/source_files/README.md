This folder has to saved in the same folder where tools folder (likely in the gprMax folder) is located.

- make_Bscan_0511_1814.py contains the python code to generate n A-scans containing a cylinder of radius varying sinusoidally between 0.03m and 0.05m. 
- format_Bscan_file_0511_1814.txt contains the format of the .in files that the python script will output. The name of format file used in the make_Bscan_0511_1814.py script must be updated if any changes are made to the format file being currently used.
- run_in_files.py is the python script containing the gprMax command to generate the .out files corresponding to the .in files. This file needs to be executed from the folder containing the tools folder that is downloaded along with the gprMax software.


For implementing MUSIC algorithm, the matlab files required are 
- convert_gprmax_output_to_mat.m for converting the .out B-scan file from gprMax to .mat file
- music_algorithm_implementation.m for implementing MUSIC algorithm

Present Status (2024/11/07):
Matlab script worked for an example signal, but was inconsistent when applied to the B-scan (_0511_1814_merged.out) generated using gprMax.

Status on 2024/11/15:  As per source file MUSIC_respiratory_rate_modified_data_mat_transposed.m

The slow variation (the sine wave pattern in 20 column Radargram) in the column direction is considered. We increased the size of data matrix by copying the data matrix 16 times (16 x 20). Therefore, covariance matrix is 320 x 320. 

The output obtained is :
 Estimated Frequencies (Hz):
    0.2493
The above output is consistent when a sample rate of 54 is given. Please check here. This should be same as the sample rate used to generate radargram. 

The MUSIC spectrum obtained has a leading downward trend, the exact reason for this is not clear.




