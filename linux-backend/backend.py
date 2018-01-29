import os
from pwd import getpwnam
import shutil
from pwd import getpwnam

def make_web_home(homedir):
  try:
   os.makedirs(homedir,exist_ok=True)
  except:
   print("error creating directory {}".format(homedir))

  try:
     os.chown(homedir, getpwnam('ftp').pw_uid, getpwnam('apache').pw_gid)
  except:
   print("error setting permissions on {}".format(homedir))

def remove_web_home(homedir):
  print("Removing directory : " , homedir[:-7])
  shutil.rmtree(homedir[:-7] , ignore_errors=True)



def make_mail_home(homedir):
  try:
   os.makedirs(homedir,exist_ok=True)
  except:
   print("error creating directory {}".format(homedir))

  try:
     os.chown(homedir, getpwnam('dovecot').pw_uid, getpwnam('dovecot').pw_gid)
  except:
   print("error setting permissions on {}".format(homedir))

def remove_mail_home(homedir):
  remove_web_home(homedir)


