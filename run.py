import os
import sys
from pathlib import Path

def setup_environment():
    # Додаємо поточну директорію до PYTHONPATH
    current_dir = Path(__file__).parent.absolute()
    sys.path.append(str(current_dir))

    # Додаємо шлях до бібліотеки в PATH
    if sys.platform == "win32":
        dll_path = current_dir / "backend/build/Debug"
        os.environ["PATH"] = str(dll_path) + os.pathsep + os.environ["PATH"]
    else:
        lib_path = current_dir / "backend/build/lib"
        if "LD_LIBRARY_PATH" not in os.environ:
            os.environ["LD_LIBRARY_PATH"] = ""
        os.environ["LD_LIBRARY_PATH"] = str(lib_path) + os.pathsep + os.environ["LD_LIBRARY_PATH"]

def main():
    setup_environment()
    
    # Імпортуємо та запускаємо головне вікно
    try:
        from frontend.gui.main_window import MainWindow
        from PyQt5.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()