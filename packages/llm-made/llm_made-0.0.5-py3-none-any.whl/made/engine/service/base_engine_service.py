from abc import ABC, abstractmethod


class BaseEngineService(ABC):
    @abstractmethod
    def run(self, messages, ollama_config):
        pass
