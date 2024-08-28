# from typing import Any, Dict

# import pytest
# from autogen.agentchat import AssistantAgent, UserProxyAgent

# from fastagency.core.autogen import AutoGenTeam, AutogenTeamAgents
# from fastagency.core.base import ConsoleIO


# @pytest.mark.openai
# def test_simple(openai_gpt4o_mini_llm_config: Dict[str, Any]) -> None:
#     team = AutoGenTeam()

#     @team.factory(name="my team", description="my team description")
#     def create_team() -> AutogenTeamAgents:
#         initial_agent = UserProxyAgent(
#             name="user_proxy", human_input_mode="NEVER", max_consecutive_auto_reply=5
#         )
#         receiving_agent = AssistantAgent(
#             name="assistant", llm_config=openai_gpt4o_mini_llm_config
#         )

#         return {
#             "initial_agent": initial_agent,
#             "receiving_agent": receiving_agent,
#         }

#     my_team = team.create(session_id="session_id", io=ConsoleIO())

#     my_team.init_chat("Write me a sonnet about lige in Zagreb")
