import logging
from typing import Any, Iterable, Type

from openai import Completion, ChatCompletion
from openai.openai_object import OpenAIObject


from jarvis.config.openai import OPEN_AI
from jarvis.gpt.context import PromptType, ContextHandler
from nltk.tokenize import word_tokenize

logger: logging.Logger = logging.getLogger(__name__)


class _QuestionCompressor:

    @classmethod
    def zip_question(cls, question: str, remove_vowels: bool = False) -> str:
        if remove_vowels:
            question: str = cls.remove_vowels(question)
        tokens: list[str] = word_tokenize(question.lower())
        summary: str = ' '.join(tokens)
        return summary

    @classmethod
    def remove_vowels(cls, text):
        vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
        words = text.split()
        output_words = []
        for word in words:
            if "-" in word or "'" in word or len(word) < 3:
                output_words.append(word)
                continue
            output_word = word.translate(str.maketrans('', '', ''.join(vowels)))
            output_words.append(output_word)
        output = " ".join(output_words)
        return output


class AbstractCompletion:
    DAVINCI_MODEL: str = 'text-davinci-003'
    CHAT_GPT_MODEL: str = 'gpt-3.5-turbo'

    @classmethod
    def setup_kwargs(
            cls,
            **kwargs
    ) -> dict[str, Any]:
        default_kwargs: dict[str, Any] = {
            'max_tokens': OPEN_AI.answer_tokens_limit,
            'n': 1,
            'stop': None,
            'temperature': 0,
        }
        default_kwargs.update(kwargs)
        return default_kwargs

    @classmethod
    def create(cls, question: str, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    async def acreate(cls, question: str, *args, **kwargs):
        raise NotImplementedError


class DavinciEngine(AbstractCompletion):

    @classmethod
    def create(cls, question: str, *args, **kwargs):
        logger.info(question)
        return Completion.create(
            *args,
            **cls.setup_kwargs(
                engine=OPEN_AI.model_engine,
                prompt=f'{question}\nAnswer language: {OPEN_AI.answer_language}',
                **kwargs
            )
        )

    @classmethod
    async def acreate(cls, question: str, *args, **kwargs):
        logger.info(question)
        return await Completion.acreate(
            *args,
            **cls.setup_kwargs(
                engine=OPEN_AI.model_engine,
                prompt=f'{question}\nAnswer language: {OPEN_AI.answer_language}',
                **kwargs
            )
        )


class ChatGPTEngine(AbstractCompletion):
    messages: list = [{'role': 'system', 'content': f'{OPEN_AI.calibration_message}'}]

    @classmethod
    def create(cls, question: str, *args, **kwargs):
        logger.info(question)
        cls.messages.append({'role': 'user', 'content': question})
        answer = ChatCompletion.create(
            *args,
            **cls.setup_kwargs(
                model=OPEN_AI.model_engine,
                messages=cls.messages,
                **kwargs
            )
        )
        cls.messages.append(answer.choices[0].message)
        return answer

    @classmethod
    async def acreate(cls, question: str, *args, **kwargs):
        logger.info(question)
        cls.messages.append({'role': 'user', 'content': question})
        answer = await ChatCompletion.acreate(
            *args,
            **cls.setup_kwargs(
                model=OPEN_AI.model_engine,
                messages=cls.messages,
                **kwargs
            )
        )
        cls.messages.append(answer.choices[0].message)
        return answer


def engine_type_factory() -> Type[ChatGPTEngine | DavinciEngine]:
    match OPEN_AI.model_engine:
        case AbstractCompletion.CHAT_GPT_MODEL:
            return ChatGPTEngine
        case AbstractCompletion.DAVINCI_MODEL:
            return DavinciEngine
        case _:
            raise NotImplementedError


class SimpleGPT:
    @property
    def engine(self) -> Type[ChatGPTEngine | DavinciEngine]:
        return engine_type_factory()

    @classmethod
    def prepare_answer(cls, answer_list: list[OpenAIObject]) -> str:
        match cls.engine.__name__:
            case ChatGPTEngine.__name__:
                return answer_list[0].message.content
            case DavinciEngine.__name__:
                return ''.join(
                    [x.text for x in answer_list]
                )

    @classmethod
    async def async_process_question(cls, question: str, **kwargs) -> str:
        answer = await cls.engine.acreate(question, **kwargs)
        return cls.prepare_answer(answer.choices)

    @classmethod
    def process_question(cls, question: str, **kwargs) -> str:
        choices = cls.engine.create(question, **kwargs).choices
        return cls.prepare_answer(choices)

    @classmethod
    def process_dialog(
            cls,
            prompts: Iterable[PromptType],
            compress_question: bool = False,
            compress_answer: bool = False,
            q_compressor: Type[_QuestionCompressor] = _QuestionCompressor,
            context_handler: ContextHandler = None,
            **kwargs
    ) -> ContextHandler:

        if context_handler is None:
            context_handler: ContextHandler = ContextHandler()
        for prompt in prompts:
            question: str = context_handler.make_question(prompt)
            try:
                if compress_question:
                    question: str = q_compressor.zip_question(question, kwargs.pop('remove_vowels', False))
                answer: str = cls.process_question(
                    question,
                    **kwargs
                )
                if compress_answer:
                    answer: str = q_compressor.zip_question(answer)
            except ValueError as e:
                match e.args[0]:
                    case 'Question must be provided and not empty.':
                        continue
                    case _:
                        raise e
            else:
                context_handler.register_answer(answer)
        return context_handler

    @classmethod
    async def async_process_dialog(
            cls,
            prompts: Iterable[PromptType],
            compress_question: bool = False,
            compress_answer: bool = False,
            q_compressor: Type[_QuestionCompressor] = _QuestionCompressor,
            context_handler: ContextHandler = None,
            **kwargs
    ) -> ContextHandler:
        if context_handler is None:
            context_handler: ContextHandler = ContextHandler()
        for prompt in prompts:
            question: str = context_handler.make_question(prompt)
            try:
                if compress_question:
                    question: str = q_compressor.zip_question(question, kwargs.pop('remove_vowels', False))
                answer: str = await cls.async_process_question(
                    question,
                    **kwargs
                )
                if compress_answer:
                    answer: str = q_compressor.zip_question(answer)
            except ValueError as e:
                match e.args[0]:
                    case 'Question must be provided and not empty.':
                        continue
                    case _:
                        raise e
            else:
                context_handler.register_answer(answer)
        return context_handler
