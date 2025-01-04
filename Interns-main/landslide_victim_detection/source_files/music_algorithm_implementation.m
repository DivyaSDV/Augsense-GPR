clear all;
close all;

% Parameters
fs = 1000;      % Sampling frequency (samples per second)
T = 1;          % Duration (seconds)
t = 0:1/fs:T-1/fs;  % Time vector

% Signal components (frequencies in Hz)
f1 = 50;    % Frequency of the first sinusoid
f2 = 150;   % Frequency of the second sinusoid
f3 = 300;   % Frequency of the third sinusoid

% Amplitudes
A1 = 1;
A2 = 0.8;
A3 = 0.6;

% Generate sample signal
signal = A1*sin(2*pi*f1*t) + A2*sin(2*pi*f2*t) + A3*sin(2*pi*f3*t);

% Add white Gaussian noise to the signal
snr = 20; % Signal-to-noise ratio in dB
noisy_signal = awgn(signal, snr, 'measured');

% Plot the noisy signal
% figure;
% plot(t, noisy_signal);
% title('Noisy Signal');
% xlabel('Time (s)');
% ylabel('Amplitude');

% MUSIC Algorithm Parameters
%M = 50;  % Number of elements in data vector (window length)
M = 2894;
R = 2;  % Number of sinusoidal components to estimate (model order)

% Forming the data matrix using sliding windows
%data_matrix = buffer(noisy_signal, M, M-1, 'nodelay');

data = load("C:\Work\MatlabScripts\MusicAlgorithm\landslide_bscans\landslide_decluttered.mat");
data_matrix = data.decluttered_bscan;

% Add white Gaussian noise to the signal
% snr = 5; % Signal-to-noise ratio in dB
% noisy_signal = awgn(data_matrix, snr, 'measured');
% data_matrix = noisy_signal;

% Covariance matrix of the data
Rxx = (data_matrix * data_matrix') / size(data_matrix, 2);

% Eigenvalue decomposition
[eigenVectors, eigenValues] = eig(Rxx);
eigenValues = diag(eigenValues);

% Sort eigenvalues in descending order
[eigenValues, idx] = sort(eigenValues, 'descend');
eigenVectors = eigenVectors(:, idx);

% Signal subspace (choose first R eigenvectors)
En = eigenVectors(:, R+1:end);  % Noise subspace

% MUSIC Spectrum
frequencies = 0.01:0.01:0.4;  % Frequency grid (search space)
P_music = zeros(size(frequencies));

for i = 1:length(frequencies)
    steering_vector = exp(-1j*2*pi*frequencies(i)*(0:M-1)'/fs);
    P_music(i) = 1 / abs(steering_vector' * (En * En') * steering_vector);
end

% Normalize the spectrum
P_music = 10*log10(P_music / max(P_music));

% Plot the MUSIC Spectrum
figure;
plot(frequencies, P_music);
title('MUSIC Spectrum');
xlabel('Frequency (Hz)');
ylabel('Power (dB)');
grid on;

% Identify peaks in the MUSIC spectrum
% [~, locs] = findpeaks(P_music, frequencies, 'MinPeakHeight', -5, 'MinPeakDistance', 20);
[~, locs] = findpeaks(P_music, frequencies, 'MinPeakHeight', -5 , 'MinPeakDistance', 0.1);
disp('Estimated Frequencies (Hz):');
disp(locs);