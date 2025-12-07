import customtkinter as ctk

from services.auth_service import login


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        center_frame = ctk.CTkFrame(self, fg_color="transparent", width=240)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        center_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            center_frame,
            text="Login",
            font=("Arial", 24, "bold"),
            anchor="center"
        )
        title_label.pack(fill="x", pady=(0, 20))

        self.username = ctk.CTkEntry(
            center_frame,
            placeholder_text="Username"
        )
        self.username.pack(fill="x", pady=10)

        self.password = ctk.CTkEntry(
            center_frame,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(fill="x", pady=10)

        login_btn = ctk.CTkButton(
            center_frame,
            text="Login",
            command=lambda: self.handle_login(controller),
        )
        login_btn.pack(pady=20, fill="x")

        self.error_label = ctk.CTkLabel(center_frame, text="", text_color="red")
        self.error_label.pack()

        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.place(relx=0.5, rely=0.95, anchor="s")

        admin_label = ctk.CTkLabel(bottom_frame, text="Bukan admin?")
        admin_label.pack(side="left")

        login_button = ctk.CTkButton(
            bottom_frame,
            width=0,
            text="Kembali",
            fg_color="transparent",
            hover=False,
            text_color="#1e90ff",
            command=lambda: controller.show_page("home_page")
        )
        login_button.pack(side="left", padx=5)

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
