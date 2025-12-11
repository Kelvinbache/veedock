import uvicorn
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
@limiter.limit("5/minute")
def controller(request:Request):
    return {"hello": "word"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info", reload=True)
