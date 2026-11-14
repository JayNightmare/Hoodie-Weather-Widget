import os
import sys
from pathlib import Path

def test_startup_files_exist():
    """Test that all required startup files exist."""
    base_dir = Path(__file__).parent.parent
    
    # Check main application file
    main_app = base_dir / "weather_widget_app.py"
    assert main_app.exists(), f"Main application file not found: {main_app}"
    
    # Check batch file exists
    batch_file = base_dir / "start_widget.bat"
    assert batch_file.exists(), f"Startup batch file not found: {batch_file}"
    
    # Check install script exists
    install_script = base_dir / "install.py"
    assert install_script.exists(), f"Install script not found: {install_script}"
    
    return True

def test_startup_batch_content():
    """Test that the batch file has proper content to prevent loops."""
    base_dir = Path(__file__).parent.parent
    batch_file = base_dir / "start_widget.bat"
    
    if not batch_file.exists():
        assert False, "Batch file doesn't exist"
    
    content = batch_file.read_text()
    
    # Check for lock file mechanism to prevent restart loops
    assert "LOCKFILE" in content, "Batch file should have lock file mechanism"
    assert "already running" in content.lower(), "Batch file should check for existing instances"
    
    # Check for proper error handling
    assert "python --version" in content, "Batch file should check Python installation"
    assert "weather_widget_app.py" in content, "Batch file should reference main app"
    
    # Check for startup folder cleanup on error (prevents restart loops)
    assert "Removing from startup" in content, "Batch file should remove itself from startup on critical errors"
    
    return True

def test_application_import():
    """Test that the main application can be imported without display."""
    try:
        # Add the base directory to path
        base_dir = Path(__file__).parent.parent
        src_path = base_dir / "src"
        sys.path.insert(0, str(src_path))
        
        # Try importing without initializing GUI
        from api.weather_api import WeatherAPI
        from core.hoodie_calculator import HoodieComfortCalculator
        from core.settings_manager import SettingsManager
        
        # These should import successfully
        api = WeatherAPI()
        calc = HoodieComfortCalculator()
        settings = SettingsManager()
        
        return True
    except ImportError as e:
        assert False, f"Failed to import core modules: {e}"
    except Exception as e:
        # Other exceptions are ok - we're not testing functionality, just imports
        return True

if __name__ == "__main__":
    test_startup_files_exist()
    test_startup_batch_content()
    test_application_import()
    print("[GOOD] All startup tests passed!")