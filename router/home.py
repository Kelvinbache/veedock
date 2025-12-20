from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from dependencies.limit import limiter

home = APIRouter()

templates = Jinja2Templates(directory="templates")


@home.get("/home")
@limiter.limit("5/minute")
def controlle_login_user(request:Request):
    return templates.TemplateResponse(request=request, name="home.html", context={})
