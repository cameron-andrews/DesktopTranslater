from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from googletrans import Translator
from pypinyin import lazy_pinyin, Style

class TranslationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.last_chinese_text = None
        self.translator = Translator()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.chinese_label = QLabel(self)
        layout.addWidget(self.chinese_label)

        self.pinyin_label = QLabel(self)
        layout.addWidget(self.pinyin_label)

        self.english_label = QLabel(self)
        layout.addWidget(self.english_label)

    def add_translation(self, chinese_text):
        """
        Translate Chinese text to English and update the labels.

        :param chinese_text: Input Chinese text.
        """
        if chinese_text is None or chinese_text == self.last_chinese_text:
            return

        try:
            # Translate Chinese text to English
            translation = self.translator.translate(chinese_text, dest='en')
            english_text = translation.text

            # Display Chinese, Pinyin, and English
            pinyin_text = ' '.join(lazy_pinyin(chinese_text, style=Style.NORMAL))
            self.chinese_label.setText(f"Chinese: {chinese_text}")
            self.pinyin_label.setText(f"Pinyin: {pinyin_text}")
            self.english_label.setText(f"English: {english_text}")

            # Update last Chinese text
            self.last_chinese_text = chinese_text
        except Exception as ex:
            print(f"Failed translating: {ex}")
            print(f"Failed translating text: {chinese_text}, {type(chinese_text)}")