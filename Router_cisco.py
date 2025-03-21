import telnetlib
import socket
from dependency import CiscoBackupError

class Router_cisco:
    def router_backup(self,
                      device_name,
                      device_ip, 
                      server, 
                      passwordTelnet, 
                      passwordEnable,
                      version):
        backupfile = f"default_config/{device_name}-V{version}"
        try:
            tn = telnetlib.Telnet(device_ip, timeout=10)
            tn.read_until(b"Password: ")
            tn.write(passwordTelnet.encode())
            tes = tn.read_until(b">")
            if '>' not in tes.decode():
                tn.close()
                raise CiscoBackupError("Telnet Password is wrong")
            tn.write(b"enable\n")
            tes = tn.read_until(b"Password: ", timeout=5)
            if '#' not in tes.decode():
                tn.write(passwordEnable.encode())
                tes =tn.read_until(b'#', timeout=5)
                if '#' not in tes.decode():
                    tn.close()
                    raise CiscoBackupError("EXEC Password is wrong")
            command = f'copy startup-config ftp://ukdw:ukdw@{server}/{backupfile}\n'
            tn.write(command.encode())
            read = f'[{server}]?'
            tn.read_until(read.encode())
            tn.write(b'\n')
            read = f'[{backupfile}]?'
            tn.read_until(read.encode())
            tn.write(b'\n')
            tes = tn.read_until(b'#', timeout=10)
            if "Error" in tes.decode():
                tn.close
                raise CiscoBackupError("Backup Failed. Check the file name or the server's status.")
            tn.close()
            return True
        except (EOFError, TimeoutError, socket.timeout,CiscoBackupError) as e:
            print(f"{e}")
            return False


    def router_restore (self,device_name,device_ip, server, passwordTelnet, passwordEnable,version):
        backupfile = f"default_config/{device_name}-V{version}"
        #destination = "startup-config"
        try:
            tn = telnetlib.Telnet(device_ip, timeout=10)  # Set a timeout value
            tn.read_until(b"Password: ")
            tn.write(passwordTelnet.encode())
            tes = tn.read_until(b">",timeout=5)
            if '>' not in tes.decode():
                tn.close
                raise CiscoBackupError("Telnet Password is wrong")
            tn.write(b"enable\n")
            tes = tn.read_until(b"Password: ", timeout=5)
            if '#' not in tes.decode():
                tn.write(passwordEnable.encode())
                tes =tn.read_until(b'#', timeout=5)
                if '#' not in tes.decode():
                    tn.close
                    raise CiscoBackupError("EXEC Password is wrong") 
            command = f'copy ftp://ukdw:ukdw@{server}/{backupfile} startup-config\n'
            tn.write(command.encode())
            read = f'[startup-config]?'
            tn.read_until(read.encode(),timeout=5)
            tn.write(b'\n')
            tes = tn.read_until(b'#', timeout=5)
            if "Error" in tes.decode():
                tn.close()
                raise CiscoBackupError("Recovery Failed. Check the file name or the server's status.") 
            tn.write(b'reload\n')
            tes= tn.read_until(b']',timeout=5)
            if 'yes/no' in tes.decode():
                tn.write(b'no\n')
                tn.read_until(b'[confirm]',timeout=5)
                print("A",end=' ')
            tn.write(b'\n')
            tn.close()
            return True
        except (EOFError, TimeoutError, socket.timeout,CiscoBackupError) as e:
            print(f"{e}")
            return False
        
#tes=Router_cisco()
#guh =tes.router_backup('R1-1','10.1.0.11','192.168.100.25','ukdw\n','ukdw\n',1)
#print(guh)