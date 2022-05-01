from pathlib import Path

from pydantic import BaseModel


class CommandResult(BaseModel):
    input: str
    output: str
    cwd: Path

    def __str__(self) -> str:
        return f"{self.input}\n{self.output}"
