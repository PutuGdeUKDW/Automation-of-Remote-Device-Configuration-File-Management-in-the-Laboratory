from Switch_cisco import Switch_cisco as SWprocess
from Router_cisco import Router_cisco as Rprocess
from Mikrotik import Mikrotik_process as Mprocess
from db_access import Db_access as Db_process
import json

class Manager:
    def __init__(self, config_file="config.json"):
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Assign values from JSON to instance variables
        self.passwordTelnet = config["passwordTelnet"] + "\n"
        self.passwordEnable = config["passwordEnable"] + "\n"
        self.userMikrotik = config["userMikrotik"]
        self.passwordMikrotik = config["passwordMikrotik"]
        self.server = config["server"]

    
    def router_control(self,mode,data_piranti,versi=1):
        nama_piranti=data_piranti[0]
        ip_piranti=data_piranti[1]
        process = Rprocess()
        if mode == 0:
            if process.router_backup(nama_piranti,ip_piranti,self.server,self.passwordTelnet,self.passwordEnable,versi):
                print("DONE!")
                return True
            else:
                return False
        elif mode ==1:
            if process.router_restore(nama_piranti,ip_piranti,self.server,self.passwordTelnet,self.passwordEnable,versi):
                print("RESTORED")
                return True
            else:
                return False

    def switch_control(self,mode,data_piranti,versi=1):
        nama_piranti=data_piranti[0]
        ip_piranti=data_piranti[1]
        process = SWprocess()
        if mode == 0:
            if process.switch_backup(nama_piranti,ip_piranti,self.server,self.passwordTelnet,self.passwordEnable,versi):
                print("DONE!")
                return True
            else:
                return False
        elif mode ==1:
            if process.switch_restore(nama_piranti,ip_piranti,self.server,self.passwordTelnet,self.passwordEnable,versi):
                print("RESTORED")
                return True
            else:
                return False
        
    def mikrotik_control(self,mode,data_piranti,versi=1):
        nama_piranti=data_piranti[0]
        ip_piranti=data_piranti[1]
        process = Mprocess()
        if mode==0:
            if process.mikrotik_backup(nama_piranti,ip_piranti,self.userMikrotik,self.passwordMikrotik,self.server,versi):
                print("DONE!")
                return True
            else:
                return False
        elif mode==1:
            if process.mikrotik_restore(nama_piranti,ip_piranti,self.userMikrotik,self.passwordMikrotik,self.server,versi):
                print("RESTORED")
                return True
            else:
                return False

    def processing(self,mode=0,nama=None,ips=None, Noblok=None,piranti=None):
        print('START')
        db_process = Db_process()
        if not db_process.is_server_on():
            print("Aborting. Check the MySql Server status.")
            return
        pirantiInfo = db_process.get_pirantiInfo(
            nama_piranti=nama,
            ip_address=ips,
            blok=Noblok,
            tipe_piranti= piranti
            )
        #print(pirantiInfo)
        status= True
        versi=1
        if mode==0:
            desc = input("Enter a description for the backup: ")
            versi = db_process.set_version(desc)
            print(f"New backup version created: {versi}")
        if mode==1:
            db_process.get_version()
            print("Pilih versi yang ingin di input.")
            versi = int(input("Versi: "))
        print("\nProcess Start!")
        for piranti in pirantiInfo:
            #print(piranti[0],piranti[1],end="\t: ")
            print(f"{piranti[0]:<5} {piranti[1]:<13} : ", end='')
            if piranti[3]=='router_cisco':
                status=self.router_control(mode,piranti,versi)
            elif piranti[3]=='switch_cisco':
                status=self.switch_control(mode,piranti,versi)
            elif piranti[3]=='mikrotik':
                status= self.mikrotik_control(mode,piranti,versi)
            
            if status==False and mode==0:
                print("\nGagal backup.\n[1]Cancel\n[2]Lanjut")
                hasil = input("Gagal backup. Tekan : ")
                if hasil=='1':
                    print("PROCESS GAGAL! CANCEL!")
                    db_process.cancel_input(versi)
                    break
                else:
                    status=True
            if mode==0:
                db_process.input_defaultConfig(piranti,versi)



#tes = Manager()
#tes.processing(mode=0,nama=None,ips=None, Noblok=None,piranti=None)

#Parameter  :
#INT mode=0: Backup Process, mode=2: Recovery Process
#LISTSTRING nama=['R1-1','S-21'] or STRING nama='M1-1'
#LISTSTRING ips=['10.10.0.11','172.17.10.11'] or STRING ips='M1-1'
#LISTINT Noblok=[1,2,3] or INT Noblok=4
#LISTSTRING piranti=['switch_cisco','mikrotik'] or STRING piranti='router_cisco'