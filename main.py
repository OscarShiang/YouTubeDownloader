import sys
import os
import youtube_dl
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from layout import Ui_Form

class YDLRunnable(QRunnable):
    def __init__(self, url, dest, dtype, progress_bar, done_signal):
        QRunnable.__init__(self)

        self.url = url
        self.dest = dest
        self.dialog = progress_bar
        self.signal = done_signal

        opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
            'outtmpl': os.path.join(dest, '%(title)s.%(ext)s'),
            'progress_hooks': [self.check_progress],
            'merge_output_format': 'mp4',
        }
        if dtype == 'audio':
            opts['format'] = 'bestaudio[ext=m4a]'
            opts['merge_output_format'] = 'm4a'

            self.remain_files = 1
        else:
            self.remain_files = 2
        self.ydl = youtube_dl.YoutubeDL(opts)
        self.dtype = opts['merge_output_format']

    def check_progress(self, data):
        if self.dialog.wasCanceled():
            raise KeyboardInterrupt
            return

        if data['status'] == 'error':
            self.signal.emit(1, 'Something went wrong')
            return
        elif data['status'] == 'finished':
            print('%s has been downloaded' % data['filename'])

            self.remain_files -= 1
            if self.remain_files == 0:
                self.signal.emit(0,
                    '%s has been downloaded' % data['filename'])
            return

        downloaded = data.get('downloaded_bytes')
        total = data.get('total_bytes')
        if not total:
            total = data.get('total_bytes_estimate')

        percentage = downloaded * 100 / total
        QMetaObject.invokeMethod(self.dialog, "setValue",
            Qt.ConnectionType.QueuedConnection, Q_ARG(int, int(percentage)))

        eta = data.get('eta', 0)
        seconds = eta % 60
        minutes = eta // 60

        if minutes > 0:
            QMetaObject.invokeMethod(self.dialog, "setLabelText",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, '%.1f%% downloaded  %d minutes left'
                    % (percentage, minutes)))
        else:
            QMetaObject.invokeMethod(self.dialog, "setLabelText",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, '%.1f%% downloaded  %d seconds left'
                    % (percentage, seconds)))

    def run(self):
        try:
            info = self.ydl.extract_info(self.url, download=False)
            if os.path.exists(os.path.join(
                    self.dest, f'{info["title"]}.{self.dtype}')):
                QMetaObject.invokeMethod(self.dialog, "reset",
                    Qt.ConnectionType.QueuedConnection)
                self.signal.emit(0, 'The file has been already downloaded')
            else:
                self.ydl.extract_info(self.url, download=True)
                
        except KeyboardInterrupt:
            print('The operation was canceled')
            QMetaObject.invokeMethod(self.dialog, "reset",
                Qt.ConnectionType.QueuedConnection)
            self.signal.emit(1, 'The operation was canceled')
        except Exception as e:
            print('Something went wrong')
            QMetaObject.invokeMethod(self.dialog, "reset",
                Qt.ConnectionType.QueuedConnection)
            self.signal.emit(1, f'Something went wrong: {e}')


class LayoutWindow(QMainWindow):
    done_signal = pyqtSignal(int, str, name='done signal')

    def __init__(self):
        super(LayoutWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.quitButton.clicked.connect(self.close)
        self.ui.pasteButton.clicked.connect(self.copy_from_clipboard)
        self.ui.browseButton.clicked.connect(self.browse_directory)
        self.ui.downloadButton.clicked.connect(self.begin_downloading)

        self.done_signal.connect(self.finalize)

    def copy_from_clipboard(self):
        content = QApplication.clipboard().text()
        self.ui.urlEdit.setText(content)

    def browse_directory(self):
        dest = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.destEdit.setText(dest)

    def begin_downloading(self):
        url = self.ui.urlEdit.text()
        dest = self.ui.destEdit.text()

        if url == '' or dest == '':
            QMessageBox.warning(self, 'Warning',
                'URL and Destination should not be empty')
            print('URL and Destination should not be empty')
            return

        dtype = ''
        if self.ui.audioRadio.isChecked():
            dtype = 'audio'
        else:
            dtype = 'video'

        self.progress_bar = QProgressDialog(
            parent=self, labelText="Downloading ...")
        self.progress_bar.setCancelButton(None)
        self.progress_bar.show()

        try:
            self.loading = YDLRunnable(url, dest,
                dtype, self.progress_bar, self.done_signal)
            QThreadPool.globalInstance().start(self.loading)
        except:
            QMessageBox.warning(self, 'Warning', 'Something went wrong')

    def finalize(self, status, message):
        if status == 0:
            QMessageBox.information(self, 'Information', message)
        else:
            QMessageBox.warning(self, 'Warning', message)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = LayoutWindow()
    window.show()

    sys.exit(app.exec())
