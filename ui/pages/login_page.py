import customtkinter as ctk

from services.auth_service import login


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Main container dengan 2 kolom
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=50, pady=30)

        # Grid configuration untuk 2 kolom
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Left Frame - Login Form
        self.login_frame = ctk.CTkFrame(
            self.main_container, corner_radius=20, width=350
        )
        self.login_frame.grid(row=0, column=0, padx=(0, 20), sticky="nsew")
        self.login_frame.pack_propagate(False)

        # Right Frame - Numpad
        self.numpad_frame = ctk.CTkFrame(
            self.main_container, corner_radius=20, width=350
        )
        self.numpad_frame.grid(row=0, column=1, padx=(20, 0), sticky="nsew")
        self.numpad_frame.pack_propagate(False)

        # ===== LEFT SIDE - LOGIN FORM =====
        # Title
        title_label = ctk.CTkLabel(
            self.login_frame,
            text="Admin Login",
            font=("Roboto", 24, "bold"),
        )
        title_label.pack(pady=(40, 30), padx=30)

        # Username
        self.username = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="First Password",
            show="*",
            width=280,
            height=45,
            corner_radius=10,
            font=("Roboto", 14),
        )
        self.username.pack(pady=(0, 15), padx=30)
        self.username.bind("<FocusIn>", lambda e: self.set_active_entry("username"))

        # Password
        self.password = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Second Password",
            show="*",
            width=280,
            height=45,
            corner_radius=10,
            font=("Roboto", 14),
        )
        self.password.pack(pady=(0, 20), padx=30)
        self.password.bind("<FocusIn>", lambda e: self.set_active_entry("password"))

        # Login Button
        login_btn = ctk.CTkButton(
            self.login_frame,
            text="Login",
            width=280,
            height=45,
            corner_radius=20,
            font=("Roboto", 14, "bold"),
            command=lambda: self.handle_login(controller),
        )
        login_btn.pack(pady=(0, 10), padx=30)

        # Error Label
        self.error_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            text_color=("red", "#ff5555"),
            font=("Roboto", 12),
        )
        self.error_label.pack(pady=(0, 10))

        # Separator line
        separator = ctk.CTkFrame(
            self.login_frame, height=2, fg_color=("gray85", "gray25")
        )
        separator.pack(fill="x", padx=30, pady=(10, 10))

        # Back button
        back_btn = ctk.CTkButton(
            self.login_frame,
            text="Back to Shop",
            fg_color="transparent",
            text_color=("gray50", "gray50"),
            hover_color=("gray90", "gray20"),
            width=280,
            height=35,
            font=("Roboto", 12),
            command=lambda: controller.show_page("shop_page"),
        )
        back_btn.pack(pady=(0, 30), padx=30)

        # ===== RIGHT SIDE - NUMPAD =====
        # Numpad title
        numpad_title = ctk.CTkLabel(
            self.numpad_frame,
            text="Numpad",
            font=("Roboto", 20, "bold"),
        )
        numpad_title.pack(pady=(40, 20), padx=30)

        # Active entry indicator
        self.active_entry_label = ctk.CTkLabel(
            self.numpad_frame,
            text="Active: None",
            font=("Roboto", 12),
            text_color=("gray50", "gray70"),
        )
        self.active_entry_label.pack(pady=(0, 20))

        # Numpad buttons grid
        self.numpad_buttons_frame = ctk.CTkFrame(
            self.numpad_frame, fg_color="transparent"
        )
        self.numpad_buttons_frame.pack(pady=10, padx=30)

        # Numpad buttons configuration
        buttons = [("1", "2", "3"), ("4", "5", "6"), ("7", "8", "9"), ("C", "0", "←")]

        self.active_entry = None  # Track which entry is active

        # Create numpad buttons
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                btn = ctk.CTkButton(
                    self.numpad_buttons_frame,
                    text=button_text,
                    width=70,
                    height=60,
                    font=("Roboto", 18, "bold"),
                    command=lambda text=button_text: self.numpad_click(text),
                    corner_radius=10,
                )
                btn.grid(row=i, column=j, padx=5, pady=5)

        # Instructions label
        instructions = ctk.CTkLabel(
            self.numpad_frame,
            text="Click on a password field above,\nthen use numpad to enter numbers",
            font=("Roboto", 12),
            text_color=("gray50", "gray70"),
            justify="center",
        )
        instructions.pack(pady=(30, 40))

    def set_active_entry(self, entry_name):
        """Set which entry field is currently active"""
        self.active_entry = entry_name
        if entry_name == "username":
            self.active_entry_label.configure(text="Active: First Password")
            self.username.focus_set()
        else:
            self.active_entry_label.configure(text="Active: Second Password")
            self.password.focus_set()

    def numpad_click(self, value):
        """Handle numpad button clicks"""
        if not self.active_entry:
            return

        current_entry = (
            self.username if self.active_entry == "username" else self.password
        )

        if value == "C":
            # Clear the entire field
            current_entry.delete(0, "end")
        elif value == "←":
            # Delete last character
            current_position = current_entry.index("insert")
            if current_position > 0:
                current_entry.delete(current_position - 1, current_position)
        else:
            # Insert number at cursor position
            current_entry.insert("insert", value)

    def handle_login(self, controller):
        username = self.username.get()
        password = self.password.get()

        if not username:
            self.error_label.configure(text="Username tidak boleh kosong!")
            return

        if not password:
            self.error_label.configure(text="Password tidak boleh kosong!")
            return

        result = login(username, password)
        print(result)

        if result.get("success"):
            # Login Access
            self.controller.show_page("admin_page")
            # Clear inputs
            self.username.delete(0, "end")
            self.password.delete(0, "end")
            self.error_label.configure(text="")
        else:
            self.error_label.configure(text="Login failed. Check credentials.")
