from typing import List

from made.chat_chain.repository.chat_chain_repository import ChatChainRepository
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl


class ChatChainRepositoryImpl(ChatChainRepository):
    def execute_step(
        self,
        env: ChatEnvRepositoryImpl,
        phase: BasePhaseRepositoryImpl,
    ):
        phase.execute(env)

    def execute_chain(
        self,
        env: ChatEnvRepositoryImpl,
        phases: List[BasePhaseRepositoryImpl],
    ):
        for phase in phases:
            self.execute_step(env=env, phase=phase)

    # TODO directory generation with tree
    def preprocessing(self):
        pass

    # TODO clean directory(pycache, etc.)
    def postprocessing(self):
        pass
