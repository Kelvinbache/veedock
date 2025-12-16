import uvicorn
import json

from fastapi import FastAPI, Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# local
from db.posgrest_db import conn
from cache.redis_db import r


limiter = Limiter(
    key_func=get_remote_address,
)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
@limiter.limit("5/minute") #---> limit of call 
def controllerAllItems(request:Request):
    
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
                r.set(CACHE_KEY, json.dumps(response), ex=TTL_SECONDS)              
                return {"response postgres": response}
    
    except Exception as e:
          raise HTTPException(status_code=500, detail=f"Connect fall with redis: {e}")    


@app.get("/{itemId}")
@limiter.limit("5/minute") #---> limit of call 
def controller_item(request:Request, itemId:int):
   
   cache_data = None

   try:
       cache_data = r.hgetall(f"item:{itemId}")
     
       if cache_data:
          return {"response redis": cache_data}
      
       else:
    
        with conn.cursor() as cur: 
   
            cur.execute("SELECT num, data FROM test WHERE id = %s", (itemId,))
    
            response = cur.fetchone()

            if response is None:
                 raise HTTPException(status_code = 404, detail=f"not found")
        
            else: 
                                
                schemall_data = {"num":response[0], "data":response[1]} # Delete item shape manual with Date and time 
                r.hset(f"item:{itemId}", mapping=schemall_data)

                return {"response postgres": response}
            

   except Exception as e:
          raise HTTPException(status_code=500, detail=f"Connect fall with redis: {e}") 



@app.post("/")
@limiter.limit("5/minute") #---> limit of call 
def controller_post(request:Request):
    try:
       with conn.cursor() as cur: 
         cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
         conn.commit()  
       
       return {"response":"ok"}
        
    except Exception as err:
       raise HTTPException(status_code = 500, detail=f"error{err}")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info", reload=True)
