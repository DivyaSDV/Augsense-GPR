close all;

% Specify the dataset path for Ez
dataset_path = '/rxs/rx1/Ez';
%[human_bscan, attributes] = hdf5read('C:\Work\gprMaxOutputs\human_1_merged.out',dataset_path)

%[human_bscan, attributes] = hdf5read("C:\Work\MatlabScripts\human_2_gprmax_output\human_2_merged.out", dataset_path)
[landslide_bscan, attributes] = hdf5read("C:\Work\MatlabScripts\MusicAlgorithm\landslide_bscans\_0511_1814_merged.out", dataset_path)

%figure,imagesc(human_bscan)
[rows cols] = size(landslide_bscan)
ez_data_transposed = transpose(landslide_bscan)
[transposed_rows transposed_cols] = size(ez_data_transposed)
save("landslide_Bscan.mat","ez_data_transposed")
figure,imagesc(landslide_bscan)

figure,imagesc(ez_data_transposed)
radargram = ez_data_transposed
%radargram = radargram-mean(radargram(:));

% Calculate the mean of each column
column_means = mean(ez_data_transposed);


% Subtract the mean from each column
ez_data_centered = ez_data_transposed - column_means;
figure,imagesc(ez_data_centered)
save("landslide_mean_subtracted.mat","ez_data_centered")

% Just removing initial 500 rows to remove direct signal
decluttered_bscan = ez_data_transposed(500:transposed_rows,:);
figure,imagesc(decluttered_bscan)
save("landslide_decluttered.mat","decluttered_bscan")

%
% disp(h5info('C:\Work\gprMaxOutputs\human_1_merged.out'))
% h5disp('C:\Work\gprMaxOutputs\landslide_1_merged.out')
    
