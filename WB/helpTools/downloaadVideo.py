# import requests
# import os

# def download_file(url, name):
#     headers = {}
#     existing_file_size = 0

#     if os.path.exists(name):
#         existing_file_size = os.path.getsize(name)
#         headers['Range'] = f'bytes={existing_file_size}-'

#     print(f"Starting/Resuming download from: {existing_file_size} bytes")
    
#     while True:
#         try:
#             response = requests.get(url, headers=headers, stream=True, timeout=10)
#             total_size = int(response.headers.get('content-length', 0)) + existing_file_size

#             with open(name, 'ab') as f: # Ensure the file is opened in append+binary mode
#                 if 'content-range' in response.headers:
#                     # This means 'Range' request was successful
#                     print("Resuming download at byte:", existing_file_size)
#                 else:
#                     # This means the server ignored the 'Range' header and is sending from the beginning
#                     existing_file_size = 0 # Reset to start over
#                     f.seek(existing_file_size)

#                 for chunk in response.iter_content(chunk_size=8192):
#                     if chunk: # filter out keep-alive new chunks
#                         f.write(chunk)
#                         existing_file_size += len(chunk)
#                         done = int(50 * existing_file_size / total_size)
#                         print(f"\r[{'=' * done}{' ' * (50-done)}] {existing_file_size} / {total_size} bytes", end='', flush=True)
#             if existing_file_size >= total_size:
#                 break # Exit the loop if the download is complete
#         except requests.exceptions.RequestException as e:
#             print(f"\nError occurred: {e}, retrying...\n")
#             headers['Range'] = f'bytes={existing_file_size}-' # Set range header to resume download

#     print("\nDownload completed.")

# url = 'https://edge-msk-3.kinescopecdn.net/1f0a5d3a-c69a-403c-9095-600ae39f68cb/videos/ad4de264-8904-4374-b958-6c7eb77eba6d/assets/84c0b21f-1f8a-430e-b25d-03f3449dd724/0/898780979/1080p.mp4'
# name = "F:\\Downloads\\14.mp4"

# # Start or resume download
# download_file(url, name)

import subprocess
import os

# Пути к файлам
n = str(14)
video_file_path = rf"F:\Downloads\dwhelper\5.2.1.mp4" # Путь к вашему видеофайлу (без аудио)
audio_file_path = rf"F:\Downloads\dwhelper\5.2.mp4" # Путь к вашему аудиофайлу
output_file_path = rf"F:\Downloads\dwhelper\5.2.compl.mp4" # Путь к файлу результата

# Команда для слияния видео и аудио
command = [
    r"C:\Program Files\ffmpeg-N-115233-g8670615743-win64-gpl\bin\ffmpeg.exe",  # Замените C:\\path\\to\\ffmpeg\\bin\\ffmpeg на ваш реальный путь к ffmpeg
    '-i', video_file_path,  # Исходное видео
    '-i', audio_file_path,  # Исходная аудиодорожка
    '-c:v', 'copy',  # Копирование видеодорожки без перекодирования
    '-c:a', 'copy',  # Копирование аудиодорожки без перекодирования
    '-shortest',  # Опция позволяет обрезать выходной файл до длины самой короткой дорожки
    output_file_path  # Файл вывода
]

# Запуск команды с помощью subprocess
process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Проверка статуса завершения процесса
if process.returncode == 0:
    print('Видео и аудио успешно соединены!')
    os.remove(video_file_path)
    os.remove(audio_file_path)
else:
    print('Произошла ошибка при слиянии видео и аудио.')
    print(process.stderr.decode())  # Вывод ошибки (если есть) для диагностики