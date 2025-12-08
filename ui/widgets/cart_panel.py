import customtkinter as ctk


class CartPanel(ctk.CTkFrame):
    def __init__(self, parent, on_buy=None, **kwargs):
        super().__init__(parent, corner_radius=0, **kwargs)

        self.cart_items = {}
        self.on_buy = on_buy

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Keranjang Belanja", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.items_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.items_frame.grid(row=1, column=0, sticky="nsew", padx=10)

        footer = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        footer.grid_columnconfigure(0, weight=1)

        self.total_label = ctk.CTkLabel(footer, text="Total: $0", font=("Arial", 14))
        self.total_label.grid(row=0, column=0, sticky="e", pady=(0, 10))

        self.buy_button = ctk.CTkButton(
            footer, text="Checkout", width=180, height=40, command=self.handle_buy
        )
        self.buy_button.grid(row=1, column=0, sticky="e")

    def handle_buy(self):
        if self.on_buy:
            self.on_buy(self.get_cart_data())

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
                text=self.cart_items[slug]["qty"]
            )
        else:
            row = len(self.cart_items)

            name_lbl = ctk.CTkLabel(self.items_frame, text=name)
            name_lbl.grid(row=row, column=0, sticky="w")

            minus_btn = ctk.CTkButton(
                self.items_frame,
                text="-",
                width=25,
                command=lambda: self.change_qty(slug, price, -1),
            )
            minus_btn.grid(row=row, column=1, padx=5)

            qty_lbl = ctk.CTkLabel(self.items_frame, text="1")
            qty_lbl.grid(row=row, column=2, padx=5)

            plus_btn = ctk.CTkButton(
                self.items_frame,
                text="+",
                width=25,
                command=lambda: self.change_qty(slug, price, +1),
            )
            plus_btn.grid(row=row, column=3, padx=5)

            self.cart_items[slug] = {
                "id": product_id,
                "qty": 1,
                "price": price,
                "name_lbl": name_lbl,
                "qty_lbl": qty_lbl,
                "minus": minus_btn,
                "plus": plus_btn,
            }

        self.update_total()

    def change_qty(self, slug, price, delta):
        item = self.cart_items[slug]
        item["qty"] += delta

        if item["qty"] <= 0:
            self.remove_item(slug)
            return

        item["qty_lbl"].configure(text=item["qty"])
        self.update_total()

    def remove_item(self, slug):
        for w in self.cart_items[slug].values():
            if hasattr(w, "destroy"):
                w.destroy()

        del self.cart_items[slug]
        self.repack_rows()
        self.update_total()

    def repack_rows(self):
        for i, (slug, item) in enumerate(self.cart_items.items()):
            item["name_lbl"].grid(row=i, column=0, sticky="w")
            item["minus"].grid(row=i, column=1, padx=5)
            item["qty_lbl"].grid(row=i, column=2, padx=5)
            item["plus"].grid(row=i, column=3, padx=5)

    def update_total(self):
        total = sum(item["qty"] * item["price"] for item in self.cart_items.values())
        self.total_label.configure(text=f"Total        ${total}")

    def clear_cart(self):
        for slug in list(self.cart_items.keys()):
            self.remove_item(slug)
