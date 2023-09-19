import os 
import subprocess
import json

class CodeRunner():
 def __init__(self, env_name) :
    self.env_name=env_name
    #self.env_name.path="  "

 def create_virtual_env(self):
    try:
       command_create=['python', '-m','venv',self.env_name]
       subprocess.run(command_create,check=True)
       print(f'Virtual Environment {self.env_name} created successfully!')
    except subprocess.CalledProcessError:
       print(f'Unable to careate virtual Environment {self.env_name}.')
       
    
 def run_code(self,user_code):
    try:
       #activate virtual environment
       activate_script=os.path.join(self.env_name,'bin','activate')
       activate_cmd=f'source {activate_script}'
       
       
       #run user code
       command_activate=[activate_cmd,'&&','python','-c',user_code]
       result=subprocess.run(command_activate,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,text=True)
       
       #print output
       print("Output: ",result.stdout)
       print("Errors: ",result.stderr)
       

    except subprocess.CalledProcessError:
       print(f'Unable to run code in your virtual environment')


 def run_json(self,json_file):
    try:
       with open(json_file,'r') as file:
          data=json.load(file)
          if 'code' in data:
             code_to_run=data['code']
             self.run_code_in_virenv(code_to_run)
          else:
             print('JSON file does not cotain a "code" field')


    except FileNotFoundError:
       print("f'File {json_file} does not found!")
    except json.JSONDecodeError:
       print("f'Unable to decode JSON file {json_file}.")





code_runner=CodeRunner()

