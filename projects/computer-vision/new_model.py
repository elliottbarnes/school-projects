import numpy as np
import pandas as pd

from keras import models
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, Activation, BatchNormalization
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# #### Defining some constants #### #

# All the emotions labels mapped
from keras_preprocessing.image import ImageDataGenerator

EMOTIONS = {0: 'Happy', 1: 'Neutral'}
# Number of emotions
NUM_OF_EMOTIONS = len(EMOTIONS.keys())
# Number of images to process at once
BATCH_SIZE = 32
# Number of epochs to run the CNN through
EPOCHS = 50
# Read data again from the csv file
IMPORT_FROM_SCRATCH = True


def get_image_labels(data, usage):
    """
    Returns all the labels for all the corresponding images in order of the dataset
    :param data: the dataframe to retrieve the data from - currently it accepts a dataframe object created by pandas
    :param usage: the usage to extract - possible values for given dataset are Training, PrivateTest, and PublicTest
    :return: a numpy array of all the labels
    """
    return to_categorical(np.array(list(data[data.Usage == usage].emotion)))


def get_image_data(data, usage):
    """
    Returns all the normalized image data as numpy arrays
    :param data: the dataframe to retrieve the data from - currently it accepts a dataframe object created by pandas
    :param usage: the usage to extract - possible values for given dataset are Training, PrivateTest, and PublicTest
    :return: a numpy array of all the images as numpy array
    """

    filtered_data = data[data.Usage == usage]
    image_array = np.zeros(shape=(len(filtered_data), 48, 48, 1))

    for i, row in enumerate(filtered_data.index):
        image = np.fromstring(list(filtered_data.pixels)[i], dtype=int, sep=' ')
        image = np.reshape(image, (48, 48, 1)) / 255.
        image_array[i] = image

    return image_array


def initialize_data(import_data_again=False):
    """
    Initialize all the data for training, testing and validating the neural network
    :param import_data_again: decides whether to import data again from scratch or reuse saved files
    :return: a list of all the different datas
    """

    print("Reading data...")
    to_return = {}

    # Read the data set from the csv file
    data = pd.read_csv("../Dataset/fer2013.csv").query('emotion == 3 or emotion == 6')
    data.loc[data.emotion == 3, 'emotion'] = 0
    data.loc[data.emotion == 6, 'emotion'] = 1

    if import_data_again:
        # Get all the labels and save them in their respective files
        training_labels_import = get_image_labels(data, 'Training')
        np.save("../Dataset/training_labels.npy", training_labels_import)
        validation_labels_import = get_image_labels(data, 'PrivateTest')
        np.save("../Dataset/validation_labels.npy", validation_labels_import)
        test_labels_import = get_image_labels(data, 'PublicTest')
        np.save("../Dataset/test_labels.npy", test_labels_import)

        # Get all image data and save them in their respective files
        training_data_import = get_image_data(data, 'Training')
        np.save("../Dataset/training_data.npy", training_data_import)
        validation_data_import = get_image_data(data, 'PrivateTest')
        np.save("../Dataset/validation_data.npy", validation_data_import)
        test_data_import = get_image_data(data, 'PublicTest')
        np.save("../Dataset/test_data.npy", test_data_import)

    # Load data from the saved files
    to_return["train_labels"] = np.load("../Dataset/training_labels.npy")
    to_return["val_labels"] = np.load("../Dataset/validation_labels.npy")
    to_return["test_labels"] = np.load("../Dataset/test_labels.npy")
    to_return["train_data"] = np.load("../Dataset/training_data.npy")
    to_return["val_data"] = np.load("../Dataset/validation_data.npy")
    to_return["test_data"] = np.load("../Dataset/test_data.npy")

    # Add different variations to the training data
    train_datagen = ImageDataGenerator(
        rotation_range=30,
        shear_range=0.3,
        zoom_range=0.3,
        width_shift_range=0.4,
        height_shift_range=0.4,
        horizontal_flip=True,
        fill_mode='nearest')

    to_return["train_data_augmented"] = train_datagen.flow(
        x=to_return["train_data"],
        y=to_return["train_labels"],
        batch_size=BATCH_SIZE,
        shuffle=True)

    # Calculates the weights for the different emotions
    to_return["weights"] = (data[data.Usage == 'Training'].emotion.value_counts() / data[data.Usage == 'Training'].count()[0]).to_dict()
    print("Data Read Complete!")
    return to_return


def create_sequential_model():
    """
    Creates a sequential model for the deep CNN. The goal is to guess emotions
    :return: a sequential model object
    """
    print("Creating a Sequential model")
    # Create the sequential model for the CNN
    model_int = models.Sequential()

    model_int.add(Conv2D(32, (3, 3), input_shape=(48, 48, 1)))
    model_int.add(Activation("relu"))
    model_int.add(MaxPool2D((2, 2)))
    model_int.add(BatchNormalization())

    model_int.add(Conv2D(64, (3, 3)))
    model_int.add(Dropout(0.1))
    model_int.add(Activation("relu"))
    model_int.add(MaxPool2D((2, 2)))
    model_int.add(BatchNormalization())

    model_int.add(Flatten())
    model_int.add(Dense(64))
    model_int.add(Activation("relu"))

    model_int.add(Flatten())
    model_int.add(Dense(32))
    model_int.add(Activation("relu"))

    model_int.add(Dense(NUM_OF_EMOTIONS))
    model_int.add(Activation('softmax'))

    # Compile the model using categorical cross entropy as the loss function and Adam optimization as the optimizer
    model_int.compile(optimizer="adam",
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

    print(model_int.summary())
    print("Model Creation Complete!")
    return model_int


def train_model(training_model, training_data, validation_data, validation_labels, emotion_weights):
    # Callback function, it is called after every epoch. Saves the best version of the model in a file and prints
    # some stats
    checkpoint = ModelCheckpoint('emotion_model.h5',
                                 monitor='val_loss',
                                 mode='min',
                                 save_best_only=True,
                                 verbose=1)

    earlystop = EarlyStopping(monitor='val_loss',
                              min_delta=0,
                              patience=5,
                              verbose=1,
                              restore_best_weights=True
                              )

    reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                  factor=0.2,
                                  patience=3,
                                  verbose=1,
                                  min_delta=0.0001)

    # Train the model
    return training_model.fit(training_data,
                              validation_data=(validation_data, validation_labels),
                              epochs=EPOCHS,
                              callbacks=[earlystop, checkpoint, reduce_lr],
                              batch_size=BATCH_SIZE,
                              class_weight=emotion_weights)


if __name__ == '__main__':
    dataset_data = initialize_data(import_data_again=IMPORT_FROM_SCRATCH)

    model = create_sequential_model()
    history = train_model(training_model=model,
                          training_data=dataset_data["train_data_augmented"],
                          validation_data=dataset_data["val_data"],
                          validation_labels=dataset_data["val_labels"],
                          emotion_weights=dataset_data["weights"])

    # Evaluate the validation accuracy and loss
    val_loss, val_acc = model.evaluate(dataset_data["test_data"], dataset_data["test_labels"])
    print(f"Validation Accuracy: {val_acc},\nValidation Loss: {val_loss}")
