from pydantic import BaseModel, ConfigDict, Field

from bbi.domain.memory import MemoryCard


class DialogueTurn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: str
    content: str = Field(min_length=1, max_length=8_000)


class CallbackEvent(BaseModel):
    memory_id: str
    explicit: bool = False


class ConversationInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    conversation_id: str
    owner_id: str
    character_id: str
    active_branch: str = "main"
    current_message: str = Field(min_length=1, max_length=8_000)
    recent_turns: list[DialogueTurn] = Field(default_factory=list, max_length=20)
    callback_history: list[CallbackEvent] = Field(default_factory=list)
    candidate_memories: list[MemoryCard] = Field(default_factory=list, max_length=20)
