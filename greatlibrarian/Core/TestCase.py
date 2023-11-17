from abc import ABC, abstractmethod


class TestCase(ABC):
    """TestCase abstract class
    """
    @abstractmethod
    def run(self):
        """Main function of the LLM

        Args:
            prompt (str): Prompt.

        Returns:
            str: Response from the LLM.
        """
        pass
    
    @abstractmethod
    def eval(self) -> float:
        """Evaluate if the testcase is good enough.

        Returns:
            float: The score of the case, best is 1.0 and worst is 0.0.
        """
        pass
    
    
    