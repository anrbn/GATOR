import cmd, sys, os, importlib, textwrap, concurrent.futures, colorama, platform
from tabulate import tabulate
from itertools import groupby

if platform.system() == "Windows":
    colorama.init()

RESET = colorama.Style.RESET_ALL
BOLD = colorama.Style.BRIGHT
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
MAGENTA = colorama.Fore.MAGENTA
BG_YELLOW = colorama.Back.YELLOW

print(f"""{BOLD}{MAGENTA}


  ▄████  ▄▄▄      ████████▓ ▒█████   ██▀███  
 ██▒ ▀█▒▒████▄    ▓  ██▒ ▓▒▒██▒  ██▒▓██ ▒ ██▒
▒██░▄▄▄░▒██  ▀█▄  ▒ ▓██░ ▒░▒██░  ██▒▓██ ░▄█ ▒
░▓█  ██▓░██▄▄▄▄██ ░ ▓██▓ ░ ▒██   ██░▒██▀▀█▄  
░▒▓███▀▒ ▓█   ▓██▒  ▒██▒ ░ ░ ████▓▒░░██▓ ▒██▒
 ░▒   ▒  ▒▒   ▓▒█░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
  ░   ░   ▒   ▒▒ ░    ░      ░ ▒ ▒░   ░▒ ░ ▒░
░ ░   ░   ░   ▒     ░      ░ ░ ░ ▒    ░░   ░ 
      ░       ░  ░             ░ ░     ░     
{RESET}                                                 
                                    
                ~ from the swamps, to the cloud
""")

