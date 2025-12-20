# token
from jose import jwt
from typing import Annotated
from pydantic import BaseModel

# fastApi
from fastapi import APIRouter,Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# local
from dependencies.limit import limiter

router_login = APIRouter()
oauth2_shema = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    username:str
    password:str

async def get_token_user(token:Annotated[str, Depends(oauth2_shema)]):
    try:
       payload  = jwt.decode(token, 'secret', algorithms=['HS256'])       
       username = payload.get("sub")

       if username is None:
          raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
       
       return username
    
    except Exception as err:
        print(err)
        raise HTTPException( status_code=401,detail="Could not validate credentials")

@router_login.post("/token")
@limiter.limit("5/minute")
def controlle_login(request:Request,from_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    if from_data.username == "kelvin" and from_data.password == "1234":
    
       token = jwt.encode({'sub': from_data.username}, 'secret', algorithm='HS256')
        
       return RedirectResponse(url="/home", status_code=302, headers= {"access_token": token, "token_type": "bearer", "Cache-Control":"no-cache"}) # Redirige a /dashboard
    
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")



@router_login.get("/login")
@limiter.limit("5/minute")
def controlle_login_user(request:Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@router_login.get("/login_up")
@limiter.limit("5/minute")
def controlle_login_user(request:Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


###
# Taks  
# 1) config the backend for send email
# 2) Config the email, and save token cache for a period of time, example: 10 min
# 3) Do a sign up, and save data in postgres
# 4) Do a sign in, config the data
# ##