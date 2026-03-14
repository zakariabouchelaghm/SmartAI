import customtkinter as tk
from MemoAI import Memo

# Appearance Settings
tk.set_appearance_mode("Dark")
tk.set_default_color_theme("blue")

class MemoApp(tk.CTk):
    def __init__(self):
        super().__init__()

        # --- Data & Logic Setup ---
        self.memo_logic = Memo()
        self.current_id = None
        self.card_titles = {}
        self.card_notes = {}

        # --- Window Setup ---
        self.title("MemoAI")
        self.geometry('1000x700')
        
        # Grid Layout (Sidebar vs Main Area)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_editor()
        
        # Load initial notes
        self.init_notes()

    def setup_sidebar(self):
        """Creates the search bar, add button, and scrollable list."""
        self.left_sidebar = tk.CTkFrame(self, fg_color="transparent", width=250)
        self.left_sidebar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Search Group
        self.search_entry = tk.CTkEntry(self.left_sidebar, placeholder_text="Search notes...")
        self.search_entry.pack(padx=5, pady=(15, 0), fill="x")
        
        self.search_button = tk.CTkButton(self.left_sidebar, text='Search', command=self.search_notes)
        self.search_button.pack(padx=5, pady=(5, 10), fill="x")

        # Add Note Button
        self.add_button = tk.CTkButton(self.left_sidebar, text="+ New Note", 
                                       fg_color="#28a745", hover_color="#218838",
                                       command=self.prepare_new_note)
        self.add_button.pack(padx=5, pady=5, fill="x")

        # Scrollable Area
        self.scrollable_frame = tk.CTkScrollableFrame(self.left_sidebar, width=220)
        self.scrollable_frame.pack(padx=5, pady=10, fill="both", expand=True)

    def setup_main_editor(self):
        """Creates the right-side editor area."""
        self.note_Frame = tk.CTkFrame(self, fg_color="transparent")
        self.note_Frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        self.note_Frame.grid_columnconfigure(0, weight=1)
        self.note_Frame.grid_rowconfigure(1, weight=1)

        self.title_entry = tk.CTkTextbox(
            self.note_Frame, font=tk.CTkFont(size=40, weight="bold"),
            fg_color="transparent", border_width=0, height=60
        )
        self.title_entry.grid(row=0, column=0, sticky="ew", pady=(10, 0))

        self.note_entry = tk.CTkTextbox(
            self.note_Frame, font=tk.CTkFont(size=18),
            fg_color="transparent", border_width=0
        )
        self.note_entry.grid(row=1, column=0, sticky="nsew", pady=10)

        # Permanent Save Button
        self.save_button = tk.CTkButton(
            self.note_Frame, text="Save Changes", 
            command=self.handle_save,
            fg_color="#1f6aa5", font=tk.CTkFont(weight="bold")
        )
        self.save_button.grid(row=2, column=0, pady=20)

    # --- Logic Methods ---

    def add_card(self, note_id, title, note):
        """Dynamically creates a card in the sidebar."""
        card = tk.CTkFrame(self.scrollable_frame, corner_radius=8, 
                           fg_color=("#F2F2F2", "#2B2B2B"), border_width=1)
        card.pack(fill="x", padx=5, pady=5)
        card.grid_columnconfigure(0, weight=1)

        # Title on card
        t_lbl = tk.CTkLabel(card, text=title, font=tk.CTkFont(size=14, weight="bold"))
        t_lbl.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))
        self.card_titles[note_id] = t_lbl

        # Snippet on card
        snippet = note[:40] + "..." if len(note) > 40 else note
        n_lbl = tk.CTkLabel(card, text=snippet, font=tk.CTkFont(size=11), text_color="gray")
        n_lbl.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 5))
        self.card_notes[note_id] = n_lbl

        # Delete button
        del_btn = tk.CTkButton(card, text="✕", width=20, height=20, fg_color="transparent",
                               hover_color="#ff4d4d", command=lambda: self.delete_note(note_id, card))
        del_btn.grid(row=0, column=1, padx=5, pady=5)

        # Click to Edit Bindings
        for widget in [card, t_lbl, n_lbl]:
            widget.bind("<Button-1>", lambda e: self.load_note_into_editor(note_id, title, note))

    def load_note_into_editor(self, note_id, title, note):
        self.current_id = note_id
        self.title_entry.delete("0.0", "end")
        self.note_entry.delete("0.0", "end")
        self.title_entry.insert("0.0", title)
        self.note_entry.insert("0.0", note)

    def handle_save(self):
        title = self.title_entry.get("0.0", "end-1c")
        content = self.note_entry.get("0.0", "end-1c")
        
        if self.current_id is None: # It's a brand new note
            new_id = self.memo_logic.add_note(content, title)
            self.refresh_sidebar()
            self.current_id = new_id
        else: # Update existing
            self.memo_logic.modify_note(self.current_id, title, content)
            self.update_card_live(title, content)

    def update_card_live(self, title, content):
        if self.current_id in self.card_titles:
            self.card_titles[self.current_id].configure(text=title)
            snippet = content[:40] + "..." if len(content) > 40 else content
            self.card_notes[self.current_id].configure(text=snippet)

    def prepare_new_note(self):
        self.current_id = None
        self.title_entry.delete("0.0", "end")
        self.note_entry.delete("0.0", "end")
        self.title_entry.insert("0.0", "New Title")
        self.note_entry.insert("0.0", "Start typing...")

    def delete_note(self, note_id, card_widget):
        card_widget.destroy()
        self.memo_logic.delete_note(note_id)
        if self.current_id == note_id:
            self.prepare_new_note()

    def search_notes(self):
        # 1. Clear current sidebar UI
        self.clear_cards()
        
        # 2. Get the search query
        query = self.search_entry.get()
        
        # If search is empty, just show all notes normally
        if not query.strip():
            self.init_notes()
            return

        similarities = {}
        notes = self.memo_logic.show_notes()
        
        # 3. Calculate similarity for every note
        for note in notes:
            # note[0] is the ID
            similarities[note[0]] = self.memo_logic.get_similarity_note(query, note[0])
        
        # 4. Sort by similarity score (highest first)
        sorted_notes = dict(sorted(similarities.items(), key=lambda x: x[1], reverse=True))
        
        # 5. Display the results
        # Note: Your original logic handled >3 and <3 similarly, 
        # so we can use one clean loop to render the results.
        for note_id in sorted_notes:
            # Only display if there is some relevance (optional: add a threshold)
            note_data = self.memo_logic.fetch_note(note_id)
            if note_data:
                self.add_card(note_data[0], note_data[2], note_data[1])

    def clear_cards(self):
        for child in self.scrollable_frame.winfo_children():
            child.destroy()
        self.card_titles.clear()
        self.card_notes.clear()

    def refresh_sidebar(self):
        self.clear_cards()
        self.init_notes()

    def init_notes(self):
        notes = self.memo_logic.show_notes()
        for note in notes:
            self.add_card(note[0], note[2], note[1])

if __name__ == "__main__":
    app = MemoApp()
    app.mainloop()