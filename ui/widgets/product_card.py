import customtkinter as ctk

from utils.load_image_url import load_image_url


class ProductCard(ctk.CTkFrame):
    def __init__(self, parent, product_id, name, stock, price, image_url, slug, on_click=None, **kwargs):
        super().__init__(parent, corner_radius=8, **kwargs)

        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.price = price
        self.slug = slug
        self.on_click = on_click

        self.img = load_image_url(image_url, size=(120, 120))

        self.grid_columnconfigure(0, weight=1)

        self.bind("<Button-1>", self._clicked)

        self.image_box = ctk.CTkFrame(self, height=120, corner_radius=6, fg_color="transparent")
        self.image_box.grid(row=0, column=0, sticky="nsew", padx=8, pady=(8, 4))
        self.image_box.bind("<Button-1>", self._clicked)

        self.image_lbl = ctk.CTkLabel(self.image_box, image=self.img, text="")
        self.image_lbl.pack(expand=True, fill="both")
        self.image_lbl.bind("<Button-1>", self._clicked)

        self.name_lbl = ctk.CTkLabel(self, text=name, anchor="w")
        self.name_lbl.grid(row=1, column=0, sticky="ew", padx=8)
        self.name_lbl.bind("<Button-1>", self._clicked)

        self.stock_lbl = ctk.CTkLabel(self, text=f"Stok : {stock}", anchor="w")
        self.stock_lbl.grid(row=2, column=0, sticky="ew", padx=8)
        self.stock_lbl.bind("<Button-1>", self._clicked)

        self.price_lbl = ctk.CTkLabel(self, text=f"Harga: ${price}", anchor="w")
        self.price_lbl.grid(row=3, column=0, sticky="ew", padx=8, pady=(0, 8))
        self.price_lbl.bind("<Button-1>", self._clicked)

    def _clicked(self, _):
        if self.on_click:
            self.on_click(self)
