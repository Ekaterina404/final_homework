import yt_dlp


def get_available_formats(url):
    """Возвращает доступные форматы для данного URL.

        Args:
            url (str): URL.

        Returns:
            List[Dict[str, str]]: список форматов, каждый в виде словаря.
        """
    with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return [{'format_id': f['format_id'],
                 'resolution': f.get('resolution', 'audio'),
                 'ext': f['ext']}
                for f in info.get('formats', []) if f.get('acodec') != 'none'
                or f.get('vcodec') != 'none']


def download_video(url: str, format_id: int, save_path: str) -> tuple[str, str]:
    """Загружает видео в указанном формате.

        Args:
            url (str): URL.
            format_id (int): Формат ID of the selected format.
            save_path (str): Каталог для сохранения загруженного файла.

        Returns:
            tuple[str, str]: название видео и расширение файла.
        """
    ydl_opts = {
        'format': format_id,
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info['title'], info['ext']


progress_status = {"percent": 0}


def progress_hook(d: dict[str, str]) -> None:
    """Обновляет статус прогресса загрузки.

        Args:
            d (dict[str, str]): Данные о текущем состоянии загрузки.
                Полезные ключи:
                - 'status': 'downloading' или 'finished'.
                - '_percent_str': Процент завершения (только при 'downloading').
        """
    if d['status'] == 'downloading':
        progress_status['percent'] = float(d['_percent_str'].strip('% '))
    elif d['status'] == 'finished':
        progress_status['percent'] = 100
