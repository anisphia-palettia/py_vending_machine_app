import customtkinter as ctk


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.pack_propagate(False)

        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        welcome_label = ctk.CTkLabel(center_frame, text="Selamat Datang!", font=("Arial", 24, "bold"))
        welcome_label.pack(side="top", pady=(0, 24))

        belanja_btn = ctk.CTkButton(
            center_frame,
            width=200,
            text="Belanja",
       
            command=lambda: controller.show_page("shop_page")
        )
        belanja_btn.pack()

        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.place(relx=0.5, rely=0.95, anchor="s")

        admin_label = ctk.CTkLabel(bottom_frame, text="Anda adalah admin?")
        admin_label.pack(side="left")

        login_button = ctk.CTkButton(
            bottom_frame,
            width=0,
            text="Login",
            fg_color="transparent",
            hover=False,
            text_color="#1e90ff",
            command=lambda: controller.show_page("login_page")
        )
        login_button.pack(side="left", padx=5)
