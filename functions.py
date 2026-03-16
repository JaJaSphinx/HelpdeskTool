import webbrowser
import pyperclip
import re
import os
import subprocess
import tempfile



##Custom 
import config

class Functions:
        def url_google_func():
            webbrowser.get('windows-default').open_new_tab(r'https://www.google.com/')
            return 
        def url_hub_func():
            webbrowser.get('windows-default').open_new_tab(r'https://thehub.knightsplc.com/login?returnUrl=%2F')
            return 

        def url_manage_engine():
            webbrowser.get('windows-default').open_new_tab(r'https://knightsplc.sdpondemand.manageengine.eu/app/itdesk/HomePage.do')
            return

        def url_mimecast():
            webbrowser.get('windows-default').open_new_tab(r'https://login-uk.mimecast.com/u/login/?gta=administration&link=administration-dashboard#/login')
            return    

        def url_exchange_admin():
            webbrowser.get('windows-default').open_new_tab(r'https://admin.exchange.microsoft.com/#/')
            return

        def url_maas():
            webbrowser.get('windows-default').open_new_tab(r'https://m2.maas360.com/emc/')
            return
        
        def vm_quickfind():
            webbrowser.open_new(r'\\knights\it\Documentation\VM_Hosts\VMQuickFind.exe - Shortcut')
            return

        def snipping_tool():
            webbrowser.open_new(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Snipping Tool')
            return

        def space_sniffer():
            webbrowser.open_new(r'\\knights\it\Software\Space\SpaceSniffer\SpaceSniffer.exe')
            return

        def wiz_tree():
            webbrowser.open_new(r'\\knights\it\Software\WizTree\WizTree64.exe - Shortcut')
            return

        def putty():
            webbrowser.open_new(r'\\knights\it\Software\PuTTY\putty.exe')
            return

        def partner_import():
            webbrowser.open_new(r'\\knights\it\Software\P4W Tools\P4W File Import Tool\Partner Import Tool v1.1.exe') 
            return
        def partner_import_copy():
            partner_import_url = r"\\knights\it\Software\P4W Tools\P4W File Import Tool"
            pyperclip.copy(partner_import_url)
            return

        def partner_export():
            webbrowser.open_new(r'\\knights\it\Software\P4W Tools\P4W File Export Tool\Partner Export Tool v2.3\Partner Export Tool v2.3.exe')
            return  
        def partner_export_copy():
            partner_url = r"\\knights\it\Software\P4W Tools\P4W File Export Tool\Partner Export Tool v2.3"
            pyperclip.copy(partner_url)
            return
        
        def simple_laps_gui():
            webbrowser.open_new(r'\\knights\it\software\helpdesktool\benb\simplelapsgui.exe')
            return
        def simple_laps_gui_copy():
            simple_laps_gui = r"\\knights\it\software\helpdesktool\benb"
            pyperclip.copy(simple_laps_gui)
            return
        
        def rds_cleanup():
            webbrowser.open_new(r'\\knights\it\Software\RDS_Profile_Cleanup\User Profile Cleanup v1.2 - Copy.exe') 
            return
        def rds_cleanup_copy():
            rds_cleanup_url = r"\\knights\it\team\software\rds_profile_cleanup"
            pyperclip.copy(rds_cleanup_url)
            return
        

        def open_emails(event, email):
            mailto_link = f"mailto:{email}"
            webbrowser.open(mailto_link)


        #Open File Browser 
        def open_file_browser_with_path(base_path, additional_text):
            
            characters = re.findall(r'[A-Za-z]', additional_text)
            updated_path = os.path.join(base_path, *characters, additional_text)

            if os.path.exists(updated_path):
                webbrowser.open_new(updated_path)
                res = "Path Found, scroll down to find security details"
                #return res
            else: 
                res = f"Path does not exist {updated_path}"
                pdoc_result = ""
                return res, pdoc_result
            
        #Print Security to GUI 
            command = ["icacls", updated_path]

            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                if result.returncode !=0:
                    admin_user = input("Enter admin username: ")
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".bat") as tmp_file:
                        tmp_file.write(f'icacls "{updated_path}\n'.encode('utf-8'))
                        tmp_file.write(f'pause\n'.encode('utf-8'))
                        batch_file_path = tmp_file.name
                    runas_command = [
                        "runas",
                        f"/user:{admin_user}"
                        f'cmd /c "{batch_file_path}'
                    ]
                    subprocess.run(runas_command)
                    os.remove(batch_file_path)
                    return res, result.stdout 
                else:      
                    entity_number = additional_text
                    entity_number_str = re.escape(str(entity_number))
                    pattern = rf"{entity_number_str}\b"
                    match = re.search(pattern, result.stdout)
                    if match:
                        useful_data = result.stdout[match.end():].strip()
                        clean_output = "\n".join(line.strip() for line in useful_data.splitlines())
                        return res, clean_output
                    else:
                        clean_output = "Number not found in result"
                        return res, clean_output            
            except subprocess.CalledProcessError as e:
                return f"An Error occurred: {e}"



        def find_rds_connection(user):
            import pyodbc
            if user:
                try:
                    conn_str = f'DRIVER={{SQL Server}};SERVER={config.target_instance};DATABASE={config.target_db};Trusted_Connection=yes;'
                    conn = pyodbc.connect(conn_str, autocommit=True)
                    Ver_cursor = conn.cursor()
                    SQL = f'''
                    SELECT TOP (10)
                    Username,
                    Netbios
                    FROM rds.Session
                    INNER JOIN rds.Target ON Target.Id = Session.TargetId
                    WHERE Username = '{user}' '''
                    Ver_cursor.execute(SQL)
                    res = Ver_cursor.fetchall()
                    if res == []:
                        SQL = f'''
                        SELECT TOP (10)
                        Username,
                        Netbios
                        FROM rds.Session
                        INNER JOIN rds.Target ON Target.Id = Session.TargetId
                        WHERE Username LIKE '%{user}%' '''
                        Ver_cursor.execute(SQL)
                        res = Ver_cursor.fetchall()
                        if res == []:
                            f'''
                            SELECT TOP (10)
                            Username,
                            Netbios
                            FROM rds.Session
                            INNER JOIN rds.Target ON Target.Id = Session.TargetId
                            WHERE Username LIKE '%{user}%' '''
                            if res == []:
                                Ver_cursor.close()
                                res = "No results found"
                                return res 
                        else:
                            res = '\n'.join(str(row) for row in res)
                            Ver_cursor.close()
                            return res
                        
                    else: 
                        res = '\n'.join(str(row) for row in res)
                        Ver_cursor.close()
                        return res
                    
                except Exception as e:
                    res = f"An error occured: {e}"
                    return res
            else: 
                res = "Please Enter a Username..."
                return res
            
        def open_find_open_upd():
            webbrowser.open_new(r'\\knights\it\Software\UPD\FindOpenUPD_v1.0.exe')
            return
        def open_close_open_upd():
            webbrowser.open_new(r'\\knights\it\Software\UPD\CloseUPDFilesv1.3.exe')
            return


