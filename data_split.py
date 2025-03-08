import os
import shutil
import random

source_dir = "training_data"
dataset_dir = "annotated_data"
label_dir = "yolo_annotations"
train_ratio, val_ratio = 0.7, 0.2  # 70% train, 20% val, 10% test

images = [
    os.path.join(root, f)
    for root, _, files in os.walk(source_dir)
    for f in files
    if f.endswith(".png")
]

random.shuffle(images)

train_split = int(len(images) * train_ratio)
val_split = int(len(images) * (train_ratio + val_ratio))

splits = {
    "train": images[:train_split],
    "val": images[train_split:val_split],
    "test": images[val_split:],
}

images_with_people, images_without_people = 0, 0

for split, split_images in splits.items():
    img_dest = os.path.join(dataset_dir, "images", split)
    label_dest = os.path.join(dataset_dir, "labels", split)

    os.makedirs(img_dest, exist_ok=True)
    os.makedirs(label_dest, exist_ok=True)

    for img in split_images:
        label = img.replace(".png", ".txt").replace(source_dir, label_dir)

        shutil.copy(img, os.path.join(img_dest, os.path.basename(img)))

        if os.path.exists(label):
            shutil.copy(label, os.path.join(label_dest, os.path.basename(label)))
            images_with_people += 1
        else:
            images_without_people += 1

print(
    f"There were {images_with_people} images with and {images_without_people} without people."
)
