import customtkinter as ctk

from ui.pages.coin_page import CoinPage
from ui.pages.login_page import LoginPage
from ui.pages.shop_page import ShopPage
from ui.pages.admin_page import AdminPage
from ui.pages.create_product_page import CreateProductPage
from ui.pages.update_product_page import UpdateProductPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Vending Machine App")
        self.geometry("900x550")

        container = ctk.CTkFrame(self, corner_radius=0)
        container.pack(side="right", fill="both", expand=True)

        self.pages = {
            "login_page": LoginPage(container, controller=self),
            "shop_page": ShopPage(container, controller=self),
            "coin_page": CoinPage(container, controller=self),
            "admin_page": AdminPage(container, controller=self),
            "create_product_page": CreateProductPage(container, controller=self),
            "update_product_page": UpdateProductPage(container, controller=self),
        }

        self.show_page("shop_page")

    def show_page(self, name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(fill="both", expand=True)

        if hasattr(self.pages[name], "refresh"):
            self.pages[name].refresh()
