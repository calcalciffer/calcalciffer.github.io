from typing import List, Optional, Dict
from datetime import datetime, UTC
from typing import Annotated
from pydantic import BaseModel, Field, BeforeValidator, PlainSerializer

class StatModel(BaseModel):
    index: int
    id: Dict[str, str] # discord_id
    mu: float
    sigma: float
    games: int
    wins: int
    first: int
    subbedIn: int
    subbedOut: int
    civs: Dict[str, int] = {}
    lastModified: Optional[datetime] = datetime(2026, 1, 1, 0, 0, 0)

class PlayerModel(BaseModel):
    id: Dict[str, str] | int
    team: Optional[int] = None
    leader: Optional[str] = None
    position: Optional[int] = None
    flags: List[str] = []
    delta: Optional[float] = 0
    combined_delta: Optional[float] = 0

class MatchModel(BaseModel):
    _id: str
    validation_msg_id: Dict[str, str]
    gametype: Optional[str] = None
    is_cloud: Optional[bool] = False
    players: List[PlayerModel]
    
class MatchParseModel(BaseModel):
    matches: List[MatchModel]


class ParsedPlayerModel(BaseModel):
    steam_id: Optional[str] = None
    user_name: Optional[str] = None
    civ: str
    team: int
    leader: Optional[str] = None
    player_alive: Optional[bool] = None
    discord_id: Optional[str] = None
    placement: Optional[int] = None
    quit: bool = False
    delta: float = 0.0
    season_delta: Optional[float] = None
    combined_delta: Optional[float] = None
    is_sub: bool = False
    subbed_out: bool = False

class ParsedMatchModel(BaseModel):
    game: str  # parsers return "civ6" or "civ7"
    turn: int
    age: Optional[str] = None
    map_type: str
    game_mode: str  # allow "", "FFA", "Teamer", "Duel"
    is_cloud: bool
    players: List[ParsedPlayerModel]
    parser_version: str
    discord_messages_id_list: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approved_at: Optional[datetime] = None
    approver_discord_id: Optional[str] = None
    flagged: bool = False
    flagged_by: Optional[str] = None
    save_file_hash: str
    reporter_discord_id: str

class ParsedMatchParseModel(BaseModel):
    matches: List[ParsedMatchModel]
