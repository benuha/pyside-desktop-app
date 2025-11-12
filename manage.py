import json
import os
import subprocess
import sys

from PIL.Image import Resampling


def convert_files():
    config_files = [
        ["resources/resources.qrc", "app/_ui"],
        ["app/*.ui", "app/_ui"],
        ["app/**/*.ui", "app/_ui"],
        ["app/**/**/*.ui", "app/_ui"],
    ]

    for file_pattern, output_dir in config_files:
        for root, _, files in os.walk(os.path.dirname(file_pattern)):
            for file in files:
                if file.endswith(".ui"):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(
                        output_dir, os.path.splitext(file)[0] + "_ui.py"
                    )
                    subprocess.run(
                        ["pyside6-uic", input_file, "-o", output_file, "--from-imports"]
                    )
                elif file.endswith(".qrc"):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(
                        output_dir, os.path.splitext(file)[0] + "_rc.py"
                    )
                    subprocess.run(["pyside6-rcc", input_file, "-o", output_file])


def convert_png_to_ico(png_path, ico_path, size=32):
    """Convert a PNG image to ICO format with multiple sizes."""
    from PIL import Image

    img = Image.open(png_path)
    resized_img = img.resize(
        (size, size), Resampling.LANCZOS
    )  # Use LANCZOS for high-quality
    resized_img.save(ico_path, format="ICO", sizes=[(size, size)])
    sys.exit(0)


def create_exe_file():
    """Build the Desktop app executable using PyInstaller directly.

    Ensures the correct Python DLL (pythonXY.dll) is bundled to avoid
    LoadLibrary errors like "python39.dll not found" on target machines.
    """
    # Base command
    cmd = [
        "pyinstaller",
        "-y",
        "--clean",
        "--noupx",
        "--noconsole",
        "--onedir",
        "--icon=resources/icons/app.ico",
        "--name=MyApp",
        "--add-data=resources;resources",
    ]

    # Try to locate the Python DLL and force-include it
    try:
        major, minor = sys.version_info.major, sys.version_info.minor
        dll_name = f"python{major}{minor}.dll"
        candidates = [
            os.path.join(sys.base_prefix),
            os.path.join(sys.base_prefix, "DLLs"),
            os.path.dirname(sys.executable),
        ]
        # Typical locations
        dll_path = None
        for c in candidates:
            if c and os.path.isdir(c):
                p = os.path.join(c, dll_name)
                if os.path.isfile(p):
                    dll_path = os.path.abspath(p)
                    break
        if dll_path:
            # Place next to the executable inside one-dir
            cmd.append(f"--add-binary={dll_path};.")
            print(f"Including Python DLL: {dll_path}")
        else:
            print(
                f"Warning: Could not find {dll_name}. PyInstaller should bundle it automatically, but if you still see missing-DLL errors, install the same Python version on the build machine."
            )
    except Exception as e:
        print(f"Warning while searching for Python DLL: {e}")

    # Entry point
    cmd.append("app/main.py")

    # Use subprocess.run so output streams to console
    subprocess.run(cmd)


if __name__ == "__main__":
    usage = "Usage: python manage.py [ --convert-uic | --create-exe ]"
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)

    if sys.argv[1] == "--convert-uic":
        convert_files()
    elif sys.argv[1] == "--create-exe":
        create_exe_file()
    elif sys.argv[1] == "--convert-png-to-ico":
        if len(sys.argv) != 4:
            print(
                "Usage: python manage.py --convert-png-to-ico <input_png> <output_ico>"
            )
            sys.exit(1)
        input_png = sys.argv[2]
        output_ico = sys.argv[3]
        convert_png_to_ico(input_png, output_ico)
    else:
        print(usage)
        sys.exit(1)
