echo "ftp:x:50:" > /etc/group.ftp

[ -f "/etc/passwd.ftp" ] || echo "" > /etc/passwd.ftp

sed -i '/^AuthUserFile/{h;s/=.*/=\/etc\/passwd.ftp/};${x;/^$/{s//AuthUserFile \/etc\/passwd.ftp/;H};x}'  /etc/proftpd.conf
sed -i '/^AuthGroupFile/{h;s/=.*/=\/etc\/group.ftp/};${x;/^$/{s//AuthGroupFile \/etc\/group.ftp/;H};x}'  /etc/proftpd.conf


sed -i '/^RequireValidShell/{h;s/.*/RequireValidShell off/};${x;/^$/{s//RequireValidShell off/;H};x}'  /etc/proftpd.conf

sed -i '/^DirFakeUser/{h;s/.*/DirFakeUser on \~/};${x;/^$/{s//DirFakeUser on ~/;H};x}'  /etc/proftpd.conf
sed -i '/^DirFakeGroup/{h;s/.*/DirFakeGroup on \~/};${x;/^$/{s//DirFakeGroup on ~/;H};x}'  /etc/proftpd.conf
