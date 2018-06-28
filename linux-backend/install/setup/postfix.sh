postconf -e "home_mailbox = Maildir/"
postconf -e "inet_interfaces = all"
postconf -e "message_size_limit = 80920000"
postconf -e "virtual_mailbox_limit = 102400000"
postconf -e "disable_vrfy_command = yes"
postconf -e "virtual_minimum_uid = 89"
postconf -e "virtual_uid_maps = static:97"
postconf -e "virtual_gid_maps = static:97"
postconf -e 'virtual_alias_maps = hash:/etc/postfix/virtual'
postmap /etc/postfix/virtual
postconf -e "virtual_mailbox_base = /var/mail/vhosts"
postconf -e "virtual_mailbox_maps = hash:/etc/postfix/vmailbox"
postmap /etc/postfix/vmailbox
postconf -e "virtual_alias_maps = hash:/etc/postfix/virtual"
postmap /etc/postfix/virtual
postconf -e "virtual_mailbox_domains = /etc/postfix/virtual_domains"
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
postconf -e "smtpd_sasl_auth_enable = yes"
postconf -e "smtpd_sasl_path = private/auth"
postconf -e "smtpd_sasl_service = smtp"
postconf -e "smtpd_sasl_type = dovecot"
postconf -e "smtpd_helo_required = yes"
postconf -e "smtpd_delay_reject = yes"
postconf -e "strict_rfc821_envelopes = yes"
postconf -e "smtpd_helo_restrictions = permit_mynetworks, reject_non_fqdn_hostname,reject_invalid_hostname, reject_unknown_helo_hostname permit"
postconf -e "smtpd_recipient_restrictions =   permit_sasl_authenticated,   reject_invalid_hostname,   reject_non_fqdn_hostname,   reject_non_fqdn_sender,   reject_non_fqdn_recipient,   reject_unknown_sender_domain,   reject_unknown_recipient_domain,   permit_mynetworks,   permit"
