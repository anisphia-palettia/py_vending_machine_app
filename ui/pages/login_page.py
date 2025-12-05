import customtkinter as ctk


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        center_frame = ctk.CTkFrame(self, fg_color="transparent", width=240)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        center_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            center_frame,
            text="Login Page",
            font=("", 24, "bold"),
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 15))

        self.username = ctk.CTkEntry(
            center_frame,
            placeholder_text="Masukkan username..."
        )
        self.username.pack(fill="x", pady=5)

        self.password = ctk.CTkEntry(
            center_frame,
            placeholder_text="Masukkan password...",
            show="*"
        )
        self.password.pack(fill="x", pady=5)

        login_btn = ctk.CTkButton(
            center_frame,
            text="Login",
            command=lambda: self.do_login(controller),
        )
        login_btn.pack(pady=5, fill="x")

        self.error_label = ctk.CTkLabel(center_frame, text="", text_color="red")
        self.error_label.pack()

    def do_login(self, controller):
        user = self.username.get()
        pwd = self.password.get()

        if not user:
            self.error_label.configure(text="Username tidak boleh kosong!")
            return

        if not pwd:
            self.error_label.configure(text="Password tidak boleh kosong!")
            return

        print("Username:", user)
        print("Password:", pwd)
