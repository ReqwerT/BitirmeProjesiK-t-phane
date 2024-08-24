import cv2
import tkinter as tk
from tkinter import filedialog, Label, Button

# Video dosyasını yüklemek için video capture nesnesini başlat
def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)

# Arka plan çıkarma nesnesini oluştur
def create_background_subtractor():
    return cv2.createBackgroundSubtractorMOG2()

# Her kareyi işleme al
def process_frame(video_capture, back_sub):
    ret, frame = video_capture.read()
    if not ret:
        return None, None
    fg_mask = back_sub.apply(frame)
    return frame, fg_mask

# Kareyi ekranda göster
def display_frame(window_name, frame):
    cv2.imshow(window_name, frame)

# Kaynakları serbest bırak
def release_resources(video_capture):
    video_capture.release()
    cv2.destroyAllWindows()

# Video segmentasyonunu çalıştır
def run_video_segmentation(video_path):
    video_capture = initialize_video_capture(video_path)
    back_sub = create_background_subtractor()

    while True:
        frame, fg_mask = process_frame(video_capture, back_sub)
        if frame is None:
            break
        display_frame('Segmented Frame', fg_mask)
        
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or cv2.getWindowProperty('Segmented Frame', cv2.WND_PROP_VISIBLE) < 1:  # 'q' tuşuna basıldığında veya pencere kapatıldığında döngüyü kır
            break

    release_resources(video_capture)

# Dosya seçici aç ve segmentasyon başlat
def select_video_and_run_segmentation():
    video_path = filedialog.askopenfilename(title="Video Seç", filetypes=[("Video Dosyaları", "*.mp4;*.avi;*.mov")])
    if video_path:
        run_video_segmentation(video_path)

# Ana GUI fonksiyonu
def main():
    root = tk.Tk()
    root.title("Video Segmentasyonu")
    root.geometry("300x150")

    label = Label(root, text="Bir video dosyası seçin:")
    label.pack(pady=10)

    select_button = Button(root, text="Video Seç", command=select_video_and_run_segmentation)
    select_button.pack(pady=10)

    exit_button = Button(root, text="Çıkış", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

# Ana fonksiyon
if __name__ == "__main__":
    main()
