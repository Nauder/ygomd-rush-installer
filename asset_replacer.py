import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime
import UnityPy
from UnityPy.enums import TextureFormat
from PIL import Image
import io


class AssetReplacerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unity Asset Replacer")
        self.root.geometry("600x400")

        # Asset bundle file path
        self.bundle_path = tk.StringVar()

        # Face names mapping
        self.face_names = {
            "card_frame00": "normal.png",
            "card_frame01": "effect.png",
            "card_frame02": "ritual.png",
            "card_frame03": "fusion.png",
            "card_frame07": "spell.png",
            "card_frame08": "trap.png",
            "card_frame09": "token.png",
            "card_frame10": "synchro.png",
            "card_frame12": "xyz.png",
            "card_frame13": "pendn.png",
            "card_frame14": "pend.png",
            "card_frame15": "pendx.png",
            "card_frame16": "pends.png",
            "card_frame17": "pendf.png",
            "card_frame18": "link.png",
            "card_frame19": "pendf.png",
        }

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # File selection frame
        file_frame = ttk.LabelFrame(
            main_frame, text="Select Unity AssetBundle File", padding="10"
        )
        file_frame.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        # File path entry
        ttk.Entry(file_frame, textvariable=self.bundle_path, width=60).grid(
            row=0, column=0, padx=(0, 10)
        )
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(
            row=0, column=1
        )

        # Process button
        ttk.Button(main_frame, text="Replace Assets", command=self.process_assets).grid(
            row=1, column=0, pady=10
        )

        # Log text area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0)
        )

        self.log_text = tk.Text(log_frame, height=15, width=70)
        scrollbar = ttk.Scrollbar(
            log_frame, orient="vertical", command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select unity3d File",
            filetypes=[("Unity3D files", "*.unity3d"), ("All files", "*.*")],
        )
        if filename:
            self.bundle_path.set(filename)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def create_backup(self, original_path):
        """Create a backup of the original file with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = original_path.replace(".unity3d", f"_backup_{timestamp}.unity3d")

        try:
            shutil.copy2(original_path, backup_path)
            self.log(f"Backup created: {os.path.basename(backup_path)}")
            return backup_path
        except Exception as e:
            raise Exception(f"Failed to create backup: {str(e)}")

    def process_assets(self):
        if not self.bundle_path.get():
            messagebox.showerror(
                "Error", "Please select a Unity AssetBundle file first."
            )
            return

        if not os.path.exists(self.bundle_path.get()):
            messagebox.showerror("Error", "Selected file does not exist.")
            return

        # Clear log
        self.log_text.delete(1.0, tk.END)

        try:
            self.log("Loading Unity AssetBundle...")
            env = UnityPy.load(self.bundle_path.get())

            replaced_count = 0

            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()

                    # Apply filter
                    if (
                        hasattr(data, "m_Name")
                        and hasattr(data, "m_CompleteImageSize")
                        and "card_frame" in data.m_Name
                    ):

                        self.log(f"Found matching asset: {data.m_Name}")

                        # Check if we have a replacement for this asset
                        if data.m_Name in self.face_names:
                            replacement_file = self.face_names[data.m_Name]
                            replacement_path = os.path.join("res", replacement_file)

                            if os.path.exists(replacement_path):
                                self.log(
                                    f"Replacing {data.m_Name} with {replacement_file}"
                                )

                                # Load replacement image
                                with open(replacement_path, "rb") as f:
                                    replacement_data = f.read()

                                # Replace the texture data
                                img = Image.open(io.BytesIO(replacement_data))
                                data.m_Width, data.m_Height = img.size

                                data.set_image(
                                    img=img, target_format=TextureFormat.RGBA32
                                )
                                data.save()
                                replaced_count += 1

                                self.log(f"Successfully replaced {data.m_Name}")
                            else:
                                self.log(
                                    f"Warning: Replacement file not found: {replacement_path}"
                                )
                        else:
                            self.log(f"No replacement defined for: {data.m_Name}")

            if replaced_count == 0:
                self.log("No assets were replaced.")
                messagebox.showinfo("Info", "No matching assets found to replace.")
                return

            # Ask user for confirmation to replace original file
            confirm_msg = (
                f"Found and processed {replaced_count} assets.\n\n"
                "Do you want to:\n"
                "• Create a backup of the original file\n"
                "• Replace the original file with the modified version\n\n"
                "Click 'Yes' to proceed or 'No' to save as a separate file."
            )

            replace_original = messagebox.askyesno(
                "Replace Original File?", confirm_msg, icon="question"
            )

            if replace_original:
                # Create backup first
                self.log("\nCreating backup of original file...")
                backup_path = self.create_backup(self.bundle_path.get())

                # Save modified data to original file
                self.log("Replacing original file with modified version...")
                with open(self.bundle_path.get(), "wb") as f:
                    f.write(env.file.save())

                self.log("Process completed!")
                self.log(f"Replaced {replaced_count} assets")
                self.log(
                    f"Original file updated: {os.path.basename(self.bundle_path.get())}"
                )
                self.log(f"Backup saved as: {os.path.basename(backup_path)}")

                messagebox.showinfo(
                    "Success",
                    f"Process completed!\n\n"
                    f"• Replaced {replaced_count} assets\n"
                    f"• Original file updated\n"
                    f"• Backup created: {os.path.basename(backup_path)}",
                )
            else:
                # Save as separate file (original behavior)
                output_path = self.bundle_path.get().replace(
                    ".unity3d", "_modified.unity3d"
                )
                with open(output_path, "wb") as f:
                    f.write(env.file.save())

                self.log("Process completed!")
                self.log(f"Replaced {replaced_count} assets")
                self.log(f"Modified file saved as: {os.path.basename(output_path)}")

                messagebox.showinfo(
                    "Success",
                    f"Process completed!\n\n"
                    f"• Replaced {replaced_count} assets\n"
                    f"• Modified file saved as: {os.path.basename(output_path)}",
                )

        except Exception as e:
            error_msg = f"Error processing assets: {str(e)}"
            self.log(error_msg)
            messagebox.showerror("Error", error_msg)


def main():
    root = tk.Tk()
    app = AssetReplacerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
