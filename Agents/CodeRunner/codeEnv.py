import os 
import subprocess
import json

class CodeRunner():
 def __init__(self, env_name) :
    self.env_name=env_name
    # name of the virtual environment
    self.env_path ="/home/ubuntu/moe/GreatLibrarian/Agents/CodeRunner/VirEnv"
    # path of the virtual environment

 def create_virtual_env(self):
    try:
       command_create=['python', '-m','venv',self.env_path]
       subprocess.run(command_create,check=True)
       print(f'Virtual Environment {self.env_name} created successfully!')
    except subprocess.CalledProcessError:
       print(f'Unable to careate virtual Environment {self.env_name}.')
       
 def clr_screen(self):
        """clear history output, remain the latest output"""
        if os.name=='posix':
            os.system('clear')  #Mac/Linux/Unix
        elif os.name=='nt':
            os.system('cls')  #Win
    
 def run_code(self,user_code):
    """execute code from user or json file"""
    try:
       #clear prehistory
       self.clr_screen()

       #activate virtual environment
       activate_script=os.path.join(self.env_path,'bin','activate')
       print(f'Activate script path:{activate_script}')
      
       
       
       #run user code
       command_activate=[activate_script,'&&','python','-c',user_code]
       result=subprocess.run(command_activate,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True,
                             text=True)
       
       #print output
       print("Output: ",result.stdout)
       print("Errors: ",result.stderr)
       

    except subprocess.CalledProcessError:
       print(f'Unable to run code in your virtual environment')
      #print('Error running code in virtual environment.')


 def run_json(self,json_file):
    try:
       with open(json_file,'r') as file:
          data=json.load(file)
          if 'code' in data:
             code_to_run=data['code']
             self.run_code(code_to_run)
          else:
             print('JSON file does not cotain a "code" field')


    except FileNotFoundError:
       print("f'File {json_file} does not found!")
    except json.JSONDecodeError:
       print("f'Unable to decode JSON file {json_file}.")




# example usage
if __name__ == "__main__":
    env_name = 'my virtualenv'
    print("Enter Python code to run in virtual environment (press Ctrl+Z or Ctrl+D to execute): ")
    
    # Read lines of code until Ctrl+Z (Windows) or Ctrl+D (Unix/Linux/Mac) is pressed
    code_lines = []
    while True:
        try:
            line = input()
            code_lines.append(line)
        except EOFError:
            break
    
    # Join the code lines into a single string
    code_to_run = '\n'.join(code_lines)
    
    runner = CodeRunner(env_name)
    runner.create_virtual_env()
    runner.run_code(code_to_run)
    # runner.run_json(json_file_path)


   
