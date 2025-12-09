import customtkinter as ctk


class CartPanel(ctk.CTkFrame):
    def __init__(self, parent, on_buy=None, on_login=None, **kwargs):
        # Use default styling, no fixed header fg_color="#1E1E1E"
        super().__init__(parent, corner_radius=0, width=300, **kwargs) 

        self.cart_items = {}
        self.on_buy = on_buy
        self.on_login = on_login

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False) # Force fixed width if needed

        # --- Header ---
        header = ctk.CTkFrame(self, fg_color="transparent", height=60, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header, 
            text="Your Cart", 
            font=("Roboto", 22, "bold"), 
            # text_color="#FFFFFF", # Use default text color
            anchor="w"
        )
        title.grid(row=0, column=0, sticky="w")
        
        subtitle = ctk.CTkLabel(
            header,
            text="Ready to checkout?",
            font=("Roboto", 12),
            text_color=("gray60", "gray70"),
            anchor="w"
        )
        subtitle.grid(row=1, column=0, sticky="w")

        # --- List Area ---
        self.items_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.items_frame.grid(row=1, column=0, sticky="nsew", padx=10)

        # --- Footer ---
        footer = ctk.CTkFrame(self, corner_radius=15) # Default surface color
        footer.grid(row=2, column=0, sticky="ew", padx=15, pady=20)
        footer.grid_columnconfigure(0, weight=1)

        self.total_label = ctk.CTkLabel(
            footer, 
            text="Total: $0.00", 
            font=("Roboto", 18, "bold"),
            # text_color="#FFFFFF"
        )
        self.total_label.grid(row=0, column=0, sticky="ew", pady=(15, 5))

        self.buy_button = ctk.CTkButton(
            footer, 
            text="Checkout Now", 
            width=200, 
            height=45, 
            corner_radius=25,
            font=("Roboto", 14, "bold"),
            # fg_color="#2196F3", # Use default theme color
            # hover_color="#1976D2",
            command=self.handle_buy
        )
        self.buy_button.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 5))

        # Admin Login Button (Text Style)
        self.login_btn = ctk.CTkButton(
            footer,
            text="Admin Login",
            width=100,
            height=20,
            font=("Roboto", 11),
            fg_color="transparent",
            text_color=("gray50", "gray50"),
            hover_color=("gray85", "gray25"),
            command=self.handle_login
        )
        self.login_btn.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))

    def handle_buy(self):
        if self.on_buy:
            self.on_buy(self.get_cart_data())
            
    def handle_login(self):
        if self.on_login:
            self.on_login()

    def get_cart_data(self):
        cart_list = []

        for slug, item in self.cart_items.items():
            cart_list.append(
                {
                    "id": item["id"],
                    "slug": slug,
                    "quantity": item["qty"],
                    "price": item["price"],
                    "subtotal": item["qty"] * item["price"],
                }
            )

        total = sum(i["subtotal"] for i in cart_list)

        return {"items": cart_list, "total": total}

    def add_item(self, product_id, slug, name, price):
        if slug in self.cart_items:
            self.cart_items[slug]["qty"] += 1
            self.cart_items[slug]["qty_lbl"].configure(
                text=str(self.cart_items[slug]["qty"])
            )
        else:
            # Container for Item
            item_frame = ctk.CTkFrame(self.items_frame, corner_radius=10)
            item_frame.pack(fill="x", pady=5, padx=5) # Use pack for automatic stacking
            item_frame.grid_columnconfigure(0, weight=1)

            # Name and Price
            name_lbl = ctk.CTkLabel(item_frame, text=name, font=("Roboto", 13, "bold"), anchor="w")
            name_lbl.grid(row=0, column=0, sticky="ew", padx=10, pady=(5,0))
            
            price_sub_lbl = ctk.CTkLabel(item_frame, text=f"${price}", font=("Roboto", 11), text_color=("gray60", "gray70"), anchor="w")
            price_sub_lbl.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,5))

            # Controls
            ctrl_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            ctrl_frame.grid(row=0, column=1, rowspan=2, padx=5, sticky="e")

            minus_btn = ctk.CTkButton(
                ctrl_frame,
                text="-",
                width=30,
                height=30,
                corner_radius=15,
                fg_color="transparent",
                border_width=1,
                border_color=("gray70", "gray30"),
                text_color=("gray10", "gray90"),
                font=("Arial", 14, "bold"),
                command=lambda: self.change_qty(slug, price, -1),
            )
            minus_btn.pack(side="left", padx=2)

            qty_lbl = ctk.CTkLabel(ctrl_frame, text="1", font=("Roboto", 14), width=30)
            qty_lbl.pack(side="left", padx=2)

            plus_btn = ctk.CTkButton(
                ctrl_frame,
                text="+",
                width=30,
                height=30,
                corner_radius=15,
                fg_color="transparent",
                border_width=1,
                border_color=("gray70", "gray30"),
                text_color=("gray10", "gray90"),
                font=("Arial", 14, "bold"),
                command=lambda: self.change_qty(slug, price, +1),
            )
            plus_btn.pack(side="left", padx=2)

            self.cart_items[slug] = {
                "id": product_id,
                "qty": 1,
                "price": price,
                "frame": item_frame, # Store frame to destroy later
                "qty_lbl": qty_lbl,
            }

        self.update_total()

    def change_qty(self, slug, price, delta):
        item = self.cart_items[slug]
        item["qty"] += delta

        if item["qty"] <= 0:
            self.remove_item(slug)
            return

        item["qty_lbl"].configure(text=str(item["qty"]))
        self.update_total()

    def remove_item(self, slug):
        if slug in self.cart_items:
            self.cart_items[slug]["frame"].destroy()
            del self.cart_items[slug]
        self.update_total()

    def update_total(self):
        total = sum(item["qty"] * item["price"] for item in self.cart_items.values())
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def clear_cart(self):
        for slug in list(self.cart_items.keys()):
            self.remove_item(slug)

