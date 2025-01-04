% This code worked and gave following output 15.11.24. 14.30 pm
% Estimated Frequencies (Hz): 0.2494

close all;
% Parameters

fs = 54;      % Confirm that this is the actual sampling rate for your data
T = 1;          % Duration (seconds)
t = 0:1/fs:T-1/fs;  % Time vector

% MUSIC Algorithm Parameters
M = 2894;
R = 1;  % Since we expect a single frequency component

data = load("C:\Work\MatlabScripts\MusicAlgorithm\landslide_bscans\landslide_decluttered.mat");
data_matrix = data.decluttered_bscan;
figure,imagesc(data_matrix)
%%% Commenting on seeing no improvement
% % Expanding the matrix by concatenating multiple times. 
% % Concatenate the matrix four times along the columns
expanded_matrix = repmat(data_matrix, 1, 16);
% The size of expanded_matrix will now be 2894 x 80
data_matrix = expanded_matrix;

% % Add white Gaussian noise to the signal (optional)
snr = 20; % Try with higher SNR for stability
noisy_signal = awgn(data_matrix, snr, 'measured');
data_matrix = noisy_signal;
% 
% % Covariance matrix of the data
%Rxx = (data_matrix * data_matrix') / size(data_matrix, 2);

% Taking transpose of data matrix before covariance computation 
Rxx = (data_matrix' * data_matrix) / size(data_matrix, 1);
%% ---- Replacing above covariance with following code ----
% % Covariance Matrix Estimation with averaging across time snapshots
% L = 20;  %20 % Choose snapshot length based on structure of data matrix
% Rxx = zeros(320, 320);
% for i = 1:L:size(data_matrix, 2)-L
%     snapshot = data_matrix(:, i:i+L-1);
% 
%     Rxx = Rxx + (snapshot * snapshot') / L;
% end
% Rxx = Rxx / (size(data_matrix, 2) / L);
%% --- end the covariance matrix computation

% Assuming Rxx is already calculated as above
figure;
imagesc(Rxx);         % Create a heatmap of the covariance matrix
colorbar;             % Show color bar to indicate scale
title('Covariance Matrix Heatmap');
xlabel('Signals');
ylabel('Signals');

% Eigenvalue decomposition
[eigenVectors, eigenValues] = eig(Rxx);
eigenValues = diag(eigenValues);

% Sort eigenvalues in descending order
[eigenValues, idx] = sort(eigenValues, 'descend');
eigenVectors = eigenVectors(:, idx);

% Signal subspace (choose first R eigenvectors)
En = eigenVectors(:, R+1:end);  % Noise subspace

% MUSIC Spectrum
%frequencies = 0.01:0.01:0.4;  % Increase resolution of frequency grid

frequencies = 0.02:0.0001:0.3;  % Increase resolution of frequency grid
P_music = zeros(size(frequencies));
M = 320;
for i = 1:length(frequencies)
    steering_vector = exp(-1j*2*pi*frequencies(i)*(0:M-1)'/fs);
    P_music(i) = 1 / abs(steering_vector' * (En * En') * steering_vector);
end

% Normalize the spectrum
P_music = 10*log10(P_music / max(P_music));
% Plot the MUSIC Spectrum without normalization
figure;
plot(frequencies, (P_music));
title('MUSIC Spectrum');
xlabel('Frequency (Hz)');
ylabel('Power (dB)');
grid on;

% Identify peaks in the MUSIC spectrum
[~, locs] = findpeaks((P_music), frequencies, 'MinPeakHeight', -5, 'MinPeakDistance', 0.2);

disp('Estimated Frequencies (Hz):');
disp(locs);
