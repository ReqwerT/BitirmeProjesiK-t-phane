import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button
from moviepy.editor import VideoFileClip

# Video dosyasını yüklemek için video capture nesnesini başlat
def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)

# Hareket tespiti ve video özetleme
def summarize_video(video_path, output_path):
    video_capture = initialize_video_capture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    back_sub = cv2.createBackgroundSubtractorMOG2(history=700, varThreshold=10, detectShadows=True)

    frame_count = 0
    sampling_rate = 2  # Her 2 karede bir işle

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % sampling_rate != 0:
            continue

        fg_mask = back_sub.apply(frame)
        _, thresh = cv2.threshold(fg_mask, 15, 255, cv2.THRESH_BINARY)
        movement_ratio = np.sum(thresh) / (width * height)

        if movement_ratio > 0.002:  # Daha düşük bir hareket algılama eşiği
            out.write(frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or cv2.getWindowProperty('Video Özeti', cv2.WND_PROP_VISIBLE) < 1:
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()

# Dosya seçici aç ve video özetleme işlemini başlat
def select_video_and_summarize():
    video_path = filedialog.askopenfilename(title="Video Seç", filetypes=[("Video Dosyaları", "*.mp4;*.avi;*.mov")])
    if video_path:
        output_path = filedialog.asksaveasfilename(title="Özet Videoyu Kaydet", defaultextension=".mp4", filetypes=[("MP4 Dosyası", "*.mp4")])
        if output_path:
            summarize_video(video_path, output_path)
            clip = VideoFileClip(output_path)
            clip.preview()  # Özetlenen videoyu oynat

# Ana GUI fonksiyonu
def main():
    root = tk.Tk()
    root.title("Video Özeti Oluşturma")
    root.geometry("300x150")

    label = Label(root, text="Bir video dosyası seçin:")
    label.pack(pady=10)

    select_button = Button(root, text="Video Seç", command=select_video_and_summarize)
    select_button.pack(pady=10)

    exit_button = Button(root, text="Çıkış", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

# Ana fonksiyon
if __name__ == "__main__":
    main()
