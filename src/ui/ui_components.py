"""
UI components module for the weather widget.
Contains reusable UI components and styling functions with enhanced modern styling.
"""

import tkinter as tk
from tkinter import ttk

# Try to import modern styling libraries
try:
    import ttkbootstrap as ttk_bs
    from ttkbootstrap.constants import *

    TTKBOOTSTRAP_AVAILABLE = True
except ImportError:
    TTKBOOTSTRAP_AVAILABLE = False
    print("ttkbootstrap not available. Using standard tkinter styling.")

try:
    import customtkinter as ctk

    CUSTOMTKINTER_AVAILABLE = True
except ImportError:
    CUSTOMTKINTER_AVAILABLE = False


class UIComponents:
    """Collection of UI components and styling utilities with enhanced modern styling"""

    # Enhanced color scheme with modern colors
    COLORS = {
        "bg_primary": "#1e1e1e",  # Modern dark background
        "bg_secondary": "#2d2d30",  # Slightly lighter dark
        "bg_accent": "#0e0e0e",  # Darker accent
        "text_primary": "#ffffff",  # Pure white text
        "text_secondary": "#cccccc",  # Light gray text
        "text_muted": "#999999",  # Muted gray text
        "accent_blue": "#007acc",  # Modern blue
        "accent_orange": "#ff8c00",  # Vibrant orange
        "accent_green": "#16a085",  # Modern green
        "accent_red": "#e74c3c",  # Modern red
        "accent_yellow": "#f1c40f",  # Bright yellow
        "button_hover": "#005a9e",  # Darker blue hover
        "progress_bg": "#3c3c3c",  # Progress background
        "progress_green": "#2ecc71",  # Bright green
        "progress_yellow": "#f39c12",  # Orange-yellow
        "progress_red": "#e74c3c",  # Bright red
        "border": "#404040",  # Border color
        "shadow": "#000000",  # Shadow color
    }

    # Enhanced font configurations with modern fonts
    FONTS = {
        "title": ("Segoe UI", 14, "bold"),
        "large": ("Segoe UI", 18, "bold"),
        "normal": ("Segoe UI", 11),
        "small": ("Segoe UI", 10),
        "tiny": ("Segoe UI", 9),
        "micro": ("Segoe UI", 8),
    }

    @classmethod
    def create_styled_button(
        cls,
        parent,
        text,
        command=None,
        color="accent_blue",
        font="small",
        width=None,
        height=None,
        style="modern",
        **kwargs,
    ):
        """Create a styled button with enhanced modern appearance"""

        if TTKBOOTSTRAP_AVAILABLE and style == "modern":
            # Use ttkbootstrap for modern styling
            style_map = {
                "accent_blue": "primary",
                "accent_green": "success",
                "accent_red": "danger",
                "accent_orange": "warning",
                "accent_yellow": "warning",
                "text_muted": "secondary",
            }

            button = ttk_bs.Button(
                parent,
                text=text,
                command=command,
                bootstyle=style_map.get(color, "primary"),
                **kwargs,
            )
        else:
            # Enhanced tkinter styling with modern appearance
            bg_color = cls.COLORS.get(color, cls.COLORS["accent_blue"])
            hover_color = cls.COLORS.get("button_hover", "#005a9e")

            button = tk.Button(
                parent,
                text=text,
                command=command,
                bg=bg_color,
                fg="white",
                font=cls.FONTS.get(font, cls.FONTS["small"]),
                bd=0,
                relief="flat",
                activebackground=hover_color,
                activeforeground="white",
                cursor="hand2",
                padx=15,
                pady=8,
                **kwargs,
            )

            # Add hover effects
            def on_enter(e):
                button.config(bg=hover_color)

            def on_leave(e):
                button.config(bg=bg_color)

            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

        if width:
            button.config(width=width)
        if height:
            button.config(height=height)

        return button

    @classmethod
    def create_styled_label(
        cls,
        parent,
        text="",
        font="normal",
        color="text_primary",
        bg="bg_primary",
        **kwargs,
    ):
        """Create a styled label with consistent appearance"""
        text_color = cls.COLORS.get(color, cls.COLORS["text_primary"])
        bg_color = cls.COLORS.get(bg, cls.COLORS["bg_primary"])

        return tk.Label(
            parent,
            text=text,
            font=cls.FONTS.get(font, cls.FONTS["normal"]),
            bg=bg_color,
            fg=text_color,
            **kwargs,
        )

    @classmethod
    def create_styled_frame(cls, parent, bg="bg_primary", **kwargs):
        """Create a styled frame with consistent background"""
        bg_color = cls.COLORS.get(bg, cls.COLORS["bg_primary"])

        return tk.Frame(parent, bg=bg_color, **kwargs)

    @classmethod
    def create_styled_entry(cls, parent, font="normal", **kwargs):
        """Create a styled entry field with modern appearance"""
        if TTKBOOTSTRAP_AVAILABLE:
            return ttk_bs.Entry(
                parent,
                font=cls.FONTS.get(font, cls.FONTS["normal"]),
                bootstyle="primary",
                **kwargs,
            )
        else:
            # Enhanced styling for standard Entry
            entry = tk.Entry(
                parent,
                font=cls.FONTS.get(font, cls.FONTS["normal"]),
                bg="#ffffff",
                fg="#000000",
                insertbackground="#007acc",
                bd=1,
                relief="solid",
                highlightthickness=1,
                highlightcolor=cls.COLORS["accent_blue"],
                **kwargs,
            )

            # Add focus effects
            def on_focus_in(e):
                entry.config(
                    highlightcolor=cls.COLORS["accent_blue"], highlightthickness=2
                )

            def on_focus_out(e):
                entry.config(highlightthickness=1)

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

            return entry

    @classmethod
    def create_progress_canvas(cls, parent, height=20):
        """Create a styled canvas for progress bars"""
        return tk.Canvas(
            parent,
            height=height,
            bg=cls.COLORS["bg_secondary"],
            highlightthickness=1,
            highlightbackground=cls.COLORS["bg_primary"],
        )

    @classmethod
    def draw_progress_bar(cls, canvas, level):
        """Draw a three-section progress bar on the given canvas"""
        canvas.delete("all")

        canvas_width = canvas.winfo_width()
        if canvas_width <= 1:
            # Canvas not ready, try again later
            canvas.after(100, lambda: cls.draw_progress_bar(canvas, level))
            return

        canvas_height = canvas.winfo_height() or 20

        # Draw progress bar background
        canvas.create_rectangle(
            0,
            0,
            canvas_width,
            canvas_height,
            fill=cls.COLORS["progress_bg"],
            outline=cls.COLORS["bg_secondary"],
            width=1,
        )

        # Define the three sections
        section_width = canvas_width / 3

        # Colors for each section (Green, Yellow, Red)
        colors = [
            cls.COLORS["progress_green"],
            cls.COLORS["progress_yellow"],
            cls.COLORS["progress_red"],
        ]

        # Draw the three sections
        for i in range(3):
            x1 = i * section_width
            x2 = (i + 1) * section_width

            # Base color section
            canvas.create_rectangle(
                x1 + 1,
                1,
                x2 - 1,
                canvas_height - 1,
                fill=colors[i],
                outline="",
                width=0,
            )

            # Section separators
            if i < 2:  # Don't draw separator after last section
                canvas.create_line(
                    x2, 1, x2, canvas_height - 1, fill=cls.COLORS["bg_primary"], width=1
                )

        # Draw the indicator
        indicator_x = level * canvas_width

        # Main indicator circle
        canvas.create_oval(
            indicator_x - 6,
            2,
            indicator_x + 6,
            canvas_height - 2,
            fill=cls.COLORS["text_primary"],
            outline=cls.COLORS["bg_primary"],
            width=2,
        )

        # Indicator highlight
        canvas.create_oval(
            indicator_x - 3, 5, indicator_x + 1, 9, fill="#ffffff", outline=""
        )

    @classmethod
    def setup_window_style(
        cls,
        window,
        title="Hoodie Weather Widget",
        size="800x600",
        topmost=True,
        alpha=0.95,
    ):
        """Apply consistent window styling"""
        window.title(title)
        window.geometry(size)
        window.configure(bg=cls.COLORS["bg_primary"])

        if topmost:
            window.attributes("-topmost", True)

        try:
            window.attributes("-alpha", alpha)
        except:
            print("Transparency not supported on this system")

        return window

    @classmethod
    def create_popup_window(cls, parent, title="Popup", size="800x600", alpha=0.95):
        """Create a styled popup window"""
        popup = tk.Toplevel(parent)
        popup.title(title)
        popup.geometry(size)
        popup.configure(bg=cls.COLORS["bg_secondary"])
        popup.attributes("-topmost", True)

        try:
            popup.attributes("-alpha", alpha)
        except:
            pass

        return popup

    @classmethod
    def create_modern_popup(cls, parent, title="Settings", size="900x300"):
        """Create a modern styled popup window with enhanced appearance"""
        if TTKBOOTSTRAP_AVAILABLE:
            popup = ttk_bs.Toplevel(parent)
        else:
            popup = tk.Toplevel(parent)

        popup.title(title)
        popup.geometry(size)
        popup.configure(bg=cls.COLORS["bg_secondary"])
        popup.resizable(False, False)
        popup.transient(parent)
        popup.grab_set()

        # Center the popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")

        # Add subtle transparency and modern styling
        try:
            popup.attributes("-alpha", 0.97)
            popup.attributes("-topmost", True)
        except:
            pass

        # Add shadow effect with border
        try:
            popup.configure(relief="solid", bd=1)
        except:
            pass

        return popup

    @classmethod
    def create_enhanced_settings_popup(cls, parent, weather_widget):
        """Create a beautiful settings popup with modern styling"""
        popup = cls.create_modern_popup(parent, "⚙ Widget Settings", "500x400")

        # Main container with padding
        main_frame = cls.create_styled_frame(popup, bg="bg_secondary")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Header with icon and title
        header_frame = cls.create_styled_frame(main_frame, bg="bg_secondary")
        header_frame.pack(fill="x", pady=(0, 20))

        title = cls.create_styled_label(
            header_frame,
            text="🧥 Hoodie Weather Settings",
            font="title",
            color="text_primary",
            bg="bg_secondary",
        )
        title.pack()

        subtitle = cls.create_styled_label(
            header_frame,
            text="Configure your weather widget preferences",
            font="small",
            color="text_secondary",
            bg="bg_secondary",
        )
        subtitle.pack(pady=(5, 0))

        # Location Settings Section with modern card-like appearance
        location_frame = cls.create_styled_frame(main_frame, bg="bg_primary")
        location_frame.pack(fill="x", pady=(0, 15))
        location_frame.configure(relief="solid", bd=1)

        # Section header
        section_header = cls.create_styled_frame(location_frame, bg="bg_primary")
        section_header.pack(fill="x", padx=15, pady=(15, 10))

        location_title = cls.create_styled_label(
            section_header,
            text="📍 Location Settings",
            font="normal",
            color="accent_blue",
            bg="bg_primary",
        )
        location_title.pack(anchor="w")

        # Radio buttons for location mode
        radio_frame = cls.create_styled_frame(location_frame, bg="bg_primary")
        radio_frame.pack(fill="x", padx=15, pady=(5, 10))

        location_var = tk.StringVar(value="auto")

        auto_radio = tk.Radiobutton(
            radio_frame,
            text="🌐 Auto-detect location (IP-based)",
            variable=location_var,
            value="auto",
            bg=cls.COLORS["bg_primary"],
            fg=cls.COLORS["text_primary"],
            selectcolor=cls.COLORS["bg_secondary"],
            activebackground=cls.COLORS["bg_primary"],
            activeforeground=cls.COLORS["text_primary"],
            font=cls.FONTS["small"],
        )
        auto_radio.pack(anchor="w", pady=2)

        manual_radio = tk.Radiobutton(
            radio_frame,
            text="📌 Set location manually",
            variable=location_var,
            value="manual",
            bg=cls.COLORS["bg_primary"],
            fg=cls.COLORS["text_primary"],
            selectcolor=cls.COLORS["bg_secondary"],
            activebackground=cls.COLORS["bg_primary"],
            activeforeground=cls.COLORS["text_primary"],
            font=cls.FONTS["small"],
        )
        manual_radio.pack(anchor="w", pady=2)

        # Manual location entry
        entry_frame = cls.create_styled_frame(location_frame, bg="bg_primary")
        entry_frame.pack(fill="x", padx=15, pady=(5, 15))

        cls.create_styled_label(
            entry_frame,
            text="Location (e.g., London, UK):",
            font="small",
            color="text_secondary",
            bg="bg_primary",
        ).pack(anchor="w", pady=(0, 5))

        location_entry = cls.create_styled_entry(entry_frame)
        location_entry.pack(fill="x", pady=(0, 10))

        # Test button
        test_btn = cls.create_styled_button(
            entry_frame, text="🌍 Test Location", color="accent_orange", style="modern"
        )
        test_btn.pack(anchor="w")

        # Current location info section
        info_frame = cls.create_styled_frame(main_frame, bg="bg_primary")
        info_frame.pack(fill="x", pady=(0, 20))
        info_frame.configure(relief="solid", bd=1)

        info_header = cls.create_styled_label(
            info_frame,
            text="ℹ Current Location Info",
            font="normal",
            color="accent_green",
            bg="bg_primary",
        )
        info_header.pack(padx=15, pady=(15, 5), anchor="w")

        # Get current location info from weather widget
        current_location = getattr(weather_widget, "weather_data", {}).get(
            "full_location", "Unknown"
        )
        current_coords = getattr(weather_widget, "weather_data", {}).get(
            "coordinates", "Unknown"
        )

        current_info_label = cls.create_styled_label(
            info_frame,
            text=f"Location: {current_location}\nCoordinates: {current_coords}",
            font="small",
            color="text_secondary",
            bg="bg_primary",
            justify="left",
        )
        current_info_label.pack(padx=15, pady=(0, 15), anchor="w")

        # Bottom buttons with improved spacing
        button_frame = cls.create_styled_frame(main_frame, bg="bg_secondary")
        button_frame.pack(fill="x", pady=(10, 0))

        # Left side buttons
        left_buttons = cls.create_styled_frame(button_frame, bg="bg_secondary")
        left_buttons.pack(side="left")

        save_btn = cls.create_styled_button(
            left_buttons, text="💾 Save Settings", color="accent_green", style="modern"
        )
        save_btn.pack(side="left", padx=(0, 10))

        # Right side buttons
        right_buttons = cls.create_styled_frame(button_frame, bg="bg_secondary")
        right_buttons.pack(side="right")

        reset_btn = cls.create_styled_button(
            right_buttons, text="🔄 Reset", color="accent_orange", style="modern"
        )
        reset_btn.pack(side="right", padx=(10, 0))

        cancel_btn = cls.create_styled_button(
            right_buttons,
            text="❌ Cancel",
            command=popup.destroy,
            color="text_muted",
            style="modern",
        )
        cancel_btn.pack(side="right")

        return popup, location_var, location_entry

    # @classmethod
