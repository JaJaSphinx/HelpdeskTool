import customtkinter as ctk
import threading 
import time 
import os
import json
from PIL import Image

#Custom
from gui import App



class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        width = 300
        height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.title("Loading")
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.overrideredirect(True)
        self.loading_label = ctk.CTkLabel(self, text="Loading...", fg_color="transparent")
        self.loading_label.pack(expand=True)
        self.load_image = Image.open(r'\\knights\it\Team\Lewis H\py\py\SplashScreen1.png')
        self.load_image = ctk.CTkImage(self.load_image, size=(300,200))
        self.show_image = ctk.CTkLabel(self, text="", image=self.load_image)
        self.show_image.pack(expand=True) 

        threading.Thread(target=self.load_main_app, daemon=True).start()

    def load_main_app(self):

        #time.sleep(5)          
        #Load user links from a file
        def load_links() -> dict:
            if os.path.exists('user_links.json'):
                with open('user_links.json', 'r') as f:
                    return json.load(f)
            return {"hot_links": [], "users": {}}
        
        
        #Get the current Windows system username
        def get_current_user() -> str:
            try:
                getcurrent_user = os.getlogin()
                print(getcurrent_user, "Opened")
            except Exception as e: 
                #if unable to retrieve username, failover to a generic user
                print(f"Error getting system username: {e}")
                getcurrent_user = "Unknown User"
            return getcurrent_user


        data: dict = load_links()
        self.loading_label.configure(text="Getting Username...")
        time.sleep(0.5)
        current_user: str = get_current_user()
        self.loading_label.configure(text=f"Getting Username... {current_user}")
        time.sleep(0.5)
        self.loading_label.configure(text=f"Building {current_user}'s tabs...")
        time.sleep(0.3)
        hot_links: list = data.get("hot_links", [])
        user_data: dict = data.get("users", {})
        self.loading_label.configure(text=f"Building {current_user}'s tabs... OK")
        time.sleep(0.3)
        self.after(0, lambda: self.start_main_app(current_user, hot_links, user_data))


    def start_main_app(self, current_user, hot_links, user_data):
        self.destroy()
        app = App(current_user, hot_links, user_data)
        app.mainloop()

if __name__ == "__main__":
    splash = SplashScreen()
    splash.mainloop()