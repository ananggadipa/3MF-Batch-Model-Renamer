import zipfile
import tempfile
import shutil
import os
import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


# -----------------------------
# Utilities
# -----------------------------

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)


def extract_metadata(model_path):
    with open(model_path, "r", encoding="utf-8") as f:
        content = f.read()

    def get_value(tag):
        match = re.search(
            rf'<metadata name="{tag}">(.*?)</metadata>',
            content,
            flags=re.DOTALL
        )
        return match.group(1) if match else ""

    return get_value("Title"), get_value("Description"), get_value("Designer")


# -----------------------------
# Core 3MF Editor
# -----------------------------

def edit_3mf_metadata(input_path, title, description, designer, overwrite):
    temp_dir = tempfile.mkdtemp()

    try:
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        model_path = os.path.join(temp_dir, "3D", "3dmodel.model")

        if not os.path.exists(model_path):
            raise Exception("3dmodel.model not found.")

        with open(model_path, "r", encoding="utf-8") as f:
            content = f.read()

        def replace_or_insert(tag, value):
            nonlocal content
            if value is None:
                return

            pattern = rf'(<metadata name="{tag}">)(.*?)(</metadata>)'

            def replacer(match):
                return match.group(1) + value + match.group(3)

            if re.search(pattern, content, flags=re.DOTALL):
                content = re.sub(pattern, replacer, content, flags=re.DOTALL)
            elif value != "":
                insert_point = content.find("<metadata")
                new_tag = f'\n  <metadata name="{tag}">{value}</metadata>\n'
                content = content[:insert_point] + new_tag + content[insert_point:]

        replace_or_insert("Title", title)
        replace_or_insert("Description", description)
        replace_or_insert("Designer", designer)

        with open(model_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

        if overwrite:
            output_path = input_path
        else:
            folder = os.path.dirname(input_path)
            safe_title = sanitize_filename(title if title else "edited")
            output_path = os.path.join(folder, f"{safe_title}.3mf")

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            for foldername, _, filenames in os.walk(temp_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zip_out.write(file_path, arcname)

        return output_path

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# -----------------------------
# Batch Mode (Drag onto EXE)
# -----------------------------

def process_multiple(files):
    results = []

    for file_path in files:
        if not file_path.lower().endswith(".3mf"):
            continue

        filename_title = os.path.splitext(os.path.basename(file_path))[0]

        try:
            edit_3mf_metadata(
                file_path,
                filename_title,  # Title = filename
                None,            # Keep description
                None,            # Keep designer
                True             # Overwrite
            )
            results.append(f"✔ {os.path.basename(file_path)}")
        except Exception as e:
            results.append(f"✘ {os.path.basename(file_path)} - {str(e)}")

    messagebox.showinfo("Batch Done", "\n".join(results))


# -----------------------------
# GUI Mode
# -----------------------------

def load_file(path):
    selected_file.delete(0, tk.END)
    selected_file.insert(0, path)

    try:
        with zipfile.ZipFile(path, 'r') as zip_ref:
            temp_dir = tempfile.mkdtemp()
            zip_ref.extractall(temp_dir)

            model_path = os.path.join(temp_dir, "3D", "3dmodel.model")
            title, desc, designer = extract_metadata(model_path)

            title_entry.delete(0, tk.END)
            title_entry.insert(0, title)

            description_entry.delete(0, tk.END)
            description_entry.insert(0, desc)

            designer_entry.delete(0, tk.END)
            designer_entry.insert(0, designer)

            shutil.rmtree(temp_dir)

    except:
        pass


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("3MF Files", "*.3mf")])
    if file_path:
        load_file(file_path)


def use_filename_as_title():
    file_path = selected_file.get().strip()
    if not file_path:
        messagebox.showerror("Error", "Select a file first.")
        return

    filename = os.path.splitext(os.path.basename(file_path))[0]
    title_entry.delete(0, tk.END)
    title_entry.insert(0, filename)


def process_file():
    file_path = selected_file.get().strip()
    title = title_entry.get().strip()
    description = description_entry.get().strip()
    designer = designer_entry.get().strip()
    overwrite = overwrite_var.get()

    if not file_path:
        messagebox.showerror("Error", "Select a file.")
        return

    try:
        output = edit_3mf_metadata(file_path, title, description, designer, overwrite)
        messagebox.showinfo("Success", f"Saved:\n{output}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# -----------------------------
# Entry Point
# -----------------------------

if len(sys.argv) > 1:
    root = tk.Tk()
    root.withdraw()
    process_multiple(sys.argv[1:])
    root.destroy()
    sys.exit()


app = tk.Tk()
app.title("3MF Metadata Editor")
app.geometry("600x300")

tk.Label(app, text="3MF File").pack()

selected_file = tk.Entry(app, width=80)
selected_file.pack(pady=5)

tk.Button(app, text="Browse", command=browse_file).pack()

tk.Label(app, text="Title").pack()
title_entry = tk.Entry(app, width=80)
title_entry.pack()

tk.Button(app, text="Use Filename as Title", command=use_filename_as_title).pack(pady=5)

tk.Label(app, text="Description").pack()
description_entry = tk.Entry(app, width=80)
description_entry.pack()

tk.Label(app, text="Designer").pack()
designer_entry = tk.Entry(app, width=80)
designer_entry.pack()

overwrite_var = tk.BooleanVar()
tk.Checkbutton(app, text="Overwrite Original File", variable=overwrite_var).pack()

tk.Button(app, text="Apply Changes", command=process_file).pack(pady=10)

app.mainloop()
