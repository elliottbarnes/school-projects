import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import random
from keras.models import load_model

EMOTIONS = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}
PATH_FOR_MODEL_FILES = "../Models"


def get_files_list():
    """
    Gets all the files inside the models folder
    :return:
    """
    f_list = []
    for f in os.listdir(PATH_FOR_MODEL_FILES):
        path_extended = PATH_FOR_MODEL_FILES + "/" + f
        for int_path in os.listdir(path_extended):
            f_list.append(path_extended + "/" + int_path)
    return f_list


def read_output_file(path):
    file = open(path, "r")
    lines = file.readlines()

    filtered_lines = list(filter(lambda k: '[==============================]' in k, lines))
    filtered_lines = list(map(lambda k: k.split(" "), filtered_lines))

    val_loss = []
    val_acc = []
    loss = []
    acc = []
    labels_epoch = []

    epoch = 1
    for line in filtered_lines:
        if len(line) == 17:
            loss.append(float(line[7]))
            acc.append(float(line[10]))
            val_loss.append(float(line[13]))
            val_acc.append(float(line[16].strip("\n")))
            labels_epoch.append(epoch)
            epoch = epoch + 1

    labels_epoch = list(reversed(labels_epoch))
    val_loss.reverse()
    val_acc.reverse()
    loss.reverse()
    acc.reverse()

    return {
        "val_loss": val_loss,
        "val_acc": val_acc,
        "loss": loss,
        "acc": acc,
        "labels_epoch": labels_epoch,
        "model": path.split("/")[-2]
    }


def make_plot_for_file(path):
    out = read_output_file(path)

    fig = plt.figure(figsize=(15, 9))
    fig.tight_layout()
    fig.canvas.set_window_title("Accuracy vs Loss for: " + out["model"])

    plt.subplot(1, 2, 1)
    plt.title("Loss vs Validation Loss")
    plt.plot(out["labels_epoch"], out["val_loss"], '-b', label="val_loss")
    plt.plot(out["labels_epoch"], out["loss"], '--k', label="loss")
    plt.xlabel("epoch")
    plt.ylabel("loss")
    plt.yticks(np.arange(0, 1.6, step=0.1))
    plt.xticks(np.arange(0, len(out["labels_epoch"]) + 1, step=3))
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title("Accuracy vs Validation Accuracy")
    plt.plot(out["labels_epoch"], out["val_acc"], '-r', label="val_acc")
    plt.plot(out["labels_epoch"], out["acc"], '--g', label="acc")
    plt.xlabel("epoch")
    plt.ylabel("accuracy")
    plt.yticks(np.arange(0, 1.1, step=0.1))
    plt.xticks(np.arange(0, len(out["labels_epoch"]) + 1, step=3))
    plt.legend()


def plot_images_on_figure(fig, columns, rows, images, labels):
    fig.tight_layout()
    for i in range(1, columns * rows + 1):
        fig.add_subplot(rows, columns, i)
        plt.title(str(i) + ": " + labels[i - 1])
        plt.gray()
        plt.imshow(images[i-1])


def get_image_data(data, emotions_to_show, numbers=5, data_type="Training"):
    images = []
    for item in emotions_to_show:
        sample = random.sample(list(data.query("Usage == '" + data_type + "' and emotion == " + str(item)).pixels), numbers)

        for img in sample:
            image = np.fromstring(img, dtype=int, sep=' ')
            image = np.reshape(image, (48, 48, 1)) / 255.
            images.append(image)

    return images


def show_sample_dataset(data, emotions_to_show):
    number_of_samples = 5

    labels = []
    for i in range(len(emotions_to_show)):
        for j in range(number_of_samples):
            labels.append(EMOTIONS[emotions_to_show[i]])

    images = get_image_data(data, emotions_to_show, numbers=number_of_samples, data_type="Training")

    fig = plt.figure(figsize=(15, 9))
    fig.canvas.set_window_title("Training Sample From Each Category")
    plot_images_on_figure(fig, number_of_samples, len(emotions_to_show), images, labels)


def show_class_weight(data, emotions_to_show, type='Training'):
    query_str = ""

    for i in range(len(emotions_to_show)):
        if len(emotions_to_show) - 1 == i:
            query_str = query_str + " emotion == " + str(emotions_to_show[i])
        else:
            query_str = query_str + " emotion == " + str(emotions_to_show[i]) + " or"

    filtered_data = data.query(query_str)[data.Usage == type]
    weights = (filtered_data.emotion.value_counts() / filtered_data.count()[0]).to_dict()
    keys = tuple(map(lambda k: EMOTIONS[k], weights.keys()))
    values = list(weights.values())

    fig = plt.figure()
    fig.canvas.set_window_title("Distribution of Sample Data for: " + type)

    plt.pie(values, labels=keys, autopct='%1.1f%%', startangle=90, colors=['#0091ea', '#cfd8dc', '#607d8b'])
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    t = ""
    for i in emotions_to_show:
        t += '{:10s} {:s} \n'.format(EMOTIONS[i] + ":", str(filtered_data[data.emotion == i].emotion.value_counts().values[0]))

    plt.text(0.02, 0.85, t, fontsize=12, transform=plt.gcf().transFigure)


