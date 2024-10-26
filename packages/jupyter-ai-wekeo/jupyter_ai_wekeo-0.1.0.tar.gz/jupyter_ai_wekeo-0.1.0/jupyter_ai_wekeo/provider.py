from typing import ClassVar, List, Optional

from jupyter_ai import BaseProvider, Field
from jupyter_ai_magics.models.persona import JUPYTERNAUT_AVATAR_ROUTE, Persona
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from .llm import WekeoLLM

HUMAN_MESSAGE_TEMPLATE = """
History: {{history}}
Human: {{input}}

"""


class WekeoProvider(BaseProvider, WekeoLLM):
    id: ClassVar[str] = "wekeo-provider"
    name: ClassVar[str] = "Wekeo Provider"
    models: ClassVar[List[str]] = ["server"]
    help: ClassVar[str] = ""
    model_id_key: ClassVar[str] = "model_id_key"
    model_id_label: ClassVar[str] = "model_id_label"
    fields: ClassVar[List[Field]] = []
    """User inputs expected by this provider when initializing it. Each `Field` `f`
    should be passed in the constructor as a keyword argument, keyed by `f.key`."""
    unsupported_slash_commands: ClassVar[set] = {"/learn", "/ask", "/generate", "/fix"}
    persona: ClassVar[Optional[Persona]] = Persona(
        name="WEkEO Experimental AI-based Assistant",
        avatar_route=JUPYTERNAUT_AVATAR_ROUTE,
    )

    def get_chat_prompt_template(self) -> PromptTemplate:
        """
        Produce a prompt template optimised for chat conversation.
        The template should take two variables: history and input.
        """
        name = self.__class__.name
        if self.is_chat_provider:
            return ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(HUMAN_MESSAGE_TEMPLATE).format(
                        provider_name=name, local_model_id=self.model_id
                    ),
                    MessagesPlaceholder(variable_name="history"),
                    HumanMessagePromptTemplate.from_template(
                        HUMAN_MESSAGE_TEMPLATE,
                        template_format="jinja2",
                    ),
                ]
            )
        else:
            return PromptTemplate(
                input_variables=["history", "input", "context"],
                template=HUMAN_MESSAGE_TEMPLATE,
                template_format="jinja2",
            )
