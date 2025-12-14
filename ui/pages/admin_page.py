import customtkinter as ctk
from services.product_service import products_find_all, product_delete
from tkinter import messagebox


class AdminPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Layout: Sidebar (Left) + Content (Right)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content_area()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)  # Spacer at bottom

        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="Admin Panel", font=("Roboto", 20, "bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar,
            text="Products",
            fg_color=("gray75", "gray25"),
            font=("Roboto", 14, "bold"),
            anchor="w",
            height=40,
        )
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_logout = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            font=("Roboto", 14),
            anchor="w",
            height=40,
            command=self._logout,
        )
        self.btn_logout.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    def _build_content_area(self):
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Header Row
        header_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        self.header_lbl = ctk.CTkLabel(
            header_frame, text="Product Management", font=("Roboto", 24, "bold")
        )
        self.header_lbl.pack(side="left")

        # Create Product Button
        self.btn_create = ctk.CTkButton(
            header_frame,
            text="Create Product",
            command=self._go_to_create,
            font=("Roboto", 14, "bold"),
            height=36,
        )
        self.btn_create.pack(side="right")

        # Product List Container
        self.product_list_frame = ctk.CTkScrollableFrame(
            self.content, fg_color="transparent"
        )
        self.product_list_frame.grid(row=1, column=0, sticky="nsew")

    def refresh(self):
        # Clear existing
        for widget in self.product_list_frame.winfo_children():
            widget.destroy()

        # Fetch products
        res = products_find_all()
        if not res.get("success"):
            err = ctk.CTkLabel(self.product_list_frame, text="Failed to load products")
            err.pack(pady=20)
            return

        products = res.get("data", [])

        for p in products:
            self._add_product_row(p)

    def _add_product_row(self, product):
        p_id = product.get("id")
        name = product.get("name", "Unknown")
        stock = product.get("quantity", 0)
        price = product.get("price", 0)

        row_frame = ctk.CTkFrame(self.product_list_frame, corner_radius=10)
        row_frame.pack(fill="x", pady=5)
        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, weight=0) # Edit button
        row_frame.grid_columnconfigure(2, weight=0) # Delete button

        # Info
        info_text = f"{name}\n${price} - Stock: {stock}"
        lbl = ctk.CTkLabel(
            row_frame, text=info_text, font=("Roboto", 14), anchor="w", justify="left"
        )
        lbl.grid(row=0, column=0, sticky="ew", padx=15, pady=10)

        # Edit Button
        btn_edit = ctk.CTkButton(
            row_frame,
            text="Edit",
            width=80,
            height=30,
            fg_color=("gray75", "gray25"),
            text_color=("gray10", "gray90"),
            command=lambda p=product: self._go_to_update(p),
        )
        btn_edit.grid(row=0, column=1, padx=(5, 5), pady=10, sticky="e")

        # Delete Button
        btn_delete = ctk.CTkButton(
            row_frame,
            text="Delete",
            width=80,
            height=30,
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            text_color="white",
            command=lambda p=product: self._confirm_delete(p),
        )
        btn_delete.grid(row=0, column=2, padx=(5, 15), pady=10, sticky="e")

    def _go_to_create(self):
        self.controller.show_page("create_product_page")

    def _go_to_update(self, product):
        update_page = self.controller.pages["update_product_page"]
        update_page.set_product(product)
        self.controller.show_page("update_product_page")

    def _confirm_delete(self, product):
        if messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete '{product.get('name')}'?"
        ):
            res = product_delete(product.get("id"))
            if res.get("success"):
                self.refresh()
            else:
                messagebox.showerror(
                    "Error", f"Failed to delete product: {res.get('message')}"
                )

    def _logout(self):
        self.controller.show_page("login_page")
