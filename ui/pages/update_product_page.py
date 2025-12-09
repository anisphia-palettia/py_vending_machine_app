import customtkinter as ctk
from tkinter import filedialog
import os
from services.product_service import product_update, upload_image


class UpdateProductPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product_id = None
        self.selected_image_path = None
        self.original_image_filename = ""

        # Layout: Center Box
        self.center_frame = ctk.CTkFrame(self, corner_radius=15)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            self.center_frame, text="Update Product", font=("Roboto", 20, "bold")
        )
        title.pack(pady=20, padx=40)

        # Fields
        self.name_entry = ctk.CTkEntry(
            self.center_frame, placeholder_text="Name", width=300
        )
        self.name_entry.pack(pady=10, padx=20)

        self.slug_entry = ctk.CTkEntry(
            self.center_frame, placeholder_text="Slug", width=300
        )
        self.slug_entry.pack(pady=10, padx=20)

        self.price_entry = ctk.CTkEntry(
            self.center_frame, placeholder_text="Price (Number)", width=300
        )
        self.price_entry.pack(pady=10, padx=20)

        self.qty_entry = ctk.CTkEntry(
            self.center_frame, placeholder_text="Quantity (Number)", width=300
        )
        self.qty_entry.pack(pady=10, padx=20)

        # Image Upload
        img_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        img_frame.pack(pady=10, padx=20, fill="x")

        self.btn_choose_img = ctk.CTkButton(
            img_frame, text="Change Image", command=self.choose_image, width=100
        )
        self.btn_choose_img.pack(side="left")

        self.img_label = ctk.CTkLabel(
            img_frame, text="Current: None", text_color="gray"
        )
        self.img_label.pack(side="left", padx=10)

        # Buttons
        btn_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        btn_save = ctk.CTkButton(
            btn_frame,
            text="Update",
            command=self.update_product,
            font=("Roboto", 14, "bold"),
        )
        btn_save.pack(side="left", padx=10)

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.cancel,
        )
        btn_cancel.pack(side="left", padx=10)

        self.msg_label = ctk.CTkLabel(self.center_frame, text="", text_color="red")
        self.msg_label.pack(pady=(0, 20))

    def set_product(self, product_data):
        self.product_id = product_data.get("id")
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, product_data.get("name", ""))

        self.slug_entry.delete(0, "end")
        self.slug_entry.insert(0, product_data.get("slug", ""))

        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, str(product_data.get("price", 0)))

        self.qty_entry.delete(0, "end")
        self.qty_entry.insert(0, str(product_data.get("quantity", 0)))

        self.original_image_filename = product_data.get("image", "") or ""
        self.selected_image_path = None

        img_display = (
            f"Current: {self.original_image_filename}"
            if self.original_image_filename
            else "Current: None"
        )
        self.img_label.configure(text=img_display)

        self.msg_label.configure(text="")

    def choose_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if file_path:
            self.selected_image_path = file_path
            self.img_label.configure(text="New: " + os.path.basename(file_path))

    def cancel(self):
        self.controller.show_page("admin_page")

    def update_product(self):
        if not self.product_id:
            return

        name = self.name_entry.get()
        slug = self.slug_entry.get()
        price = self.price_entry.get()
        qty = self.qty_entry.get()

        if not name or not slug or not price or not qty:
            self.msg_label.configure(
                text="Please fill all required fields", text_color="red"
            )
            return

        try:
            price = float(price)
            qty = int(qty)
        except ValueError:
            self.msg_label.configure(
                text="Price and Quantity must be numbers", text_color="red"
            )
            return

        # Handle Image Upload
        image_filename = self.original_image_filename
        if self.selected_image_path:
            self.msg_label.configure(text="Uploading new image...", text_color="blue")
            self.update_idletasks()
            try:
                res = upload_image(self.selected_image_path)
                if res.get("success"):
                    image_filename = (
                        res.get("data", {}).get("filename") or res.get("filename") or ""
                    )
                else:
                    self.msg_label.configure(
                        text=f"Image upload failed: {res.get('message')}",
                        text_color="red",
                    )
                    return
            except Exception as e:
                self.msg_label.configure(
                    text=f"Upload Error: {str(e)}", text_color="red"
                )
                return

        data = {
            "name": name,
            "slug": slug,
            "price": price,
            "quantity": qty,
            "image": image_filename,
        }

        res = product_update(self.product_id, data)
        if res.get("success"):
            self.msg_label.configure(text="Product Updated!", text_color="green")
            self.controller.show_page("admin_page")
            self.controller.pages["admin_page"].refresh()
        else:
            self.msg_label.configure(
                text=f"Error: {res.get('message', 'Unknown')}", text_color="red"
            )
