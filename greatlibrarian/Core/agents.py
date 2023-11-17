from abc import ABC, abstractmethod


class Agents(ABC):
    """Agents abstract class
    """
    @abstractmethod
    def __call__(self, prompt:str) -> str:
        """Main function of the agents, interact with the LLM, should call process() to actually run the agents.

        Args:
            prompt (str): Receive the LLM's prompt.

        Returns:
            str: Response to the LLM.
        """
        pass
    
    @abstractmethod
    def process(self, *args, **kwds):
        """What agents actually do.
        """
        pass
    
    @abstractmethod
    def help(self) -> str:
        """Tell LLM how to use this agents.

        Returns:
            str: The document of the agent.
        """
        pass