import subprocess
import shutil
import time
import os

# def runcmd(command):
#     ret = subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=1)
#     if ret.returncode == 0:
#         print("success:",ret)
#     else:
#         print("error:",ret)

# ["dir","/b"])#序列参数
# runcmd("exit 1")#字符串参数





class CodeRunner():
 def __init__(self) :
    self.virtual_env_path='VirEnv'


 def create_virtual_env(self):
    try:
        #create virtual env
        subprocess.run(['python','-m','venv','VirEnv'],stdout=subprocess,stderr=subprocess.PIPE,timeout=None)



    except Exception as e:
        return{
            'error':f"Failed to create a virtual environment :{str(e)}"

        }
    
 def run_code(self,user_code):
    try:
       #create virtual environment
       self.create_virtual_env()

       #run code from user in virtual environment
       result=subprocess.run([f'{self.virtual_env_path}/bin/python','-c',user_code],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

       #get result
       output=result.stdout.decode('utf-8')
       error=result.stderr.decode('utf-8')

       return {
          'output':output,
          'error':error
       }

    except Exception as e:
        return{
           'error':str(e)

        }
    
    finally:
       #clear virtual environment
       shutil.rmtree(self.virtual_env_path,ignore_errors=True)
    
code_runner=CodeRunner()

# #
# user_code="""
# print("hello world!)
# """

# result=code_runner.run_code(user_code)

# print("Output:")
# print(result['output'])

# print("Error:")
# print(result['error'])


# def run_code(user_code):
#     try:
#         #create virtual env
#         virtual_env=subprocess.Popen(['python','-m','venv','VirEnv'],stdout=subprocess,stderr=subprocess.PIPE)
#         virtual_env.communicate()
        
#         #activate virtual_env
#         activate_env=subprocess.Popen(['source','VirEnv/bin/activate'],shell=True,stdout=subprocess,stderr=subprocess.PIPE)
#         activate_env.communicate()

#         #run code from users in virtual_env
#         result=subprocess.run(['python','-c',user_code],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)


#         #get results
#         output=result.stdout.decode('utf-8')
#         error=result.stderr.decode('utf-8')

#         return{
#             'output': output,
#             'error': error
#         }
#     except Exception as e:
#         return{
#             'error': str(e)
#         }
    

#code input 
