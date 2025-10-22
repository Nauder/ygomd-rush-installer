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
3. Click "Replace Assets" to process the file
4. Choose whether to replace the original file (with backup) or save as a new file

## How it works

The application:
- Loads the Unity AssetBundle file using UnityPy
- Filters assets that match the criteria:
  - Has `m_Name` and `m_CompleteImageSize` attributes
  - Contains "card_frame" in the name
- Replaces matching assets with corresponding images from the `res` folder
- Asks for user confirmation to either:
  - Replace the original file (after creating a timestamped backup)
  - Save as a separate modified file

## Supported Card Frames

The application replaces the following card frame assets:
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
- card_frame19 → pendf.png

## License
This project is licensed under the terms specified in the LICENSE file

## Credits

- [Phanthelia](https://www.deviantart.com/phanthelia) for the original Rush Duel card frame template used in this mod