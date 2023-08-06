#!/home/kamalch/miniconda3/bin/python
import os

cwd = os.getcwd()
# os.chdir("jarvis_leaderboard")
cmd = "mkdocs serve"
os.system(cmd)
os.chdir(cwd)
