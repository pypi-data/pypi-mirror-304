import os
from typing import List

from made.chat_chain.repository.chat_chain_repository import ChatChainRepository
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.tools.file.repository.file_tool_repository_impl import FileToolRepositoryImpl
from made.tools.git.repository.git_tool_repository_impl import GitToolRepositoryImpl


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
    def preprocessing(self, env: ChatEnvRepositoryImpl, root: str = "project_zoo"):
        workspace = os.path.join(root, env.config.directory)
        os.makedirs(workspace, exist_ok=True)
        FileToolRepositoryImpl.create_empty_file(os.path.join(workspace, "__init__.py"))
        log_path = os.path.join(workspace, "logs")
        os.makedirs(log_path, exist_ok=True)
        if env.config.git_management:
            GitToolRepositoryImpl.create_gitignore(workspace)
            FileToolRepositoryImpl.update_file(os.path.join(workspace, ".gitignore"), "logs/")

    # TODO clean directory(pycache, etc.)
    def postprocessing(self):
        pass
