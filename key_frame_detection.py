import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, Label, Button

# Video dosyasını yüklemek için video capture nesnesini başlat
def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)

# Anahtar kareleri tespit etme fonksiyonu
def detect_key_frames(video_path, output_dir, threshold=13):
    video_capture = initialize_video_capture(video_path)
    
    # İlk kareyi al ve gri tona çevir
    ret, prev_frame = video_capture.read()
    if not ret:
        print("Video okunamadı!")
        return
    
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_counter = 0
    key_frame_counter = 0

    key_frames = []

    # Klasörün var olup olmadığını kontrol et, yoksa oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_diff = cv2.absdiff(prev_gray, gray)
        diff_score = np.sum(frame_diff) / (gray.shape[0] * gray.shape[1])

        if diff_score > threshold:
            key_frame_counter += 1
            key_frame_name = f"key_frame_{key_frame_counter}.jpg"
            save_path = os.path.join(output_dir, key_frame_name)
            cv2.imwrite(save_path, frame)
            key_frames.append((frame_counter, save_path))
            print(f"Anahtar kare tespit edildi: {save_path}, Fark Skoru: {diff_score:.2f}")
        
        prev_gray = gray
        frame_counter += 1

        cv2.imshow('Video', frame)
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
            break

    video_capture.release()
    cv2.destroyAllWindows()

    print(f"Toplam {key_frame_counter} anahtar kare tespit edildi.")
    return key_frames

# Dosya seçici aç ve anahtar kare tespiti işlemini başlat
def select_video_and_detect_key_frames():
    video_path = filedialog.askopenfilename(title="Video Seç", filetypes=[("Video Dosyaları", "*.mp4;*.avi;*.mov")])
    if video_path:
        output_dir = filedialog.askdirectory(title="Anahtar Kareleri Kaydetmek İçin Klasör Seç")
        if output_dir:
            detect_key_frames(video_path, output_dir)

# Ana GUI fonksiyonu
def main():
    root = tk.Tk()
    root.title("Anahtar Kare Tespiti")
    root.geometry("300x150")

    label = Label(root, text="Bir video dosyası seçin:")
    label.pack(pady=10)

    select_button = Button(root, text="Video Seç", command=select_video_and_detect_key_frames)
    select_button.pack(pady=10)

    exit_button = Button(root, text="Çıkış", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

# Ana fonksiyon
if __name__ == "__main__":
    main()
