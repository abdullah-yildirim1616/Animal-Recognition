import os
import torch
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from datetime import datetime

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.classes = [14, 15, 16, 17, 18, 19, 20, 21]

def save_cropped_animal(img, label, box):
    folder = os.path.join("animals", label)
    os.makedirs(folder, exist_ok=True)
    
    x1, y1, x2, y2 = map(int, box)
    cropped = img[y1:y2, x1:x2]
    
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    cv2.imwrite(os.path.join(folder, filename), cropped)

def detect_animals(file_path):
    img = cv2.imread(file_path)
    results = model(img)
    
    labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    names = model.names
    h, w, _ = img.shape
    
    for i in range(len(labels)):
        row = cords[i]
        if row[4] >= 0.3:
            x1, y1, x2, y2 = int(row[0]*w), int(row[1]*h), int(row[2]*w), int(row[3]*h)
            label = names[int(labels[i])]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            save_cropped_animal(img, label, (x1, y1, x2, y2))
    
    cv2.imwrite("detected.jpg", img)
    return "detected.jpg"

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        result_path = detect_animals(file_path)
        show_result(result_path)

def show_result(image_path):
    img = Image.open(image_path)
    img = img.resize((600, 400))
    img_tk = ImageTk.PhotoImage(img)
    panel.config(image=img_tk)
    panel.image = img_tk

root = tk.Tk()
root.title("Animal Detector")
root.geometry("700x600")

title = tk.Label(root, text="Animal Detection System", font=("Helvetica", 18, "bold"))
title.pack(pady=20)

btn_upload = tk.Button(root, text="Görsel Yükle", command=upload_image, font=("Helvetica", 14))
btn_upload.pack(pady=10)

panel = tk.Label(root)
panel.pack(pady=20)

root.mainloop()