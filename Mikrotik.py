import socket
import paramiko
from dependency import MikrotikBackupError
from paramiko.ssh_exception import AuthenticationException, SSHException


class Mikrotik_process:
    def mikrotik_backup(self,device_name,device_ip, userMikrotik, passwordMikrotik, server, version):
        backupfile = device_name+"_putu.backup"
        src_path=f'default_config/{device_name}-V{version}.backup'
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(device_ip, username=userMikrotik, password=passwordMikrotik, look_for_keys=False)
            stdin, stdout, stderr = ssh_client.exec_command(f'/system backup save name={backupfile}')
            while not stdout.channel.exit_status_ready():
                pass
            output = stdout.read().decode().strip()
            
            print(output,end='. ')
            command = f'/tool fetch address={server} user=ukdw password=ukdw src-path={backupfile} dst-path="{src_path}" mode=ftp upload=yes'
            stdin, stdout, stderr = ssh_client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                pass
            output = stdout.read().decode().strip()
            if "finished" in output:
                #print("Upload Done",end='. ')
                pass
            else:
                ssh_client.close()
                raise MikrotikBackupError("FTP upload failed")   
            ssh_client.close()
            return True
        except (EOFError, TimeoutError, socket.timeout, MikrotikBackupError,AuthenticationException, SSHException, Exception) as e:
            print(f"Backup failed: {e}")
            return False

    def mikrotik_restore(self,device_name,device_ip, userMikrotik, passwordMikrotik, server, version):
        backupfile = device_name+"_putu.backup"
        src_path=f'default_config/{device_name}-V{version}.backup'
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(device_ip, username=userMikrotik, password=passwordMikrotik, look_for_keys=False)
            command = f'/tool fetch address={server} user=ukdw password=ukdw dst-path={backupfile} src-path="{src_path}" mode=ftp'
            stdin, stdout, stderr = ssh_client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                pass
            output = stdout.read().decode().strip()
            #print(output)
            if 'finished' in output:
                result = "Download finished,"
                #print(result,end=' ')
            else:
                ssh_client.close()
                raise MikrotikBackupError("FTP download failed") 
            #time.sleep(3)
            command1 = f'/system backup load name={backupfile} password=1'
            stdin, stdout, stderr = ssh_client.exec_command(command1)
            output = stdout.read().decode().strip()
            while not stdout.channel.exit_status_ready():
                pass
            print(output,end='. ')
            ssh_client.close()
            return True
        except (EOFError, TimeoutError, socket.timeout,MikrotikBackupError,AuthenticationException, SSHException, Exception) as e:
            print(f"{e}")
            return False