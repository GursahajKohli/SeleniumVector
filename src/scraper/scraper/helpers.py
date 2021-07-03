from enum import Enum, auto

class PaginationConfigOption(Enum):
    NONE = auto()
    NEXTPAGE = auto()
    PAGENUMBER = auto()
    INFINITESCROLL = auto()