from abc import ABC, abstractmethod


class GitToolRepository(ABC):
    @abstractmethod
    def git_init():
        pass

    @abstractmethod
    def create_gitignore():
        pass
    
    @abstractmethod
    def git_commit():
        pass
    
    @abstractmethod
    def git_add():
        pass