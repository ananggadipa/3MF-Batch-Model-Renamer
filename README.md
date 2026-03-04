# 3MF Title Cleaner

Batch update the internal **Title metadata** inside `.3mf` files to
match their filenames.

Designed to prevent printer overwrite issues when exporting multiple
variants from CAD or slicer software.

------------------------------------------------------------------------

## 🚩 The Problem

When exporting multiple variants, generated `.3mf` files often share the
same internal `<model name="">` value --- even if the filenames are
different.

Many printers (including Bambu printers) use this internal Title as the
display name.

If multiple files share the same Title: - They may overwrite each
other - They appear identical on the printer - File management becomes
confusing

------------------------------------------------------------------------

## ✅ The Solution

This tool automatically:

1.  Opens the `.3mf` file (ZIP container)
2.  Edits `3D/3dmodel.model`
3.  Sets `<model name="...">` to match the filename
4.  Repackages the file
5.  Saves it in-place

Geometry and slicer settings remain untouched.

------------------------------------------------------------------------

## ✨ Features

-   Batch processing
-   Drag-and-drop support
-   Cross-platform (Windows / macOS / Linux)
-   In-place modification
-   Lightweight and fast
-   No external dependencies (CLI version)

------------------------------------------------------------------------

# 🚀 Usage

## 🖥 Windows (Executable)

1.  Download the latest `.exe` from **Releases**
2.  Select one or more `.3mf` files
3.  Drag them onto the `.exe`
4.  Done

No installation required.

------------------------------------------------------------------------

## 🐍 Python (All Platforms)

### Requirements

-   Python 3.8+

### Drag & Drop

Drag one or more `.3mf` files onto:

    3mf_title_tool.py

### Terminal Usage

``` bash
python 3mf_title_tool.py file1.3mf file2.3mf file3.3mf
```

All files will be updated in-place.

------------------------------------------------------------------------

# 🔧 What Gets Modified

Inside the `.3mf` archive:

    3D/3dmodel.model

Specifically:

``` xml
<model name="OldTitle">
```

Becomes:

``` xml
<model name="FilenameWithoutExtension">
```

Only the first `<model>` tag is modified.

------------------------------------------------------------------------

# ⚠️ Notes

-   Files are modified in-place
-   No automatic backup is created
-   Only Title metadata is changed
-   Geometry, slicer settings, and machine profiles remain untouched

If needed, create backups before processing.

------------------------------------------------------------------------

# 🧠 Technical Overview

`.3mf` files are ZIP containers.

Processing workflow:

1.  Extract archive to temporary directory
2.  Modify XML metadata
3.  Repackage archive
4.  Replace original file atomically

Designed to minimize corruption risk.

------------------------------------------------------------------------

# 📦 Version

v1.0.0

------------------------------------------------------------------------

# 📄 License

MIT License
