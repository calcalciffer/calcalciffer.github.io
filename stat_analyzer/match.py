from typing import List, Optional, Dict
from datetime import datetime, UTC
from typing import Annotated
from pydantic import BaseModel, Field, BeforeValidator, PlainSerializer

class StatModel(BaseModel):
    index: int
    id: str  # discord_id
    mu: float
    sigma: float
    games: int
    wins: int
    first: int
    subbedIn: int
    subbedOut: int
    civs: Dict[str, int] = {}
    lastModified: Optional[datetime] = datetime.now(UTC)

class PlayerModel(BaseModel):
    id: Dict[str, str] | int
    team: Optional[int] = None
    leader: Optional[str] = None
    position: Optional[int] = None
    flags: List[str] = []
    delta: Optional[float] = 0

class MatchModel(BaseModel):
    _id: str
    validation_msg_id: Dict[str, str]
    gametype: Optional[str] = None
    is_cloud: Optional[bool] = False
    players: List[PlayerModel]
    
class MatchParseModel(BaseModel):
    matches: List[MatchModel]