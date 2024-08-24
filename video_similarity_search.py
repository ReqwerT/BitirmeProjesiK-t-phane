import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, Label, Button
import winsound
import traceback

# Video dosyasını yüklemek için video capture nesnesini başlat
def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)

# Şablon (template) seçimi ve video üzerinde benzerlik araması
def find_similarity_in_video(video_path, template_paths, output_dir):
    video_capture = initialize_video_capture(video_path)
    templates = [cv2.imread(template_path) for template_path in template_paths]

    # Her bir şablonun yüklendiğinden emin olun
    for template_path, template in zip(template_paths, templates):
        if template is None:
            print(f"Şablon dosyası açılamadı: {template_path}")
            return

    # Klasörün var olup olmadığını kontrol et, yoksa oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    similarity_found = [False] * len(templates)
    frame_counter = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_counter += 1

        for idx, template in enumerate(templates):
            template_height, template_width = template.shape[:2]
            result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > 0.6:  # Benzerlik eşiğini düşürdük
                top_left = max_loc
                bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(frame, f"Benzerlik {idx+1}: {max_val:.2f}", (10, 30 + 40 * idx), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                print(f"Şablon {idx+1} için benzerlik bulundu! Skor: {max_val:.2f}")
                
                # Benzerlik bulunduğunda kareyi kaydet
                if not similarity_found[idx]:  # İlk kez benzerlik bulunursa sesli bildirim yap
                    winsound.Beep(1000 + 200 * idx, 200)
                    similarity_found[idx] = True

                # Her benzerlik için benzersiz bir dosya adı oluştur
                save_path = os.path.join(output_dir, f"match_{idx+1}_frame_{frame_counter}.png")
                
                try:
                    # Kaydetme işlemi başarılı mı kontrol et
                    if cv2.imwrite(save_path, frame):
                        print(f"Kare kaydedildi: {save_path}")
                    else:
                        print(f"Kare kaydedilemedi: {save_path}. Dosya yazma işlemi başarısız.")
                except Exception as e:
                    print(f"Kare kaydedilemedi: {save_path}. Hata: {str(e)}")
                    traceback.print_exc()
        
        cv2.imshow('Benzerlik Araması', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or cv2.getWindowProperty('Benzerlik Araması', cv2.WND_PROP_VISIBLE) < 1:
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Dosya seçici aç ve benzerlik araması işlemini başlat
def select_video_and_find_similarity():
    video_path = filedialog.askopenfilename(title="Video Seç", filetypes=[("Video Dosyaları", "*.mp4;*.avi;*.mov")])
    if video_path:
        template_paths = filedialog.askopenfilenames(title="Şablon Resimlerini Seç", filetypes=[("Resim Dosyaları", "*.png;*.jpg;*.jpeg")])
        if template_paths:
            output_dir = filedialog.askdirectory(title="Kayıt Klasörünü Seç")
            if output_dir:
                find_similarity_in_video(video_path, template_paths, output_dir)

# Ana GUI fonksiyonu
def main():
    root = tk.Tk()
    root.title("Video Benzerlik Araması")
    root.geometry("300x150")

    label = Label(root, text="Bir video dosyası ve şablonları seçin:")
    label.pack(pady=10)

    select_button = Button(root, text="Video ve Şablonları Seç", command=select_video_and_find_similarity)
    select_button.pack(pady=10)

    exit_button = Button(root, text="Çıkış", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

# Ana fonksiyon
if __name__ == "__main__":
    main()
