from abc import ABC, abstractmethod


class ChatChainRepository(ABC):
    @abstractmethod
    def execute_step(self, env, phase):
        pass

    @abstractmethod
    def execute_chain(self, env, phases):
        pass

    @abstractmethod
    def preprocessing(self):
        pass

    @abstractmethod
    def postprocessing(self):
        pass
