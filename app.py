import tkinter as tk
from tkinter import filedialog, messagebox
from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    video_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return video_id.group(1) if video_id else None

def download_subtitles():
    url = url_entry.get()
    video_id = get_video_id(url)
    
    if not video_id:
        messagebox.showerror("Error", "Invalid YouTube URL")
        return
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch subtitles: {str(e)}")
        return
    
    file_type = file_type_var.get()
    file_extension = ".srt" if file_type == "SRT" else ".txt"
    
    file_path = filedialog.asksaveasfilename(defaultextension=file_extension,
                                             filetypes=[(f"{file_type} files", f"*{file_extension}")])
    
    if not file_path:
        return
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            if file_type == "SRT":
                write_srt(file, transcript)
            elif file_type == "TXT":
                write_txt(file, transcript)
            else:  # TXT (Formatted)
                write_txt_formatted(file, transcript)
        
        messagebox.showinfo("Success", f"Subtitles saved as {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save subtitles: {str(e)}")

def write_srt(file, transcript):
    for i, line in enumerate(transcript, 1):
        start = line['start']
        end = start + line['duration']
        text = line['text']
        file.write(f"{i}\n")
        file.write(f"{format_time(start)} --> {format_time(end)}\n")
        file.write(f"{text}\n\n")

def write_txt(file, transcript):
    for line in transcript:
        file.write(f"{line['text']}\n")

def write_txt_formatted(file, transcript):
    full_text = " ".join(line['text'] for line in transcript)
    paragraphs = re.split(r'\n{2,}', full_text)
    for paragraph in paragraphs:
        file.write(f"{paragraph.strip()}\n\n")

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# Create the main window
root = tk.Tk()
root.title("YouTube Subtitle Downloader")
root.geometry("400x200")

# URL input
url_label = tk.Label(root, text="YouTube URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# File type selection
file_type_var = tk.StringVar(value="SRT")
file_type_frame = tk.Frame(root)
file_type_frame.pack(pady=5)

srt_radio = tk.Radiobutton(file_type_frame, text="SRT", variable=file_type_var, value="SRT")
srt_radio.pack(side=tk.LEFT)

txt_radio = tk.Radiobutton(file_type_frame, text="TXT", variable=file_type_var, value="TXT")
txt_radio.pack(side=tk.LEFT)

txt_formatted_radio = tk.Radiobutton(file_type_frame, text="TXT (Formatted)", variable=file_type_var, value="TXT_FORMATTED")
txt_formatted_radio.pack(side=tk.LEFT)

# Download button
download_button = tk.Button(root, text="Download Subtitles", command=download_subtitles)
download_button.pack(pady=10)

root.mainloop()