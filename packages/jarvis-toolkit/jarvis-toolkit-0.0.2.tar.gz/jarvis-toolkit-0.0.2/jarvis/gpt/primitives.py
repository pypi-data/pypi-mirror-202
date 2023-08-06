from abc import abstractmethod
from dataclasses import dataclass
from typing import Literal


class PromptInterface:

    @abstractmethod
    def generate_question(self, previous_context_body: str) -> str:
        ...


@dataclass
class BasePrompt(PromptInterface):
    body: str

    def generate_question(self, previous_context_body: str) -> str:
        return f'''Question: {self.body}{previous_context_body}'''

    async def async_generate_question(self, previous_context_body: str) -> str:
        return self.generate_question(previous_context_body)


@dataclass
class SpeechPrompt(BasePrompt):
    def generate_question(self, previous_context_body: str) -> str:
        return f'''{self.body}{previous_context_body}'''


@dataclass
class BusinessPrompt(BasePrompt):
    business_context: str

    def generate_question(self, previous_context_body: str) -> str:
        base_question: str = BasePrompt(self.body).generate_question(previous_context_body)
        return f'{base_question}\nBusiness context: {self.business_context}'


@dataclass
class CodePrompt(BusinessPrompt):
    code_context: str
    language: Literal['python']

    def generate_question(self, previous_context_body: str) -> str:
        if self.business_context:
            question: str = BusinessPrompt(self.body, self.business_context).generate_question(previous_context_body)
        else:
            question: str = BasePrompt(self.body).generate_question(previous_context_body)
        return "\n".join(
            (
                question,
                f"\nCode context:\n\n{self.code_context}",
                f"Language: {self.language}"
            )
        )
