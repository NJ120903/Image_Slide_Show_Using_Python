import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import itertools

class CyberImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Image Viewer")
        self.root.configure(bg='black')

        # Main frame
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(pady=20, padx=20)

        # Left frame for thumbnails
        self.left_frame = tk.Frame(self.main_frame, bg='black')
        self.left_frame.grid(row=0, column=0, padx=10)

        # Center frame for main image
        self.center_frame = tk.Frame(self.main_frame, bg='black')
        self.center_frame.grid(row=0, column=1, padx=10)

        # Right frame for thumbnails
        self.right_frame = tk.Frame(self.main_frame, bg='black')
        self.right_frame.grid(row=0, column=2, padx=10)

        self.image_label = tk.Label(self.center_frame, bg='black')
        self.image_label.pack()

        self.button_frame = tk.Frame(root, bg='black')
        self.button_frame.pack(pady=20)

        self.open_button = tk.Button(self.button_frame, text="Open Folder", command=self.open_folder, bg='cyan', fg='black')
        self.open_button.grid(row=0, column=0, padx=10)

        self.start_button = tk.Button(self.button_frame, text="Start Slideshow", command=self.start_slideshow, bg='cyan', fg='black')
        self.start_button.grid(row=0, column=1, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop Slideshow", command=self.stop_slideshow, bg='cyan', fg='black')
        self.stop_button.grid(row=0, column=2, padx=10)

        self.interval_label = tk.Label(self.button_frame, text="Interval (s):", bg='black', fg='cyan')
        self.interval_label.grid(row=1, column=0, padx=10, pady=10)

        self.interval_entry = tk.Entry(self.button_frame, bg='black', fg='cyan', width=5)
        self.interval_entry.grid(row=1, column=1, padx=10, pady=10)
        self.interval_entry.insert(0, "2")  # Default interval of 2 seconds

        self.images = []
        self.image_iter = None
        self.current_image = None
        self.slideshow_running = False
        self.images_viewed = 0

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
            self.image_iter = itertools.cycle(self.images)
            self.images_viewed = 0
            self.show_thumbnails()
            self.show_next_image()

    def show_thumbnails(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        for idx, image_path in enumerate(self.images):
            image = Image.open(image_path)
            image.thumbnail((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            if idx % 2 == 0:
                thumb_label = tk.Label(self.left_frame, image=photo, bg='black')
                thumb_label.image = photo  # keep a reference to avoid garbage collection
                thumb_label.pack(pady=5)
            else:
                thumb_label = tk.Label(self.right_frame, image=photo, bg='black')
                thumb_label.image = photo  # keep a reference to avoid garbage collection
                thumb_label.pack(pady=5)

    def show_next_image(self):
        if self.image_iter:
            self.current_image = next(self.image_iter)
            image = Image.open(self.current_image)
            image = image.resize((800, 600), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)
            self.root.update()

    def start_slideshow(self):
        self.slideshow_running = True
        self.run_slideshow()

    def run_slideshow(self):
        if self.slideshow_running:
            if self.images_viewed >= len(self.images):
                self.stop_slideshow()
                messagebox.showinfo("Slideshow", "All photos have been viewed.")
            else:
                self.show_next_image()
                self.images_viewed += 1
                try:
                    interval = int(self.interval_entry.get()) * 1000
                except ValueError:
                    interval = 2000  # Default to 2 seconds if invalid input
                self.root.after(interval, self.run_slideshow)

    def stop_slideshow(self):
        self.slideshow_running = False

if __name__ == "__main__":
    root = tk.Tk()
    viewer = CyberImageViewer(root)
    root.mainloop()
