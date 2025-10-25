# Unity Asset Replacer

A simple Tkinter GUI application that replaces card frame assets in Yu-Gi-Oh! Master Duel with custom images.

## Requirements

- Python 3.7+
- UnityPy
- Pillow (PIL)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python asset_replacer.py
```

2. Click "Browse" to select your `data.unity3d` file
3. Place your replacement images in the appropriate folders:
   - Card frame images in `res/frame/` (using the predefined mapping)
   - Other asset replacements in `res/mask/` (matching the asset name)
4. Click "Replace Assets" to process the file
5. Choose whether to replace the original file (with automatic timestamped backup) or save as a new file

## How it works

The application:
- Loads the Unity AssetBundle file using UnityPy
- Searches for two types of assets to replace:
  - **Card Frame Assets**: Assets containing "card_frame" in the name
  - **Mask Assets**: Any assets matching filenames in the `res/mask` folder
- Replaces matching assets with corresponding images from the `res` folder structure
- Asks for user confirmation to either:
  - Replace the original file (after creating a timestamped backup)
  - Save as a separate modified file

## Asset Replacement Types

### Card Frame Assets
The application replaces the following card frame assets from `res/frame/`:
- card_frame00 → normal.png
- card_frame01 → effect.png
- card_frame02 → ritual.png
- card_frame03 → fusion.png
- card_frame07 → spell.png
- card_frame08 → trap.png
- card_frame09 → token.png
- card_frame10 → synchro.png
- card_frame12 → xyz.png
- card_frame13 → pendn.png
- card_frame14 → pend.png
- card_frame15 → pendx.png
- card_frame16 → pends.png
- card_frame17 → pendf.png
- card_frame18 → link.png
- card_frame19 → pendr.png

### Mask Assets
The application also supports replacing any asset with a corresponding image file in `res/mask/`. Simply place your replacement images in the `res/mask/` folder with the same filename (without extension) as the asset you want to replace. Supported image formats include PNG, JPG, JPEG, BMP, and TGA.

## License
This project is licensed under the terms specified in the LICENSE file

## Credits

- [Phanthelia](https://www.deviantart.com/phanthelia) for the original Rush Duel card frame template used in this mod
- [human123091](https://next.nexusmods.com/profile/human123091) for the mask effects
- [Artineo2](https://forums.nexusmods.com/profile/37121345-artineo2/) for the Pendulum/Ritual card frame