from abc import ABC, abstractmethod
from typing import List


# ----------------------------
# Command Pattern - Base Class
# ----------------------------
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# ----------------------------
# Editor Class
# ----------------------------
class Editor:
    def __init__(self):
        self.text_buffer: List[str] = []
        self.cursor: int = 0
        self.undo_stack: List[Command] = []
        self.redo_stack: List[Command] = []

    def insert_text(self, text: str):
        command = InsertCommand(self, text)
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def delete_text(self, count: int):
        command = DeleteCommand(self, count)
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def move_cursor(self, offset: int):
        command = MoveCursorCommand(self, offset)
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)

    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.undo_stack.append(command)

    def __str__(self):
        text = ''.join(self.text_buffer)
        return text[:self.cursor] + '|' + text[self.cursor:]


# ----------------------------
# Insert Command
# ----------------------------
class InsertCommand(Command):
    def __init__(self, editor: Editor, text: str):
        self.editor = editor
        self.text = text
        self.position = editor.cursor

    def execute(self):
        for i, ch in enumerate(self.text):
            self.editor.text_buffer.insert(self.position + i, ch)
        self.editor.cursor += len(self.text)

    def undo(self):
        for _ in self.text:
            del self.editor.text_buffer[self.position]
        self.editor.cursor = self.position


# ----------------------------
# Delete Command
# ----------------------------
class DeleteCommand(Command):
    def __init__(self, editor: Editor, count: int = 1):
        self.editor = editor
        self.count = count
        self.deleted_text = ""
        self.position = max(0, editor.cursor - count)

    def execute(self):
        self.deleted_text = ''.join(
            self.editor.text_buffer[self.position:self.editor.cursor])
        del self.editor.text_buffer[self.position:self.editor.cursor]
        self.editor.cursor = self.position

    def undo(self):
        for i, ch in enumerate(self.deleted_text):
            self.editor.text_buffer.insert(self.position + i, ch)
        self.editor.cursor = self.position + len(self.deleted_text)


# ----------------------------
# Move Cursor Command
# ----------------------------
class MoveCursorCommand(Command):
    def __init__(self, editor: Editor, offset: int):
        self.editor = editor
        self.offset = offset
        self.prev_cursor = editor.cursor

    def execute(self):
        new_cursor = self.editor.cursor + self.offset
        self.editor.cursor = max(0, min(len(self.editor.text_buffer), new_cursor))

    def undo(self):
        self.editor.cursor = self.prev_cursor


# ----------------------------
# Sample Usage
# ----------------------------
if __name__ == "__main__":
    editor = Editor()

    print(">> Insert 'Hello'")
    editor.insert_text("Hello")
    print(editor)  # Hello|

    print(">> Move cursor back by 2")
    editor.move_cursor(-2)
    print(editor)  # Hel|lo

    print(">> Insert 'y'")
    editor.insert_text("y")
    print(editor)  # Hely|lo

    print(">> Delete last 2 characters")
    editor.delete_text(2)
    print(editor)  # Hel|

    print(">> Undo")
    editor.undo()
    print(editor)  # Hely|lo

    print(">> Undo again")
    editor.undo()
    print(editor)  # Hel|lo

    print(">> Redo")
    editor.redo()
    print(editor)  # Hely|lo