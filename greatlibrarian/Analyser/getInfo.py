import re
import platform
import warnings
from typing import Tuple, Union, Dict, List


class GetInfo:
    """A class to extract information from dialog."""

    def __init__(
        self,
        log_path,
    ) -> None:
        self.log_path = log_path

    def get_eval_result(self) -> Dict[str, List[float]]:
        """
        A function to get the socre information from the log file.
        The function can find the score record by finding text in a particular format that defined by the field(language understanding/coding...)
        Parameters:
        line:One of the lines in the log file.
        Returns:A dict that contains the model's score under each metric in the current testcase
        The dict is formatted like this:{'knowledge understanding':[1,0,1],'coding':[1,0]......}
        """
        file_path = self.log_path
        lines = []
        score_dict = {}
        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            lines = file.readlines()

        for line in lines:
            score, field = self.extract_info(line)
            if field:
                if field in score_dict:
                    score_dict[field].append(score)
                else:
                    score_dict[field] = []
                    score_dict[field].append(score)


        return score_dict

    def extract_info(self, line) -> Tuple[Union[float, None], Union[str, None]]:
        """
        A function to extract the valid information of score from the log file.
        The function can find the score information after the dialogue in a log file, such as: The model gets 0.3 points in this testcase by keyword method.
        Parameters:
        log_path:The path of the log file, which includes the record of dialogue and score information.
        Returns:One group of the score information like:(evalue_method,score)
        """

        pattern = r"The final score of this testcase is (\d+\.\d+), in (\w+) field."
        match = re.search(pattern, line)
        if match:
            score = match.group(1)
            field = match.group(2)
            return float(score), field
        else:
            return None, None


