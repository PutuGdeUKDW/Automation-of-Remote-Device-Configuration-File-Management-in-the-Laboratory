from Skripsi import Manager
from db_access import Db_access
class MainInterface:
    def __init__(self):
        self.manager = Manager()
        self.db = Db_access()

    def get_input(self, prompt, is_list=False):
        user_input = input(prompt).strip()
        if not user_input:
            return None
        if is_list:
            return [item.strip() for item in user_input.split(',')]
        return user_input

    def run(self):
        if not self.db.is_server_on():
            print("Aborting. Check the MySql Server status.")
            return
        print("Welcome to the Backup/Restore System")
        print("[0] Backup")
        print("[1] Restore")
        while True:
            try:
                mode = int(input("Select mode (0 or 1): "))
                if mode == 1 or mode == 0:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input.")
        
        blok_avail= self.db.get_groupBY('blok')
        blok=[]
        print("Available Blok:")
        for i in blok_avail:
            print(f"Blok {i[1]:<5}", end=' ')
            blok.append(i[1])
        print()
        while True:
            try:
                Noblok = self.get_input("Enter block number(s) (comma-separated for multiple, or leave blank to pick all): ", is_list=True)
                if Noblok:
                    Noblok = [int(n) for n in Noblok]
                    if max(Noblok)>max(blok):
                        raise ValueError  
                elif not Noblok:
                    Noblok = None
                break
            except ValueError:
                print("Invalid input.")
        piranti_avail=self.db.get_groupBY('tipe_piranti')
        for i in range(len(piranti_avail)):
            print(f'[{i}] {piranti_avail[i][1]}')
        while True:
            try:
                piranti = self.get_input("Enter device type(s) (comma-separated for multiple types, or leave blank to skip): ", is_list=True)
                if piranti:
                    piranti1=[]
                    for i in piranti:
                        #print(piranti_avail[5])
                        if int(i)-1>len(piranti_avail):
                            raise ValueError
                        piranti1.append(piranti_avail[int(i)][1])
                    piranti=piranti1
                    break
                    #print(piranti)
                elif not piranti:
                    piranti = None
                    break
            except (ValueError, TypeError, IndexError):
                print("Invalid input.")
        
        nama_piranti=self.db.get_pirantiInfo(tipe_piranti=piranti,blok=Noblok)
        counter=1
        for i in range(len(nama_piranti)):
            adad=f'[{i}]'
            print(f'{adad:<4} {nama_piranti[i][0]} {nama_piranti[i][1]:<15}',end=' ')
            if counter==3:
                counter=0
                print()
            counter+=1
        print()        
        while True:
            try:
                nama = self.get_input("Enter device name(s) (comma-separated for multiple devices, or leave blank to pick all): ", is_list=True)
                if nama:
                    nama1=[]
                    for i in nama:
                        #print(piranti_avail[5])
                        if int(i)-1>len(nama_piranti):
                            raise ValueError
                        nama1.append(nama_piranti[int(i)][0])
                    nama=nama1
                    break
                    #print(piranti)
                elif not nama:
                    nama = None
                    break
            except (ValueError, TypeError, IndexError):
                print("Invalid input.")
        #ips = self.get_input("Enter IP address(es) (comma-separated for multiple IPs, or leave blank to pick all): ", is_list=True)
        
        if nama:
            Noblok=None
            piranti=None

        print(mode)
        print(nama)
        print(Noblok)
        print(piranti)
        


        print("\nStarting the process...")
        self.manager.processing(mode=mode, nama=nama, ips=None, Noblok=Noblok, piranti=piranti)


if __name__ == "__main__":
    interface = MainInterface()
    interface.run()
