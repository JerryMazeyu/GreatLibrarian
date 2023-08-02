import re


class Getinfo():
    def __init__(self, log_path, ) -> None:
        self.log_path = log_path

    def get_eval_result(self) -> dict:

        """
        A function to get the socre information from the log file.
        The function can find the score record by finding text in a particular format that defined by the EvalMethods(keyword/toolUsage...)
        Parameters:
        line:One of the lines in the log file.
        Returns:A dict that contains the model's score under each metric in the current testcase
        The dict is formatted like this:{'keyword':[0.7,0.5,0.8],'toolUsage':[0.3,0.9],'gpt4Eval':[0.1,0.3]}

        """
        file_path = self.log_path
        lines = []
        score_dict = {'keywords': [], 'toolUsage': [], 'gpt4Eval': [],'blacklist':[]}

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            eval_method, score = self.extract_info(line)
            if eval_method and score:
                score_dict[eval_method].append(score)
        print(score_dict)
        return (score_dict)

    def extract_info(self,line):

        """
        A function to extract the valid information of score from the log file.
        The function can find the score information after the dialogue in a log file, such as: The model gets 0.3 points in this testcase by keyword method.
        Parameters:
        log_path:The path of the log file, which includes the record of dialogue and score information.
        Returns:One group of the score information like:(evalue_method,score)

        """

        pattern = r'The model gets (\d+\.\d+) points in this testcase by (\w+) method.'
        match = re.search(pattern, line)
        if match:
            score = match.group(1)
            eval_method = match.group(2)
            return eval_method, float(score)
        else:
            return None, None
