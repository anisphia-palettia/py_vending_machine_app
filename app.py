import customtkinter as ctk

from ui.pages.home_page import HomePage
from ui.pages.login_page import LoginPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Vending Machine App")
        self.geometry("900x550")

        container = ctk.CTkFrame(self, corner_radius=0)
        container.pack(side="right", fill="both", expand=True)

        self.pages = {
            "home_page": HomePage(container, controller=self),
            "login_page": LoginPage(container, controller=self),
        }

        self.show_page("home_page")

    def show_page(self, name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(fill="both", expand=True)
