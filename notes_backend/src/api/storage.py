import os
import uuid
import json
from typing import List, Optional
from threading import Lock
from .models import Note, NoteCreate

class FileNoteStorage:
    """
    File-based storage for notes, storing in a single JSON file.
    Thread-safe for simple use cases.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._lock = Lock()
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump([], f)

    def _load_notes(self) -> List[dict]:
        with self._lock:
            with open(self.filepath, "r") as f:
                return json.load(f)

    def _save_notes(self, notes: List[dict]):
        with self._lock:
            with open(self.filepath, "w") as f:
                json.dump(notes, f, indent=2)

    # PUBLIC_INTERFACE
    def list_notes(self) -> List[Note]:
        """Returns a list of all notes."""
        notes = self._load_notes()
        return [Note(**note) for note in notes]

    # PUBLIC_INTERFACE
    def get_note(self, note_id: str) -> Optional[Note]:
        """Returns a note by its ID, or None if not found."""
        notes = self._load_notes()
        for note in notes:
            if note.get("id") == note_id:
                return Note(**note)
        return None

    # PUBLIC_INTERFACE
    def create_note(self, note: NoteCreate) -> Note:
        """Creates and stores a new note, returning the note with its ID."""
        notes = self._load_notes()
        new_note = Note(id=str(uuid.uuid4()), **note.dict())
        notes.append(new_note.dict())
        self._save_notes(notes)
        return new_note

    # PUBLIC_INTERFACE
    def update_note(self, note_id: str, note_update: NoteCreate) -> Optional[Note]:
        """Updates note fields, returns updated note or None if not found."""
        notes = self._load_notes()
        for idx, note in enumerate(notes):
            if note.get("id") == note_id:
                updated = Note(id=note_id, **note_update.dict())
                notes[idx] = updated.dict()
                self._save_notes(notes)
                return updated
        return None

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: str) -> bool:
        """Deletes a note by its ID. Returns True if note existed and was deleted."""
        notes = self._load_notes()
        filtered = [n for n in notes if n.get("id") != note_id]
        removed = len(filtered) < len(notes)
        if removed:
            self._save_notes(filtered)
        return removed
