import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
from PyQt6.QtWidgets import QTextEdit
from .python_highlighter import PythonHighlighter

class CodeEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.setup_editor()
        
    def setup_editor(self):
        self.installEventFilter(self)
        
        self.setStyleSheet("""
            QTextEdit {
                background-color: #111111;
                color: #D4D4D4;
                font-family: Consolas;
                font-size: 12pt;
                selection-background-color: #264f78;
                border: 1px solid #3c3c3c;
                padding: 10px;
            }
            QScrollBar:vertical {border: none;background-color: transparent;width: 10px;margin: 25px 0 0px 0;}
            QScrollBar::handle:vertical{border-radius: 4px;border-color: rgba(216, 216, 216, 75%);border-width: 1px; border-style: solid; background-color: rgba(216, 216, 216, 75%); min-height: 25px;}
            QScrollBar::add-line:vertical{width: 0px; height: 0px;}
            QScrollBar::sub-line:vertical{width: 0px; height: 0px;}
            QScrollBar::add-page:vertical{background-color: transparent;}
            QScrollBar::sub-page:vertical{background-color: transparent;}
            QScrollBar:horizontal {border: none;background-color: transparent;width: 10px;margin: 25px 0 10px 0;}
        """)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        self.highlighter = PythonHighlighter(self.document())

    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress and isinstance(obj, CodeEditor):
            if event.key() in {Qt.Key.Key_Return, Qt.Key.Key_Enter}:
                return self.handle_python_auto_tab(obj)
        return super().eventFilter(obj, event)

    def handle_python_auto_tab(self, editor):
        cursor = editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.KeepAnchor)

        current_line = cursor.selectedText()
        current_indent = len(current_line) - len(current_line.lstrip())
        extra_indent = 0

        stripped_line = current_line.strip()

        indent_keywords = (':', 'def ', 'class ', 'if ', 'else:', 'elif ', 'while ', 
                           'for ', 'try:', 'except:', 'finally:', 'with ', '{')

        if stripped_line.endswith(':') or stripped_line.endswith('{') or any(stripped_line.startswith(kw) for kw in indent_keywords):
            extra_indent = 4
        
        total_indent = current_indent + extra_indent

        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        cursor.insertText('\n' + ' ' * total_indent) 
        if stripped_line.endswith('{'):
            cursor.insertText('\n' + '}')
            cursor.movePosition(QTextCursor.MoveOperation.Up)
            cursor.movePosition(QTextCursor.MoveOperation.EndOfLine)

        editor.setTextCursor(cursor)

        return True
