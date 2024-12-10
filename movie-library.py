import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import datetime
import pandas as pd
import subprocess

VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.wmv', '.mov', '.flv')

class VideoFileScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video File Scanner")
        self.root.geometry("600x400")
        self.root.configure(bg="darkgrey")

        
        self.directories = []  
        self.video_data = []   
        self.loaded_data = []  

        
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Movie Database", font=("Arial", 16, "bold"), bg="darkgrey", fg="white")
        title_label.pack(pady=10)

        # Buttons
        button1 = ttk.Button(self.root, text="1. Select Movie Location", command=self.add_directory)
        button1.pack(pady=10)

        button2 = ttk.Button(self.root, text="2. Add Additional Location", command=self.add_directory)
        button2.pack(pady=10)

        button3 = ttk.Button(self.root, text="3. Finish & Save to Database", command=self.finish_and_save)
        button3.pack(pady=10)

        button4 = ttk.Button(self.root, text="4. Search Video Files > 700 MB", command=self.search_large_videos)
        button4.pack(pady=10)

        button5 = ttk.Button(self.root, text="5. Show Video Files", command=self.show_video_list)
        button5.pack(pady=10)

        button6 = ttk.Button(self.root, text="6. Load Saved Database", command=self.load_database)
        button6.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="Status: Waiting for input", bg="darkgrey", fg="white", wraplength=500)
        self.status_label.pack(pady=20)

    def add_directory(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.directories.append(folder_selected)
            self.status_label.config(text=f"Added folder: {folder_selected}")
        else:
            self.status_label.config(text="No folder selected.")

    def scan_videos(self):
        self.video_data = [] 
        for directory in self.directories:
            for root_dir, _, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith(VIDEO_EXTENSIONS):
                        file_path = os.path.join(root_dir, file)
                        try:
                            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
                            resolution, duration = self.get_video_info(file_path)
                            date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            self.video_data.append({
                                "Path": file_path,
                                "Movie Name": os.path.splitext(file)[0],
                                "File Name": file,
                                "File Size (MB)": round(file_size, 2),
                                "Resolution": resolution,
                                "Duration": duration,
                                "Date Added": date_added
                            })
                        except Exception as e:
                            print(f"Failed to process {file}: {e}")

    def get_video_info(self, file_path):
        cap = cv2.VideoCapture(file_path)
        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            resolution = f"{width}x{height}"
            frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = round(frames / fps) if fps > 0 else 0
            minutes = duration // 60
            seconds = duration % 60
            cap.release()
            return resolution, f"{minutes}m {seconds}s"
        return "Unknown", "Unknown"

    def finish_and_save(self):
        if not self.directories:
            messagebox.showerror("Error", "No directories selected!")
            return

        self.status_label.config(text="Scanning video files... Please wait.")
        self.scan_videos()

        if not self.video_data:
            messagebox.showinfo("No Videos", "No video files found.")
            return

        df = pd.DataFrame(self.video_data)
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Success", f"Video data saved to {save_path}")

    def search_large_videos(self):
        folder_selected = filedialog.askdirectory()
        if not folder_selected:
            self.status_label.config(text="No directory selected.")
            return

        large_videos = []
        for root_dir, _, files in os.walk(folder_selected):
            for file in files:
                if file.lower().endswith(VIDEO_EXTENSIONS):
                    file_path = os.path.join(root_dir, file)
                    file_size = os.path.getsize(file_path) / (1024 * 1024)
                    if file_size > 700:
                        large_videos.append(f"{file} - {round(file_size, 2)} MB")

        if large_videos:
            messagebox.showinfo("Large Videos Found", "\n".join(large_videos))
        else:
            messagebox.showinfo("No Large Videos", "No videos larger than 700MB found.")

    def show_video_list(self):
        if not self.video_data and not self.loaded_data:
            messagebox.showinfo("No Data", "No video files to display. Please scan folders first.")
            return

        video_list = self.video_data if self.video_data else self.loaded_data

        window = tk.Toplevel(self.root)
        window.title("Video Files List")
        window.geometry("1000x1000")

        # scrollable canvas
        canvas = tk.Canvas(window)
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # scrollable frame
        for i, video in enumerate(video_list):
            info = f"{i+1}. {video['File Name']} | {video['File Size (MB)']} MB | {video['Resolution']} | {video['Duration']}"
            label = ttk.Label(scrollable_frame, text=info, anchor="w")
            label.pack(fill="x", pady=2)

            # Play button
            play_button = ttk.Button(scrollable_frame, text="Play", command=lambda path=video['Path']: self.play_video(path))
            play_button.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_database(self):
        # Load from Excel file
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
            self.loaded_data = df.to_dict(orient="records")  # Convert to list of dictionaries
            messagebox.showinfo("Success", "Database loaded successfully.")
            self.status_label.config(text=f"Loaded database from {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load database: {e}")

    def play_video(self, path):
        try:
            if os.name == "nt":  # Windows
                os.startfile(path)
            else:  # Linux/Mac
                subprocess.call(["open", path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play video: {e}")

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoFileScannerApp(root)
    root.mainloop()