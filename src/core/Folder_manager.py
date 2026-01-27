from tkinter import filedialog
from gui.components.Button import Button
import os

class FolderManager:
    
    
    def __init__(self):
        self.backgrounds_dir = None
        self.celebrities_dir = None
        self.objects_dir = None
        self.items_dir = None
        self.cars_dir = None
        self.clocks_dir = None
        self.phones_dir = None
        self.tgstuff_dir = None
        
        self.all_paths_to_backgrounds_images = [] 
        self.all_paths_to_celebrities_images = []
        self.all_paths_to_objects_images = []
        self.all_paths_to_items_images = []
        self.all_paths_to_cars_images = []
        self.all_paths_to_clocks_images = []
        self.all_paths_to_phones_images = []
        self.all_paths_to_tgstuff_images = []
        self.paths_to_texts = []
        
    def _get_image_paths(self, folder_path: str) -> list[str]:
        if not folder_path or not os.path.isdir(folder_path):
            return []
        supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')  # додав .webp як у твоєму прикладі
        return [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(supported_extensions)
        ]
    
    def reload_all_paths(self):
        """Перезавантажує списки файлів з обраних папок (для нових доданих файлів)"""
        if self.backgrounds_dir:
            self.all_paths_to_backgrounds_images = self._get_image_paths(self.backgrounds_dir)
        if self.celebrities_dir:
            self.all_paths_to_celebrities_images = self._get_image_paths(self.celebrities_dir)
        if self.objects_dir:
            self.all_paths_to_objects_images = self._get_image_paths(self.objects_dir)
        if self.items_dir:
            self.all_paths_to_items_images = self._get_image_paths(self.items_dir)
        if self.cars_dir:
            self.all_paths_to_cars_images = self._get_image_paths(self.cars_dir)
        if self.clocks_dir:
            self.all_paths_to_clocks_images = self._get_image_paths(self.clocks_dir)
        if self.phones_dir:
            self.all_paths_to_phones_images = self._get_image_paths(self.phones_dir)
        if self.tgstuff_dir:
            self.all_paths_to_tgstuff_images = self._get_image_paths(self.tgstuff_dir)
        
        # Для текстів не перезавантажуємо, бо це один файл, а не папка
        # Якщо треба — можемо змінити на вибір папки з txt

    def take_background_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select Backgrounds Folder")
        if selected_folder:
            self.backgrounds_dir = selected_folder
            self.all_paths_to_backgrounds_images = self._get_image_paths(selected_folder)
        button.set_active(bool(self.all_paths_to_backgrounds_images))
        print(f"Backgrounds folder: {self.backgrounds_dir}")
        print(self.all_paths_to_backgrounds_images)

    def take_celebrities_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select Celebrities Folder")
        if selected_folder:
            self.celebrities_dir = selected_folder
            self.all_paths_to_celebrities_images = self._get_image_paths(selected_folder)
        button.set_active(bool(self.all_paths_to_celebrities_images))
        print(f"Celebrities folder: {self.celebrities_dir}")
        print(self.all_paths_to_celebrities_images)

    def take_object_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select Objects Folder")
        if selected_folder:
            self.objects_dir = selected_folder
            self.all_paths_to_objects_images = self._get_image_paths(selected_folder)
        button.set_active(bool(self.all_paths_to_objects_images))
        print(f"Objects folder: {self.objects_dir}")
        print(self.all_paths_to_objects_images)
    
    def take_items_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select Items Folder")
        if selected_folder:
            self.items_dir = selected_folder
            self.all_paths_to_items_images = self._get_image_paths(selected_folder)
        button.set_active(bool(self.all_paths_to_items_images))
        print(f"Items folder: {self.items_dir}")
        print(self.all_paths_to_items_images)

    def take_cars_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select Cars Folder")
        if selected_folder:
            self.cars_dir = selected_folder
            self.all_paths_to_cars_images = self._get_image_paths(selected_folder)
        button.set_active(bool(self.all_paths_to_cars_images))
        print(f"Cars folder: {self.cars_dir}")
        print(self.all_paths_to_cars_images)

    def take_clocks_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select Clocks Folder")
        if selected_folder:
            self.clocks_dir = selected_folder
            self.all_paths_to_clocks_images = self._get_image_paths(selected_folder)
        button.set_active(bool(self.all_paths_to_clocks_images))
        print(f"Clocks folder: {self.clocks_dir}")
        print(self.all_paths_to_clocks_images)

    def take_phones_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select Phones Folder")
        if selected_folder:
            self.phones_dir = selected_folder
            self.all_paths_to_phones_images = self._get_image_paths(selected_folder)
        button.set_active(bool(self.all_paths_to_phones_images))
        print(f"Phones folder: {self.phones_dir}")
        print(self.all_paths_to_phones_images)

    def take_tgstuff_folder(self, button: Button):
        selected_folder = filedialog.askdirectory(title="Select TGstuff Folder")
        if selected_folder:
            self.tgstuff_dir = selected_folder
            self.all_paths_to_tgstuff_images = self._get_image_paths(selected_folder)
        button.set_active(bool(self.all_paths_to_tgstuff_images))
        print(f"TGstuff folder: {self.tgstuff_dir}")
        print(self.all_paths_to_tgstuff_images)
    
    def take_text_file(self, button: Button):
        selected_file = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if selected_file:
            self.paths_to_texts = [selected_file]
        button.set_active(bool(self.paths_to_texts))
        print(f"Text file: {self.paths_to_texts}")