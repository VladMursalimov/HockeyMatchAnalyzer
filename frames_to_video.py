import cv2
import os
import re


def frames_to_video(image_folder, video_name):
    # Путь к папке с изображениями
    video_name = 'analyzed_' + video_name
    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else 0

    # Получаем список всех файлов с расширением .jpg в папке
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]

    # Сортируем файлы по числовому значению, извлеченному из имени
    images.sort(key=extract_number)

    # Путь к первому изображению, чтобы определить размеры
    first_image_path = os.path.join(image_folder, images[0])

    # Определяем размеры видео на основе первого изображения
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Создаем объект VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Кодек для MP4
    video = cv2.VideoWriter(video_name, fourcc, 30, (width, height))

    # Добавляем каждое изображение в видео
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)  # Добавляем кадр в видео

    # Освобождаем ресурсы
    video.release()
    cv2.destroyAllWindows()

    print(f'Видео сохранено как {video_name}')


# frames_to_video('tactics_results', 'test2_merged_tactic.mp4')