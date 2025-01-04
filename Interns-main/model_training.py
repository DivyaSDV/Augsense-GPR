import os
import regex as re
import numpy as np

# Define paths
cnn_data_dir = '/content/Interns/dataset_generated/cnn_dataset'
lstm_data_dir = '/content/Interns/dataset_generated/lstm_dataset'

# Load data
def load_data(cnn_dir, lstm_dir):
    cnn_files = sorted([os.path.join(cnn_dir, f) for f in os.listdir(cnn_dir) if f.endswith('.npy')])
    lstm_files = sorted([os.path.join(lstm_dir, f) for f in os.listdir(lstm_dir) if f.endswith('.npy')])

    X_f1 = []
    X_f2 = []
    y = []

    for cnn_file, lstm_file in zip(cnn_files, lstm_files):
        # Load features
        f1_feature = np.load(cnn_file)
        f2_feature = np.load(lstm_file)

        # Extract label from filename
        label = int(os.path.basename(cnn_file).split('mm_dia')[0])

        # Append to lists
        X_f1.append(f1_feature)
        X_f2.append(f2_feature)
        y.append(label)

    return np.array(X_f1), np.array(X_f2), np.array(y)

# Load the data
X_f1, X_f2, y = load_data(cnn_data_dir, lstm_data_dir)
# y = y.astype('float32')
# Combine X_f1 and X_f2
X_combined = list(zip(X_f1, X_f2))


from sklearn.model_selection import train_test_split
X_combined_train, X_combined_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

# Convert the lists of tuples into separate lists of inputs
X_f1_train, X_f2_train = zip(*X_combined_train)
X_f1_test, X_f2_test = zip(*X_combined_test)



X_f1_train = np.array(X_f1_train)
X_f2_train = np.array(X_f2_train)
X_f1_test = np.array(X_f1_test)
X_f2_test = np.array(X_f2_test)






# Define a mapping from original class names to new integer labels
class_mapping = {
    6: 0, 8: 1, 10: 2, 12: 3, 16: 4, 18: 5, 20: 6, 22: 7, 24: 8
}

# Convert original labels to integer labels using the mapping
y_train_mapped = np.array([class_mapping[label] for label in y_train])
y_test_mapped = np.array([class_mapping[label] for label in y_test])





import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, LSTM, Dense, Flatten, Concatenate, BatchNormalization, ReLU


input_shape_f1 = (1273, 200, 1)  # Modified shape for spatial input
input_shape_f2 = (200, 1273)    # Modified shape for sequential input

# Define inputs
input_f1 = Input(shape=input_shape_f1, name='input_f1')
input_f2 = Input(shape=input_shape_f2, name='input_f2')

# CNN branch for feature f1 (with Batch Normalization)
x1 = Conv2D(filters=32, kernel_size=(3, 3))(input_f1)
x1 = BatchNormalization()(x1)
x1 = ReLU()(x1)
x1 = MaxPooling2D(pool_size=(2, 2))(x1)

x1 = Conv2D(filters=64, kernel_size=(3, 3))(x1)
x1 = BatchNormalization()(x1)
x1 = ReLU()(x1)
x1 = MaxPooling2D(pool_size=(2, 2))(x1)

x1 = Conv2D(filters=128, kernel_size=(3, 3))(x1)
x1 = BatchNormalization()(x1)
x1 = ReLU()(x1)
x1 = MaxPooling2D(pool_size=(2, 2))(x1)

x1 = Conv2D(filters=256, kernel_size=(3, 3))(x1)
x1 = BatchNormalization()(x1)
x1 = ReLU()(x1)
x1 = MaxPooling2D(pool_size=(2, 2))(x1)

x1 = Conv2D(filters=512, kernel_size=(3, 3))(x1)
x1 = BatchNormalization()(x1)
x1 = ReLU()(x1)
x1 = MaxPooling2D(pool_size=(2, 2))(x1)

x1 = Flatten()(x1)

# LSTM branch for feature f2 (with Batch Normalization)
x2 = LSTM(units=100, return_sequences=False)(input_f2)
x2 = BatchNormalization()(x2)

# Concatenate CNN and LSTM outputs
x3 = Concatenate()([x1, x2])

# Fully connected layers
x3 = Dense(units=64)(x3)
x3 = BatchNormalization()(x3)
x3 = ReLU()(x3)

x3 = Dense(units=32)(x3)
x3 = BatchNormalization()(x3)
x3 = ReLU()(x3)

# Output layer with 9 classes
output = Dense(units=9, activation='softmax')(x3)

# Define the model
model = tf.keras.Model(inputs=[input_f1, input_f2], outputs=output, name='multi_input_model_with_batch_norm')

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])






# Train the model
history = model.fit(
    [X_f1_train, X_f2_train],  # Inputs
    y_train_mapped,                   # Labels
    epochs=3,                 # Number of epochs
    batch_size=32,             # Batch size
    validation_data=([X_f1_test, X_f2_test], y_test_mapped)  # Validation data
)













































