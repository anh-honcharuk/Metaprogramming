from abc import ABC, abstractmethod


class AutomatMatch(ABC):

    @abstractmethod
    def match(self, text, position):
        pass

