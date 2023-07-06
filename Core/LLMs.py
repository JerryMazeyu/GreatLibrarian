from abc import ABC, abstractmethod


class LLMs(ABC):
    """LLMs abstract class
    """
    @abstractmethod
    def __call__(self, prompt:str) -> str:
        """Main function of the LLM

        Args:
            prompt (str): Prompt.

        Returns:
            str: Response from the LLM.
        """
        pass
    
    