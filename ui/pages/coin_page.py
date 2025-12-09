from services.product_service import product_update_quantity
import customtkinter as ctk


class CoinPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.cart_items = []
        self.total_amount = 0
        self.inserted_amount = 0

        # Layout: 2 Columns (Order Summary | Payment)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Left Side: Order Summary ---
        self.summary_frame = ctk.CTkFrame(
            self, corner_radius=15, fg_color="transparent"
        )
        self.summary_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_rowconfigure(1, weight=1)

        summary_title = ctk.CTkLabel(
            self.summary_frame,
            text="Order Summary",
            font=("Roboto", 24, "bold"),
            text_color=("gray60", "gray70"),
        )
        summary_title.grid(row=0, column=0, sticky="w", pady=(20, 10), padx=20)

        # Big Total Display
        self.total_container = ctk.CTkFrame(self.summary_frame, corner_radius=15)
        self.total_container.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        self.total_label_title = ctk.CTkLabel(
            self.total_container, text="Total to Pay", font=("Roboto", 14)
        )
        self.total_label_title.pack(pady=(20, 5))

        self.total_label = ctk.CTkLabel(
            self.total_container,
            text="$0.00",
            font=("Roboto", 48, "bold"),  # very big
        )
        self.total_label.pack(pady=(0, 20))

        # Back Button (moved to left side bottom)
        self.back_button = ctk.CTkButton(
            self.summary_frame,
            text="Cancel Order",
            height=40,
            fg_color="transparent",
            border_width=1,
            border_color=("gray70", "gray30"),
            text_color=("gray10", "gray90"),
            font=("Roboto", 14),
            command=lambda: controller.show_page("shop_page"),
        )
        self.back_button.grid(row=2, column=0, sticky="ew", padx=20, pady=20)

        # --- Right Side: Payment ---
        self.payment_frame = ctk.CTkFrame(self, corner_radius=15)
        self.payment_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.payment_frame.grid_columnconfigure(0, weight=1)

        payment_title = ctk.CTkLabel(
            self.payment_frame, text="Insert Coins", font=("Roboto", 24, "bold")
        )
        payment_title.pack(pady=(20, 10))

        # Payment Status Group
        status_frame = ctk.CTkFrame(self.payment_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=20, pady=10)

        # Inserted
        self.inserted_label = ctk.CTkLabel(
            status_frame, text="Inserted: $0.00", font=("Roboto", 18, "bold")
        )
        self.inserted_label.pack(side="left", padx=10)

        # Change
        self.change_label = ctk.CTkLabel(
            status_frame,
            text="Change: $0.00",
            font=("Roboto", 18, "bold"),
            text_color=("green", "lightgreen"),
        )
        self.change_label.pack(side="right", padx=10)

        # Coin Grid
        self.coins_frame = ctk.CTkFrame(self.payment_frame, fg_color="transparent")
        self.coins_frame.pack(pady=20, padx=20)

        coins = [1, 2, 5, 10, 20, 50, 100]
        # Auto grid logic
        c = 3  # columns
        for i, coin in enumerate(coins):
            btn = ctk.CTkButton(
                self.coins_frame,
                text=f"${coin}",
                width=75,
                height=75,
                corner_radius=37,  # Circle
                font=("Roboto", 18, "bold"),
                fg_color=("gray85", "gray25"),
                text_color=("gray10", "gray90"),
                command=lambda c=coin: self.insert_coin(c),
            )
            row, col = divmod(i, c)
            btn.grid(row=row, column=col, padx=10, pady=10)

        # Pay Button
        self.pay_button = ctk.CTkButton(
            self.payment_frame,
            text="COMPLETE PAYMENT",
            state="disabled",
            height=60,
            corner_radius=10,
            font=("Roboto", 20, "bold"),
            command=self.process_payment,
        )
        self.pay_button.pack(side="bottom", fill="x", padx=20, pady=20)

    def set_total(self, cart_data):
        """Dipanggil dari page sebelumnya"""
        self.cart_items = cart_data.get("items", [])
        self.total_amount = cart_data.get("total", 0)
        self.inserted_amount = 0
        self.update_ui()

    def insert_coin(self, amount):
        self.inserted_amount += amount
        self.update_ui()

    def update_ui(self):
        self.total_label.configure(text=f"${self.total_amount:.2f}")
        self.inserted_label.configure(text=f"Inserted: ${self.inserted_amount:.2f}")

        change = self.inserted_amount - self.total_amount
        if change >= 0:
            self.change_label.configure(
                text=f"Change: ${change:.2f}", text_color=("green", "lightgreen")
            )
            self.pay_button.configure(state="normal")  # Uses default theme color
        else:
            self.change_label.configure(
                text="Change: $0.00", text_color=("gray70", "gray30")
            )
            self.pay_button.configure(state="disabled")

    def process_payment(self):
        print("\n--- PROCESSING PAYMENT ---")
        updates = []

        # Buat payload updates
        for item in self.cart_items:
            updates.append(
                {
                    "id": item["id"],
                    "quantity": -item["quantity"],  # kurangi stok
                }
            )

        print(f"Updates Payload: {updates}")

        # -------------------------------
        #       KIRIM UPDATE KE API
        # -------------------------------
        for update in updates:
            try:
                print(f"Updating product {update['id']} ...")
                result = product_update_quantity(update["id"], update["quantity"])
                print(f"API Response: {result}")
            except Exception as e:
                print(f"Failed to update product {update['id']}: {e}")

        print("Payment Successful!")
        change = self.inserted_amount - self.total_amount

        self.show_change_popup(change)

    def show_change_popup(self, change):
        popup = ctk.CTkToplevel(self)
        popup.title("Payment Successful")
        popup.geometry("300x200")
        popup.resizable(False, False)

        # Center the popup relative to the main window if possible, or just screen
        # For simplicity, let's just center on screen roughly or rely on OS
        # Or better, center on parent
        popup.transient(self)  # Make it modal-like on top of window
        popup.grab_set()  # Modal interaction

        # Center Content
        container = ctk.CTkFrame(popup, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        lbl = ctk.CTkLabel(
            container, text="Payment Complete!", font=("Roboto", 18, "bold")
        )
        lbl.pack(pady=(10, 5))

        change_text = f"Your Change:\n${change:.2f}"
        change_lbl = ctk.CTkLabel(
            container,
            text=change_text,
            font=("Roboto", 16),
            text_color=("green", "lightgreen"),
        )
        change_lbl.pack(pady=10)

        ok_btn = ctk.CTkButton(
            container,
            text="Collect Change & Items",
            command=lambda: self.finish_transaction(popup),
        )
        ok_btn.pack(pady=(10, 0))

        # Determine position center
        self.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (300 // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (200 // 2)
        popup.geometry(f"+{x}+{y}")

    def finish_transaction(self, popup):
        popup.destroy()

        # Reset setelah payment
        self.cart_items = []
        self.total_amount = 0
        self.inserted_amount = 0

        # Clear ShopPage Cart
        shop_page = self.controller.pages["shop_page"]
        if hasattr(shop_page, "clear_cart"):
            shop_page.clear_cart()

        self.controller.show_page("shop_page")
