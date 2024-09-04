from ultralytics import YOLO
import cv2
import os


# Загрузка предобученной модели YOLOv8
def annotation_field(modelpath, video_path, type):
    model = YOLO(modelpath)

    # Загрузка видео
    cap = cv2.VideoCapture(video_path)

    # Директории для сохранения аннотированных кадров и меток
    output_dir = video_path.replace('.mp4', '') + '_annotated_frames_' + type.replace('0', 'players').replace('1',
                                                                                                              'field')
    labels_dir = 'labels_' + video_path.replace('.mp4', '') + type.replace('0', '_players').replace('1', '_field')

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    frame_count = 0

    # Новые названия классов
    class_names = ['big_red_circle', 'blue_border', 'center', 'red_border', 'red_circle', 'vorota']
    # Цвета для классов
    colors = {
        0: (0, 0, 255),  # big_red_circle - красный
        1: (255, 0, 0),  # blue_border - синий
        2: (0, 255, 0),  # center - зеленый
        3: (0, 255, 255),  # red_border - желтый
        4: (255, 165, 0),  # red_circle - оранжевый
        5: (255, 255, 200)  # vorota - белый
    }

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Детекция объектов с помощью YOLOv8
        results = model(frame)

        filtered_boxes = results[0].boxes

        # Отрисовка bounding boxes для всех объектов
        for box in filtered_boxes:
            cls = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Координаты боксов

            # Получаем имя объекта на основе класса
            player_name = class_names[cls] if cls < len(class_names) else f'Unknown Class {cls}'
            color = colors.get(cls, (255, 255, 255))  # Используем белый цвет по умолчанию

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
