import os
import sys
from yt_dlp import YoutubeDL


def download_youtube(video_url, mode="1", output_path="."):
    """Скачивает YouTube видео в зависимости от выбранного режима."""

    if mode in ("1", "2"):
        output_path = "./video"
    elif mode == "3":
        output_path = "./music"

    # ОПРЕДЕЛЯЕМ ПУТЬ К FFmpeg ВНУТРИ EXE
    # Если программа запущена как .exe, sys._MEIPASS указывает на временную папку сборки
    if getattr(sys, 'frozen', False):
        ffmpeg_dir = sys._MEIPASS
    else:
        ffmpeg_dir = "."  # Если запускаем просто как .py скрипт

    ydl_opts = {
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "ffmpeg_location": ffmpeg_dir,  # Указываем правильный путь
    }

    if mode == "1":
        print("🚀 Выбрано: Максимальное качество")
        ydl_opts["format"] = "bestvideo+bestaudio/best"
        ydl_opts["merge_output_format"] = "mp4"
    elif mode == "2":
        print("🎬 Выбрано: Качество до 720p (MP4)")
        # Ищет раздельное видео до 720p + лучшее аудио. 
        # Если такого нет, берет лучшее цельное видео/аудио до 720p.
        ydl_opts["format"] = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        ydl_opts["merge_output_format"] = "mp4"
    elif mode == "3":
        print("🎵 Выбрано: Только аудио (MP3)")
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ]
    else:
        print("❌ Неверный режим. Скачиваем в максимальном качестве.")
        ydl_opts["format"] = "bestvideo+bestaudio/best"
        ydl_opts["merge_output_format"] = "mp4"

    try:
        print("⏳ Подключение...")
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            print(f"📦 Найдено: {info_dict.get('title', 'Без названия')}")
            ydl.download([video_url]) 
            print(f"\n✅ Успешно сохранено в папочку: {output_path}\n")
    except Exception as e:
        print(f"❌ Ошибка: {e}\n")


if __name__ == "__main__":
    print("=== YouTube Downloader запущен ===")
    print("Для выхода из программы введите 'exit' или просто нажмите Enter без ссылки.")
    
    while True:
        url = input("Введите ссылку на YouTube: ").strip()

        if not url or url.lower() in ('exit', 'выход', 'q'):
            print("Выход из программы. Пока!")
            break

        print("\nВыберите режим скачивания:")
        print("1 — Максимальное качество")
        print("2 — Качество 720p")
        print("3 — Только аудио (MP3)")
        choice = input("Введите цифру (1, 2 или 3): ").strip()

        download_youtube(url, mode=choice)
