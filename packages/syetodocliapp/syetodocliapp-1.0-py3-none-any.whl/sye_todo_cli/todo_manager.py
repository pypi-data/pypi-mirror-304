import json
import os

class TodoManager:
    def __init__(self, filename='todo.json'):
        self.filename = filename
        self.todos = self.load_todos()
    
    def load_todos(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        else:
            return []
    
    def save_todos(self):
        with open(self.filename,'w') as file:
            json.dump(self.todos, file)
            
    def add_todo(self, todo):
        self.todos.append({"task":todo, "completed":False})
        self.save_todos()
    
    def remove_todo(self, index):
        if 0 <= index < len(self.todos):
            del self.todos[index]
            self.save_todos()
        else:
            raise IndexError(f"Todo does not exist.")
    
    def list_todos(self):
        return self.todos
    