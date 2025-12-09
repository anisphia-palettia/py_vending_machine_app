import customtkinter as ctk

from services.auth_service import login


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Center Container (Card)
        self.center_frame = ctk.CTkFrame(self, corner_radius=20, width=320)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Ensure frame respects width/height if needed, or let it expand
        # self.center_frame.pack_propagate(False)

        # Title
        title_label = ctk.CTkLabel(
            self.center_frame,
            text="Admin Login",
            font=("Roboto", 24, "bold"),
        )
        title_label.pack(pady=(30, 20), padx=30)

        # Username
        self.username = ctk.CTkEntry(
            self.center_frame,
            placeholder_text="Username",
            width=260,
            height=40,
            corner_radius=10,
            font=("Roboto", 14),
        )
        self.username.pack(pady=(0, 15), padx=30)

        # Password
        self.password = ctk.CTkEntry(
            self.center_frame,
            placeholder_text="Password",
            show="*",
            width=260,
            height=40,
            corner_radius=10,
            font=("Roboto", 14),
        )
        self.password.pack(pady=(0, 20), padx=30)

        # Login Button
        login_btn = ctk.CTkButton(
            self.center_frame,
            text="Login",
            width=260,
            height=40,
            corner_radius=20,
            font=("Roboto", 14, "bold"),
            command=lambda: self.handle_login(controller),
        )
        login_btn.pack(pady=(0, 10), padx=30)

        # Error Label
        self.error_label = ctk.CTkLabel(
            self.center_frame,
            text="",
            text_color=("red", "#ff5555"),
            font=("Roboto", 12),
        )
        self.error_label.pack(pady=(0, 10))

        # Bottom / Back Navigation
        # Separator line
        separator = ctk.CTkFrame(
            self.center_frame, height=2, fg_color=("gray85", "gray25")
        )
        separator.pack(fill="x", padx=30, pady=(10, 10))

        back_btn = ctk.CTkButton(
            self.center_frame,
            text="Back to Shop",
            fg_color="transparent",
            text_color=("gray50", "gray50"),
            hover_color=("gray90", "gray20"),
            width=260,
            height=30,
            font=("Roboto", 12),
            command=lambda: controller.show_page("shop_page"),
        )
        back_btn.pack(pady=(0, 20), padx=30)

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
