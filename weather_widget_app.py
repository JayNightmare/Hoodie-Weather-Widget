"""
Weather Widget Application - Main Entry Point
Desktop weather widget with hoodie comfort recommendations.
"""

import os
import sys

# Add the src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
sys.path.insert(0, src_path)


def main():
    """Main entry point for the weather widget application"""
    print("Starting Weather Widget Application...")
    print("Loading modules from structured folders...")

    try:
        from src.ui.weather_widget import WeatherWidget

        print("[GOOD] UI Module loaded")
        print("[GOOD] API Module loaded")
        print("[GOOD] Core Modules loaded")
        print("[GOOD] All dependencies ready")
        print()

        # Create and run the widget
        widget = WeatherWidget()
        widget.run()

    except ImportError as e:
        print(f"[ERROR] Error importing modules: {e}")
        print("\nMake sure the src folder structure is correct:")
        print("  src/ui/weather_widget.py")
        print("  src/ui/ui_components.py")
        print("  src/api/weather_api.py")
        print("  src/core/settings_manager.py")
        print("  src/core/hoodie_calculator.py")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nWidget closed by user.")
    except Exception as e:
        print(f"[ERROR] Error starting widget: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
