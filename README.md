# 3MF Batch Model Title Renamer

Batch update the **Title metadata** inside `.3mf` files to match their filenames.

Designed for Bambu Studio and general 3D printing workflows.

A `.3mf` file is a ZIP container that includes a `3D/3dmodel.model` XML file. When exporting multiple model variants from CAD or slicers, the internal `<metadata name="Title">` value often remains identical across files — even if the filenames differ.

On some printers, file management relies on this internal Title metadata rather than the filename, which can result in unintended overwrites on the SD card.

This lightweight tool extracts the 3MF archive, updates the `<metadata name="Title">` field to match the filename, and repackages the file — preventing conflicts and accidental overwrites.

---

## ✨ What It Does

When you drag one or more `.3mf` files onto the app:

* Sets **Title = filename**
* Overwrites the original file
* Keeps **Description** unchanged
* Keeps **Designer** unchanged
* Shows a summary when finished

No internet required.
No external dependencies.

---

## 🪟 Windows Usage

1. Download the latest `.exe` from **Releases**
2. Select one or more `.3mf` files
3. Drag them onto the `.exe`
4. Done

---

## 🍎 macOS Usage

Option 1 — Run the Python script directly:

```bash
python3 3mf_editor.py
```

Option 2 — Build the app yourself:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed 3mf_editor.py
```

This will generate a `.app` inside the `dist` folder.

> Note: macOS may show a security warning for unsigned apps.
> Right-click → Open → Confirm.

---

## 🛠 Build (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole 3mf_editor.py
```

The executable will be inside:

```
dist/
```

---

## 📦 How It Works

`.3mf` files are ZIP archives.

This tool:

1. Extracts the archive
2. Edits `3D/3dmodel.model`
3. Replaces the `<metadata name="Title">` value
4. Repackages the file

---

## ⚠️ Important

* Files are overwritten in batch mode.
* Always keep backups if working with critical projects.

---

## 💡 Why This Exists

Sometimes project titles inside 3MF files don’t match filenames.
This tool fixes that instantly — in bulk.

---

## License

MIT License

Use it. Modify it. Improve it.
