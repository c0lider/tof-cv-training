import json
import os
from pathlib import Path


def convert_coco_to_yolo(coco_json_path, output_dir, image_dir=None):
    """
    Convert COCO format annotations to YOLO format

    Args:
        coco_json_path: Path to the COCO JSON file
        output_dir: Directory where YOLO annotations will be saved
        image_dir: Directory containing the images (optional)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load COCO JSON file
    with open(coco_json_path, "r") as f:
        coco_data = json.load(f)

    # Create a dictionary to map category IDs to continuous indices (0-based)
    categories = {cat["id"]: idx for idx, cat in enumerate(coco_data["categories"])}

    # Map image IDs to their filenames
    image_map = {img["id"]: img for img in coco_data["images"]}

    # Group annotations by image ID
    annotations_by_image = {}
    for ann in coco_data["annotations"]:
        img_id = ann["image_id"]
        if img_id not in annotations_by_image:
            annotations_by_image[img_id] = []
        annotations_by_image[img_id].append(ann)

    # Convert annotations for each image
    for img_id, anns in annotations_by_image.items():
        img_info = image_map[img_id]
        image_width = img_info["width"]
        image_height = img_info["height"]

        # Create YOLO annotation file (same basename but with .txt extension)
        base_filename = Path(img_info["file_name"]).stem
        yolo_filepath = os.path.join(output_dir, f"{base_filename}.txt")

        with open(yolo_filepath, "w") as f:
            for ann in anns:
                # Get category index (YOLO expects 0-based indices)
                category_idx = categories[ann["category_id"]]

                # Convert COCO bbox [x, y, width, height] to YOLO format [x_center, y_center, width, height]
                # All values normalized to be between 0 and 1
                x, y, w, h = ann["bbox"]
                x_center = (x + w / 2) / image_width
                y_center = (y + h / 2) / image_height
                norm_w = w / image_width
                norm_h = h / image_height

                # Write annotation in YOLO format: class x_center y_center width height
                f.write(f"{category_idx} {x_center} {y_center} {norm_w} {norm_h}\n")

    # Generate dataset.yaml file for YOLOv8
    yaml_path = os.path.join(output_dir, "dataset.yaml")
    with open(yaml_path, "w") as f:
        category_names = {
            idx: cat["name"]
            for cat in coco_data["categories"]
            for cat_id, idx in categories.items()
            if cat_id == cat["id"]
        }

        # Determine paths based on provided parameters
        if image_dir:
            train_path = image_dir
        else:
            # If no image directory specified, assume parent directory of output_dir
            train_path = str(Path(output_dir).parent)

        f.write(f"# YOLOv8 dataset configuration\n")
        f.write(f"path: {train_path}\n")
        f.write(f"train: images/train\n")
        f.write(f"val: images/val\n")
        f.write(f"test: images/test\n\n")
        f.write(f"# Classes\n")
        f.write(f"names:\n")
        for idx in range(len(category_names)):
            f.write(f"  {idx}: {category_names[idx]}\n")

    print(f"Conversion complete. YOLO annotations saved to {output_dir}")
    print(f"Dataset configuration saved to {yaml_path}")
    print(
        f"You may need to adjust the paths in {yaml_path} according to your directory structure"
    )


if __name__ == "__main__":
    input_directory = "training_data"
    output_path = "yolo_annotations"

    folders = [
        os.path.join(input_directory, f)
        for f in os.listdir(input_directory)
        if os.path.isdir(os.path.join(input_directory, f))
    ]

    for folder in folders:
        try:
            convert_coco_to_yolo(
                os.path.join(folder, "instances_default.json"),
                os.path.join(output_path, folder.split("/")[-1]),
            )
        except:
            pass
