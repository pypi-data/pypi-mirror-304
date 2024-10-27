from fwdi.Application.Abstractions.base_config import BaseConfig

class ResponseConfig(BaseConfig):
    def __init__(self) -> None:
        super().__init__()
        self.Text:str = "Fine"