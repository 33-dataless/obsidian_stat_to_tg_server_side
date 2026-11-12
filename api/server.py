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
        self.app = FastAPI(self.lifespan)

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
                log.debug("DECTYPTION: OK")
                payload = Payload.model_validate(raw_data)
                log.debug("VALIDATION: OK")
                self.receiver.process(payload)
                log.debug("GET DATA SUCCESS")

                return {"status": "success"}

            except ValueError as e:
                print("[ERROR] Decryption/JSON:", repr(e))
                raise HTTPException(status_code=400, detail="Invalid payload")

            except ValidationError as e:
                print("[ERROR] Validation:", e.errors())
                raise HTTPException(status_code=422, detail="Validation failed")

        @self.app.get("/health")
        async def health():
            log.debug("HEALTH: OK")
            return {"status": "ok"}
