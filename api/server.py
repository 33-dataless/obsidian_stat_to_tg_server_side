from fastapi import FastAPI, Request, HTTPException
from pydantic import ValidationError

from core.crypto import Crypto
from services.receiver import Receiver
from data.models import Payload

from logging import getLogger

log = getLogger(__name__)

class Server:
    def __init__(self, lifespan):
        self.lifespan = lifespan
        self.app = FastAPI(lifespan=self.lifespan)

        self.crypto = Crypto()
        self.receiver = Receiver()

        self._register_routes()

    def _register_routes(self):
        @self.app.post("/api/data")
        async def receive_data(request: Request):
            log.debug("SERVER ACCEPT REQUEST")
            encrypted = await request.body()
            try:
                raw_data = self.crypto.decrypt(encrypted)
                log.debug("DECRYPTION: OK")

                payload = Payload.model_validate(raw_data)
                log.debug("VALIDATION: OK")

                self.receiver.process(payload)
                log.debug("GET DATA SUCCESS")

                return {"status": "success"}

            except ValidationError as e:
                log.exception("Validation error")
                raise HTTPException(
                    status_code=422,
                    detail="Validation failed"
                )

            except ValueError as e:
                log.exception("Decryption/JSON error")
                raise HTTPException(
                    status_code=400,
                    detail="Invalid payload"
                )

        @self.app.get("/health")
        async def health():
            return {"status": "ok"}