def show_dataset_weight(data, emotions_to_show):
    query_str = ""

    for i in range(len(emotions_to_show)):
        if len(emotions_to_show) - 1 == i:
            query_str = query_str + " emotion == " + str(emotions_to_show[i])
        else:
            query_str = query_str + " emotion == " + str(emotions_to_show[i]) + " or"

    filtered_data = data.query(query_str)
    weights = (filtered_data.Usage.value_counts() / filtered_data.count()[0]).to_dict()
    keys = tuple(map(lambda k: k, weights.keys()))
    values = list(weights.values())

    fig = plt.figure()
    fig.canvas.set_window_title("Distribution of Dataset")

    plt.pie(values, labels=keys, autopct='%1.1f%%', startangle=90, colors=['#0091ea', '#cfd8dc', '#607d8b'])
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    t = ""
    for i in ['Training', 'PublicTest', 'PrivateTest']:
        t += '{:15s} {:s} \n'.format(i + ":",
                                     str(filtered_data[data.Usage == i].emotion.value_counts().values[0]))

    plt.text(0.02, 0.80, t, fontsize=12, transform=plt.gcf().transFigure)


def show_validation_plots(path):
    file = open(path, "r")
    lines = file.readlines()

    filtered_lines = list(filter(lambda k: 'Validation' in k, lines))
    filtered_lines = list(map(lambda k: k.replace(",", ""), filtered_lines))
    filtered_lines = list(map(lambda k: k.replace("\n", ""), filtered_lines))
    filtered_lines = np.array(list(map(lambda k: k.split(": "), filtered_lines)))

    y_pos = np.arange(2)
    performance = list(np.around(filtered_lines[:, 1].astype(float), 2))

    fig = plt.figure(figsize=(13, 5))
    fig.canvas.set_window_title(path.split("/")[-2])
    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, list(filtered_lines[:, 0]))
    plt.xticks(np.arange(0, 1.2, step=0.1))
    plt.title("Validation Accuracy vs Validation Loss")

    for index, value in enumerate(performance):
        plt.text(value, index, str(value))


def show_predictions_on_validation_data(data, path, emotions):
    classifier = load_model(path)
    images = get_image_data(data, emotions, numbers=5, data_type="PublicTest")
    labels = []

    for img in images:
        preds = classifier.predict(np.expand_dims(img, axis=0))[0]
        pred_index = preds.argmax()
        label = EMOTIONS[emotions[pred_index]] + " %.2f%%" % float(preds[pred_index] * 100)
        labels.append(label)

    fig = plt.figure(figsize=(15, 9))
    fig.canvas.set_window_title("Predictions Using Model: " + path.split("/")[-2])
    plot_images_on_figure(fig, 5, len(emotions), images, labels)


def show_total_time(path):
    file = open(path, "r")
    lines = file.readlines()

    filtered_lines = filter(lambda k: '[==============================]' in k, lines)
    filtered_lines = map(lambda k: k.split(" "), filtered_lines)
    filtered_lines = map(lambda k: k[3], filtered_lines)
    filtered_lines = map(lambda k: k.replace("s", ""), filtered_lines)
    filtered_lines = list(map(lambda k: int(k), filtered_lines))
    total_time_taken = sum(filtered_lines)/60
    print("Total time taken to train model {:s} is {:f} minutes".format(path.split("/")[-2], total_time_taken))


if __name__ == '__main__':
    all_files = get_files_list()
    emotions_to_use = [3, 6, 5]
    data_read = pd.read_csv("../Dataset/fer2013.csv")

    # If you just want a single model then put this if condition immediately inside the for loop
    # `if f_path.split("/")[-2] == "M12-87-only-two-emotions":`

    for f_path in all_files:
        if f_path.split("/")[-2] == "M21-81":
            if f_path.endswith(".txt"):
                show_total_time(f_path)
                show_validation_plots(f_path)
                make_plot_for_file(f_path)
            if f_path.endswith(".h5"):
                show_predictions_on_validation_data(data_read, f_path, emotions_to_use)

    show_sample_dataset(data_read, emotions_to_use)
    show_class_weight(data_read, emotions_to_use, 'Training')
    show_class_weight(data_read, emotions_to_use, 'PrivateTest')
    show_class_weight(data_read, emotions_to_use, 'PublicTest')
    show_dataset_weight(data_read, emotions_to_use)
    plt.show()
