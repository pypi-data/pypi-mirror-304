from abc import ABC, abstractmethod


class FileToolRepository(ABC):
    @abstractmethod
    def create_empty_file(file_path):
        pass

    @abstractmethod
    def read_file(file_path):
        pass

    @abstractmethod
    def write_file(file_path, content):
        pass

    @abstractmethod
    def update_file(file_path, content):
        pass

    @abstractmethod
    def delete_file(file_path):
        pass

    @abstractmethod
    def get_file_name_from_text(text: str, regex: str = r"(\w+\.\w+)"):
        pass

    @abstractmethod
    def get_contents_from_text(text, regex):
        pass

    @abstractmethod
    def build_directory_structure(tree_structure):
        pass

    @abstractmethod
    def convert_tree_structure_to_dict(tree_structure):
        pass
