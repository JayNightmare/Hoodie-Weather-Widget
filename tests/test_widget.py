import tkinter as tk
import os
import sys
import pytest


@pytest.mark.skipif(
    not os.environ.get("DISPLAY") and sys.platform != "win32",
    reason="No display available.",
)
def test_tk_widget():
    # Simple test to see if tkinter works
    root = tk.Tk()
    root.title("Test Widget")
    root.geometry("300x280")

    # Position window at top-right of screen
    screen_width = root.winfo_screenwidth()
    x = screen_width - 320  # 300 width + 20 margin
    y = 20  # 20 pixels from top
    root.geometry(f"300x280+{x}+{y}")

    # Basic styling
    root.configure(bg="#2c3e50")
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.9)

    # Add some content
    label = tk.Label(
        root, text="Test Widget", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white"
    )
    label.pack(pady=50)

    button = tk.Button(
        root,
        text="Close",
        command=root.quit,
        bg="#e74c3c",
        fg="white",
        font=("Arial", 10),
    )
    button.pack(pady=20)

    print("Starting test widget...")
    root.mainloop()
    print("Test widget closed.")
