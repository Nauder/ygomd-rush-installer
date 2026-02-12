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
            "card_frame19": "pendr.png",
        }

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Folder selection frame
        file_frame = ttk.LabelFrame(
            main_frame, text="Select Bundles Path", padding="10"
        )
        file_frame.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        # Folder path entry
        ttk.Entry(file_frame, textvariable=self.bundle_path, width=60).grid(
            row=0, column=0, padx=(0, 10)
        )
        ttk.Button(file_frame, text="Browse", command=self.browse_folder).grid(
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

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Bundles Path")
        if folder:
            self.bundle_path.set(folder)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def create_backup(self, original_path):
        """Create a backup of the original file with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = original_path + f"_backup_{timestamp}"

        try:
            shutil.copy2(original_path, backup_path)
            self.log(f"Backup created: {os.path.basename(backup_path)}")
            return backup_path
        except Exception as e:
            raise Exception(f"Failed to create backup: {str(e)}")

    def get_mask_files(self):
        """Get all image files from res/mask folder and create a mapping"""
        mask_folder = os.path.join("res", "mask")
        mask_files = {}

        if os.path.exists(mask_folder):
            for filename in os.listdir(mask_folder):
                if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tga")):
                    # Use filename without extension as asset name
                    asset_name = os.path.splitext(filename)[0]
                    mask_files[asset_name] = os.path.join(mask_folder, filename)

        return mask_files

    def process_assets(self):
        if not self.bundle_path.get():
            messagebox.showerror("Error", "Please select a bundles path first.")
            return

        bundle_file = os.path.join(self.bundle_path.get(), "0000", "0e", "0e5c5d56")

        if not os.path.exists(bundle_file):
            messagebox.showerror(
                "Error",
                f"Bundle file not found:\n{bundle_file}\n\nMake sure the selected folder contains 0000/0e/0e5c5d56.",
            )
            return

        # Clear log
        self.log_text.delete(1.0, tk.END)

        try:
            self.log(f"Loading bundle: {bundle_file}")
            env = UnityPy.load(bundle_file)

            # Get mask files mapping
            mask_files = self.get_mask_files()
            if mask_files:
                self.log(
                    f"Found {len(mask_files)} mask files: {', '.join(mask_files.keys())}"
                )
            else:
                self.log("No mask files found in res/mask folder")

            replaced_count = 0

            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()

                    if hasattr(data, "m_Name") and hasattr(data, "m_CompleteImageSize"):
                        asset_name = data.m_Name
                        replacement_path = None
                        replacement_source = None

                        # Check for card frame replacements
                        if "card_frame" in asset_name and asset_name in self.face_names:
                            replacement_file = self.face_names[asset_name]
                            replacement_path = os.path.join(
                                "res", "frame", replacement_file
                            )
                            replacement_source = "frame"

                        # Check for mask replacements
                        elif asset_name in mask_files:
                            replacement_path = mask_files[asset_name]
                            replacement_source = "mask"

                        if replacement_path and os.path.exists(replacement_path):
                            self.log(f"Found matching asset: {asset_name}")
                            self.log(
                                f"Replacing {asset_name} with {os.path.basename(replacement_path)} ({replacement_source})"
                            )

                            try:
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

                                self.log(f"Successfully replaced {asset_name}")
                            except Exception as e:
                                self.log(f"Error replacing {asset_name}: {str(e)}")

                        elif replacement_path:
                            self.log(
                                f"Warning: Replacement file not found: {replacement_path}"
                            )

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
                backup_path = self.create_backup(bundle_file)

                # Save modified data to original file
                self.log("Replacing original file with modified version...")
                with open(bundle_file, "wb") as f:
                    f.write(env.file.save())

                self.log("Process completed!")
                self.log(f"Replaced {replaced_count} assets")
                self.log(f"Original file updated: {bundle_file}")
                self.log(f"Backup saved as: {os.path.basename(backup_path)}")

                messagebox.showinfo(
                    "Success",
                    f"Process completed!\n\n"
                    f"• Replaced {replaced_count} assets\n"
                    f"• Original file updated\n"
                    f"• Backup created: {os.path.basename(backup_path)}",
                )
            else:
                # Save as separate file next to the original
                output_path = bundle_file + "_modified"
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
