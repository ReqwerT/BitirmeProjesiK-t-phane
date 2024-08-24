import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button

# Video dosyasını yüklemek için video capture nesnesini başlat
def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)

# Kalabalık analizi fonksiyonu
def crowd_analysis(video_path):
    video_capture = initialize_video_capture(video_path)
    
    # İlk kareyi al ve gri tona çevir
    ret, first_frame = video_capture.read()
    if not ret:
        print("Video okunamadı!")
        return
    
    prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(first_frame)
    mask[..., 1] = 255

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Mevcut kareyi gri tona çevir
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Optik akış kullanarak kalabalık hareketini tespit et
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        
        # Akışı polar koordinatlara dönüştür
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        
        # Hareket yönlerini renklendir
        mask[..., 0] = angle * 180 / np.pi / 2
        mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        
        # Görselleştirmek için optik akış görüntüsü oluştur
        rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
        dense_flow = cv2.addWeighted(frame, 1, rgb, 2, 0)

        # Kalabalık yoğunluğu göstergesi olarak ortalama hareketi hesapla
        mean_movement = np.mean(magnitude)
        cv2.putText(dense_flow, f"Kalabalik Yogunlugu: {mean_movement:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Kalabalik Analizi', dense_flow)
        prev_gray = gray

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or cv2.getWindowProperty('Kalabalik Analizi', cv2.WND_PROP_VISIBLE) < 1:
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Dosya seçici aç ve kalabalık analizi işlemini başlat
def select_video_and_analyze_crowd():
    video_path = filedialog.askopenfilename(title="Video Seç", filetypes=[("Video Dosyaları", "*.mp4;*.avi;*.mov")])
    if video_path:
        crowd_analysis(video_path)

# Ana GUI fonksiyonu
def main():
    root = tk.Tk()
    root.title("Kalabalık Analizi")
    root.geometry("300x150")

    label = Label(root, text="Bir video dosyası seçin:")
    label.pack(pady=10)

    select_button = Button(root, text="Video Seç", command=select_video_and_analyze_crowd)
    select_button.pack(pady=10)

    exit_button = Button(root, text="Çıkış", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

# Ana fonksiyon
if __name__ == "__main__":
    main()
