import os
import subprocess
import shlex

class VirtualEnvRunner:
    def __init__(self, env_name,env_path):
        self.env_name = env_name
        self.env_path=env_path

    def create_virtualenv(self):
        if not os.path.exists(self.env_path):
          try:
            command=f'python -m venv {self.env_path}'
            args=shlex.split(command)
            subprocess.run(args, check=True,capture_output=True)
            print(f'Virtual environment {self.env_name} created successfully.')
            print(f'Virtual encironment path: {os.path.abspath(self.env_name)}')
          except subprocess.CalledProcessError:
            print('Error creating virtual environment.')
        else:
            print(f'Virtual environment {self.env_name} already exists at {os.path.abspath(self.env_path)}.')

    def run_code_in_virtualenv(self, code):
        try:
            # Activate the virtual environment
            activate_script = os.path.join(self.env_path, 'bin', 'activate')
            activate_cmd = f'bash -i -c "source {activate_script}"'

           
            # Run user input code
            result = subprocess.run([activate_cmd, '&&', 'python', '-c', code], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE, 
                                    shell=True, 
                                    text=True)
            
            # Print the output
            print("Output:")
            print(result.stdout)
            print("Errors:")
            print(result.stderr)
            
        except subprocess.CalledProcessError:
            print(f'Unable to run code in your virtual environment')
            #print('Error running code in virtual environment.')


# Example usage:
if __name__ == '__main__':
    env_name = 'my_virtualenv'
    env_path='/home/ubuntu/moe/GreatLibrarian/greatlibrarian/Agents/CodeRunner/VirEnv'
    code_to_run = input("Enter Python code to run: ")
    
    runner = VirtualEnvRunner(env_name,env_path)
    runner.create_virtualenv()
    runner.run_code_in_virtualenv(code_to_run)
