from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
class NoteCreate(BaseModel):
    """Schema for creating a new note."""
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content/body of the note")

# PUBLIC_INTERFACE
class Note(NoteCreate):
    """Schema for a note (with ID)."""
    id: str = Field(..., description="Unique identifier for the note")
