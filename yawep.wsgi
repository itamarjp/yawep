import sys
sys.stdout = sys.stderr
sys.path.insert(0, '/usr/share/yawep/venv')
#sys.path.insert(1, '/usr/share/yawep/venv')

activate_this = '/usr/share/yawep/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

#activate_this = '/usr/share/yawep/venv/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))


import app as appx
