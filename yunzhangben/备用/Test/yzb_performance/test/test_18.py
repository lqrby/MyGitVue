# import socket
 
 
# def is_ipv4(ip):
#     try:
#         socket.inet_pton(socket.AF_INET, ip)
#     except AttributeError:  # no inet_pton here, sorry
#         try:
#             socket.inet_aton(ip)
#         except socket.error:
#             return False
#         return ip.count('.') == 3
#     except socket.error:  # not a valid ip
#         return False
#     return True
 
 
# def is_ipv6(ip):
#     try:
#         socket.inet_pton(socket.AF_INET6, ip)
#     except socket.error:  # not a valid ip
#         return False
#     return True
 
 
# def check_ip(ip):
#     return is_ipv4(ip)  or is_ipv6(ip)

import os
p=os.popen("ping 58.253.156.150")
x=p.read()
p.close()
if x.count('TTL'):
    print("ping通了")
else:
    print("ping不通")

