"""App methods in the Object menu."""

from tkinter import simpledialog
from typing import TYPE_CHECKING

from component import Component

if TYPE_CHECKING:
    from app import App

import tkinter as tk


class TileDialog:
    """A dialog to get tile parameters from the user."""

    def __init__(self, parent: tk.Tk) -> None:
        """Initialize the TileDialog.

        Parameters
        ----------
        parent : tk.Tk
            The parent window of the dialog.

        """
        self.top = tk.Toplevel(parent)
        self.top.title("Tile Rectangles")

        tk.Label(self.top, text="X Start:").grid(row=0, column=0)
        self.x_start = tk.Entry(self.top)
        self.x_start.grid(row=0, column=1)

        tk.Label(self.top, text="Y Start:").grid(row=1, column=0)
        self.y_start = tk.Entry(self.top)
        self.y_start.grid(row=1, column=1)

        tk.Label(self.top, text="X Spacing:").grid(row=2, column=0)
        self.x_spacing = tk.Entry(self.top)
        self.x_spacing.grid(row=2, column=1)

        tk.Label(self.top, text="Y Spacing:").grid(row=3, column=0)
        self.y_spacing = tk.Entry(self.top)
        self.y_spacing.grid(row=3, column=1)

        tk.Label(self.top, text="Number of X:").grid(row=4, column=0)
        self.num_x = tk.Entry(self.top)
        self.num_x.grid(row=4, column=1)

        tk.Label(self.top, text="Number of Y:").grid(row=5, column=0)
        self.num_y = tk.Entry(self.top)
        self.num_y.grid(row=5, column=1)

        tk.Button(self.top, text="OK", command=self.ok).grid(row=6, column=0)
        tk.Button(self.top, text="Cancel", command=self.cancel).grid(row=6, column=1)

        self.result = None

    def ok(self) -> None:
        """Handle the OK button click."""
        try:
            x_start = int(self.x_start.get())
            y_start = int(self.y_start.get())
            x_spacing = int(self.x_spacing.get())
            y_spacing = int(self.y_spacing.get())
            num_x = int(self.num_x.get())
            num_y = int(self.num_y.get())
            self.result = (x_start, y_start, x_spacing, y_spacing, num_x, num_y)
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid integers.")
            return
        self.top.destroy()

    def cancel(self) -> None:
        """Handle the Cancel button click."""
        self.top.destroy()


def add_component(app: "App") -> None:
    """Add a new component to the canvas.

    Parameters
    ----------
    app : App
        The application instance.

    """
    group = app.group_var.get()
    if not group:
        simpledialog.messagebox.showerror("Error", "No group is selected. Create or select a group to begin.")
        return
    x, y = 50, 50
    component = Component(app, x, y, app.comp_width, app.comp_height, group)
    component.set_color(app.colors[group])
    app.groups[group].append(component)
    app.deselect_all()
    component.select()
    app.update_label(component)


def delete_component(app: "App") -> None:
    """Delete the selected components from the canvas."""
    for comp in app.selected_components:
        app.groups[comp.group].remove(comp)
        comp.delete()
    app.selected_components.clear()


def tile(app: "App") -> None:
    """Tile components based on user input."""
    group = app.group_var.get()
    if not group:
        simpledialog.messagebox.showerror("Error", "No group is selected. Create or select a group to begin.")
        return

    dialog = TileDialog(app.root)
    app.root.wait_window(dialog.top)
    if dialog.result:
        x_start, y_start, x_spacing, y_spacing, num_x, num_y = dialog.result
        for i in range(num_x):
            for j in range(num_y):
                x = x_start + i * x_spacing
                y = y_start + j * y_spacing
                component = Component(app, x, y, app.comp_width, app.comp_height, group)
                component.set_color(app.colors[group])
                app.groups[group].append(component)
        app.update_label(app.groups[group][-1])
