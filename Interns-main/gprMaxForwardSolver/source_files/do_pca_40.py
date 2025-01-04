import numpy as np
from scipy.io import loadmat, savemat
from sklearn.decomposition import PCA

def perform_pca(input_file, output_file, n_components=40):
    # Load the combined matrix from the .mat file
    mat_contents = loadmat(input_file)
    combined_matrix = mat_contents['combined_matrix']

    # Reshape the matrix for PCA: (samples, features)
    reshaped_matrix = combined_matrix.reshape(combined_matrix.shape[0] * combined_matrix.shape[1], combined_matrix.shape[2])

    # Perform PCA
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(reshaped_matrix)

    # Reshape back to the original dimensions but with reduced components
    pca_matrix = principal_components.reshape(combined_matrix.shape[0], combined_matrix.shape[1], n_components)
    
    # Save the PCA-reduced matrix to a .mat file
    savemat(output_file, {"pca_matrix": pca_matrix})
    print(f"Saved PCA-reduced matrix to {output_file}")

if __name__ == "__main__":
    input_file = "combined_ascans.mat"  # Path to the .mat file containing the combined matrix
    output_file = "pca_reduced_ascans.mat"  # Path to save the PCA-reduced matrix
    n_components = 40  # Number of principal components to keep

    perform_pca(input_file, output_file, n_components)
