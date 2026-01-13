from tkinter import filedialog
from gui.components.Button import Button
import os

class FolderManager:
    
    def __init__(self):
        self.all_paths_to_backgrounds_images = [] 
        self.all_paths_to_celebrities_images = []
        self.all_paths_to_objects_images = []
        self.all_paths_to_items_images = []
        self.paths_to_texts = []
        
    def _get_image_paths(self, folder_path: str) -> list[str]:
        if not folder_path:
            return []
        supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        return [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(supported_extensions)
        ]
    
    def take_background_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select Backgrounds Folder")
        if selected_folder:
            self.all_paths_to_backgrounds_images = self._get_image_paths(selected_folder)
        button.set_active()
        # Optionally: print or return for UI update

    def take_celebrities_folder(self, button: Button):  # Fixed name
        selected_folder = filedialog.askdirectory(title="Select Celebrities Folder")
        if selected_folder:
            self.all_paths_to_celebrities_images = self._get_image_paths(selected_folder)
        button.set_active()

    def take_object_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select Objects Folder")
        if selected_folder:
            self.all_paths_to_objects_images = self._get_image_paths(selected_folder)
        button.set_active()
    
    def take_items_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select Items Folder")
        if selected_folder:
            self.all_paths_to_items_images = self._get_image_paths(selected_folder)
        button.set_active()
    
    def take_text_file(self, button: Button):
        selected_file = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if selected_file:
            self.paths_to_texts = [selected_file]
        button.set_active()