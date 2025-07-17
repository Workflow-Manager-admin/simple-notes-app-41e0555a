from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

from .models import Note, NoteCreate
from .storage import FileNoteStorage

# Project-level constants
STORAGE_FILE = os.environ.get("NOTES_STORAGE_FILE", os.path.join(os.path.dirname(__file__), "notes_db.json"))

openapi_tags = [
    {"name": "Health", "description": "Health check and status endpoints."},
    {"name": "Notes", "description": "Endpoints for managing notes (CRUD)."}
]

app = FastAPI(
    title="Notes API",
    description="A simple API for creating, reading, updating, and deleting notes.",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single storage instance
storage = FileNoteStorage(STORAGE_FILE)


@app.get(
    "/", 
    tags=["Health"], 
    summary="Health Check",
    description="Simple health check endpoint for the Notes API",
    response_description="Healthy status message"
)
def health_check():
    """Returns health status of the backend."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get(
    "/notes",
    response_model=List[Note],
    tags=["Notes"],
    summary="List all notes",
    response_description="A list of notes"
)
def list_notes():
    """
    Retrieve all notes in the system.
    Returns a list (possibly empty) of note objects.
    """
    return storage.list_notes()


# PUBLIC_INTERFACE
@app.post(
    "/notes",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    tags=["Notes"],
    summary="Create a new note",
    response_description="The newly created note"
)
def create_note(note: NoteCreate):
    """
    Create a new note.
    - **title**: title for the note
    - **content**: note body
    Returns the created note with its assigned ID.
    """
    return storage.create_note(note)


# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=Note,
    tags=["Notes"],
    summary="Get a single note by ID",
    response_description="The requested note"
)
def get_note(note_id: str):
    """
    Get note details by note ID.
    - **note_id**: ID of the note to retrieve
    Returns the note, or 404 if not found.
    """
    note = storage.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=Note,
    tags=["Notes"],
    summary="Update an existing note",
    response_description="The updated note"
)
def update_note(note_id: str, note_update: NoteCreate):
    """
    Update a note's title/content by note ID.
    - **note_id**: ID of the note to update
    - **body**: new title/content for the note
    Returns the updated note, or 404 if not found.
    """
    updated = storage.update_note(note_id, note_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    tags=["Notes"],
    summary="Delete a note",
    response_description="Delete status"
)
def delete_note(note_id: str):
    """
    Delete a note by its ID.
    - **note_id**: ID for the note to delete
    Returns 204 if deleted, 404 if note not found.
    """
    deleted = storage.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted"}
