import os

def merge_txt_files(folder1, folder2, output_folder):
    # Создаем директорию для выходных данных, если она не существует
    os.makedirs(output_folder, exist_ok=True)

    # Получаем список файлов в каждой папке
    files_folder1 = [f for f in os.listdir(folder1) if f.endswith('.txt')]
    files_folder2 = [f for f in os.listdir(folder2) if f.endswith('.txt')]

    # Объединяем файлы из каждой папки
    for filename in files_folder1:
        file_path1 = os.path.join(folder1, filename)
        file_path2 = os.path.join(folder2, filename)

        # Открываем файл из первой папки
        with open(file_path1, 'r') as f1:
            content1 = f1.read()

        # Проверяем наличие файла во второй папке
        if filename in files_folder2:
            # Если файл существует во второй папке, читаем его содержимое
            with open(file_path2, 'r') as f2:
                content2 = f2.read()
            # Объединяем содержимое
            merged_content = content1 + "\n" + content2
        else:
            # Если файла нет во второй папке, просто используем содержимое первого файла
            merged_content = content1

        # Сохраняем объединенное содержимое в выходной папке
        with open(os.path.join(output_folder, filename), 'w') as output_file:
            output_file.write(merged_content)

    # Обработка файлов, которые есть только во второй папке
    for filename in files_folder2:
        if filename not in files_folder1:
            file_path2 = os.path.join(folder2, filename)
            with open(file_path2, 'r') as f2:
                content2 = f2.read()
            # Сохраняем содержимое во выходной папке
            with open(os.path.join(output_folder, filename), 'w') as output_file:
                output_file.write(content2)

    print(f"Файлы успешно объединены в папку: {output_folder}")

# # Пример использования функции
# folder1_path = 'labelsField/labels'  # Замените на путь к первой папке
# folder2_path = 'labelsPlayer/labels'  # Замените на путь ко второй папке
# output_folder_path = 'labelsMerged'  # Замените на путь к выходной папке
#
# merge_txt_files(folder1_path, folder2_path, output_folder_path)