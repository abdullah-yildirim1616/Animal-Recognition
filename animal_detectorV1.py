import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

window = tk.Tk()
window.title("Animal Detector")
window.geometry("600x400")
window.configure(bg="#f0f0f0")

title_label = tk.Label(window, text="🐾 Animal Detector", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=30)

def upload_image():
    messagebox.showinfo("Upload", "Fotoğraf yükleme fonksiyonu burada çalışacak.")

def start_camera():
    messagebox.showinfo("Live Camera", "Kamera ile canlı tanıma burada çalışacak.")

upload_btn = tk.Button(window, text="📁 Upload Image", command=upload_image, font=("Helvetica", 14), width=20, bg="#ffffff")
upload_btn.pack(pady=10)

camera_btn = tk.Button(window, text="📷 Live Camera", command=start_camera, font=("Helvetica", 14), width=20, bg="#ffffff")
camera_btn.pack(pady=10)

window.mainloop()