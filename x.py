import dns.resolver
import os

domain = 'xmr.crypto-pool.fr'
answers = dns.resolver.query(domain,'A')
for server in answers:
    print("blocking {}".format(server))
    os.system("route add -host {} reject".format(server))
    os.system("iptables -A INPUT -s {} -j DROP".format(server))
    os.system("iptables -A OUTPUT -d {} -j DROP".format(server))
