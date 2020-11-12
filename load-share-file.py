from paramiko import SSHClient
from scp import SCPClient
import time

server = '192.168.137.222'
username = 'pi'
password = 'raspberry'
server_path = '/home/pi/gpio-music-box/file_to_share.txt'
local_path = 'D:\\microprocessors_file'
share_file_path = 'D:\\microprocessors_file\\file_to_share.txt'

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(server, username=username, password=password)

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())

while True:
    scp.get(server_path, local_path)
    time.sleep(0.4)

scp.close()