import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QComboBox, QSpinBox, QDoubleSpinBox, QFileDialog,
                            QTabWidget, QTextEdit, QCheckBox, QProgressBar,
                            QMessageBox, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QLinearGradient, QPainter
from create_test_audio import create_test_audio
from transcribe_audio import transcribe_audio

class StyledButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setFont(QFont('Segoe UI', 10))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)

class StyledComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(35)
        self.setFont(QFont('Segoe UI', 10))
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                padding: 5px;
                background: white;
                color: #212121;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #212121;
                selection-background-color: #BBDEFB;
                selection-color: #212121;
            }
        """)

class StyledSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(35)
        self.setFont(QFont('Segoe UI', 10))
        self.setStyleSheet("""
            QSpinBox {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                padding: 5px;
                background: white;
                color: #212121;
            }
        """)

class StyledDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(35)
        self.setFont(QFont('Segoe UI', 10))
        self.setStyleSheet("""
            QDoubleSpinBox {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                padding: 5px;
                background: white;
                color: #212121;
            }
        """)

class StyledTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont('Segoe UI', 10))
        self.setStyleSheet("""
            QTextEdit {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                padding: 8px;
                background: white;
                color: #212121;
            }
        """)

class StyledLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(35)
        self.setFont(QFont('Segoe UI', 10))
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                padding: 5px;
                background: white;
                color: #212121;
            }
        """)

class AudioWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, task_type, **kwargs):
        super().__init__()
        self.task_type = task_type
        self.kwargs = kwargs

    def run(self):
        try:
            if self.task_type == "tts":
                result = create_test_audio(**self.kwargs)
                self.finished.emit(f"Audio file created successfully: {result}")
            elif self.task_type == "stt":
                result = transcribe_audio(**self.kwargs)
                self.finished.emit(f"Transcription completed: {result}")
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IntelliControl - Text to Speech & Speech Recognition")
        self.setMinimumSize(900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QTabWidget::pane {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                background: white;
            }
            QTabBar::tab {
                background: #E0E0E0;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #2196F3;
                color: white;
            }
            QLabel {
                font-family: 'Segoe UI';
                font-size: 11pt;
                color: #212121;
            }
            QProgressBar {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                text-align: center;
                background-color: #F5F5F5;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 5px;
            }
        """)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create header
        header = QLabel("IntelliControl")
        header.setFont(QFont('Segoe UI', 24, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #1976D2; margin-bottom: 20px;")
        layout.addWidget(header)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Create TTS tab
        tts_tab = QWidget()
        tabs.addTab(tts_tab, "Text to Speech")
        self.setup_tts_tab(tts_tab)
        
        # Create STT tab
        stt_tab = QWidget()
        tabs.addTab(stt_tab, "Speech Recognition")
        self.setup_stt_tab(stt_tab)
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #E0E0E0;
                color: #212121;
                font-family: 'Segoe UI';
            }
        """)
        
        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(10)
        layout.addWidget(self.progress_bar)

    def setup_tts_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Text input
        text_label = QLabel("Enter text:")
        text_label.setStyleSheet("color: #212121; font-weight: bold;")
        self.text_input = StyledTextEdit()
        self.text_input.setMinimumHeight(150)
        self.text_input.setPlaceholderText("Type or paste your text here...")
        layout.addWidget(text_label)
        layout.addWidget(self.text_input)
        
        # Voice selection
        voice_layout = QHBoxLayout()
        voice_label = QLabel("Language:")
        voice_label.setStyleSheet("color: #212121;")
        self.voice_combo = StyledComboBox()
        
        # Use the same language dictionary as in the STT tab
        self.tts_languages = {
            "English (US)": "en-US",
            "English (UK)": "en-GB",
            "Spanish": "es-ES",
            "French": "fr-FR",
            "German": "de-DE",
            "Italian": "it-IT",
            "Portuguese": "pt-PT",
            "Russian": "ru-RU",
            "Japanese": "ja-JP",
            "Korean": "ko-KR",
            "Chinese (Simplified)": "zh-CN",
            "Chinese (Traditional)": "zh-TW",
            "Hindi": "hi-IN",
            "Arabic": "ar-SA",
            "Dutch": "nl-NL",
            "Swedish": "sv-SE",
            "Norwegian": "nb-NO",
            "Danish": "da-DK",
            "Finnish": "fi-FI",
            "Greek": "el-GR",
            "Turkish": "tr-TR",
            "Polish": "pl-PL",
            "Czech": "cs-CZ",
            "Hungarian": "hu-HU",
            "Romanian": "ro-RO",
            "Bulgarian": "bg-BG",
            "Ukrainian": "uk-UA",
            "Vietnamese": "vi-VN",
            "Thai": "th-TH",
            "Indonesian": "id-ID",
            "Telugu": "te-IN",
            "Tamil": "ta-IN",
            "Kannada": "kn-IN",
            "Malayalam": "ml-IN",
            "Bengali": "bn-IN"
        }
        
        # Add languages to combo box
        self.voice_combo.addItems(self.tts_languages.keys())
        
        voice_layout.addWidget(voice_label)
        voice_layout.addWidget(self.voice_combo)
        layout.addLayout(voice_layout)
        
        # Rate control
        rate_layout = QHBoxLayout()
        rate_label = QLabel("Speech Rate (WPM):")
        rate_label.setStyleSheet("color: #212121;")
        self.rate_spin = StyledSpinBox()
        self.rate_spin.setRange(50, 300)
        self.rate_spin.setValue(150)
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(self.rate_spin)
        layout.addLayout(rate_layout)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Volume:")
        volume_label.setStyleSheet("color: #212121;")
        self.volume_spin = StyledDoubleSpinBox()
        self.volume_spin.setRange(0.0, 1.0)
        self.volume_spin.setValue(1.0)
        self.volume_spin.setSingleStep(0.1)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_spin)
        layout.addLayout(volume_layout)
        
        # Output file
        output_layout = QHBoxLayout()
        output_label = QLabel("Output File:")
        output_label.setStyleSheet("color: #212121;")
        self.output_edit = StyledLineEdit()
        self.output_edit.setText("output/speech.mp3")
        self.output_edit.setReadOnly(True)
        browse_button = StyledButton("Browse...")
        browse_button.clicked.connect(self.browse_output_file)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(browse_button)
        layout.addLayout(output_layout)
        
        # Generate button
        generate_button = StyledButton("Generate Audio")
        generate_button.clicked.connect(self.generate_audio)
        layout.addWidget(generate_button)
        
        # Add some spacing
        layout.addStretch()

    def setup_stt_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Input file
        input_layout = QHBoxLayout()
        input_label = QLabel("Input Audio File:")
        input_label.setStyleSheet("color: #212121; font-weight: bold;")
        self.input_edit = StyledLineEdit()
        self.input_edit.setReadOnly(True)
        browse_button = StyledButton("Browse...")
        browse_button.clicked.connect(self.browse_input_file)
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(browse_button)
        layout.addLayout(input_layout)
        
        # Language selection
        language_layout = QHBoxLayout()
        language_label = QLabel("Language:")
        language_label.setStyleSheet("color: #212121;")
        self.language_combo = StyledComboBox()
        
        # Comprehensive list of languages with their codes
        self.languages = {
            "English (US)": "en-US",
            "English (UK)": "en-GB",
            "Spanish": "es-ES",
            "French": "fr-FR",
            "German": "de-DE",
            "Italian": "it-IT",
            "Portuguese": "pt-PT",
            "Russian": "ru-RU",
            "Japanese": "ja-JP",
            "Korean": "ko-KR",
            "Chinese (Simplified)": "zh-CN",
            "Chinese (Traditional)": "zh-TW",
            "Hindi": "hi-IN",
            "Arabic": "ar-SA",
            "Dutch": "nl-NL",
            "Swedish": "sv-SE",
            "Norwegian": "nb-NO",
            "Danish": "da-DK",
            "Finnish": "fi-FI",
            "Greek": "el-GR",
            "Turkish": "tr-TR",
            "Polish": "pl-PL",
            "Czech": "cs-CZ",
            "Hungarian": "hu-HU",
            "Romanian": "ro-RO",
            "Bulgarian": "bg-BG",
            "Ukrainian": "uk-UA",
            "Vietnamese": "vi-VN",
            "Thai": "th-TH",
            "Indonesian": "id-ID",
            "Telugu": "te-IN",
            "Tamil": "ta-IN",
            "Kannada": "kn-IN",
            "Malayalam": "ml-IN",
            "Bengali": "bn-IN"
        }
        
        # Add languages to combo box
        self.language_combo.addItems(self.languages.keys())
        
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        layout.addLayout(language_layout)
        
        # Auto-save option
        self.auto_save_check = QCheckBox("Auto-save transcription")
        self.auto_save_check.setStyleSheet("color: #212121;")
        self.auto_save_check.setChecked(True)
        layout.addWidget(self.auto_save_check)
        
        # Transcribe button
        transcribe_button = StyledButton("Transcribe Audio")
        transcribe_button.clicked.connect(self.transcribe_audio)
        layout.addWidget(transcribe_button)
        
        # Transcription result
        result_label = QLabel("Transcription Result:")
        result_label.setStyleSheet("color: #212121; font-weight: bold;")
        self.result_text = StyledTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(200)
        layout.addWidget(result_label)
        layout.addWidget(self.result_text)
        
        # Add some spacing
        layout.addStretch()

    def browse_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Audio File", "output/speech.mp3", "MP3 Files (*.mp3)"
        )
        if file_path:
            self.output_edit.setText(file_path)

    def browse_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Audio File", "", "Audio Files (*.mp3 *.wav *.ogg)"
        )
        if file_path:
            self.input_edit.setText(file_path)

    def generate_audio(self):
        text = self.text_input.toPlainText()
        if not text:
            QMessageBox.warning(self, "Error", "Please enter some text to convert to speech.")
            return
        
        output_file = self.output_edit.text()
        
        # Get the language code from the selected language name
        language_name = self.voice_combo.currentText()
        language_code = self.tts_languages.get(language_name, "en-US")
        
        rate = self.rate_spin.value()
        volume = self.volume_spin.value()
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage("Generating audio...")
        
        # Create worker thread
        self.worker = AudioWorker("tts", text=text, output_file=output_file, language=language_code)
        self.worker.finished.connect(self.on_tts_complete)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def transcribe_audio(self):
        input_file = self.input_edit.text()
        if not input_file or not os.path.exists(input_file):
            QMessageBox.warning(self, "Error", "Please select a valid audio file.")
            return
        
        # Get the language code from the selected language name
        language_name = self.language_combo.currentText()
        language_code = self.languages.get(language_name, "en-US")
        auto_save = self.auto_save_check.isChecked()
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage("Transcribing audio...")
        
        # Create worker thread
        self.worker = AudioWorker("stt", input_file=input_file, language=language_code, auto_save=auto_save)
        self.worker.finished.connect(self.on_stt_complete)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_tts_complete(self, message):
        self.progress_bar.setValue(100)
        self.statusBar().showMessage("Ready")
        QMessageBox.information(self, "Success", message)

    def on_stt_complete(self, message):
        self.progress_bar.setValue(100)
        self.statusBar().showMessage("Ready")
        self.result_text.setText(message)

    def on_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("Error occurred")
        QMessageBox.critical(self, "Error", error_message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 