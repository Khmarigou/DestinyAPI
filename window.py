import urllib.request
import sqlite

from PIL import Image
from customtkinter import *


class App(CTk):
    def __init__(self):
        super().__init__()

        self.characters = []

        # Creating window
        self.title("Khmarigou's DIM.py")
        self.geometry("800x600")
        set_appearance_mode("system")
        self.after(0, lambda: self.wm_state('zoomed'))

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = CTkFrame(master=self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = CTkLabel(master=self.navigation_frame,
                                               text="Khmarigou's DIM",
                                               compound="left",
                                               font=CTkFont(size=15, weight="bold")
                                               )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.authentification_button = CTkButton(self.navigation_frame,
                                                 height=40,
                                                 border_spacing=10,
                                                 text="Authentification",
                                                 fg_color="transparent",
                                                 text_color=("gray10", "gray90"),
                                                 hover_color=("gray70", "gray30"),
                                                 anchor="w",
                                                 command=self.authentification_button_event)
        self.authentification_button.grid(row=1, column=0, sticky="ew")

        self.inventory_button = CTkButton(self.navigation_frame,
                                                    height=40,
                                                    border_spacing=10,
                                                    text="Inventory",
                                                    fg_color="transparent",
                                                    text_color=("gray10", "gray90"),
                                                    hover_color=("gray70", "gray30"),
                                                    anchor="w",
                                                    command=self.inventory_button_event)
        self.inventory_button.grid(row=2, column=0, sticky="ew")

        self.frames = []

        # Create Authentiication frame
        self.authentification_frame = CTkFrame(master=self)
        self.authentification_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frames.append({"frame":self.authentification_frame, "name":"authentification", "button":self.authentification_button})

        self.authentification_label = CTkLabel(master=self.authentification_frame,
                                               text="Authentification",
                                               compound="left",
                                               font=CTkFont(size=15, weight="bold")
                                               )
        self.authentification_label.grid(row=0, column=0, padx=20, pady=20)

        # Create Inventory frame
        self.inventory_frame = CTkScrollableFrame(master=self)
        self.inventory_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frames.append({"frame":self.inventory_frame, "name":"inventory", "button":self.inventory_button})

        # Select default frame
        self.select_frame_by_name("inventory")

        self.curDataBase = sqlite.getDataBase("fr")


    def select_frame_by_name(self, name):
        for frame in self.frames:
            if frame["name"] == name:
                frame["frame"].grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
                frame["button"].configure(fg_color=("gray75", "gray25"))
            else:
                frame["frame"].grid_forget()
                frame["button"].configure(fg_color="transparent")

    def authentification_button_event(self):
        self.select_frame_by_name("authentification")

    def inventory_button_event(self):
        self.select_frame_by_name("inventory")

    def addCharacter(self, character):
        self.characters.append(character)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        urllib.request.urlretrieve(
            'https://www.bungie.net' + character.emblemBackgroundPath,
            "./images/char_" + character.id + "_emblemBackground.png")
        imageEmblemBackground = CTkImage(Image.open(os.path.join(image_path, "char_" + character.id + "_emblemBackground.png")), size=(200, 40))
        emblemPath1 = CTkLabel(master=self.inventory_frame,
                                image=imageEmblemBackground,
                                text="",
                                compound="left",
                                font=CTkFont(size=15, weight="bold")
                                )
        emblemPath1.grid(row=0, column=len(self.characters), padx=20, pady=20)

        charlight = CTkLabel(master=self.inventory_frame,
                                  text=character.light,
                                  compound="left",
                                  font=CTkFont(size=15, weight="bold"),
                                  bg_color="transparent"
                                  )
        charlight.grid(row=0, column=len(self.characters), padx=20, pady=20)
        i = 1
        for item in character.getEquipement():
            itemProperties = sqlite.getItem(item.get("itemHash"), self.curDataBase)
            CTkLabel(master=self.inventory_frame,
                        text=itemProperties.get("displayProperties").get("name"),
                        compound="left",
                        font=CTkFont(size=15, weight="bold"),
                        bg_color="transparent"
                        ).grid(row=i, column=len(self.characters), padx=10, pady=10)
            i += 1
