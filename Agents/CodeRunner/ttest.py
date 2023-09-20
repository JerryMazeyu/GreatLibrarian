import os
import subprocess

class VirtualEnvRunner:
    def __init__(self, env_name):
        self.env_name = env_name

    def create_virtualenv(self):
        try:
            subprocess.run(['python', '-m', 'venv', self.env_name], check=True)
            print(f'Virtual environment {self.env_name} created successfully.')
        except subprocess.CalledProcessError:
            print('Error creating virtual environment.')

    def run_code_in_virtualenv(self, code):
        try:
            # Activate the virtual environment
            activate_script = os.path.join(self.env_name, 'bin', 'activate')
            activate_cmd = f'source {activate_script}'

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
            print(f'Virtual encironment path: {os.path.abspath(self.env_name)}')
        except subprocess.CalledProcessError:
            #print('Error running code in virtual environment.')


# Example usage:
if __name__ == '__main__':
    env_name = 'my_virtualenv'
    code_to_run = input("Enter Python code to run: ")
    
    runner = VirtualEnvRunner(env_name)
    runner.create_virtualenv()
    runner.run_code_in_virtualenv(code_to_run)
