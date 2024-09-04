import os
import cv2
import numpy as np

# Задаем классы и соответствующие им индексы
class_names = [
    'big_red_circle', 'blue_border', 'center',
    'red_border', 'red_circle', 'vorota',
    'Player1', 'Player2', 'Referee'
]


def determine_tactics_and_draw(txt_folder, img_folder, output_folder, frame_rate):
    # Создаем папку для выходных изображений, если она не существует
    os.makedirs(output_folder, exist_ok=True)

    # Получаем список всех .txt файлов в указанной папке
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    # Словарь для хранения предыдущих координат игроков
    previous_positions = {}

    for txt_file in txt_files:
        # Определяем путь к .txt файлу и соответствующему изображению .jpg
        txt_file_path = os.path.join(txt_folder, txt_file)
        img_file_name = txt_file.replace('.txt', '.jpg')
        img_file_path = os.path.join(img_folder, img_file_name)

        # Проверяем, существует ли изображение
        if not os.path.exists(img_file_path):
            print(f"Изображение {img_file_name} не найдено. Пропускаем файл {txt_file}.")
            continue

        # Загружаем изображение
        image = cv2.imread(img_file_path)

        # Проверяем, успешно ли загружено изображение
        if image is None:
            print(f"Ошибка при загрузке изображения {img_file_name}. Пропускаем файл {txt_file}.")
            continue

        # Открываем файл .txt и читаем аннотации с использованием кодировки utf-8
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()



        # Переменные для хранения скорости игроков
        speeds = {}
        all_speeds = [1]
        # Счетчики игроков
        players_team1 = 0  # Количество игроков команды 1 (классы 6 и 7)
        players_team2 = 0  # Количество игроков команды 2 (классы 8 и 9)
        goals_exist = False  # Флаг для определения наличия ворот
        center_exist = False
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue  # Пропускаем строки с недостаточным количеством данных

            cls = int(parts[0])  # Класс объекта
            if cls == 6 or cls == 7:
                x_center = float(parts[1])  # Центр X (нормализованный)
                y_center = float(parts[2])  # Центр Y (нормализованный)
                img_height, img_width, _ = image.shape  # Получаем размеры изображени
                # Преобразуем нормализованные координаты в пиксели
                x_center_pixel = int(x_center * img_width)
                y_center_pixel = int(y_center * img_height)
                # Используем класс для создания уникального ключа для каждого игрока
                player_id = f"Player{cls}"

                # Если это первый кадр для игрока, инициализируем его позицию
                if player_id not in previous_positions:
                    previous_positions[player_id] = (x_center_pixel, y_center_pixel)
                    speeds[player_id] = 0.0  # Начальная скорость
                    continue

                # Вычисляем расстояние перемещения
                prev_x, prev_y = previous_positions[player_id]
                distance = np.sqrt((x_center_pixel - prev_x) ** 2 + (y_center_pixel - prev_y) ** 2)

                # Вычисляем скорость (в пикселях в секунду)
                speed = distance * frame_rate  # Скорость = расстояние * частота кадров

                # Обновляем позиции и скорость
                previous_positions[player_id] = (x_center_pixel, y_center_pixel)
                speeds[player_id] = speed
                all_speeds.append(speed/100)
                # Записываем текущую скорость на изображение
                text_position = (int(x_center_pixel - 20) , int(y_center_pixel - 20))  # Положение текста над игроком
                cv2.putText(image, f"Speed: {speed/100:.1f} px/s", text_position,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 1, 1), 1)



            # Проверяем наличие ворот
            if cls == 5:
                goals_exist = True
            if cls == 2:
                center_exist = True

            # Подсчет игроков
            if cls == 6:  # Player1
                players_team1 += 1
            elif cls == 7:  # Player2
                players_team2 += 1

        # Определяем тактики на основе количества игроков
        tactic_team1 = "Gates not found"
        tactic_team2 = "Gates not found"

        if center_exist:
            if players_team1 >= 3:
                tactic_team1 = "Team 1: Active Center"
            if players_team2 >= 3:
                tactic_team2 = "Team 2: Active Center"

        elif goals_exist:
            # Тактика для команды 1
            if players_team1 >= 6:
                tactic_team1 = "Team 1: Defend 0-6"
            elif players_team1 == 3:
                tactic_team1 = "Team 1: 3-2 active attack"
            else:
                tactic_team1 = f"Team 1 players: {players_team1}"

            # Тактика для команды 2
            if players_team2 >= 6:
                tactic_team2 = "Team 2: Defend 0-6"
            elif players_team2 == 3:
                tactic_team2 = "Team 2: 3-2 active attack"
            else:
                tactic_team2 = f"Team 2 players: {players_team2}"

        # Записываем результаты на изображение
        text_position_team1 = (900, 30)  # Положение текста для команды 1
        text_position_team2 = (900, 70)  # Положение текста для команды 2

        # Отрисовка текста для команды 1
        cv2.putText(image, tactic_team1, text_position_team1,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Отрисовка текста для команды 2
        cv2.putText(image, tactic_team2, text_position_team2,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        total_speed = sum(all_speeds)
        speed_color = (0, 255, 30)
        average_speed = total_speed / len(all_speeds)
        if average_speed < 50:
            cv2.putText(image, "Slow game tempo", (900, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, speed_color, 2)
        elif 50 <= average_speed < 60:
            cv2.putText(image, "Medium Slow game tempo", (900, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, speed_color, 2)
        elif 60 <= average_speed <= 95:
            cv2.putText(image, "Middle game tempo", (900, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, speed_color, 2)
        elif average_speed > 95:
            cv2.putText(image, "High game tempo", (900, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, speed_color, 2)
        # Сохраняем аннотированное изображение
        output_file_path = os.path.join(output_folder, img_file_name)

        cv2.imwrite(output_file_path, image)


    print(f"Тактики и аннотации сохранены в папке: {output_folder}")


# # Пример использования функции
# img_folder_path = 'labelsAndImages/test2_annotated_frames_merged'  # Замените на путь к вашей папке с .jpg файлами
# txt_folder_path = 'labelsAndImages/labelsMerged'  # Замените на путь к вашей папке с .txt файлами
# output_folder_path = 'tactics_results'  # Замените на путь к выходному файлу
# determine_tactics_and_draw(txt_folder_path, img_folder_path, output_folder_path, 30)



