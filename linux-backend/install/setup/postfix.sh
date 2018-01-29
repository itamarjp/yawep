service postfix stop
postconf -e "home_mailbox = Maildir/"
postconf -e "inet_interfaces = all"
postconf -e "message_size_limit = 80920000"
postconf -e "virtual_mailbox_limit = 102400000"
postconf -e "disable_vrfy_command = yes"
postconf -e "virtual_minimum_uid = 89"
postconf -e "virtual_uid_maps = static:97"
postconf -e "virtual_gid_maps = static:97"
postconf -e 'virtual_alias_maps = hash:/etc/postfix/virtual'
touch /etc/postfix/virtual
postmap /etc/postfix/virtual
postconf -e "virtual_mailbox_base = /var/mail/vhosts"
postconf -e "virtual_mailbox_maps = hash:/etc/postfix/vmailbox"
touch /etc/postfix/vmailbox
postmap /etc/postfix/vmailbox
postconf -e "virtual_alias_maps = hash:/etc/postfix/virtual"
touch /etc/postfix/virtual
postmap /etc/postfix/virtual
postconf -e "virtual_mailbox_domains = /etc/postfix/virtual_domains"
touch /etc/postfix/virtual_domains
postmap /etc/postfix/virtual_domains
postconf -e "smtpd_tls_cert_file = /etc/letsencrypt/live/painel.ispbrasil.com.br/fullchain.pem"
postconf -e "smtpd_tls_key_file = /etc/letsencrypt/live/painel.ispbrasil.com.br/privkey.pem"
postconf -e "smtpd_tls_CAfile = /etc/letsencrypt/live/painel.ispbrasil.com.br/fullchain.pem"
postconf -e "myhostname = painel.ispbrasil.com.br"
postconf -e 'smtpd_tls_received_header = yes'
postconf -e 'smtp_tls_security_level = may'
postconf -e 'smtpd_tls_security_level = may'
postconf -e 'smtpd_tls_loglevel = 1'
postconf -e 'smtpd_tls_received_header = yes'
postconf -e 'smtp_tls_note_starttls_offer = yes'
postconf -e "smtpd_sasl_auth_enable = no"
postconf -e "smtpd_sasl_path = private/auth"
postconf -e "smtpd_sasl_service = smtp"
postconf -e "smtpd_sasl_type = dovecot"

service postfix start