
import customtkinter as ctk
import tkinter as tk
from tkinter import * #WHYYY
from PIL import Image, ImageTk
import webbrowser


from functions import Functions
from HEICConvert import HEIC


class App(ctk.CTk):
    def __init__(self, current_user, hot_links, user_data): 
        super().__init__()
        """
        All GUI for Helpdesk Tool 
        App has 5 tabs:- 
        - Links: Open frequently used links
        - PDOC Search: Open file locations, includes security of file path supplied 
        - AD: Search user account, supplies exact RDS location user is signed into 
        - Solutions: Build your own solution links to solutions you use often, unique to each user. HOT LINKS also available giving current solutions that are currently useful 
        - Contacts: Frequently needed contacts of 3rd parties 
        """
        current_user = current_user
        hot_links = hot_links
        user_data = user_data
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("KNIGHTS HELPDESK TOOL")
        self.geometry('365x365')
        self.wm_attributes("-topmost", 1)
        self.resizable(width=False, height=False)
        self.tab_view = ctk.CTkTabview(master=self, segmented_button_selected_color="#008080")
        self.tab_view.pack(fill="both", expand=True)
        
        #         #Needs revision, expected result is it resets any scrollable frames back to position 0 
        # def reset_scroll_position(event):
        #     self.canvas_4.yview_moveto(0)
        #     self.canvas_2_pdocsearch.yview_moveto(0)

        # self.tab_view.bind("<NotebookTabChanged>", lambda event: reset_scroll_position(event))
        self.tab_1_links = self.tab_view.add("Links")
        self.tab_2_pdocsearch = self.tab_view.add("PDOC Search")
        self.tab_3_apps = self.tab_view.add("Apps")
        self.tab_6_AD = self.tab_view.add("RDS")
        self.tab_4_solutions = self.tab_view.add("Solutions")
        self.tab_2_contacts = self.tab_view.add("Contacts")


        # #Needs revision, expected result is it resets any scrollable frames back to position 0 
        # def reset_scroll_position(event):
        #     self.canvas_4.yview_moveto(0)
        #     self.canvas_2_pdocsearch.yview_moveto(0)

        #Scroll function for mouse wheel
        def on_mouse_wheel(event):
            #canvas.yview_scroll(int(-1 *(event.delta / 120)), "units")
            #self.canvas_1_links.yview_scroll(int(-1 *(event.delta / 120)), "units")
            #self.canvas_4.yview_scroll(int(-1 *(event.delta / 120)), "units")
            if self.tab_2_pdocsearch:
                self.canvas_2_pdocsearch.yview_scroll(int(-1 *(event.delta / 120)), "units")
            if self.tab_4_solutions:
                self.canvas_4.yview_scroll(int(-1 *(event.delta / 120)), "units")



        # Frame in tab 2 pdocsearch for scrolling 
        self.frame_2_pdocsearch = ctk.CTkFrame(master=self.tab_2_pdocsearch)
        self.frame_2_pdocsearch.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas_2_pdocsearch = Canvas(self.frame_2_pdocsearch, bg="grey45")
        self.canvas_2_pdocsearch.pack(side=LEFT, fill="both", expand=True)
        self.scrollbar_2_pdocsearch = ctk.CTkScrollbar(self.frame_2_pdocsearch, orientation="vertical", command=self.canvas_2_pdocsearch.yview)
        self.scrollbar_2_pdocsearch.pack(side=RIGHT, fill="y")
        self.canvas_2_pdocsearch.configure(yscrollcommand=self.scrollbar_2_pdocsearch.set)
        self.canvas_2_pdocsearch.bind("<Configure>", lambda e:
                    self.canvas_2_pdocsearch.configure(scrollregion=self.canvas_2_pdocsearch.bbox("all")))
        self.content_frame_2_pdocsearch = ctk.CTkFrame(self.canvas_2_pdocsearch)# bg_color="transparent", fg_color=("transparent"))
        self.canvas_2_pdocsearch.create_window((0, 0), window=self.content_frame_2_pdocsearch, anchor="nw")

        # Frame in tab 4 solutions for scrolling 
        self.frame_4 = ctk.CTkFrame(master=self.tab_4_solutions)
        self.frame_4.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas_4 = Canvas(self.frame_4, bg="grey15")
        self.canvas_4.pack(side=LEFT, fill="both", expand=True)
        self.scrollbar_4 = ctk.CTkScrollbar(self.frame_4, orientation="vertical", command=self.canvas_4.yview)
        self.scrollbar_4.pack(side=RIGHT, fill="y")
        self.canvas_4.configure(yscrollcommand=self.scrollbar_4.set)
        self.canvas_4.bind("<Configure>", lambda e:
                    self.canvas_4.configure(scrollregion=self.canvas_4.bbox("all")))
        self.content_frame_4 = ctk.CTkFrame(self.canvas_4, bg_color="grey15")# bg_color="transparent", fg_color=("transparent"))
        self.canvas_4.create_window((0, 0), window=self.content_frame_4, anchor="nw")

        #Frame in tab 6 AD 
        self.frame_6_AD = ctk.CTkFrame(master=self.tab_6_AD)
        self.frame_6_AD.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas_6_AD = Canvas(self.frame_6_AD, bg="grey15")
        self.canvas_6_AD.pack(side=LEFT, fill="both", expand=True)
        self.content_frame_6_AD = ctk.CTkFrame(self.canvas_6_AD)# bg_color="transparent", fg_color=("transparent"))
        self.canvas_6_AD.create_window((0, 0), window=self.content_frame_6_AD, anchor="nw")

