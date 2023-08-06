from jarvis.gpt.primitives import BasePrompt, BusinessPrompt, CodePrompt

PromptType = BasePrompt | BusinessPrompt | CodePrompt


class ContextHandler:

    def __init__(self):
        self.current_question: str = ''
        self.last_question: str = ''
        self.last_answer: str = ''
        self.answers: list[str] = []
        self.questions: list[str] = []

    def make_question(self, next_: PromptType) -> str:
        prev_context_body: str = ''
        if self.string_context:
            prev_context_body = f'''\nPrevious context:{self.string_context}'''
        self.current_question = next_.generate_question(prev_context_body)
        self.last_question = f'\nQuestion: {self.current_question}'

        return self.current_question

    def register_answer(self, answer: str) -> None:
        self.questions.append(self.last_question)
        self.last_answer: str = f'\n{answer.lstrip()}'
        self.answers.append(self.last_answer)

    @property
    def string_context(self) -> str:
        return "\n".join(self.questions + self.answers)
