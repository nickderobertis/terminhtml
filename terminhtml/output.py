import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class LineEnding(str, Enum):
    LF = "\n"
    CR = "\r"
    CRLF = "\r\n"


class PromptOutput(BaseModel):
    prompt: str
    user_input: str


class LineOutput(BaseModel):
    line: str
    time: datetime.datetime
    line_ending: LineEnding
    prompt_output: Optional[PromptOutput] = None


class Output(BaseModel):
    lines: List[LineOutput]

    @property
    def delays(self) -> List[int]:
        last_time: Optional[datetime.datetime] = None
        delays: List[int] = []
        for line in self.lines:
            if last_time is not None:
                diff = line.time - last_time
                delays.append(int(diff.total_seconds() * 1000))
            last_time = line.time
        delays.append(0)
        if len(delays) != len(self.lines):
            raise ValueError(
                f"Delays should be one longer than lines to account for the "
                f"input delay. Got {len(delays)} delays and {len(self.lines)} lines."
            )
        return delays
