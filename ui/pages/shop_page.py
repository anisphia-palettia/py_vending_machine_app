import customtkinter as ctk

from core.config import API_URL
from services.product_service import products_find_all
from ui.widgets.product_card import ProductCard
from ui.widgets.cart_panel import CartPanel


class ShopPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Row 1 is now the main content

        # Header Frame
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 0)
        )

        back_btn = ctk.CTkButton(
            header_frame,
            text="< Kembali",
            width=100,
            command=lambda: controller.show_page("home_page"),
        )
        back_btn.pack(side="left")

        # Content
        self.products_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.products_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.cart_panel = CartPanel(self, on_buy=self.go_to_coin_page)
        self.cart_panel.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=10)

        self.build_products()

    def refresh(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        self.build_products()

    def build_products(self):
        cols = 3
        result = products_find_all()
        print(result)

        if not result.get("success"):
            print("Gagal mengambil produk")
            return

        products = result.get("data", [])

        for index, item in enumerate(products):
            product_id = item.get("id", 0)
            name = item.get("name", "No Name")
            price = item.get("price", 0)
            stock = item.get("quantity", 0)
            slug = item.get("slug", "")

            image_filename = item.get("image", "")
            image_url = API_URL + "/" + image_filename if image_filename else ""

            card = ProductCard(
                self.products_frame,
                product_id=product_id,
                name=name,
                slug=slug,
                stock=stock,
                price=price,
                image_url=image_url,
                on_click=self.add_to_cart,
                width=150,
                height=160,
            )

            r, c = divmod(index, cols)
            card.grid(row=r, column=c, padx=10, pady=10, sticky="nws")
            self.products_frame.grid_columnconfigure(c, weight=1)

    def add_to_cart(self, card):
        self.cart_panel.add_item(card.product_id, card.slug, card.name, card.price)

    def clear_cart(self):
        self.cart_panel.clear_cart()

    def go_to_coin_page(self, cart_data):
        print(cart_data)

        coin_page = self.controller.pages["coin_page"]
        coin_page.set_total(cart_data)

        self.controller.show_page("coin_page")
