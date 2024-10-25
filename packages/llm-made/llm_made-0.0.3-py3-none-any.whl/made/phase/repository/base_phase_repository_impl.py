from copy import deepcopy

from made.agent.service.agent_service_impl import AgentServiceImpl
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.messages.entity.chat_message.user_message import UserChatMessage
from made.engine import ModelConfig
from made.phase.entity.phase_states import PhaseStates
from made.phase.repository.base_phase_repository import BasePhaseRepository
from made.role_playing.service.role_playing_service_impl import RolePlayingServiceImpl


class BasePhaseRepositoryImpl(BasePhaseRepository):
    def __init__(
        self,
        model_config: ModelConfig,
        phase_prompt: str,
        assistant_role_name: str,
        assistant_role_prompt: str,
        user_role_name: str,
        user_role_prompt: str,
        chat_turn_limit: int = 10,
        **kwargs
    ):
        model_config = deepcopy(model_config)
        self.model_config = model_config
        if temperature := kwargs.get("temperature"):
            if temperature is not None:
                self.model_config.temperature = temperature
        if top_p := kwargs.get("top_p"):
            if top_p is not None:
                self.model_config.top_p = top_p
        self.phase_prompt = phase_prompt
        self.assistant_role_name = assistant_role_name
        self.assistant_role_prompt = assistant_role_prompt
        self.user_role_name = user_role_name
        self.user_role_prompt = user_role_prompt
        self.chat_turn_limit = chat_turn_limit

        self.seminar_conclusion = None
        self.states: PhaseStates = PhaseStates()

    def chatting(
        self,
        env: ChatEnvRepositoryImpl,
        task_prompt: str,
        phase_prompt: str,
        assistant_role_name: str,
        assistant_role_prompt: str,
        user_role_name: str,
        user_role_prompt: str,
        placeholders=None,
        chat_turn_limit=10,
    ) -> str:
        if placeholders is None:
            placeholders = {}
        if isinstance(placeholders, PhaseStates):
            placeholders = placeholders.__dict__
        assert 1 <= chat_turn_limit <= 100

        role_play_session = RolePlayingServiceImpl(
            model_config=self.model_config,
            task_prompt=task_prompt,
            assistant_role_name=assistant_role_name,
            assistant_role_prompt=assistant_role_prompt,
            user_role_name=user_role_name,
            user_role_prompt=user_role_prompt,
            background_prompt=env.config.background_prompt,
        )

        _, input_user_message = role_play_session.role_playing_repository.init_chat(
            placeholders, phase_prompt
        )
        print()
        print(
            f"\033[93m{input_user_message.role_name}\033[0m",
            ": ",
            input_user_message.content,
        )
        seminar_conclusion = None

        for _ in range(chat_turn_limit):
            assistant_response, user_response = role_play_session.step(
                input_user_message, chat_turn_limit == 1
            )
            print()
            print(
                f"\033[93m{assistant_response.message.role_name}\033[0m",
                ": ",
                assistant_response.message.content,
            )
            if user_response.message is not None:
                print()
                print(
                    f"\033[93m{user_response.message.role_name}\033[0m",
                    ": ",
                    user_response.message.content,
                )
            if (
                role_play_session.role_playing_repository.assistant_agent.agent_repository.info
            ):
                seminar_conclusion = assistant_response.message.content
                break
            if assistant_response.terminated:
                break

            if (
                role_play_session.role_playing_repository.user_agent.agent_repository.info
            ):
                seminar_conclusion = user_response.message.content
                break
            if user_response.terminated:
                break

            if chat_turn_limit > 1:
                input_user_message = user_response.message
            else:
                break
        
        # TODO seminar conclusion should be more clear
        if seminar_conclusion is None:
            conversations = (
                role_play_session.role_playing_repository.assistant_agent.agent_repository.stored_messages
            )
            todo = conversations[0].content
            conversations = "".join(
                [conversation.content for conversation in conversations[1:]]
            )
            conclude_prompt = (
                f"Below are conversation between {user_role_name} and {assistant_role_name}.:\nConversations: {conversations}"
                + f'\nYou have to conclude conversations and answer for "{todo}".\n If conversation contains code, don\'t modify the code.'
            )
            message = UserChatMessage("User", content=conclude_prompt)
            agent = AgentServiceImpl(
                role_play_session.role_playing_repository.user_system_messsge,
                self.model_config,
            )
            seminar_conclusion = agent.step(message).message.content
            if "<INFO>" not in seminar_conclusion:
                seminar_conclusion = "<INFO>" + seminar_conclusion

        seminar_conclusion = seminar_conclusion.split("<INFO>")[-1]
        print()
        print(f"\033[31mseminar conclusion\033[0m: {seminar_conclusion}")
        return seminar_conclusion

    def update_phase_states(self, env: ChatEnvRepositoryImpl):
        raise NotImplementedError

    def update_env_states(self, env: ChatEnvRepositoryImpl):
        raise NotImplementedError

    def execute(
        self,
        env: ChatEnvRepositoryImpl,
    ) -> ChatEnvRepositoryImpl:
        self.update_phase_states(env)
        self.seminar_conclusion = self.chatting(
            env=env,
            task_prompt=env.config.task_prompt,
            phase_prompt=self.phase_prompt,
            assistant_role_name=self.assistant_role_name,
            assistant_role_prompt=self.assistant_role_prompt,
            user_role_name=self.user_role_name,
            user_role_prompt=self.user_role_prompt,
            placeholders=self.states,
            chat_turn_limit=self.chat_turn_limit,
        )
        env = self.update_env_states(env)
        return env
