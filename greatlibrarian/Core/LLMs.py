from abc import ABC, abstractmethod


class LLMs(ABC):
    """LLMs abstract class
    """
    
    def __init__(self,apikey,name,llm_intro):
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro
    
    def get_intro(self):
        return self.llm_intro
    
    def get_name(self):
        return self.name
    
    @abstractmethod
    def __call__(self, prompt:str) -> str:
        """Main function of the LLM

        Args:
            prompt (str): Prompt.

        Returns:
            str: Response from the LLM when nothing is wrong(str) / 'API Problem'(str) when the API is not working.
        """
        pass
    
    