from configcronos.core.entities import Pinger
from configcronos.core.repositories import PingerRepository


class PingerService:

    def __init__(self, pinger_repository: PingerRepository):
        self.pinger_repository = pinger_repository

    def ping(self, **kwargs) -> bool:

        message = kwargs.get("message", "PING")
        alive = kwargs.get("alive", True)
        code = kwargs.get("code", 99)

        self.pinger_repository.ping(message=message, alive=alive, code=code)

        return True
