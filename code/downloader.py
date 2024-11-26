import yt_dlp


def get_available_formats(url):
    with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return [{'format_id': f['format_id'],
                 'resolution': f.get('resolution', 'audio'),
                 'ext': f['ext']}
                for f in info.get('formats', []) if f.get('acodec') != 'none'
                or f.get('vcodec') != 'none']


def download_video(url, format_id, save_path):
    ydl_opts = {
        'format': format_id,
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info['title'], info['ext']


progress_status = {"percent": 0}


def progress_hook(d):
    if d['status'] == 'downloading':
        progress_status['percent'] = d['_percent_str'].strip()
    elif d['status'] == 'finished':
        progress_status['percent'] = 100
