import os
import shutil
import winreg
from pathlib import Path


def add_to_startup():
    """Add the widget to Windows startup"""
    try:
        # Get the current script directory
        current_dir = Path(__file__).parent.absolute()
        bat_file = current_dir / "start_widget.bat"

        # Startup folder path
        startup_folder = (
            Path(os.environ["APPDATA"])
            / "Microsoft"
            / "Windows"
            / "Start Menu"
            / "Programs"
            / "Startup"
        )
        startup_file = startup_folder / "Hoodie Weather Widget.bat"

        # Copy the batch file to startup folder
        shutil.copy2(str(bat_file), str(startup_file))

        print(f"[GOOD] Added to startup: {startup_file}")
        return True

    except Exception as e:
        print(f"Error adding to startup: {e}")
        return False


def create_desktop_shortcut():
    """Create a desktop shortcut for the widget"""
    try:
        import win32com.client

        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "Hoodie Weather Widget.lnk"
        current_dir = Path(__file__).parent.absolute()

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = str(current_dir / "start_widget.bat")
        shortcut.WorkingDirectory = str(current_dir)
        shortcut.IconLocation = str(current_dir / "start_widget.bat")
        shortcut.Description = "Hoodie Weather Widget"
        shortcut.save()

        print(f"[GOOD] Desktop shortcut created: {shortcut_path}")
        return True

    except ImportError:
        print("Note: Install pywin32 for desktop shortcut creation")
        return False
    except Exception as e:
        print(f"Error creating desktop shortcut: {e}")
        return False


if __name__ == "__main__":
    print("Setting up Hoodie Weather Widget...")
    print()

    # Add to startup
    startup_success = add_to_startup()

    # Try to create desktop shortcut
    shortcut_success = create_desktop_shortcut()

    print()
    if startup_success:
        print("[GOOD] Widget will start automatically with Windows")
    else:
        print("[ERROR] Could not add to startup automatically")

    print()
    print("Setup Summary:")
    print("- Widget location:", Path(__file__).parent.absolute())
    print("- Manual start: Double-click start_widget.bat")
    print("- To remove from startup: Delete file from Windows Startup folder")
    print()
    print("IMPORTANT: Weather data is provided by Open-Meteo (free API)")
    print("No API key configuration required - it works immediately!")
    print()
    print("The widget will show live weather data for your location.")
    input("\nPress Enter to continue...")
