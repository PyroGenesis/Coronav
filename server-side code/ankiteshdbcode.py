import xmlrpc.client
s = xmlrpc.client.ServerProxy('http://192.168.0.39:8000')
# Print list of available methods
print(s.system.listMethods())