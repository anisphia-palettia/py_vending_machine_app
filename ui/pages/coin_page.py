import customtkinter as ctk

class CoinPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.cart_items = []
        self.total_amount = 0
        self.inserted_amount = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Left Side: Payment Screen (Info)
        self.screen_frame = ctk.CTkFrame(self.main_container, corner_radius=15, border_width=2, border_color="#333333")
        self.screen_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.info_container = ctk.CTkFrame(self.screen_frame, fg_color="transparent")
        self.info_container.place(relx=0.5, rely=0.5, anchor="center")

        self.total_label = ctk.CTkLabel(self.info_container, text="Total: $0", font=("Arial", 32, "bold"))
        self.total_label.pack(pady=10)

        self.inserted_label = ctk.CTkLabel(self.info_container, text="Inserted: $0", font=("Arial", 24))
        self.inserted_label.pack(pady=10)

        self.change_label = ctk.CTkLabel(self.info_container, text="Change: $0", font=("Arial", 24), text_color="green")
        self.change_label.pack(pady=10)
        
        # Right Side: Controls (Coins & Actions)
        self.controls_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.controls_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Coin Grid
        self.coins_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.coins_frame.pack(pady=(0, 20))

        coins = [1, 2, 5, 10, 20, 50, 100]
        row = 0
        col = 0
        for coin in coins:
            btn = ctk.CTkButton(
                self.coins_frame,
                text=f"${coin}",
                width=80,
                height=60,
                corner_radius=10,
                font=("Arial", 16, "bold"),
                command=lambda c=coin: self.insert_coin(c)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2: # 3 columns
                col = 0
                row += 1

        # Action Buttons
        self.pay_button = ctk.CTkButton(
            self.controls_frame,
            text="PAY NOW",
            state="disabled",
            width=200,
            height=60,
            corner_radius=10,
            font=("Arial", 20, "bold"),
            fg_color="green",
            command=self.process_payment
        )
        self.pay_button.pack(pady=10)

        self.back_button = ctk.CTkButton(
            self.controls_frame,
            text="Cancel",
            width=200,
            height=40,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"), # Adaptive color
            command=lambda: controller.show_page("shop_page")
        )
        self.back_button.pack(pady=5)

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
        self.total_label.configure(text=f"Total: ${self.total_amount}")
        self.inserted_label.configure(text=f"Inserted: ${self.inserted_amount}")
        
        change = self.inserted_amount - self.total_amount
        if change >= 0:
            self.change_label.configure(text=f"Change: ${change}")
            self.pay_button.configure(state="normal", fg_color="green")
        else:
            self.change_label.configure(text="Change: $0")
            self.pay_button.configure(state="disabled", fg_color="gray")

    def process_payment(self):
        print("\n--- PROCESSING PAYMENT ---")
        updates = []
        for item in self.cart_items:
            # Create update payload: id and negative quantity (sold)
            updates.append({
                "id": item["id"],
                "quantity_change": -item["quantity"]
            })
        
        print(f"Updates Payload: {updates}")
        print("Payment Successful!")
        print(f"Total: ${self.total_amount}, Inserted: ${self.inserted_amount}, Change: ${self.inserted_amount - self.total_amount}")
        print("--------------------------\n")

        # Reset and go back to home or shop
        # User requested "kembali dengan melakukan update" - returning to home feels safest for a completed transaction
        self.controller.show_page("home_page")
