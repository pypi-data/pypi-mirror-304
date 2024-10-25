from typing import List

from made.chat_chain.repository.chat_chain_repository_impl import (
    ChatChainRepositoryImpl,
)
from made.chat_chain.service.chat_chain_service import ChatChainService
from made.chat_env.entity.env_config import EnvConfig
from made.chat_env.entity.env_states import EnvStates
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.engine.entity.ollama_config import OllamaConfig
from made.phase.service.phase_service_impl import PhaseServiceImpl


class ChatChainServiceImpl(ChatChainService):
    def __init__(
        self,
        task_prompt: str,
        directory: str,
        phases: List[str] = [
            "DemandAnalysis",
            "LanguageChoose",
            "Coding",
            "CodeComplete",
            "CodeReviewComment",
            "CodeReviewModification",
            "TestErrorSummary",
            "TestModification",
            "Manual",
        ],
        base_url: str = "http://127.0.0.1:11434/v1/",
        model: str = "llama3.2",
        api_key: str = "ollama",
        max_tokens: int = 40000,
    ):
        self.model_config = OllamaConfig(
            base_url=base_url, model=model, api_key=api_key, max_tokens=max_tokens
        )
        self.chat_chain_repository = ChatChainRepositoryImpl()
        self.phase_service = PhaseServiceImpl(
            model_config=self.model_config,
        )

        env_config = EnvConfig(task_prompt=task_prompt, directory=directory)
        env_states = EnvStates()
        self.env = ChatEnvRepositoryImpl(env_config=env_config, env_states=env_states)
        self.phases = self.get_phases(phases)

    def get_phases(self, phases: List[str]):
        phases = [self.phase_service.get_phase(phase) for phase in phases]
        return phases

    def run(self):
        self.chat_chain_repository.preprocessing(self.env)
        self.chat_chain_repository.execute_chain(env=self.env, phases=self.phases)
        self.chat_chain_repository.postprocessing()
