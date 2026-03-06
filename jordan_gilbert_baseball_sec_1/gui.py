import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import date, datetime

import db

"""
GUI module for the Baseball Manager application.

This module provides a graphical interface using Tkinter that allows users
to manage a baseball lineup stored in a database. Users can add, remove,
move, and edit players, as well as set a game date and view days remaining
until the game.
"""

'''
Had to use help for error catching and some padding, Seen there was some padding for ew and sticky, 
wanted to implement but would take more time then needed for cleaner GUI 
Pulled comparisions from in class
'''

# =====================================================
#                   Frame/Layout
# =====================================================

class BaseballManagerFrame(ttk.Frame):
    """
    Main GUI frame for the Baseball Manager application.

    This frame contains the lineup table, date information, and
    buttons that allow users to manage players and game dates.
    """

    def __init__(self, parent):
        """
        Initialize the BaseballManagerFrame.

        Args:
            parent: The parent Tkinter window.
        """
        super().__init__(parent, padding="10 10 10 10")
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)

        db.import_csv_if_empty()

        #Overhead Vars
        self.current_date_text = tk.StringVar()
        self.game_date_text = tk.StringVar()
        self.days_until_text = tk.StringVar()
        self.game_date = date(2026, 3, 10)

        #Initis
        self.init_components()
        self.update_dates()
        self.refresh_players()

    def init_components(self):
        """
        Create and arrange all GUI widgets.

        This includes the header, date labels, player table,
        scrollbar, and action buttons.
        """
        header = ttk.Label(self, text="Baseball Manger", anchor="center")
        header.config()
        header.grid(row=0, column=0)

        #Labels for overhead
        ttk.Separator(self, orient="horizontal").grid(row=1, column=0)
        ttk.Label(self, text="Current Date:").grid(row=2, column=0)
        ttk.Label(self, textvariable=self.current_date_text).grid(row=2, column=2)
        ttk.Label(self, text="Game Date:").grid(row=3, column=0)
        ttk.Label(self, textvariable=self.game_date_text).grid(row=3, column=2)
        ttk.Label(self, text="Days Until Game:").grid(row=4, column=0)
        ttk.Label(self, textvariable=self.days_until_text).grid(row=4, column=2)

        # Table
        columns = ("bat_order", "first_name", "last_name", "position", "at_bats", "hits")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=6)

        for col, head in zip(columns, ["Bat Order", "First Name", "Last Name", "Position", "At Bats", "Hits"]):
            self.tree.heading(col, text=head)
            self.tree.column(col, anchor="center")

        #Scroll bar (origonaly required, but not so much with new sizing of geo)
        yscroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview) 
        self.tree.configure(yscrollcommand=yscroll.set)

        self.tree.grid(row=5, column=0, columnspan=3)
        yscroll.grid(row=5, column=3)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=6, column=0, columnspan=3)

        for c in range(3):
            btn_frame.columnconfigure(c, weight=1)

        ttk.Button(btn_frame, text="Game Date", command=self.set_game_date).grid(row=0, column=0)
        ttk.Button(btn_frame, text="Move Player", command=self.move_player).grid(row=0, column=1)
        ttk.Button(btn_frame, text="Edit Player Pos", command=self.edit_player_position).grid(row=0, column=2)
        ttk.Button(btn_frame, text="Add Player", command=self.add_player).grid(row=1, column=0)
        ttk.Button(btn_frame, text="Remove Player", command=self.remove_player).grid(row=1, column=1)
        ttk.Button(btn_frame, text="Edit Player Stat", command=self.edit_player_stats).grid(row=1, column=2)

        # padding
        for child in self.winfo_children():
            if child is self.tree:
                continue
            child.grid_configure(padx=6)

        for child in btn_frame.winfo_children():
            child.grid_configure(padx=25)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(5, weight=1)

    #Dates overhead
    def update_dates(self):
        """
        Update the displayed date information.

        Calculates the current date, the game date, and the
        number of days remaining until the game.
        """
        today = date.today()
        days_until = (self.game_date - today).days
        self.current_date_text.set(today.strftime("%Y-%m-%d"))
        self.game_date_text.set(self.game_date.strftime("%Y-%m-%d"))
        self.days_until_text.set(str(days_until))

# =====================================================
#               DB and the Tree helpers
# =====================================================
    def refresh_players(self):
        """
        Reload player data from the database and update the table.

        Clears the Treeview and repopulates it with the latest
        player records ordered by bat order.
        """
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Loaded from thr DB (ordered by batOrder)
        for row in db.get_players():
            player_id = row["playerID"]
            self.tree.insert(
                "",
                "end",
                iid=str(player_id),  # store playerID in iid 
                values=(row["batOrder"], row["firstName"], row["lastName"], row["position"], row["atBats"], row["hits"])
            )

    def _persist_tree_order(self):
        """
        Save the current Treeview player order back to the database.

        Updates the bat order values based on the current row order
        displayed in the GUI.
        """
        ids = [int(iid) for iid in self.tree.get_children()]
        db.set_bat_orders(ids)

    def _get_selected_player_id(self):
        """
        Retrieve the player ID of the currently selected row.

        Returns:
            int | None: The selected player's database ID or None
            if no player is selected.
        """
        selected = self.tree.selection()
        if not selected:
            return None
        return int(selected[0])


