# PySide6 Desktop App Boilerplate

A minimal starter for building cross-platform desktop apps with Python and PySide6 (Qt for Python). It includes:

- A basic `MainWindow` UI (Qt Designer `.ui` file + generated Python class)
- A thin `MainView` wrapper where you can add your logic
- Resource bundling (icons, images, fonts, translations)
- Helper scripts to convert `.ui`/`.qrc` to Python and to build a distributable with PyInstaller

This repository is intended to be used as a starting point for new apps.

---

## Quick Start

### Prerequisites
- Windows 10/11 (tested) — other platforms should work with PySide6, but build steps below focus on Windows.
- Python 3.10+ (64-bit recommended)
- A virtual environment is strongly recommended

### 1) Clone and create a virtual environment
```bash
# Clone
git clone https://github.com/<your-user>/pyside-desktop-app.git
cd pyside-desktop-app
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Run the app (development)
```bash
# Option A: module entry
python -m app.main

# Option B: direct file
python app\main.py
```

You should see a simple main window. UI is defined in `app/_ui/MainWindow_ui.py` generated from `app/_ui/MainWindow.ui`.

---

## Project Structure
```
.
├─ app/
│  ├─ main.py                 # App entry point
│  └─ view/
│     └─ MainView.py          # QMainWindow wrapper that loads the generated UI
├─ app/_ui/
│  ├─ MainWindow.ui           # Source Qt Designer file (edit this in Designer)
│  └─ MainWindow_ui.py        # Generated Python UI class (do not edit by hand)
├─ resources/                 # App assets
│  ├─ icons/
│  ├─ images/
│  ├─ fonts/
│  ├─ translations/
│  └─ resources.qrc           # Qt resource collection (optional)
├─ manage.py                  # Helper commands (convert UI/resources, build exe)
├─ requirements.txt           # Python dependencies
└─ README.md
```

---

## Working with Qt Designer UIs

This template keeps the `.ui` file under `app/_ui` and generates a Python class you import from code. Edit the `.ui` file in Qt Designer, then regenerate Python code using the helper command:

```bash
# Convert all .ui files to *_ui.py and resources.qrc to *_rc.py
python manage.py --convert-uic
```

- The generated file name pattern is `<Name>_ui.py` for each `.ui` file.
- `MainView` imports and uses `Ui_MainWindow` from `app._ui.MainWindow_ui`.
- Do not manually edit generated files; re-run the converter after changes in `.ui` or `.qrc`.

If you add new `.ui` files elsewhere, update `manage.py` or move them under `app/_ui` so the converter can find them.

---

## Theming

`MainView` keeps the base styles from the `.ui` and offers a minimal theming hook via `apply_theme()` with two themes:

- `light` (default) — restores the base stylesheet
- `dark` — appends a small dark palette; extend as needed

---

## Packaging (PyInstaller)

This project includes a convenience command to build a distributable directory using PyInstaller. It tries to include the correct Python DLL automatically (to avoid missing `pythonXY.dll` errors on target machines):

```bash
# Build a one-dir distribution under ./dist/MyApp
python manage.py --create-exe
```

Output layout (simplified):
```
dist/
└─ MyApp/
   ├─ MyApp.exe
   ├─ resources/        # copied from project resources
   └─ _internal/        # PySide6, plugins, and other runtime bits
```

Notes:
- The command uses `--onedir` (folder output). If you prefer a single-file exe (`--onefile`), customize `manage.py` or use `MyApp.spec` directly.
- If antivirus interferes, try `--noupx` (already applied) and ensure you build in a clean directory.
- Build with the same Python version/bitness as your target machines for best compatibility.

## Development Tips

- Keep your logic in `app/view` and other app modules; keep `app/_ui` strictly generated.
- When you change `.ui` or `.qrc`, re-run: `python manage.py --convert-uic`.
- For app resources referenced from `.ui` (icons/images), include them in `resources.qrc` and re-run the converter.
- Use `requirements.txt` to lock versions across the team/CI.

---

## Troubleshooting

- Blank or missing UI widgets
  - Ensure `app/_ui/MainWindow_ui.py` exists. If not, run `python manage.py --convert-uic`.
- "ModuleNotFoundError: app._ui.MainWindow_ui"
  - Regenerate UI, ensure your working directory is the project root when running the app.
- Missing `pythonXY.dll` when launching the built app
  - The helper tries to include it; verify your Python version and check console output during build.
- High DPI scaling looks off
  - Adjust `QT_SCALE_FACTOR_ROUNDING_POLICY` or test without it.

---

## Contributing

Issues and pull requests are welcome. For larger changes, please open an issue to discuss your proposal first.

---

## License

This project is licensed under the Apache License, Version 2.0 (Apache-2.0).

- SPDX-License-Identifier: Apache-2.0
- See the `LICENSE` file at the project root for the full text.
- If you redistribute binaries, include a `NOTICE` file as required by section 4(d). A simple template:

```
MyApp
Copyright (c) 2025 <Your Name or Org>

This product includes software licensed under the Apache License 2.0.
```

---

## Acknowledgements
- Qt for Python (PySide6)
- PyInstaller

