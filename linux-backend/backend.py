import os
from pwd import getpwnam
import shutil
from pwd import getpwnam
import dns.resolver

def make_web_home(homedir):
  try:
   print("Creating web directory {}".format(homedir))
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
   print("Creating mail directory {}".format(homedir))  
   os.makedirs(homedir,exist_ok=True)
  except:
   print("error creating directory {}".format(homedir))

  try:
     os.chown(homedir, getpwnam('dovecot').pw_uid, getpwnam('dovecot').pw_gid)
  except:
   print("error setting permissions on {}".format(homedir))

def remove_mail_home(homedir):
  remove_web_home(homedir)


def resolvedns(hostname):
 iplist = []
 try:
   answersv4 = dns.resolver.query(hostname,'A')
 except:
  print ("no IPv4 records for {}".format(hostname))
 else:
   for ipv4 in answersv4:
    print("{} points to {}".format(hostname,ipv4))
    iplist.append("{}".format(ipv4))

 try:
  answersv6 = dns.resolver.query(hostname,'AAAA')
 except:
  print ("no IPv6 records for {}".format(hostname))
 else:
   for ipv6 in answersv6:
    print("{} points to {}".format(hostname, ipv6))
    iplist.append("{}".format(ipv6))
 return iplist
