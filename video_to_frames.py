import cv2
import os

def video_to_frames(video_path):
    # Путь к видеофайлу

    # Создаем папку для сохранения кадров
    output_folder = video_path + 'frames'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Загружаем видео
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    save_every_n_frames = 10  # Сохраняем каждый 10-й кадр

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % save_every_n_frames == 0:
            frame_filename = os.path.join(output_folder, f'frame_{frame_count}.jpg')
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()



video_to_frames(video_path = 'pixellot_prime___ice_hockey (1080p).mp4')
