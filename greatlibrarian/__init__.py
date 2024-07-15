import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))
gl_path = os.path.abspath(os.path.join(current_path))
if gl_path not in sys.path:
    sys.path.append(gl_path)