from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.uic import loadUi
from code.downloader import get_available_formats, download_video
from code.db_handler import save_download, init_db


class MainWindow(QMainWindow):
    """Главное окно приложения для загрузки видео."""
    def __init__(self):
        """Инициализирует главное окно и компоненты интерфейса."""
        super(MainWindow, self).__init__()
        loadUi("UI/main_window.ui", self)
        init_db()

        self.selectPathButton.clicked.connect(self.select_save_path)
        self.downloadButton.clicked.connect(self.start_download)
        self.urlInput.textChanged.connect(self.load_formats)
        self.savePath = ""

    def select_save_path(self):
        """Открывает окно для выбора каталога для
         сохранения загруженных файлов."""
        path = QFileDialog.getExistingDirectory(self, "Выберите Каталог"
                                                      " для сохранения")
        if path:
            self.savePath = path
            self.pathLabel.setText(path)

    def load_formats(self):
        """Загружает доступные форматы для указанного URL-адреса видео."""
        url = self.urlInput.text().strip()
        if url:
            try:
                formats = get_available_formats(url)
                self.formatSelector.clear()
                for fmt in formats:
                    self.formatSelector.addItem(
                        f"{fmt['resolution']} - {fmt['ext']}", fmt
                    )
            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     f"Failed to load formats: {e}")

    def start_download(self):
        """Запускает процесс загрузки выбранного видео и формата."""
        url = self.urlInput.text().strip()
        if not url or not self.savePath:
            QMessageBox.warning(
                self, "Warning", "Please provide a URL and select a save path."
            )
            return

        selected_format = self.formatSelector.currentData()
        if not selected_format:
            QMessageBox.warning(self, "Warning", "Please select a format.")
            return

        try:
            title, ext = download_video(
                url, selected_format["format_id"], self.savePath
            )
            save_download(url, title, self.savePath, ext)
            QMessageBox.information(
                self, "Success", f"Downloaded {title} successfully."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Download failed: {e}")
