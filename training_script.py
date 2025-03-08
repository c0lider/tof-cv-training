if __name__ == "__main__":
    from ultralytics import YOLO

    model = YOLO("yolov8n.pt")

    model.train(
        data="annotated_data/dataset.yaml",
        epochs=50,
        imgsz=416,
        batch=8,
        device="cuda",
        plots=False
    )
