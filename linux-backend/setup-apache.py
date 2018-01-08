#!/usr/bin/env python3
import os

virtualhost = """
NameVirtualHost *:80
"""

conf_d =  "/etc/httpd/conf.d/a.conf"
welcome = "/etc/httpd/conf.d/welcome.conf"

try:
 os.unlink(welcome)
except:
 pass

file = open(conf_d,"w")
file.write(virtualhost)
file.close()

os.system("service httpd restart")



