import os
import cv2

# Задаем классы и цвета для отрисовки
class_names = [
    'big_red_circle', 'blue_border', 'center',
    'red_border', 'red_circle', 'vorota',
    'Player1', 'Player2', 'Refferee'
]

colors = {
    0: (0, 0, 255),  # big_red_circle - красный
    1: (255, 0, 0),  # blue_border - синий
    2: (0, 255, 0),  # center - зеленый
    3: (0, 255, 255),  # red_border - желтый
    4: (255, 165, 0),  # red_circle - оранжевый
    5: (255, 255, 255),  # vorota - белый
    6: (0, 255, 127),  # Player1 - лаймовый
    7: (255, 0, 255),  # Player2 - фиолетовый
    8: (255, 255, 0)  # Referee - голубой
}


def draw_bounding_boxes(txt_folder, img_folder, output_folder):
    # Создаем папку для выходных изображений, если она не существует
    os.makedirs(output_folder, exist_ok=True)

    # Получаем список всех .txt файлов в указанной папке
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    for txt_file in txt_files:
        # Определяем путь к .txt файлу и соответствующему изображению .jpg
        txt_file_path = os.path.join(txt_folder, txt_file)
        img_file_name = txt_file.replace('.txt', '.jpg')
        print(img_file_name)
        img_file_path = os.path.join(img_folder, img_file_name)

        # Проверяем, существует ли изображение
        if not os.path.exists(img_file_path):
            print(f"Изображение {img_file_name} не найдено. Пропускаем файл {txt_file}.")
            continue

        # Загружаем изображение
        image = cv2.imread(img_file_path)

        # Открываем файл .txt и читаем аннотации
        with open(txt_file_path, 'r') as f:
            lines = f.readlines()

        # Обрабатываем каждую строку (аннотацию)
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue  # Пропускаем строки с недостаточным количеством данных

            cls = int(parts[0])  # Класс объекта
            x_center = float(parts[1])  # Центр X
            y_center = float(parts[2])  # Центр Y
            width = float(parts[3])  # Ширина
            height = float(parts[4])  # Высота

            # Вычисляем координаты верхнего левого и нижнего правого углов
            img_height, img_width, _ = image.shape
            x1 = int((x_center - width / 2) * img_width)  # Левая координата
            y1 = int((y_center - height / 2) * img_height)  # Верхняя координата
            x2 = int((x_center + width / 2) * img_width)  # Правая координата
            y2 = int((y_center + height / 2) * img_height)  # Нижняя координата

            # Рисуем bounding box
            color = colors.get(cls, (255, 255, 255))  # Белый цвет по умолчанию
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

            # Пишем название класса
            label = class_names[cls]
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Сохраняем аннотированное изображение
        output_file_path = os.path.join(output_folder, img_file_name)
        cv2.imwrite(output_file_path, image)

    print(f"Аннотированные изображения сохранены в папке: {output_folder}")


# # Пример использования функции
# txt_folder_path = 'labelsMerged'  # Замените на путь к вашей папке
# img_folder = 'test2_annotated_frames'
# output_folder = img_folder + '_merged'
#
# draw_bounding_boxes(txt_folder_path, img_folder, output_folder)