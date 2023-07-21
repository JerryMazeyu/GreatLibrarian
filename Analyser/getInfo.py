class Getinfo():
    def __init__(self,log_path,) -> None:
        self.log_path=log_path
    
    def get_info(log_path) -> dict:

        """
        A function to get the socre information from the log file.
        The function can find the  score record by finding text in a particular format that defined by the EvalMethods(keyword/toolUsage...)
        Parameters:
        log_path:The path of the log file that saves the dialogue and the score record.
        Returns:A dict that contains the model's score under each metric in the current testcase
        The dict is formatted like this:{'keyword':[0.7,0.5,0.8],'toolUsage':[0.3,0.9],'gpt4Eval':[0.1,0.3]}

        """