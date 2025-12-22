# token
from typing import Annotated

# fastApi
from fastapi import APIRouter,Request, HTTPException, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# local
from dependencies.limit import limiter
from dependencies.email import model_email
from dependencies.token import crear_token_conf, decode_token

router_login = APIRouter()
oauth2_shema = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="templates")


async def get_token_user(token:Annotated[str, Depends(oauth2_shema)]):
    try:
      
       username = decode_token(token)
     
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

@router_login.post("/login_up")
@limiter.limit("5/minute")
async def controlle_login_up(request:Request, background_tasks: BackgroundTasks):
    
    data = await request.form()
    
    data_dict = dict(data) 

    token = crear_token_conf(email = data_dict.get("email"))
    
    send = await model_email(data_dict, token)
   
    background_tasks.add_task(model_email, data_dict, token)

    return {"response": send}

@router_login.post("/login")
@limiter.limit("5/minute")
def controlle_login(request:Request,from_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    if from_data.username == "kelvin" and from_data.password == "1234":
       
       token = crear_token_conf(from_data.username)

       return RedirectResponse(url="/home", status_code=302, headers= {"access_token": token, "token_type": "bearer", "Cache-Control":"no-cache"}) # Redirige a /dashboard
    
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

@router_login.get("/confirmar/{token}")
async def confirmar_cuenta(token: str):
    
    try:
        email = decode_token(token)
     
        if not email:
            raise HTTPException(status_code=400, detail= email)
        
        return {"message": "confirmed"}

    except Exception:
        raise HTTPException(status_code=400, detail="Token corrupto o inválido")


@router_login.get("/login")
def controlle_login_user(request:Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@router_login.get("/login_up")
def controlle_login_user(request:Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


###
# Taks  
# 3) Do a sign up, and save data in postgres
# 4) Do a sign in, config the data
# ##