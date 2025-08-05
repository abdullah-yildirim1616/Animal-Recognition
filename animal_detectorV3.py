import os
import cv2
import torch
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.5

animal_classes = ['cat', 'dog', 'bird', 'horse', 'sheep', 'cow']

def save_cropped_animal(image, label):
    folder = os.path.join('animals', label)
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
    filename = f"{label}_{timestamp}.jpg"
    path = os.path.join(folder, filename)
    cv2.imwrite(path, image)

root = tk.Tk()
root.title("Animal Detection System")
root.geometry("800x600")
root.configure(bg="white")

title = tk.Label(root, text="Animal Detection System", font=("Arial", 24), bg="white")
title.pack(pady=20)

image_label = tk.Label(root)
image_label.pack(pady=10)

def upload_image():
    path = filedialog.askopenfilename()
    if not path:
        return
    image = cv2.imread(path)
    results = model(image)

    for *box, conf, cls in results.xyxy[0]:
        label = model.names[int(cls)]
        if label in animal_classes:
            x1, y1, x2, y2 = map(int, box)
            cropped = image[y1:y2, x1:x2]
            save_cropped_animal(cropped, label)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(image_rgb)

    imgtk = ImageTk.PhotoImage(image=img_pil)

    image_label.imgtk = imgtk
    image_label.configure(image=imgtk)

cap = None
live_running = False

def live_camera():
    global cap, live_running
    if live_running:
        return  
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera açılamadı!")
        return
    live_running = True
    update_frame()

def update_frame():
    global cap, live_running
    if not live_running:
        return
    ret, frame = cap.read()
    if not ret:
        print("Kameradan görüntü alınamadı!")
        stop_live_camera()
        return

    results = model(frame)
    for *box, conf, cls in results.xyxy[0]:
        label = model.names[int(cls)]
        if label in animal_classes:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img_pil)

    image_label.imgtk = imgtk
    image_label.configure(image=imgtk)

    root.after(30, update_frame)

def stop_live_camera():
    global cap, live_running
    live_running = False
    if cap:
        cap.release()
        cap = None

    image_label.configure(image='')

def on_close():
    stop_live_camera()
    root.destroy()

upload_button = tk.Button(root, text="Upload Image", font=("Arial", 16), width=20, command=upload_image)
upload_button.pack(pady=10)

live_button = tk.Button(root, text="Live Camera", font=("Arial", 16), width=20, command=live_camera)
live_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()