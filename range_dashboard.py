```python
import tkinter as tk
from tkinter import ttk

# =========================
# Settings
# =========================
BG = "#0d0f12"
CARD = "#15181d"
CARD_2 = "#1b1f25"
TEXT = "#f2f4f7"
MUTED = "#8f98a5"
ACCENT = "#dce6f2"
BORDER = "#292f38"

FONT = "Segoe UI"


def clean_number(value):
    """Display numbers without unnecessary zeros."""
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))

    return f"{value:.4f}".rstrip("0").rstrip(".")


def calculate(card):
    try:
        start = float(card["start"].get())
        top = float(card["top"].get())
        step = float(card["step"].get())

        if step <= 0:
            raise ValueError

        if top < start:
            raise ValueError

        # Build levels
        levels = []
        current = start

        # Protection against invalid/infinite loops
        max_rows = 1000

        for _ in range(max_rows):
            if current > top + 1e-9:
                break

            half_step = step / 2
            lower_half = current - half_step

            if start == 0:
                growth = 0
            else:
                growth = ((current - start) / abs(start)) * 100

            levels.append(
                (
                    current,
                    lower_half,
                    growth
                )
            )

            current += step

        # Make sure exact top is included if it falls on the step structure
        if levels and abs(levels[-1][0] - top) > 1e-9:
            pass

        # Clear old table
        for item in card["tree"].get_children():
            card["tree"].delete(item)

        # Insert rows
        for i, (price, lower_half, growth) in enumerate(levels, start=1):
            card["tree"].insert(
                "",
                "end",
                values=(
                    i,
                    clean_number(price),
                    clean_number(lower_half),
                    f"{growth:.2f}%"
                )
            )

        card["count"].config(text=f"{len(levels)} levels")

    except ValueError:
        for item in card["tree"].get_children():
            card["tree"].delete(item)

        card["count"].config(text="Enter valid values")


def clear(card):
    card["start"].delete(0, tk.END)
    card["top"].delete(0, tk.END)
    card["step"].delete(0, tk.END)

    for item in card["tree"].get_children():
        card["tree"].delete(item)

    card["count"].config(text="")


def create_card(parent, number):
    card = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    row = (number - 1) // 2
    col = (number - 1) % 2

    card.grid(
        row=row,
        column=col,
        padx=8,
        pady=8,
        sticky="nsew"
    )

    parent.grid_rowconfigure(row, weight=1)
    parent.grid_columnconfigure(col, weight=1)

    # -------------------------
    # Header
    # -------------------------
    header = tk.Frame(card, bg=CARD)
    header.pack(fill="x", padx=18, pady=(16, 10))

    tk.Label(
        header,
        text=f"{number:02d}",
        font=(FONT, 18, "bold"),
        fg=TEXT,
        bg=CARD
    ).pack(side="left")

    count = tk.Label(
        header,
        text="",
        font=(FONT, 9),
        fg=MUTED,
        bg=CARD
    )
    count.pack(side="right")

    # -------------------------
    # Inputs
    # -------------------------
    inputs = tk.Frame(card, bg=CARD)
    inputs.pack(fill="x", padx=18)

    def make_input(parent, title):
        wrapper = tk.Frame(parent, bg=CARD)
        wrapper.pack(side="left", expand=True, fill="x", padx=(0, 6))

        tk.Label(
            wrapper,
            text=title,
            font=(FONT, 9),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w", pady=(0, 5))

        entry = tk.Entry(
            wrapper,
            font=(FONT, 11),
            fg=TEXT,
            bg=CARD_2,
            insertbackground=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT
        )
        entry.pack(fill="x", ipady=7)

        return entry

    start_entry = make_input(inputs, "شروع")
    top_entry = make_input(inputs, "سقف")
    step_entry = make_input(inputs, "پله")

    # -------------------------
    # Buttons
    # -------------------------
    buttons = tk.Frame(card, bg=CARD)
    buttons.pack(fill="x", padx=18, pady=12)

    calculate_button = tk.Button(
        buttons,
        text="CALCULATE",
        command=lambda: calculate(card),
        font=(FONT, 9, "bold"),
        fg=BG,
        bg=ACCENT,
        activeforeground=BG,
        activebackground=TEXT,
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=7
    )
    calculate_button.pack(side="left")

    clear_button = tk.Button(
        buttons,
        text="CLEAR",
        command=lambda: clear(card),
        font=(FONT, 9),
        fg=MUTED,
        bg=CARD_2,
        activeforeground=TEXT,
        activebackground=BORDER,
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=7
    )
    clear_button.pack(side="left", padx=6)

    # -------------------------
    # Table
    # -------------------------
    table_frame = tk.Frame(card, bg=CARD)
    table_frame.pack(fill="both", expand=True, padx=18, pady=(0, 16))

    columns = ("level", "price", "minus_half", "growth")

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=8
    )

    tree.heading("level", text="#")
    tree.heading("price", text="LEVEL")
    tree.heading("minus_half", text="− ½ STEP")
    tree.heading("growth", text="GROWTH")

    tree.column("level", width=35, anchor="center")
    tree.column("price", width=85, anchor="center")
    tree.column("minus_half", width=90, anchor="center")
    tree.column("growth", width=75, anchor="center")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    card_data = {
        "start": start_entry,
        "top": top_entry,
        "step": step_entry,
        "tree": tree,
        "count": count
    }

    # Enter key
    start_entry.bind(
        "<Return>",
        lambda event: calculate(card_data)
    )

    top_entry.bind(
        "<Return>",
        lambda event: calculate(card_data)
    )

    step_entry.bind(
        "<Return>",
        lambda event: calculate(card_data)
    )

    return card_data


# =========================
# Main Window
# =========================

root = tk.Tk()

root.title("Range Matrix")
root.geometry("1100x850")
root.minsize(900, 700)
root.configure(bg=BG)

# -------------------------
# Treeview Style
# -------------------------

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass

style.configure(
    "Treeview",
    background=CARD_2,
    foreground=TEXT,
    fieldbackground=CARD_2,
    borderwidth=0,
    rowheight=28,
    font=(FONT, 9)
)

style.configure(
    "Treeview.Heading",
    background=CARD,
    foreground=MUTED,
    relief="flat",
    font=(FONT, 8, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#303742")],
    foreground=[("selected", TEXT)]
)

# -------------------------
# Top Header
# -------------------------

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=24, pady=(22, 12))

title_frame = tk.Frame(header, bg=BG)
title_frame.pack(side="left")

tk.Label(
    title_frame,
    text="RANGE",
    font=(FONT, 22, "bold"),
    fg=TEXT,
    bg=BG
).pack(side="left")

tk.Label(
    title_frame,
    text=" MATRIX",
    font=(FONT, 22),
    fg=MUTED,
    bg=BG
).pack(side="left")

tk.Label(
    root,
    text="Levels • Half Step • Growth",
    font=(FONT, 9),
    fg=MUTED,
    bg=BG
).pack(anchor="w", padx=27)

# -------------------------
# Dashboard Area
# -------------------------

container = tk.Frame(root, bg=BG)
container.pack(
    fill="both",
    expand=True,
    padx=16,
    pady=(10, 18)
)

for r in range(2):
    container.grid_rowconfigure(r, weight=1)

for c in range(2):
    container.grid_columnconfigure(c, weight=1)

cards = []

for i in range(1, 5):
    cards.append(create_card(container, i))

# -------------------------
# Footer
# -------------------------

footer = tk.Label(
    root,
    text="RANGE MATRIX  •  4 INDEPENDENT CALCULATORS",
    font=(FONT, 8),
    fg="#626b77",
    bg=BG
)

footer.pack(pady=(0, 12))

root.mainloop()
```