# =====================================================
#                   Button Handlers
# =====================================================

    def set_game_date(self):
        """
        Prompt the user to enter a new game date.

        Updates the stored game date and refreshes the displayed
        countdown to the game.
        """
        new_date = simpledialog.askstring(
            "Set Game Date", "Enter game date (YYYY-MM-DD):", parent=self.parent
        )
        if not new_date:
            return
        try:
            self.game_date = datetime.strptime(new_date, "%Y-%m-%d").date()
            self.update_dates()
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format.")

    def add_player(self):
        """
        Prompt the user for player information and add a new player.

        The player is added to the database and the table display
        is refreshed afterward.
        """
        first = simpledialog.askstring("Add Player", "First name:", parent=self.parent)
        if first is None:
            return
        last = simpledialog.askstring("Add Player", "Last name:", parent=self.parent)
        if last is None:
            return
        pos = simpledialog.askstring("Add Player", "Position:", parent=self.parent)
        if pos is None:
            return
        at_bats = simpledialog.askstring("Add Player", "At Bats:", parent=self.parent)
        if at_bats is None:
            return
        hits = simpledialog.askstring("Add Player", "Hits:", parent=self.parent)
        if hits is None:
            return

        try:
            db.add_player(first.strip(), last.strip(), pos.strip(), int(at_bats), int(hits))
        except ValueError:
            messagebox.showerror("Error", "At Bats and Hits must be whole numbers.")
            return

        self.refresh_players()

    def remove_player(self):
        """
        Remove the selected player from the lineup.

        Deletes the player from the database and refreshes
        the displayed player list.
        """
        player_id = self._get_selected_player_id()
        if player_id is None:
            messagebox.showinfo("Info", "Select a player row first.")
            return

        db.delete_player(player_id)
        self.refresh_players()
        self._persist_tree_order()
        self.refresh_players()

    def move_player(self):
        """
        Swap the bat order positions of two players.

        Prompts the user for two bat order numbers and swaps
        the players occupying those positions in the database.
        """
        from_order = simpledialog.askinteger(
            "Move Player",
            "Enter the current bat order number of the player to move:",
            parent=self.parent,
            minvalue=1
        )
        if from_order is None:
            return

        to_order = simpledialog.askinteger(
            "Move Player",
            "Enter the bat order number to move to (this will swap with that player):",
            parent=self.parent,
            minvalue=1
        )
        if to_order is None:
            return

        if int(from_order) == int(to_order):
            messagebox.showinfo("Info", "Those bat order numbers are the same. Nothing to do.")
            return

        try:
            db.swap_bat_order(int(from_order), int(to_order))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.refresh_players()

    def edit_player_position(self):
        """
        Update the position of the selected player.

        Prompts the user for a new position and updates
        the player record in the database.
        """
        player_id = self._get_selected_player_id()
        if player_id is None:
            messagebox.showinfo("Info", "Select a player row first.")
            return

        row = db.get_player(player_id)
        if row is None:
            messagebox.showerror("Error", "That player no longer exists.")
            self.refresh_players()
            return

        new_pos = simpledialog.askstring(
            "Edit Player Position",
            "Enter new position:",
            initialvalue=row["position"],
            parent=self.parent
        )
        if new_pos is None:
            return

        db.update_player(player_id, new_pos.strip(), row["atBats"] or 0, row["hits"] or 0)
        self.refresh_players()

    def edit_player_stats(self):
        """
        Update the statistics of the selected player.

        Prompts the user to enter new at-bats and hits values
        and updates the player record in the database.
        """
        player_id = self._get_selected_player_id()
        if player_id is None:
            messagebox.showinfo("Info", "Select a player row first.")
            return

        row = db.get_player(player_id)
        if row is None:
            messagebox.showerror("Error", "That player no longer exists.")
            self.refresh_players()
            return

        new_at_bats = simpledialog.askstring(
            "Edit Player Stats",
            "Enter At Bats:",
            initialvalue=str(row["atBats"] or 0),
            parent=self.parent
        )
        if new_at_bats is None:
            return

        new_hits = simpledialog.askstring(
            "Edit Player Stats",
            "Enter Hits:",
            initialvalue=str(row["hits"] or 0),
            parent=self.parent
        )
        if new_hits is None:
            return

        try:
            db.update_player(player_id, row["position"], int(new_at_bats), int(new_hits))
        except ValueError:
            messagebox.showerror("Error", "At Bats and Hits must be whole numbers.")
            return

        self.refresh_players()

# =====================================================
#                   Main -- From class
# =====================================================

def main():
    """
    Launch the Baseball Manager GUI application.

    Establishes the database connection, creates the main
    application window, and starts the Tkinter event loop.
    """
    db.connect()

    root = tk.Tk()
    root.title("Baseball Manger")
    root.geometry("1200x400")

    BaseballManagerFrame(root)

    root.mainloop()
    
    db.close()


if __name__ == "__main__":
    main()