class MyCLI(cmd.Cmd):
    prompt = f"\n{BOLD}{MAGENTA}GATOR >{RESET} "
    modules_dir = 'modules'
    modules = {}

    def __init__(self):
        super().__init__()
        self.load_modules()
        self.project_id = None
        self.bucket_name = None
        self.account = None
        self.sadownload = None
        self.rolename = None
        self.roleid = None
        self.roledesc = None
        self.sadisplayname = None

        self.serviceaccountpath = None
        self.active_access_token = None

        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.jobs = {}
        self.service_accounts = {}
        self.access_tokens = {}

    def do_clear(self, args):
        """Clear the screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    def do_exit(self, args):
        """Exit the CLI."""
        return True
    def do_EOF(self, args):
        """Exit the CLI when Ctrl+D is pressed."""
        return True
    def emptyline(self):
        """Do nothing on an empty input line."""
        pass
    def cmdloop(self, intro=None):
            try:
                super().cmdloop(intro)
            except KeyboardInterrupt:
                #print("To exit, type 'exit' or 'Ctrl+D'.")
                self.cmdloop(intro)


    def load_modules(self):
        for root, _, files in os.walk(self.modules_dir):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    module_path = os.path.abspath(root)
                    module_name = file[:-3]
                    full_module_path = ".".join([root.replace(os.sep, "."), module_name])
                    sys.path.insert(0, module_path)
                    try:
                        module = importlib.import_module(full_module_path)
                        self.modules[full_module_path] = module
                    except ImportError:
                        print(f"{RED}- Failed to load module '{full_module_path}' from '{module_path}'.{RESET}")


    """Parameters and Commands"""
    def default(self, line):

        """Parameters:
            set projectid
            set bucket
            set account
            set sadisplayname
            set sadownload
            set rolename
            set roleid
            set roledesc
        """
        """Commands:
            Commands : Authentication 
                list auth serviceaccount
                list auth accesstoken
                import serviceaccount
                import accesstoken
                activate serviceaccount
                activate accesstoken
                delete serviceaccount <serviceaccount> / delete serviceaccount all
                delete accesstoken <access_token> / delete accesstoken all

            Commands : Recon
                recon function-list
                recon storage-tree
                recon custom-roles
                recon serviceaccounts
                recon cloudsql-list

            Commands : Privilege Escalation 
                privesc function-deploy

            Commands : Persistence
                pers service-account-keys

            Commands : Other
                other createroles
                other createsa
            
            Commands : Listings 
                list params / list params all
                list modules
                list jobs
        """

    # Parameters
        command_parts = line.strip().split()
        
        if line.startswith("set projectid "):
            project_id = line[len("set projectid "):].strip()
            self.do_set_projectid(project_id)

        elif line.startswith("set bucket "):
            bucket_name = line[len("set bucket "):].strip()
            self.do_set_bucket(bucket_name)

        elif line.startswith("set account "):
            account = line[len("set account "):].strip()
            self.do_set_account(account)

        elif line.startswith("set sadisplayname "):
            sadisplayname = line[len("set sadisplayname "):].strip()
            self.do_set_sadisplayname(sadisplayname)

        elif line.startswith("set sadownload "):
            sadownload = line[len("set sadownload "):].strip()
            self.do_set_sadownload(sadownload)

        elif line.startswith("set rolename "):
            rolename = line[len("set rolename "):].strip()
            self.do_set_rolename(rolename)

        elif line.startswith("set roleid "):
            roleid = line[len("set roleid "):].strip()
            self.do_set_roleid(roleid)

        elif line.startswith("set roledesc "):
            roledesc = line[len("set roledesc "):].strip()
            self.do_set_roledesc(roledesc)

    # Commands : Authentication  

        elif line.strip() == "list auth serviceaccount":
            self.do_list_auth_serviceaccount("")

        elif line.strip() == "list auth accesstoken":
            self.do_list_auth_accesstoken("")

        elif line.startswith("import serviceaccount "):
            serviceaccount_path = line[len("import serviceaccount "):].strip()
            self.do_import_serviceaccount(serviceaccount_path)

        elif line.startswith("import accesstoken "):
            acc_token = line[len("import accesstoken "):].strip()
            self.do_import_accesstoken(acc_token)

        elif line.startswith("activate serviceaccount "):
            serv_acc_activate = line[len("activate serviceaccount "):].strip()
            self.do_activate_serviceaccount(serv_acc_activate)

        elif line.startswith("activate accesstoken "):
            access_token_activate = line[len("activate accesstoken "):].strip()
            self.do_activate_access_token(access_token_activate)

        elif line.startswith("delete serviceaccount "):
            serviceaccount_path = line[len("delete serviceaccount "):].strip()
            self.do_delete_serviceaccount(serviceaccount_path)

        elif line.startswith("delete accesstoken "):
            acc_token = line[len("delete accesstoken "):].strip()
            self.do_delete_accesstoken(acc_token)

    # Commands : Recon

        elif len(command_parts) == 2 and command_parts[0] == "recon" and command_parts[1] == "function-list":
            self.run_recon_functionlist()
        elif len(command_parts) == 3 and command_parts[0] == "recon" and command_parts[1] == "function-list" and command_parts[2] == "params":
            self.run_recon_functionlist(list_params=True)

        elif len(command_parts) == 2 and command_parts[0] == "recon" and command_parts[1] == "storage-tree":
            self.run_recon_storage_tree()
        elif len(command_parts) == 3 and command_parts[0] == "recon" and command_parts[1] == "storage-tree" and command_parts[2] == "params":
            self.run_recon_storage_tree(list_params=True)

        elif len(command_parts) == 2 and command_parts[0] == "recon" and command_parts[1] == "custom-roles":
            self.run_recon_custom_roles()
        elif len(command_parts) == 3 and command_parts[0] == "recon" and command_parts[1] == "custom-roles" and command_parts[2] == "params":
            self.run_recon_custom_roles(list_params=True)

        elif len(command_parts) == 2 and command_parts[0] == "recon" and command_parts[1] == "serviceaccounts":
            self.run_recon_serviceaccounts()
        elif len(command_parts) == 3 and command_parts[0] == "recon" and command_parts[1] == "serviceaccounts" and command_parts[2] == "params":
            self.run_recon_serviceaccounts(list_params=True)

        elif len(command_parts) == 2 and command_parts[0] == "recon" and command_parts[1] == "cloudsql-list":
            self.run_recon_cloudsqllist()
        elif len(command_parts) == 3 and command_parts[0] == "recon" and command_parts[1] == "cloudsql-list" and command_parts[2] == "params":
            self.run_recon_cloudsqllist(list_params=True)

    # Commands : Privilege Escalation

        elif len(command_parts) == 2 and command_parts[0] == "privesc" and command_parts[1] == "function-deploy":
            self.run_privesc_functiondeploy()
        elif len(command_parts) == 3 and command_parts[0] == "privesc" and command_parts[1] == "function-deploy" and command_parts[2] == "params":
            self.run_privesc_functiondeploy(list_params=True)

    # Commands : Persistence
    
        elif len(command_parts) == 2 and command_parts[0] == "pers" and command_parts[1] == "service-account-keys":
            self.run_persistence_serviceacountkey()
        elif len(command_parts) == 3 and command_parts[0] == "pers" and command_parts[1] == "service-account-keys" and command_parts[2] == "params":
            self.run_persistence_serviceacountkey(list_params=True)

    # Commands : Other

        elif len(command_parts) == 2 and command_parts[0] == "other" and command_parts[1] == "createroles":
            self.run_other_createroles()
        elif len(command_parts) == 3 and command_parts[0] == "other" and command_parts[1] == "createroles" and command_parts[2] == "params":
            self.run_other_createroles(list_params=True)    

        elif len(command_parts) == 2 and command_parts[0] == "other" and command_parts[1] == "createsa":
            self.run_other_createsa()
        elif len(command_parts) == 3 and command_parts[0] == "other" and command_parts[1] == "createsa" and command_parts[2] == "params":
            self.run_other_createsa(list_params=True) 

    # Commands : Listings

        elif line.strip().startswith("list params"):
            args = line.strip().split()[-1] if len(line.strip().split()) > 2 else ""
            self.do_list_params(args)

        elif line.strip().startswith("list modules"):
            args = line[len("list modules"):].strip()
            self.list_modules(args)

        elif line.strip().startswith("list jobs"):
            if line.strip() == "list jobs":
                self.do_list_jobs()
            else:
                job_id = line[len("list jobs "):].strip()
                self.do_job(job_id)
   
        else:
            print(f"{RED}- Unrecognized command: {line}{RESET}")

    """Parameter - Implementation:
        set projectid
        set bucket
        set account
        set sadownload
        set rolename
        set roleid
        set roledesc
        set sadisplayname
    """
    
    def do_set_projectid(self, args):
        self.project_id = args
        print(f"{GREEN}+ Project ID set to: {self.project_id}{RESET}")


    def do_set_bucket(self, args):
        self.bucket_name = args
        print(f"{GREEN}+ Bucket set to: {self.bucket_name}{RESET}")


    def do_set_account(self, args):
        self.account = args
        print(f"{GREEN}+ Service Account set to: {self.account}{RESET}")


    def do_set_sadownload(self, args):
        self.sadownload = args
        print(f"{GREEN}+ Service Account to download set to: {self.sadownload}{RESET}")
        

    def do_set_rolename(self, args):
        self.rolename = args
        print(f"{GREEN}+ Role name set to: {self.rolename}{RESET}")


    def do_set_roleid(self, args):
        self.roleid = args
        print(f"{GREEN}+ Role ID set to: {self.roleid}{RESET}")


    def do_set_roledesc(self, args):
        self.roledesc = args
        print(f"{GREEN}+ Role Description set to: {self.roledesc}{RESET}")


    def do_set_sadisplayname(self, args):
        self.sadisplayname = args
        print(f"{GREEN}+ Service Account Display Name set to: {self.sadisplayname}{RESET}")


    """Commands : Authentication - Implementation:
        import serviceaccount
        import accesstoken
        activate serviceaccount
        activate accesstoken
        delete serviceaccount <serviceaccount> / delete serviceaccount all
        delete accesstoken <access_token> / delete accesstoken all
        list auth serviceaccount
        list auth accesstoken
    """

    def do_import_serviceaccount(self, args):
        if os.path.isfile(args):
            self.service_accounts[args] = args
            print(f"{GREEN}+ Service account '{args}' imported successfully, now you can activate it.{RESET}")
        else:
            print(f"{RED}- File '{args}' does not exist.{RESET}")


    def do_import_accesstoken(self, args):
        self.access_tokens[args] = args
        print(f"{GREEN}+ Access token was imported successfully, now you can activate it.{RESET}")


    def do_activate_serviceaccount(self, args):
        if args in self.service_accounts:
            self.serviceaccountpath = args
            self.active_access_token = None
            print(f"{GREEN}+ Service account '{args}' activated successfully.{RESET}")
            print(f"{GREEN}+ Access token deactivated.{RESET}")
        else:
            print(f"{RED}- Service account '{args}' does not exist in the imports, try to import it first.{RESET}")


    def do_activate_access_token(self, args):
        if args in self.access_tokens:
            self.active_access_token = args
            self.serviceaccountpath = None
            print(f"{GREEN}+ Access token activated successfully.{RESET}")
            print(f"{GREEN}+ Service account deactivated.{RESET}")
        else:
            print(f"{RED}- This Access Token does not exist in the imports, try to import it first.{RESET}")


    def do_delete_serviceaccount(self, args):
        if args.lower() == 'all':
            self.service_accounts = {}
            self.serviceaccountpath = None
            print(f"{GREEN}+ All Service Accounts deleted successfully.{RESET}")
        elif args in self.service_accounts:
            del self.service_accounts[args]
            if args == self.serviceaccountpath:
                self.serviceaccountpath = None
            print(f"{GREEN}+ Service account '{args}' deleted successfully.{RESET}")
        else:
            print(f"{RED}- Unknown service account '{args}'.{RESET}")


    def do_delete_accesstoken(self, args):
        if args.lower() == 'all':
            self.access_tokens = {}
            self.active_access_token = None
            print(f"{GREEN}+ All access tokens deleted successfully.{RESET}")
        elif args in self.access_tokens:
            del self.access_tokens[args]
            if args == self.active_access_token:
                self.active_access_token = None
            print(f"{GREEN}+ Access token deleted successfully.{RESET}")
        else:
            print(f"{RED}- Unknown access token.{RESET}")


    def do_list_auth_serviceaccount(self, args):
        if self.service_accounts:
                print(f"{GREEN}+ Service Accounts:{RESET}")
                for account in self.service_accounts:
                    if account == self.serviceaccountpath:
                        print(f"  {account} {GREEN}[ACTIVE]{RESET}")
                    else:
                        print(f"  {account}")
        else:
            print(f"{GREEN}- No service accounts have been imported yet.{RESET}")


    def do_list_auth_accesstoken(self, args):
        if self.access_tokens:
            print(f"{GREEN}+ Access Tokens:{RESET}")
            for token in self.access_tokens:
                if token == self.active_access_token:
                    print(f"  {token} {GREEN}[ACTIVE]{RESET}\n")                    
                else:
                    print(f"  {token}\n")                    
        else:
            print(f"{GREEN}- No access tokens have been imported yet.{RESET}")


    """Commands : Recon - Implementation:    
        recon function-list
        recon storage-tree
        recon custom-roles
        recon cloudsql-list
        recon serviceaccounts
    """
    
    def run_recon_functionlist(self, list_params=False):
        module_path = "modules.Recon.Cloud Functions.function-list"
        if module_path not in self.modules:
            print(f"{RED}- The module '{module_path}' does not exist.{RESET}")
            return
        try:
            if list_params:
                params = {
                    'project_id': self.project_id,
                }
                table_data = [["projectid", "Mandatory", params["project_id"] or "Not Set", "Sets the Project ID"]]

                headers = ["Parameter", "Type", "Value", "Description"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                return
                    
            if self.project_id is None:
                print(f"{RED}- Project ID not set. Use 'set projectid' command to set the project ID.{RESET}")
                return
            if self.serviceaccountpath is None and self.active_access_token is None:
                print(f"{RED}- No Authentication Mechanism set. Use 'activate serviceaccount' or 'activate accesstoken' command to set an authentication mechanism.{RESET}")
                return
            self.modules[module_path].run_module(self.project_id, self.serviceaccountpath, self.active_access_token)
        except Exception as e:
            print(f"{RED}- Error executing '{module_path}': {e}{RESET}")


    def run_recon_storage_tree(self, list_params=False):
        module_path = "modules.Recon.Cloud Storage.storage-tree"
        if module_path not in self.modules:
            print(f"{RED}- The module '{module_path}' does not exist.{RESET}")
            return
        try:
            if list_params:
                params = {
                    'project_id': self.project_id,
                }
                table_data = [["projectid", "Mandatory", params["project_id"] or "Not Set", "Sets the Project ID"]]

                headers = ["Parameter", "Type", "Value", "Description"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                return
                    
            if self.project_id is None:
                print(f"{RED}- Project ID not set. Use 'set projectid' command to set the project ID.{RESET}")
                return
            if self.serviceaccountpath is None and self.active_access_token is None:
                print(f"{RED}- No Authentication Mechanism set. Use 'activate serviceaccount' or 'activate accesstoken' command to set an authentication mechanism.{RESET}")
                return
            self.modules[module_path].run_module(self.project_id, self.serviceaccountpath, self.active_access_token)
        except Exception as e:
            print(f"{RED}- Error executing '{module_path}': {e}{RESET}")


    def run_recon_custom_roles(self, list_params=False):
        module_path = "modules.Recon.Cloud IAM.custom-roles"
        if module_path not in self.modules:
            print(f"{RED}- The module '{module_path}' does not exist.{RESET}")
            return
        try:
            if list_params:
                params = {
                    'project_id': self.project_id,
                }
                table_data = [["projectid", "Mandatory", params["project_id"] or "Not Set", "Sets the Project ID"]]

                headers = ["Parameter", "Type", "Value", "Description"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                return
                    
            if self.project_id is None:
                print(f"{RED}- Project ID not set. Use 'set projectid' command to set the project ID.{RESET}")
                return
            if self.serviceaccountpath is None and self.active_access_token is None:
                print(f"{RED}- No Authentication Mechanism set. Use 'activate serviceaccount' or 'activate accesstoken' command to set an authentication mechanism.{RESET}")
                return
            self.modules[module_path].run_module(self.project_id, self.serviceaccountpath, self.active_access_token)
        except Exception as e:
            print(f"{RED}- Error executing '{module_path}': {e}{RESET}")


    def run_recon_cloudsqllist(self, list_params=False):
        module_path = "modules.Recon.Cloud SQL.cloudsql-list"
        if module_path not in self.modules:
            print(f"{RED}- The module '{module_path}' does not exist.{RESET}")
            return
        try:
            if list_params:
                params = {
                    'project_id': self.project_id,
                }
                table_data = [["projectid", "Mandatory", params["project_id"] or "Not Set", "Sets the Project ID"]]

                headers = ["Parameter", "Type", "Value", "Description"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                return
                    
            if self.project_id is None:
                print(f"{RED}- Project ID not set. Use 'set projectid' command to set the project ID.{RESET}")
                return
            if self.serviceaccountpath is None and self.active_access_token is None:
                print(f"{RED}- No Authentication Mechanism set. Use 'activate serviceaccount' or 'activate accesstoken' command to set an authentication mechanism.{RESET}")
                return
            self.modules[module_path].run_module(self.project_id, self.serviceaccountpath, self.active_access_token)
        except Exception as e:
            print(f"{RED}- Error executing '{module_path}': {e}{RESET}")


    def run_recon_serviceaccounts(self, list_params=False):
        module_path = "modules.Recon.Cloud IAM.serviceaccounts"
        if module_path not in self.modules:
            print(f"{RED}- The module '{module_path}' does not exist.{RESET}")
            return
        try:
            if list_params:
                params = {
                    'project_id': self.project_id,
                }
                table_data = [["projectid", "Mandatory", params["project_id"] or "Not Set", "Sets the Project ID"]]

                headers = ["Parameter", "Type", "Value", "Description"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                return
                    
            if self.project_id is None:
                print(f"{RED}- Project ID not set. Use 'set projectid' command to set the project ID.{RESET}")
                return
            if self.serviceaccountpath is None and self.active_access_token is None:
                print(f"{RED}- No Authentication Mechanism set. Use 'activate serviceaccount' or 'activate accesstoken' command to set an authentication mechanism.{RESET}")
                return
            self.modules[module_path].run_module(self.project_id, self.serviceaccountpath, self.active_access_token)
        except Exception as e:
            print(f"{RED}- Error executing '{module_path}': {e}{RESET}")


    """Commands : Privilege Escalation - Implementation:    
        privesc function-deploy
    """

    def run_privesc_functiondeploy(self, list_params=False):
        module_path = "modules.Privilege Escalation.Cloud Functions.function-deploy"
        if module_path not in self.modules:
            print(f"{RED}- The module '{module_path}' does not exist.{RESET}")
            return
        try:
            if list_params:
                params = {
                    'project_id': self.project_id,
                    'bucket_name': self.bucket_name,
                    'account': self.account,
                    'sadownload': self.sadownload
                }
                table_data = [["projectid", "Mandatory", params["project_id"] or "Not Set", "Sets the Project ID"],
                            ["bucket", "Mandatory", params["bucket_name"] or "Not Set", "Sets the Bucket Name"],
                            ["account", "Optional", params["account"] or "Not Set", "Sets the underlying Service Account to be used by the Cloud Function"],
                            ["sadownload", "Optional", params["sadownload"] or "Not Set", "Sets the Service Account to download."]]

                headers = ["Parameter", "Type", "Value", "Description"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                return

            if self.project_id is None:
                print(f"{RED}- Project ID not set. Use 'set projectid' command to set the project ID.{RESET}")
                return
            if self.bucket_name is None:
                print(f"{RED}- Bucket not set. Use 'set bucket' command to set a bucket.{RESET}")
                return            
            if self.serviceaccountpath is None and self.active_access_token is None:
                print(f"{RED}- No Authentication Mechanism set. Use 'activate serviceaccount' or 'activate accesstoken' command to set an authentication mechanism.{RESET}")
                return            
            job_id = len(self.jobs) + 1
            print(f"{GREEN}+ Task is running in the background as a Job with ID: {job_id}.{RESET}")
            future = self.executor.submit(self.modules[module_path].run_module, self.project_id, self.serviceaccountpath, self.active_access_token, self.bucket_name, self.account, self.sadownload)
            self.jobs[job_id] = future

        except Exception as e:
            print(f"{RED}- Error executing '{module_path}': {e}{RESET}")


    """Commands : Persistence - Implementation:    
        pers service-account-keys
    """

    def run_persistence_serviceacountkey(self, list_params=False):
        module_path = "modules.Persistence.Cloud IAM.service-account-keys"
        if module_path not in self.modules:
            print(f"{RED}- The module '{module_path}' does not exist.{RESET}")
            return
        try:
            if list_params:
                params = {
                    'project_id': self.project_id,
                    'sadownload': self.sadownload,
                }
                table_data = [["projectid", "Mandatory", params["project_id"] or "Not Set", "Sets the Project ID"],
                            ["sadownload", "Optional", params["sadownload"] or "Not Set", "Sets the Service Account to download."]]

                headers = ["Parameter", "Type", "Value", "Description"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                return

            if self.project_id is None:
                print(f"{RED}- Project ID not set. Use 'set projectid' command to set the project ID.{RESET}")
                return
            if self.serviceaccountpath is None and self.active_access_token is None:
                print(f"{RED}- No Authentication Mechanism set. Use 'activate serviceaccount' or 'activate accesstoken' command to set an authentication mechanism.{RESET}")
                return
            job_id = len(self.jobs) + 1
            print(f"{GREEN}+ Task is running in the background as a Job with ID: {job_id}.{RESET}")
            future = self.executor.submit(self.modules[module_path].run_module, self.project_id, self.serviceaccountpath, self.active_access_token, self.sadownload)
            self.jobs[job_id] = future

        except Exception as e:
            print(f"{RED}- Error executing '{module_path}': {e}{RESET}")


    """ Commands : Other - Implementation:
        other createroles
        other createsa
    """

    def run_other_createroles(self, list_params=False):

        permissions_path = "/etc/GATOR/dependent/permissions.txt" if os.path.exists("/.dockerenv") else "./dependent/permissions.txt"
        module_path = "modules.Other.Cloud IAM.createroles"
        if module_path not in self.modules:
            print(f"{RED}- The module '{module_path}' does not exist.{RESET}")
            return
        try:
            if list_params:
                params = {
                    'project_id': self.project_id,
                    'permissions.txt': None,
                    'rolename': self.rolename,
                    'roleid': self.roleid,
                    'roledesc': self.roledesc
                }
                table_data = [["projectid", "Mandatory", params["project_id"] or "Not Set", "Sets the Project ID"],
                            [permissions_path, "Mandatory", params["permissions.txt"] or "N/A", "Sets the Permission(s) to assign to the Role"],
                            ["rolename", "Optional", params["rolename"] or "Not Set", "Sets the Role Name"],
                            ["roleid", "Optional", params["roleid"] or "Not Set", "Sets the Role ID"],
                            ["roledesc", "Optional", params["roledesc"] or "Not Set", "Sets the Role Description"]]

                headers = ["Parameter", "Type", "Value", "Description"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                return

            if self.project_id is None:
                print(f"{RED}- Project ID not set. Use 'set projectid' command to set the project ID.{RESET}")
                return
            if self.serviceaccountpath is None and self.active_access_token is None:
                print(f"{RED}- No Authentication Mechanism set. Use 'activate serviceaccount' or 'activate accesstoken' command to set an authentication mechanism.{RESET}")
                return            
            job_id = len(self.jobs) + 1
            print(f"{GREEN}+ Task is running in the background as a Job with ID: {job_id}.{RESET}")
            future = self.executor.submit(self.modules[module_path].run_module, self.project_id, self.serviceaccountpath, self.active_access_token, self.rolename, self.roleid, self.roledesc)
            self.jobs[job_id] = future

        except Exception as e:
            print(f"{RED}- Error executing '{module_path}': {e}{RESET}")


    def run_other_createsa(self, list_params=False):

        module_path = "modules.Other.Cloud IAM.createsa"
        if module_path not in self.modules:
            print(f"{RED}- The module '{module_path}' does not exist.{RESET}")
            return
        try:
            if list_params:
                params = {
                    'project_id': self.project_id,
                    'account': self.account,
                    'roleid': self.roleid,
                    'sadisplayname': self.sadisplayname
                }
                table_data = [["projectid", "Mandatory", params["project_id"] or "Not Set", "Sets the Project ID"],
                            ["account", "Mandatory", params["account"] or "Not Set", "Sets the Service Account Name"],
                            ["roleid", "Optional", params["roleid"] or "Not Set", "Sets the Role ID"],
                            ["sadisplayname", "Optional", params["sadisplayname"] or "Not Set", "Sets the Service Account display name"]]

                headers = ["Parameter", "Type", "Value", "Description"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                return

            if self.project_id is None:
                print(f"{RED}- Project ID not set. Use 'set projectid' command to set the project ID.{RESET}")
                return
            if self.serviceaccountpath is None and self.active_access_token is None:
                print(f"{RED}- No Authentication Mechanism set. Use 'activate serviceaccount' or 'activate accesstoken' command to set an authentication mechanism.{RESET}")
                return            
            job_id = len(self.jobs) + 1
            print(f"{GREEN}+ Task is running in the background as a Job with ID: {job_id}.{RESET}")
            future = self.executor.submit(self.modules[module_path].run_module, self.project_id, self.serviceaccountpath, self.active_access_token, self.account, 
            self.roleid, self.sadisplayname)
            self.jobs[job_id] = future

        except Exception as e:
            print(f"{RED}- Error executing '{module_path}': {e}{RESET}")


    """ Commands : Listings - Implementation:
        list params / list params all
        list jobs
        list jobs <id> / job <id>
        list modules 
    """
    
    def do_list_params(self, args):
        if args and args != "all":
            print(f"{RED}- Invalid argument: {args}. Use 'list params' or 'list params all'.{RESET}")
            return
        
        params = {
            'projectid': self.project_id,
            'bucket': self.bucket_name,
            'account': self.account,
            'sadownload': self.sadownload,
            'rolename': self.rolename,
            'roleid': self.roleid,
            'roledesc': self.roledesc,
            'sadisplayname': self.sadisplayname
        }
        table = []
        for key, value in params.items():
            if args == "all":
                table.append([key, value if value is not None else 'default'])
            else:
                if value is not None and value != 'default':
                    table.append([key, value])
        if table:
            print(tabulate(table, headers=["Parameter", "Value"], tablefmt="grid"))
        else:
            if args == "all":
                print(f"{GREEN}- All parameters have default values set.{RESET}")
            else:
                print(f"{GREEN}- All parameters have default values set, if you still wish to see all parameters use 'list params all'.{RESET}") 


    def do_list_jobs(self):
        if not self.jobs:
            print(f"{RED}- No jobs available.{RESET}")
        else:
            table_data = [(job_id, 'Completed' if job_future.done() else 'Running') for job_id, job_future in self.jobs.items()]
            headers = ["Job ID", "Status"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))


    def do_job(self, args):
        try:
            job_id = int(args)
            if job_id in self.jobs:
                job_future = self.jobs[job_id]
                if job_future.done():
                    #print(f"Job {job_id}:")
                    print(job_future.result())
                else:
                    print(f"{BOLD}{YELLOW}! Job {job_id} is not complete yet.{RESET}")
            else:
                print(f"{RED}- Error: Invalid job ID.{RESET}")
        except ValueError:
            print(f"{RED}- Error: You must provide a job ID.{RESET}")


    def list_modules(self, args=None):
        if not self.modules:
            print(f"{RED}- No modules available.{RESET}")
        else:
            if args:
                modules_to_display = {
                    key: module for key, module in self.modules.items() if args.lower() in key.lower()
                }
            else:
                modules_to_display = self.modules

            table_data = [self.get_module_info(key, module) for key, module in modules_to_display.items()]
            table_data.sort(key=lambda x: x[0])
            headers = ["Tactic", "Resource", "Module", "Command", "Description"]

            merged_table_data = []
            for attack_name, group in groupby(table_data, lambda x: x[0]):
                group_list = list(group)
                for i, row in enumerate(group_list):
                    if i == 0:
                        merged_table_data.append([attack_name] + list(row[1:]))
                    else:
                        merged_table_data.append([""] + list(row[1:]))

            print(tabulate(merged_table_data, headers=headers, tablefmt="grid"))


    def get_module_info(self, key, module):
        relpath_parts = os.path.relpath(os.path.dirname(module.__file__), self.modules_dir).split(os.sep)
        attack = relpath_parts[0] if len(relpath_parts) > 0 else "N/A"
        resource = relpath_parts[1] if len(relpath_parts) > 1 else "N/A"
        module_name = key.split(".")[-1]
        wrap_width = 50
        docstring = module.__doc__ or ''
        command = "N/A"
        description = "N/A"
        for line in docstring.split('\n'):
            if line.strip().startswith('Command:'):
                command = textwrap.fill(line.strip().replace('Command:', '').strip(), wrap_width)
            elif line.strip().startswith('Description:'):
                description = textwrap.fill(line.strip().replace('Description:', '').strip(), wrap_width)
        return attack, resource, module_name, command, description


def main():
    MyCLI().cmdloop()

if __name__ == "__main__":
    main()
