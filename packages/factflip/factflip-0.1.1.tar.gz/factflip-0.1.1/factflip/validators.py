import abc
from typing import List


class MemeValidator(abc.ABC):
    def __init__(self, max_retries: int = 5) -> None:
        super().__init__()
        self.max_retries = max_retries

    @abc.abstractmethod
    def validate_caption(self, captions: List[str]) -> bool:
        raise NotImplementedError


class DefaultMemeValidator(MemeValidator):
    def validate_caption(self, captions: List[str]) -> bool:
        return True


class FactFlipMemeValidator(MemeValidator):
    def validate_caption(self, captions: List[str]) -> bool:
        txt = " ".join(captions)

        if not txt.isupper():  # Consider relaxing that rule...
            return False
        if len(txt) < 10:
            return False
        if "1." in txt:
            return False
        if "2." in txt:
            return False
        if "meme" in txt:
            return False
        if "sorry" in txt:
            return False
        if "ASSISTANT" in txt:
            return False
        if "ASSIST" in txt:
            return False
        if "SPLIT SENTENCE" in txt:
            return False

        for i in captions:
            if len(i) <= 5:
                return False

        return True
