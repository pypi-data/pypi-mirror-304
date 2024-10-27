import tkinter as tk
from tkinter import ttk

UNCHECKED = "\u2610"
CHECKED = "\u2612"


class CheckTreeView(ttk.Treeview):
    def __init__(self, master=None, width=200, clicked=None,
                 unchecked=UNCHECKED, checked=CHECKED, **kwargs):
        """
        :param width: the width of the check list
        :param clicked: the optional function if a checkbox is clicked. Takes a
                        `iid` parameter.
        :param unchecked: the character for an unchecked box (default is
                          "\u2610")
        :param unchecked: the character for a checked box (default is "\u2612")

        Other parameters are passed to the `TreeView`.
        """
        if "selectmode" not in kwargs:
            kwargs["selectmode"] = "none"
        if "show" not in kwargs:
            kwargs["show"] = "tree"
        ttk.Treeview.__init__(self, master, **kwargs)
        self.number_selected = 0

    def item_click(self, pos_x: int, pos_y: int) -> int:
        element = self.identify("element", pos_x, pos_y)
        if element == "text":
            iid = self.identify_row(pos_y)
            self._toggle(iid)
        return self.number_selected

    def _toggle(self, iid):
        """
        Toggle the checkbox `iid`
        """
        values = list(self.item(iid).values())[2]
        new_value = UNCHECKED
        number = -1
        if values[0] == UNCHECKED:
            new_value = CHECKED
            number = 1
        values = [new_value] + [_ for _ in values[1:]]
        self.item(iid, values=values)
        self.number_selected = self.number_selected + number

    def populate(self, items: list[tuple]) -> None:
        for item in items:
            values = [UNCHECKED] + [_ for _ in item]
            self.insert('', 'end', values=values)
