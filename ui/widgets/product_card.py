import customtkinter as ctk

from utils.load_image_url import load_image_url


class ProductCard(ctk.CTkFrame):
    def __init__(self, parent, product_id, name, stock, price, image_url, slug, on_click=None, **kwargs):
        super().__init__(parent, corner_radius=15, **kwargs)

        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.price = price
        self.slug = slug
        self.on_click = on_click

        self.img = load_image_url(image_url, size=(130, 130))

        # Main Layout: Image on top, info below
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1) # Spacer

        # Image container
        self.image_box = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.image_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        
        self.image_lbl = ctk.CTkLabel(self.image_box, image=self.img, text="")
        self.image_lbl.pack(expand=True, fill="both")

        # Title
        self.name_lbl = ctk.CTkLabel(
            self, 
            text=name, 
            font=("Roboto", 14, "bold"),
            anchor="w"
        )
        self.name_lbl.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 2))

        # Price
        self.price_lbl = ctk.CTkLabel(
            self, 
            text=f"${price}", 
            font=("Roboto", 16, "bold"),
            text_color=("green", "lightgreen"), # Standard named colors or tuple for light/dark
            anchor="w"
        )
        self.price_lbl.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 5))

        # Stock (Subtle)
        stock_text = f"{stock} items left" if stock > 0 else "Out of Stock"
        stock_color = ("gray60", "gray70") if stock > 0 else "red"
        self.stock_lbl = ctk.CTkLabel(
            self, 
            text=stock_text, 
            font=("Roboto", 11),
            text_color=stock_color,
            anchor="w"
        )
        self.stock_lbl.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 10))

        # Add Button
        self.add_btn = ctk.CTkButton(
            self,
            text="Add to Cart",
            font=("Roboto", 12, "bold"),
            height=32,
            corner_radius=20,
            state="normal" if stock > 0 else "disabled",
            command=self._clicked
        )
        # Revert to default colors by not specifying fg_color unless necessary
        # If we really want distinct disabled look, ctk handles it via state="disabled" usually
        self.add_btn.grid(row=5, column=0, sticky="ew", padx=15, pady=(0, 15))

    def _clicked(self, _=None):
        if self.on_click and self.stock > 0:
            self.on_click(self)
