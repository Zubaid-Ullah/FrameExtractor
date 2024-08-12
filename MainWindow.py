import PyQt5
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QFileDialog,
                             QMessageBox)
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.fx.audio_fadein import audio_fadein
from PyQt5 import uic
import os, threading, subprocess
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PIL import Image
class Worker(QObject):
    finished = pyqtSignal()
    update_progress = pyqtSignal(int)
    def __init__(self, video_path, output_folder, interval, text_editor, pgbar, total_frames):
        super(Worker, self).__init__()
        self.video_path = video_path
        self.output_folder = output_folder
        self.interval = interval
        self.text_editor = text_editor
        self.progress_bar = pgbar
        self.total_frames = total_frames

    def run(self):
        self.extract_pictures()
        self.finished.emit()

    def extract_pictures(self):
        # Load the video clip using MoviePy
        clip = VideoFileClip(self.video_path)
        # Iterate through frames at the specified interval
        for i, frame in enumerate(clip.iter_frames(fps=clip.fps, dtype='uint8')):
            if i % self.interval == 0:  # Extract every `interval`th frame
                frame_path = os.path.join(self.output_folder, f"frame_{i + 1:04d}.png")
                Image.fromarray(frame).save(frame_path)
                self.text_editor.append(f"Extracted frame {i + 1} to {frame_path}")
                # Emit the progress signal
                self.update_progress.emit(i + 1)
                QApplication.processEvents()
        clip.close()  # Close the video clip
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        # Load the UI file
        uic.loadUi('PicExtractor.ui', self)
        self.show()
        self.setWindowTitle("Frame Extractor")
        self.findChild(PyQt5.QtWidgets.QPushButton, "SelectVideoBtn").clicked.connect(self.SelectVideo)
        self.findChild(PyQt5.QtWidgets.QPushButton, "OutputFolder").clicked.connect(self.SelectFolder)
        self.findChild(PyQt5.QtWidgets.QPushButton, "GoBtn").clicked.connect(self.Go)
        self.text_editor = self.findChild(PyQt5.QtWidgets.QTextEdit, "textEdit_2")
        self.findChild(PyQt5.QtWidgets.QPushButton, "Quit").clicked.connect(self.closeEvent)
        self.pgBar = self.findChild(PyQt5.QtWidgets.QProgressBar, "progressBar")
        try:
            subprocess.check_output(["/usr/local/bin/ffprobe", "--help"])
        except FileNotFoundError:
            print("Please install ffprobe before running this script.")
            exit()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTextEditor)
        self.timer.start(100)  # Adjust the interval (in milliseconds) based on your preference
        self.total_frames = 0  # Initialize total_frames attribute
    def updateTextEditor(self):
        QApplication.processEvents()
    def closeEvent(self, event):
        # Override the closeEvent method to prompt the user before closing
        reply = QMessageBox.question(
            self,
            'Confirmation',
            'Are you sure you want to quit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # User confirmed, close the main window
            event.accept()
        else:
            # User chose not to close the main window
            event.ignore()
    def SelectFolder(self):
        self.directory = QFileDialog.getExistingDirectory(None, "Folder")
        print(self.directory)
        self.findChild(PyQt5.QtWidgets.QTextEdit, "textEdit").append(f"Directory: {self.directory}")
    def SelectVideo(self):
        self.file, _ = QFileDialog.getOpenFileNames(None, "Select any video(s)")
        if self.file == []:
            return False
        else:
            self.findChild(PyQt5.QtWidgets.QTextEdit, "textEdit").append(f"File: {self.file[0]}")
    def update_progress_bar(self, value):
        self.pgBar.setValue(value)
        self.pgBar.setMaximum(self.total_frames)
        self.pgBar.setFormat(f"          {value}/{self.total_frames}")
    def Go(self):
        for i in self.file:
            # Calculate total frames
            clip = VideoFileClip(i)
            self.total_frames = int(clip.duration * clip.fps)
            self.findChild(PyQt5.QtWidgets.QTextEdit, "textEdit").append(f"Total Frames: {self.total_frames}")
            clip.close()
            # Pass total_frames to the Worker
            worker = Worker(i,
                            self.directory,
                            interval=int(self.findChild(PyQt5.QtWidgets.QComboBox, "comboBox").currentText()),
                            text_editor=self.text_editor,
                            pgbar=self.pgBar,
                            total_frames=self.total_frames
                            )
            # Connect the update_progress signal to the update_progress_bar method
            worker.update_progress.connect(self.update_progress_bar)
            thread = threading.Thread(target=worker.run)
            thread.start()