import json

# fastApi
from fastapi import APIRouter,Request, HTTPException, Depends
from typing import Annotated

# local
from db.posgrest_db import conn
from cache.redis_db import r
from dependencies.limit import limiter
from .login import get_token_user

router_all_items = APIRouter()


@router_all_items.get("/")
@limiter.limit("5/minute")
def controllerAllItems(request:Request, current_get:Annotated[str,Depends(get_token_user)]):
    
    if current_get == "kelvin":
       
       CACHE_KEY = "items"
       TTL_SECONDS = 300
       cache_data = None

       try:
          cache_data = r.get(CACHE_KEY)
     
          if cache_data:
            return {"response redis": json.loads(cache_data)}
      
          else:
    
            with conn.cursor() as cur: 
   
              cur.execute("SELECT * FROM test")
    
              response = cur.fetchall()

              if response is None:
                 raise HTTPException(status_code = 404, detail=f"not found")
        
              else: 
               #   r.set(CACHE_KEY, json.dumps(response), ex=TTL_SECONDS)              
                 return {"response postgres": "send"}
    
       except Exception as e:
          raise HTTPException(status_code=500, detail=f"Connect fall with redis: {e}")
    else :
         raise HTTPException(status_code=401, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
       
    

# A only item 
@router_all_items.get("/{itemId}")
def controller_item(request:Request, itemId:int):
   
   cache_data = None

   try:
       cache_data = r.hgetall(f"item:{itemId}")
     
       if cache_data:
          return {"response redis": cache_data}
      
       else:
    
        with conn.cursor() as cur: 
   
            cur.execute("SELECT num, data FROM test WHERE id = %s", (itemId,))
    
            # response = cur.fetchone()

            if response is None:
                 raise HTTPException(status_code = 404, detail=f"not found")
        
            else: 
                                
               #  schemall_data = {"num":response[0], "data":response[1]} # Delete item shape manual with Date and time 
               #  r.hset(f"item:{itemId}", mapping=schemall_data)

                return {"response postgres": "send"}
            

   except Exception as e:
          raise HTTPException(status_code=500, detail=f"Connect fall with redis: {e}") 
