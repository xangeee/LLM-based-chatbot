from pydantic import BaseModel

class PaperQueryInput(BaseModel):
    text: str

class PaperQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list[str]