import subprocess

subprocess.call("npx rimraf RiklC".split())
subprocess.call("git clone https://github.com/gx1285/RiklC.git".split())
subprocess.call("python RiklC/bot.py".split())
