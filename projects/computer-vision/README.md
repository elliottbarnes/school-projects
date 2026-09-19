# Computer Vision: Emotion Classification

An archival Python experiment for training an emotion classifier and running inference on webcam frames. The group project history credits Elliott Barnes, Muhammad Hammad, and Mackenzie Barrett.

## Included

- `new_model.py`: data preparation and convolutional-network training.
- `main.py`: OpenCV webcam inference using a trained Keras model.
- `demo.py`: plotting utilities for samples and training metrics.

## Requirements and limitations

The source imports Python, NumPy, pandas, Matplotlib, Keras, Keras Preprocessing, and OpenCV. It expects the FER2013 dataset, trained model files, and an OpenCV face-cascade file, none of which are redistributed here. Paths and APIs reflect the original environment and may require updates for current library versions. No current training or inference run is claimed.
