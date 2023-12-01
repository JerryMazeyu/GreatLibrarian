import subprocess
import shlex

command=shlex.split("python algebra.py")
process=subprocess.run(command,check=True,capture_output=True,input="yes".encode())

output=process.stdout.decode()
print(output)

error=process.stderr.decode()
print(error)