#########Function Required in GUI for Solutions Tab
        #Show info when hovering
        def show_info(e, info_text):
            global tooltip
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.geometry(f"+{e.x_root + 10}+{e.y_root + 10}")
            tooltip.wm_attributes("-topmost", 1)
            tooltip_label = tk.Label(tooltip, text=info_text, background="dark grey", relief="solid", borderwidth=1)
            tooltip_label.pack()    
        #Hide info when not hovering
        def hide_info(event):
            tooltip.destroy()

        #Tightening the formatting for JSON readability of link data
        def save_links(data):
            with open('user_links.json', 'w') as f:
                f.write('{\n')
                #Hot Links Formatting 
                f.write('   "hot_links": [\n')
                for i, link in enumerate(data["hot_links"]):
                    comma = ',' if i < len(data["hot_links"]) - 1 else '' 
                    f.write(f'      {{"title": "{link["title"]}", "url": "{link["url"]}"}}{comma}\n')
                f.write('   ],\n')
                #User Links Formatting 
                f.write('   "users": {\n')
                for idx, (user, links) in enumerate(data["users"].items()):
                    f.write(f'      "{user}": [\n')
                    for j, link in enumerate(links):
                        comma = ',' if j < len(links) - 1 else '' 
                        f.write(f'          {{"title": "{link["title"]}", "url": "{link["url"]}", "clicks": {link["clicks"]}}}{comma}\n')
                    if idx < len(data["users"]) - 1:
                        f.write('   ],\n')
                    else:
                        f.write('   ]\n')
                f.write('   }\n')

                f.write('}\n')

        # #Load user links from a file
        # def load_links() -> dict:
        #     if os.path.exists('user_links.json'):
        #         with open('user_links.json', 'r') as f:
        #             return json.load(f)
        #     return {"hot_links": [], "users": {}}

        # #Get the current Windows system username
        # def get_current_user() -> str:
        #     try:
        #         current_user = os.getlogin()
        #         print(current_user, "Opened")
        #     except Exception as e: 
        #         #if unable to retrieve username, failover to a generic user
        #         print(f"Error getting system username: {e}")
        #         current_user = "Unknown User"
        #     return current_user
        
        ##data: dict = load_links()
        ## current_user: str = get_current_user()
        ##hot_links: list = data.get("hot_links", [])
        ##user_data: list = data.get("users", {})


        #Add Buttons for Hot Links, ensure not editable like user defined
        def add_hot_link_button(self, tab, title, url):
            self.hot_link_button = ctk.CTkButton(tab, text=title, fg_color="#008080", command=lambda: webbrowser.get('windows-default').open(url))
            self.hot_link_button.pack(side="top", fill="x", pady=1)
        
        #First popup window when + is selected
        def add_link(self, tab, username):
            self.title_dialog = ctk.CTkInputDialog(text="Add Title", title="Title")
            root_x = self.winfo_rootx()
            root_y = self.winfo_rooty()
            root_width = self.winfo_width()
            root_height = self.winfo_height()
            dialog_width = 350
            dialog_height = 250
            dialog_x = root_x + (root_width // 2) - (dialog_width // 2)
            dialog_y = root_y + (root_height // 2) - (dialog_height // 2)
            self.title_dialog.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")
            title = self.title_dialog.get_input()
            #If Title popup has input, next popup window opens
            if title:
                self.url_dialog = ctk.CTkInputDialog(text="Enter Link:", title="Link")
                self.url_dialog.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")
                url = self.url_dialog.get_input()
                self.url_dialog = url
                if url:
                    #If Url popup has input, add to users list in user_links.json file 
                    add_new_link(self, tab, username, title, url)
                    user_data[username].append({'title': title, 'url': url, 'clicks': 0})
                    user_data[username].sort(key=lambda x: x['clicks'], reverse=True)
                    save_links({"hot_links": hot_links, "users": user_data})
                    refresh_tab(self, username)

        #Create new button for new link
        def add_new_link(self, tab, username, title, url, clicks=0):
            global link_button
            print("Add User Links Button Called")
            print(f"{title}")
            self.link_button = ctk.CTkButton(tab, text=title, fg_color="#008080", command=lambda: track_click(username, title, url))
            self.link_button.pack(side="top", fill="x", pady=1)
            self.link_button.clicks = clicks
            print(f"Created Button: {self.link_button}")
            self.link_button.bind("<Button-3>", lambda event: show_context_menu(self, event, username, title, url))
            #Still needs revision - Current issue, when buttons reached bottom of app, scroll does not update causing links to be 'hidden', will resolve when app next opened 
            # self.canvas_4.update_idletasks()
            # self.canvas_4.yview_moveto(1.0)
            # self.frame_4.update_idletasks()

        #Find user, create based on results 
        def create_user_tab(username, links=None):
            if current_user not in user_data: 
                print(f"Current user: {current_user} not found in JSON, creating user...")
                user_data[current_user] = []
                save_links({"hot_links": hot_links, "users": user_data})
            tab = self.content_frame_4 #Name Tab Uniquely, to be changed to default name once inplimented inside real app

            #Create Hot Section Above User Defined Links 
            self.hot_label = ctk.CTkLabel(tab, text="Hot Links", font=("Arial", 14, "bold"))
            self.hot_label.pack(side="top", pady=10, padx=134, expand=True)
            for hot_link in hot_links:
                add_hot_link_button(self, tab, hot_link['title'], hot_link['url'])
            #Create User Defined Links Section 
            self.user_label = ctk.CTkLabel(tab, text="Your Links", font=("Arial", 12, "bold"))
            self.user_label.pack(side="top", pady=(5, 0))
            self.add_link_button = ctk.CTkButton(tab, text="+", fg_color="transparent", command=lambda: add_link(self, tab, username))
            self.add_link_button.pack(side="top", pady=(0, 5))
            self.add_link_button.bind("<Enter>", lambda e, info="Add New Link": show_info(e, info))
            self.add_link_button.bind("<Leave>", hide_info)
            for link_data in links or []:
                add_new_link(self, tab, username, link_data['title'], link_data['url'], link_data.get('clicks', 0))

        # Populate tabs with saved data
        if current_user in user_data:
                    sorted_links = sorted(user_data[current_user], key=lambda x: x['clicks'], reverse=True)
                    create_user_tab(current_user, sorted_links)
        else:
                    create_user_tab(current_user, [])

        #Track User Defined Links clicks (ensure most clicked is sorted by DESC order)
        def track_click(username, title, url):
            webbrowser.get('windows-default').open(url)
            for link_data in user_data[username]:
                if link_data['title'] == title and link_data['url'] == url:
                    link_data['clicks'] += 1
                    break 
            user_data[username].sort(key=lambda x: x['clicks'], reverse=True)
            save_links({"hot_links": hot_links, "users": user_data})
            refresh_tab(self, username)

        #Right Click Button, show opens Edit Link Title or Remove Link 
        def show_context_menu(self, event, username, old_title, url):
            self.menu = tk.Menu(tearoff=0)
            self.menu.add_command(label="Edit Title", command=lambda: edit_link_title(username, old_title, url))
            self.menu.add_command(label="Remove Link", command=lambda: confirm_remove_link(username, old_title, url))
            self.menu.post(event.x_root, event.y_root)

        #Edit link title, supply with new title, update
        def edit_link_title(username, old_title, url):
            new_title_dialog = ctk.CTkInputDialog(title="Edit Title", text="Enter new title")
            root_x = self.winfo_rootx()
            root_y = self.winfo_rooty()
            root_width = self.winfo_width()
            root_height = self.winfo_height()
            dialog_width = 350
            dialog_height = 250
            dialog_x = root_x + (root_width // 2) - (dialog_width // 2)
            dialog_y = root_y + (root_height // 2) - (dialog_height // 2)
            new_title_dialog.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")
            new_title = new_title_dialog.get_input()

            if new_title:
                for link_data in user_data[username]:
                    if link_data['title'] == old_title and link_data ['url'] == url:
                        link_data['title'] = new_title
                        refresh_tab(self, username)
                        break

                save_links({"hot_links": hot_links, "users": user_data})

        #Remove link entirely, prompt "Are you sure?" before deleting
        def confirm_remove_link(username, title, url):
            answer = tk.messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove the following link '{title}'")
            if answer:
                    user_data[username] = [link for link in user_data[username] if link['title'] != title or link['url'] != url]
                    save_links({"hot_links": hot_links, "users": user_data})
                    refresh_tab(self, username)

        #The beast function, it's making sure any changes made (add, edit, delete) updates tab accordingly
        def refresh_tab(self, username):
            tab = self.content_frame_4

            for widget in tab.winfo_children():
                widget.destroy()

            self.hot_label = ctk.CTkLabel(tab, text="Hot Links", font=("Arial", 14, "bold"))
            self.hot_label.pack(side="top", pady=10, padx=134, expand=True)

            for hot_link in hot_links:
                add_hot_link_button(self, tab, hot_link['title'], hot_link['url'])

            self.user_label = ctk.CTkLabel(tab, text="Your Links", font=("Arial", 12, "bold"))
            self.user_label.pack(side="top", pady=(5, 0))
            self.add_link_button = ctk.CTkButton(tab, text="+", fg_color="transparent", command=lambda: add_link(self, tab, username))
            self.add_link_button.pack(side="top", pady=(0, 5))
                
            for link_data in user_data[username]:
                add_new_link(self, tab, username, link_data['title'], link_data['url'], link_data['clicks'])
        



 
        self.google_image = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\Google2.png')
        self.google_image = ImageTk.PhotoImage(self.google_image)
        self.hub_image = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\Menu.png')
        self.hub_image = ImageTk.PhotoImage(self.hub_image)
        self.rds_icon = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\Knights-RDS.png')
        self.rds_icon = ImageTk.PhotoImage(self.rds_icon)
        self.manage_engine_image = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\Manage Engine1.png')
        self.manage_engine_image = ImageTk.PhotoImage(self.manage_engine_image)
        self.mimecast_image = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\Mimecast_Logo.png')
        self.mimecast_image = ImageTk.PhotoImage(self.mimecast_image)
        self.exchange_image = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\Exchange.png')
        self.exchange_image = ImageTk.PhotoImage(self.exchange_image)
        self.maas_image = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\Maas360.png')
        self.maas_image = ImageTk.PhotoImage(self.maas_image)
        self.info_image = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\help1.ico')
        self.info_image = ImageTk.PhotoImage(self.info_image)
        self.info_image_rds = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\help2.ico')
        self.info_image_rds = ImageTk.PhotoImage(self.info_image_rds)
        self.copy_image = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\copy3.png')
        self.copy_image = ImageTk.PhotoImage(self.copy_image)
        self.locked_image = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\lockedR.png')
        self.locked_image = ImageTk.PhotoImage(self.locked_image)
        self.unlocked_image = Image.open(r'\\knights\it\Team\Lewis H\py\Helpdesk Tool v1.0\_Icon\unlocked.png')
        self.unlocked_image = ImageTk.PhotoImage(self.unlocked_image)
        self.url_hub = ctk.CTkButton(master=self.tab_1_links, text="The Hub", image=self.hub_image, command=Functions.url_hub_func)# height = 10, width = 10)
        self.url_hub.grid(row=0, column=0, padx=(15, 10), pady=10)
        self.url_manage_engine = ctk.CTkButton(master=self.tab_1_links, text="   Manage\n   Engine", image=self.manage_engine_image, command=Functions.url_manage_engine)
        self.url_manage_engine.grid(row=0, column=1, padx=(15, 12), pady=10)
        self.url_mimecast = ctk.CTkButton(master=self.tab_1_links, text="Mimecast", image=self.mimecast_image, command=Functions.url_mimecast)
        self.url_mimecast.grid(row=1, column=1, padx=(15, 10), pady=10)
        self.url_exchange_admin = ctk.CTkButton(master=self.tab_1_links, text="Exchange\nAdmin", image=self.exchange_image, command=Functions.url_exchange_admin)
        self.url_exchange_admin.grid(row=1, column=0, padx=(15, 12), pady=10)
        self.url_maas = ctk.CTkButton(master=self.tab_1_links, text="Maas 360", image=self.maas_image, command=Functions.url_maas)
        self.url_maas.grid(row=2, column=0, padx=(15, 10), pady=10)
        self.url_google = ctk.CTkButton(master=self.tab_1_links, text="   Google", image=self.google_image, command=Functions.url_google_func)
        self.url_google.grid(row=2, column=1, padx=(15, 12), pady=10)

        def open_file_browser_with_path_get(base_path):
            additional_text = self.pdoc_search_entry.get()
            update_pdoc_search_label, update_pdoc_security_result = Functions.open_file_browser_with_path(base_path, additional_text)
            self.pdoc_search_result.configure(text=f"{update_pdoc_search_label}")
            self.pdoc_security_result.delete("1.0", tk.END)
            self.pdoc_security_result.insert(tk.END, f"{update_pdoc_security_result}")





        #PDOC Search 
        self.pdoc_search_entry = ctk.CTkEntry(master=self.content_frame_2_pdocsearch, placeholder_text="Entity Number...", width=334)
        self.pdoc_search_entry.grid(row=3, columnspan=2, pady=5)
        self.pdoc_search_result = ctk.CTkLabel(master=self.content_frame_2_pdocsearch, text="", text_color="white")
        self.pdoc_search_result.grid(row=4, columnspan=2)
        self.pdoc_security_result = ctk.CTkTextbox(master=self.content_frame_2_pdocsearch, width=300)
        self.pdoc_security_result.grid(row=20, columnspan=2)


        base_paths = [r"\\kni-pdoc-002\docs", r"\\kni-pd-024-2\docs", r"\\kni-pd-024-1\docs", r"\\kni-pdoc-023-2\docs", r"\\kni-pdoc-023-1\docs", r"\\kni-pdoc-022-3\docs", r"\\kni-pdoc-022-2\docs", r"\\kni-pdoc-022-1\docs", r"\\kni-pdoc-021\docs", r"\\kni-pdoc-020\docs", r"\\kni-pdoc-019\docs", r"\\kni-pdoc-017\docs"]


        for i, base_path in enumerate(base_paths):
            button = ctk.CTkButton(self.content_frame_2_pdocsearch, text=f"{base_path}", command=lambda bp=base_path: open_file_browser_with_path_get(bp))
                                #command=lambda bp=base_path:
                                #Functions.open_file_browser_with_path(bp))
            button.grid(row=5 + i // 2 + 1, column=i % 2, padx=5, pady=5)


        def show_tooltip(event, text):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.wm_attributes("-topmost", 1)
            label = tk.Label(tooltip, text=text, background="dark grey", relief="solid", borderwidth=1)
            label.pack()

            event.widget.tooltip = tooltip

        def hide_tooltip(event):
            if hasattr(event.widget, 'tooltip'):
                event.widget.tooltip.destroy()
                del event.widget.tooltip

        def temp_toplevel_file_import():
            self.toplevel = ctk.CTkInputDialog(text="This app is currently unavailable...", title="App Unavailable")
            root_x = self.winfo_rootx()
            root_y = self.winfo_rooty()
            root_width = self.winfo_width()
            root_height = self.winfo_height()
            dialog_width = 350
            dialog_height = 250
            dialog_x = root_x + (root_width // 2) - (dialog_width // 2)
            dialog_y = root_y + (root_height // 2) - (dialog_height // 2)
            self.toplevel.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")
            
        #Apps Left Side (Column 0)
        self.app_vm_quickfind = ctk.CTkButton(master=self.tab_3_apps, text="VM Quick Find", command=Functions.vm_quickfind)
        self.app_vm_quickfind.grid(row=0, column=0, padx=15, pady=10)
        self.app_snipping_tool = ctk.CTkButton(master=self.tab_3_apps, text="Snipping Tool", command=Functions.snipping_tool)
        self.app_snipping_tool.grid(row=1, column=0, padx=15, pady=10)
        self.app_space_sniffer = ctk.CTkButton(master=self.tab_3_apps, text="Space Sniffer", command=Functions.space_sniffer)
        self.app_space_sniffer.grid(row=2, column=0, padx=15, pady=10)
        self.app_wiz_tree = ctk.CTkButton(master=self.tab_3_apps, text="WizTree", command=Functions.wiz_tree)
        self.app_wiz_tree.grid(row=3, column=0, padx=15, pady=10)
        self.app_putty = ctk.CTkButton(master=self.tab_3_apps, text="PuTTY", command=Functions.putty)
        self.app_putty.grid(row=4, column=0, padx=15, pady=10)

        #Custom Apps Right Side (Column 1)
        self.app_partner_export_copy = ctk.CTkButton(master=self.tab_3_apps, text="", image=self.copy_image, height=0.1, width=0.1, fg_color="transparent", hover_color="#023E8A", command=Functions.partner_export_copy)
        self.app_partner_export_copy.place(rely=0.02, relx=1.0, anchor="ne", x=5, y=0)
        self.app_partner_export_copy.bind("<Enter>", lambda event: show_tooltip(event, "Copy file path to clipboard"))
        self.app_partner_export_copy.bind("<Leave>", hide_tooltip)
        self.app_partner_export = ctk.CTkButton(master=self.tab_3_apps, text="Partner Export Tool", command=Functions.partner_export)
        self.app_partner_export.grid(row=0, column=1, padx=10, pady=10)

        self.app_rds_cleanup_copy = ctk.CTkButton(master=self.tab_3_apps, text="", image=self.copy_image, height=0.1, width=0.1, fg_color="transparent", hover_color="#023E8A", command=Functions.rds_cleanup_copy)
        self.app_rds_cleanup_copy.place(rely=0.17, relx=1.0, anchor="ne", x=5, y=0)
        self.app_rds_cleanup_copy.bind("<Enter>", lambda event: show_tooltip(event, "Copy file path to clipboard"))
        self.app_rds_cleanup_copy.bind("<Leave>", hide_tooltip)
        self.app_rds_cleanup = ctk.CTkButton(master=self.tab_3_apps, text="RDS Cleanup Tool", command=Functions.rds_cleanup)
        self.app_rds_cleanup.grid(row=1, column=1, padx=10, pady=10)

        self.app_file_import = ctk.CTkButton(master=self.tab_3_apps, text="Partner Import Tool", command=lambda: temp_toplevel_file_import())#Change to Functions.partner_import
        self.app_file_import.grid(row=2, column=1, padx=10, pady=10)
        self.app_file_import_copy = ctk.CTkButton(master=self.tab_3_apps, text="", image=self.copy_image, height=0.1, width=0.1, fg_color="transparent", hover_color="#023E8A")
        self.app_file_import_copy.place(rely=0.32, relx=1.0, anchor="ne", x=5, y=0)
        self.app_file_import_copy.bind("<Enter>", lambda event: show_tooltip(event, "Copy file path to clipboard"))
        self.app_file_import_copy.bind("<Leave>", hide_tooltip)

        self.simple_laps_gui = ctk.CTkButton(master=self.tab_3_apps, text="Simple Laps GUI", command=Functions.simple_laps_gui)
        self.simple_laps_gui.grid(row=3, column=1, padx=10, pady=10)
        self.simple_laps_gui_copy = ctk.CTkButton(master=self.tab_3_apps, text="", image=self.copy_image, height=0.1, width=0.1, fg_color="transparent", hover_color="#023E8A", command=Functions.simple_laps_gui_copy)
        self.simple_laps_gui_copy.place(rely=0.47, relx=1.0, anchor="ne", x=5, y=0)
        self.simple_laps_gui_copy.bind("<Enter>", lambda event: show_tooltip(event, "Copy file path to clipboard"))
        self.simple_laps_gui_copy.bind("<Leave>", hide_tooltip)

        self.convertheic = ctk.CTkButton(master=self.tab_3_apps, text="Convert HEIC", command= lambda:heic_input()) #command= lambda: HEIC.run_app(heic_dir=r'C:\Users\a-lhat\Desktop\PyHEIC2JPG-master'))
        self.convertheic.grid(row=4, column=1, padx=10, pady=10)

        def heic_input():
            self.heic_inputpath = ctk.CTkInputDialog(text="Enter File Path:", title="HEIC File Path")
           # self.heic_inputpath.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")
            heic_path = self.heic_inputpath.get_input()
            self.heic_inputpath = heic_path
            heic_output = HEIC.run_app(heic_dir=heic_path)
            self.popup = ctk.CTkToplevel()
            self.popup.geometry("400x300")
            self.popup.title("HEIC to JPG")
            self.popup.grab_set() #Make popup modal? 
            self.popup.wm_attributes("-topmost", 1)
            self.info_label = ctk.CTkLabel(self.popup, text="")
            self.info_label.pack(pady=5)
            self.info_process = ctk.CTkTextbox(master=self.popup, width=350)
            self.info_process.pack(pady=5)
            self.info_process.insert(tk.END, f"{heic_output}")
    
            print(f'Finished please see results: {heic_output}')





        def rds_connection_entry_get():
            print("Function Called for User get")
            get_user = self.rds_connection_entry.get()
            update_connection_label = Functions.find_rds_connection(get_user)
            self.rds_result_label.configure(text=f"{update_connection_label}")
   
        self.rds_connection_label = ctk.CTkLabel(master=self.content_frame_6_AD, text="Find Open RDS Connection", text_color="grey80", font=('CTkFont', 14), width=340)
        self.rds_connection_label.grid(row=1, columnspan=2)
        self.rds_connection_entry = ctk.CTkEntry(master=self.content_frame_6_AD, placeholder_text="Enter Username...", font=('CTkFont', 14), width=300)
        self.rds_connection_entry.grid(row=2, columnspan=2)
        self.rds_connection_button = ctk.CTkButton(master=self.content_frame_6_AD, text="Find", fg_color="#008080", command=lambda: rds_connection_entry_get())#Functions.find_rds_connection())
        self.rds_connection_button.grid(row=4, columnspan=2, pady=(5, 10))
        self.rds_result_label = ctk.CTkLabel(master=self.content_frame_6_AD, text="")
        self.rds_result_label.grid(row=3, columnspan=2)
        self.filler = ctk.CTkLabel(master=self.content_frame_6_AD, text="", height=0.01)
        self.filler.grid(row=5, columnspan=2)

        self.find_open_upd = ctk.CTkButton(master=self.content_frame_6_AD, text="Find Open UPD", fg_color="#008080", command=lambda:Functions.open_find_open_upd())
        self.find_open_upd.grid(row=6, column=0, padx=10,pady=(100, 200))

        self.close_open_upd = ctk.CTkButton(master=self.content_frame_6_AD, text="Close Open UPD", fg_color="#008080", command=lambda:Functions.open_close_open_upd())
        self.close_open_upd.grid(row=6, column=1, padx=10, pady=(100, 200))


        # self.notes_button = ctk.CTkButton(self.bottom_frame, text="NOTES", corner_radius=50, border_width=1, font=('Bahnschrift', 15), fg_color='grey20', border_color='grey15', hover_color='grey30', command=autofil_date_time)
        # self.notes_button.pack(pady=10, padx=112)
        # self.notes_button.bind("<Enter>", lambda event: show_tooltip(event, "Copy 'DATE - TIME -' onto screen"))
        # self.notes_button.bind("<Leave>", hide_tooltip)

        self.contact_vision = ctk.CTkLabel(self.tab_2_contacts, text="Vision", font=("CTkFont", 14, "bold"))
        self.contact_vision.grid(row=1, column=0, padx=(0, 15), sticky="w")
        self.contact_vision_tele = ctk.CTkTextbox(self.tab_2_contacts, height=0, width=110)# font=("CTkFont", 12))# text="01992 509555")# anchor="center")
        self.contact_vision_tele.insert("-3.0", "01992 509555")
        self.contact_vision_tele.configure(fg_color="grey13", text_color="white", border_width=0, state="disabled")
        self.contact_vision_tele.grid(row=1, column=1, padx=0, pady=(0, 0), sticky="w")
        #contact_vision_tele.place(anchor='w')
        # contact_vision_web = ctk.CTkLabel(content_frame_contacts, text="https://visionplc.customerportal.online/", anchor="n")
        # contact_vision_web.grid(row=2, column=1, pady=(0, 0), sticky="w")
        self.contact_vision_email = ctk.CTkLabel(self.tab_2_contacts, text="  clientservices@visionplc.co.uk", text_color="#4286f4", anchor="n", cursor="hand2")
        self.contact_vision_email.grid(row=2, column=1, padx=(0, 60), pady=(0, 0), sticky="w")
        self.contact_vision_email.bind("<Button-1>", lambda event: Functions.open_emails(event, "clientservices@visionplc.co.uk"))
        self.contact_cvad = ctk.CTkLabel(self.tab_2_contacts, text="CVAD", font=("CTkFont", 14, "bold"))
        self.contact_cvad.grid(row=3, column=0, sticky="w")
        self.contact_cvad_tele = ctk.CTkTextbox(self.tab_2_contacts, height=0, width=110)# text="0333 772 9544")
        self.contact_cvad_tele.insert("0.0", "0333 772 9544")
        self.contact_cvad_tele.configure(fg_color="grey13", text_color="white", border_width=0, state="disabled")
        self.contact_cvad_tele.grid(row=3, column=1, sticky="w")
        self.contact_cvad_email = ctk.CTkLabel(self.tab_2_contacts, text="  service@completevoiceanddata.com", text_color="#4286f4", anchor="n", cursor="hand2")
        self.contact_cvad_email.grid(row=4, column=1, padx=(0, 60), pady=(0, 0), sticky="w")
        self.contact_cvad_email.bind("<Button-1>", lambda event: Functions.open_emails(event, "service@completevoiceanddata.com"))
        self.contact_anza = ctk.CTkLabel(self.tab_2_contacts, text="Anza", font=("CTkFont", 14, "bold"))
        self.contact_anza.grid(row=5, column=0, sticky="w")
        self.contact_anza_tele = ctk.CTkTextbox(self.tab_2_contacts, height=0, width=120)# text="+91 7059845862")
        self.contact_anza_tele.insert("0.0", "+91 7059845862")
        self.contact_anza_tele.configure(fg_color="grey13", text_color="white", border_width=0, state="disabled")
        self.contact_anza_tele.grid(row=5, column=1, sticky="w")
        self.contact_anza_email = ctk.CTkLabel(self.tab_2_contacts, text="  prashantmaharaj@anzaservicesllp.com", text_color="#4286f4", anchor="n", cursor="hand2")
        self.contact_anza_email.grid(row=6, column=1, padx=(0, 60), pady=(0, 0), sticky="w")
        self.contact_anza_email.bind("<Button-1>", lambda event: Functions.open_emails(event, "prashantmaharaj@anzaservicesllp.com"))
        self.contact_ic = ctk.CTkLabel(self.tab_2_contacts, text="IC", font=("CTkFont", 14, "bold"))
        self.contact_ic.grid(row=7, column=0, sticky="w")
        self.contact_ic_tele = ctk.CTkTextbox(self.tab_2_contacts, height=0, width=110)# text="01782 667766")
        self.contact_ic_tele.insert("0.0", "01782 667766")
        self.contact_ic_tele.configure(fg_color="grey13", text_color="white", border_width=0, state="disabled")
        self.contact_ic_tele.grid(row=7, column=1, sticky="w")
        self.contact_ic_email = ctk.CTkLabel(self.tab_2_contacts, text="  support@ic.co.uk", text_color="#4286f4", anchor="n", cursor="hand2")
        self.contact_ic_email.grid(row=8, column=1, padx=(0, 60), pady=(0, 0), sticky="w")
        self.contact_ic_email.bind("<Button-1>", lambda event: Functions.open_emails(event, "support@ic.co.uk"))
        self.contact_infotrack = ctk.CTkLabel(self.tab_2_contacts, text="Infotrack", anchor="n", font=("CTkFont", 14, "bold"))
        self.contact_infotrack.grid(row=9, column=0, sticky="w")
        self.contact_infotrack_email = ctk.CTkLabel(self.tab_2_contacts, text="  helpdesk@infotrack.co.uk", text_color="#4286f4", anchor="n", cursor="hand2")
        self.contact_infotrack_email.grid(row=9, column=1, padx=(0, 60), pady=(0, 0), sticky="w")
        self.contact_infotrack_email.bind("<Button-1>", lambda event: Functions.open_emails(event, "helpdesk@infotrack.co.uk"))
        self.contact_advanced = ctk.CTkLabel(self.tab_2_contacts, text="Advanced", anchor="n", font=("CTkFont", 14, "bold"))
        self.contact_advanced.grid(row=10, column=0, pady=(10, 0), sticky="w")
        self.contact_advanced_tele = ctk.CTkTextbox(self.tab_2_contacts, height=0, width=110)
        self.contact_advanced_tele.insert("0.0", "0330 343 5000")
        self.contact_advanced_tele.configure(fg_color="grey13", text_color="white", border_width=0, state="disabled")
        self.contact_advanced_tele.grid(row=10, column=1, padx=(0, 60), pady=(0, 0), sticky="w")
        
        ### REVIEW (Why is this referencing canvas_2_contacts)
        #Force scroll wheel using Mouse for Tabs RDP 
        
        #self.canvas_4.bind_all("<MouseWheel>", on_mouse_wheel_2)
        self.bind_all("<MouseWheel>", on_mouse_wheel)


    #Need to get this to update canvas scroller so bottom option is not missed when adding links (also inside create_new_link function)
        self.canvas_4.update_idletasks()
        self.canvas_4.yview_moveto(1.0)
        self.frame_4.update_idletasks()
        #frame_4.yview_moveto(1.0)
        



# if __name__ == "__main__":


    
