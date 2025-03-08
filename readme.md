# TOF Camera Object Detection Dataset

-   [TOF Camera Object Detection Dataset](#tof-camera-object-detection-dataset)
    -   [📌 Overview](#-overview)
    -   [🔧 Getting Started](#-getting-started)
    -   [📂 Initial Dataset Structure](#-initial-dataset-structure)
        -   [Generate YOLO annotations](#generate-yolo-annotations)
        -   [Resulting Dataset structure](#resulting-dataset-structure)
    -   [🚆 Train the model](#-train-the-model)
        -   [Potential issues](#potential-issues)
    -   [🧍🏽 Use the model for person detection](#-use-the-model-for-person-detection)
    -   [📜 License](#-license)

## 📌 Overview

This repository contains **training images** and their corresponding **annotations** in the `training_data` folder. The dataset is designed for **object detection** using heatmap images captured from a **Time-of-Flight (ToF) camera**.

## 🔧 Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/c0lider/tof-cv-training
    cd tof-cv-training
    ```

2. Install all dependencies

    ```bash
    pip install -r requirements.txt

    ```

## 📂 Initial Dataset Structure

```
📦 training_data
 ┣ 📂 [Capture_Folders]   # Each folder contains images from one capture session
 ┃ ┣ 📂 image_1
 ┃ ┣ 📂 image_2
 ┃ ┣ 📂 ...
 ┃ ┗ 📜 instances_default.json  # COCO-formatted annotation file for that capture
```

### Generate YOLO annotations

Run the python script `coco2yolo.py` to generate YOLO annotations from COCO annotations.

### Resulting Dataset structure

In order to train a YOLOv8 machine learning model, the following folder structure is needed:

```
dataset/
│── images/
│   ├── train/
│   ├── val/
│   ├── test/
│── labels/
│   ├── train/
│   ├── val/
│   ├── test/
│── dataset.yaml
```

Generating this structure can be achieved by running the `data_split.py` script.

> The data is separated into 70% training, 20% validation and 10% test data.

## 🚆 Train the model

Run `training_script.py` to train the model. The following YOLO models are available:

-   yolov8n.pt: Smallest model, fastest but less accurate.
-   yolov8s.pt, yolov8m.pt, yolov8l.pt: Larger, more accurate but slower.

For now we will use `yolov8n.pt`.

> It is recommended to use an nvidia GPU in order to significantly speed up the training process. In that case modify the `trainin_script.py` and set `device="cuda"`

### Potential issues

If you run into an error indicating that the images or the dataset.yaml could not be found follow these steps:

-   open the ultralytics config file `settings.json`
    -   under windows the file is in `C:\Users\<YourUsernameAppData\Roaming\Ultralytics\settings.json`
    -   under macos the file is in `/Users/<YourUsernameLibrary/Application Support/Ultralytics`
-   modify the file, so that `datasets_dir` points to the project root.
-   save and close the file

## 🧍🏽 Use the model for person detection

TODO

## 📜 License

This dataset is for educational purposes.
