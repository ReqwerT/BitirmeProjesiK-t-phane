import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button

# Video dosyasını yüklemek için video capture nesnesini başlat
def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)

# Isı haritasını güncellemek için fonksiyon
def update_heatmap(heatmap, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    heatmap += gray

# Isı haritasını görselleştirmek için fonksiyon
def display_heatmap(heatmap):
    heatmap_normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap_colored = cv2.applyColorMap(heatmap_normalized.astype(np.uint8), cv2.COLORMAP_JET)
    cv2.imshow('Heatmap', heatmap_colored)

# Kaynakları serbest bırak
def release_resources(video_capture):
    video_capture.release()
    cv2.destroyAllWindows()

# Video üzerinde ısı haritası oluşturma
def run_heatmap_generation(video_path):
    video_capture = initialize_video_capture(video_path)
    ret, frame = video_capture.read()
    if not ret:
        print("Video okunamadı!")
        return
    
    # Isı haritası için başlangıç matrisi
    heatmap = np.zeros_like(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), dtype=np.float32)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        update_heatmap(heatmap, frame)
        display_heatmap(heatmap)
        
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or cv2.getWindowProperty('Heatmap', cv2.WND_PROP_VISIBLE) < 1:
            break

    release_resources(video_capture)

# Dosya seçici aç ve ısı haritası oluşturma işlemini başlat
def select_video_and_run_heatmap():
    video_path = filedialog.askopenfilename(title="Video Seç", filetypes=[("Video Dosyaları", "*.mp4;*.avi;*.mov")])
    if video_path:
        run_heatmap_generation(video_path)

# Ana GUI fonksiyonu
def main():
    root = tk.Tk()
    root.title("Isı Haritası Oluşturma")
    root.geometry("300x150")

    label = Label(root, text="Bir video dosyası seçin:")
    label.pack(pady=10)

    select_button = Button(root, text="Video Seç", command=select_video_and_run_heatmap)
    select_button.pack(pady=10)

    exit_button = Button(root, text="Çıkış", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

# Ana fonksiyon
if __name__ == "__main__":
    main()
