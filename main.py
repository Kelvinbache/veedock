import uvicorn

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dependencies.limit import limiter
from fastapi.staticfiles import StaticFiles


# router
from router.all_items import router_all_items
from router.add_data import router_add_item
from router.login import router_login
from router.home import home
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router_login, prefix="/token")
app.include_router(home)
app.include_router(router_all_items)
app.include_router(router_add_item)




if __name__ == "__main__":
    uvicorn.run("main:app", port=8090, log_level="info", reload=True)
