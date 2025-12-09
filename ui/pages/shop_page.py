import customtkinter as ctk

from core.config import API_URL
from services.product_service import products_find_all
from ui.widgets.product_card import ProductCard
from ui.widgets.cart_panel import CartPanel


class ShopPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid_columnconfigure(0, weight=1) # Main content takes all width initially
        self.grid_columnconfigure(1, weight=0) # Cart is fixed width or auto
        self.grid_rowconfigure(1, weight=1)

        # Header Frame
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(20, 10)
        )
        
        title_lbl = ctk.CTkLabel(
            header_frame, 
            text="Vending Machine Shop", 
            font=("Roboto", 28, "bold")
        )
        title_lbl.pack(side="left")

        # Content - Products
        self.products_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.products_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # Content - Cart
        self.cart_panel = CartPanel(
            self, 
            on_buy=self.go_to_coin_page,
            on_login=lambda: self.controller.show_page("login_page")
        )
        self.cart_panel.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=0, pady=0) 
        # Note: spanned row 0 to cover full height to right? 
        # Actually design calls for sidebar. Let's make it row 0-2 (full height) 
        # But header is in row 0. grid logic:
        # If cart is in col 1, row 0-2. Header is in col 0. 
        # Let's interact: 
        # row0: [ Header (col0) ] [ Cart (col1) ]
        # row1: [ Products (col0) ] [ Cart (col1, rowspan) ]
        
        # Let's adjust header payload
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))
        
        self.cart_panel.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.build_products()

    def refresh(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        self.build_products()

    def build_products(self):
        result = products_find_all()
        # Debug print(result)

        if not result.get("success"):
            print("Gagal mengambil produk")
            # Maybe show an error label
            err = ctk.CTkLabel(self.products_frame, text="Failed to load products.")
            err.pack(pady=20)
            return

        products = result.get("data", [])

        # Responsive Grid Logic (Roughly)
        # We want cards to fill width. 
        # Let's use grid with equal weights for columns.
        cols = 3 
        for i in range(cols):
            self.products_frame.grid_columnconfigure(i, weight=1)

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
                on_click=self.add_to_cart
            )

            r, c = divmod(index, cols)
            card.grid(row=r, column=c, padx=10, pady=10, sticky="ew") # stick 'ew' to fill

    def add_to_cart(self, card):
        self.cart_panel.add_item(card.product_id, card.slug, card.name, card.price)

    def clear_cart(self):
        self.cart_panel.clear_cart()

    def go_to_coin_page(self, cart_data):
        print(cart_data)

        coin_page = self.controller.pages["coin_page"]
        coin_page.set_total(cart_data)

        self.controller.show_page("coin_page")
