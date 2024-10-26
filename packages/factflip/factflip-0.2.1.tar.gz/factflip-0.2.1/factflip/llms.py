import abc
from typing import Dict, Sequence

import ollama

DEFAULT_OLLAMA_LMM = "llama3"


def get_default_ollama_llm() -> str:
    return DEFAULT_OLLAMA_LMM


class Llm(abc.ABC):
    @abc.abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def chat(self, messages: Sequence[Dict[str, str]]) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def embed(self, prompt: str) -> Sequence[float]:
        raise NotImplementedError


class OllamaLlm(Llm):
    def __init__(self, model: str = None) -> None:
        super().__init__()
        if not model:
            self.model = get_default_ollama_llm()
        else:
            self.model = model

    def generate(self, prompt: str) -> str:
        return ollama.generate(model=self.model, prompt=prompt)["response"].strip()

    def chat(self, messages: Sequence[Dict[str, str]]) -> str:
        return ollama.chat(model=self.model, messages=messages)["message"]["content"].strip()

    def embed(self, prompt: str) -> Sequence[float]:
        return ollama.embeddings(model=self.model, prompt=prompt)


def get_default_llm() -> Llm:
    return OllamaLlm()
