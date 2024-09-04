from ultralytics import YOLO
import cv2
import os


# Загрузка предобученной модели YOLOv8
def annotaion(modelpath, video_path):
    model = YOLO(modelpath)

    # Загрузка видео
    cap = cv2.VideoCapture(video_path)

    # Директории для сохранения аннотированных кадров и меток
    output_dir = video_path.replace('.mp4', '') + '_annotated_frames'
    labels_dir = 'labels'

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Детекция игроков с помощью YOLOv8
        results = model(frame)

        filtered_boxes = results[0].boxes

        # Отрисовка bounding boxes для всех объектов
        for box in filtered_boxes:
            cls = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Координаты боксов

            # Определяем имя объекта на основе класса
            if cls == 2:
                player_name = 'Ref'
            else:
                player_name = f'Player{cls + 1}'
            if cls == 0:
                color = (0, 255, 0)
            elif cls == 1:
                color = (0, 0, 255)
            elif cls == 2:
                color = (255, 0, 0)

            # Рисуем прямоугольник и подпись
            # Параметры для тонких рамок и текста
            box_thickness = 1  # Толщина рамки (уменьшена)
            font_scale = 0.5  # Размер шрифта (уменьшен)
            text_thickness = 1  # Толщина текста (уменьшена)

            # Рисуем прямоугольник и подпись
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, box_thickness)
            cv2.putText(frame, player_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, text_thickness)

        # Сохранение аннотированного кадра
        cv2.imwrite(f'{output_dir}/frame_{frame_count}.jpg', frame)

        # Экспорт аннотаций в формате YOLO
        with open(f'{labels_dir}/frame_{frame_count}.txt', 'w') as f:
            for box in filtered_boxes:
                cls = int(box.cls[0])
                x_center = box.xywh[0][0].item() / frame.shape[1]
                y_center = box.xywh[0][1].item() / frame.shape[0]
                width = box.xywh[0][2].item() / frame.shape[1]
                height = box.xywh[0][3].item() / frame.shape[0]
                label = f"{cls} {x_center} {y_center} {width} {height}\n"
                f.write(label)

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    return output_dir