import tkinter as tk


def test_tk_widget():
    """Test if tkinter widget can be built without failure."""
    try:
        # Create widget without displaying it
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
            root,
            text="Test Widget",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
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

        # Update the widget to ensure it's fully constructed
        root.update()

        # Clean up without showing
        root.destroy()

        return True
    except Exception as e:
        print(f"Widget creation failed: {e}")
        return False


if __name__ == "__main__":
    if test_tk_widget():
        print("[GOOD] Widget created successfully!")
    else:
        print("[ERROR] Widget creation failed.")
