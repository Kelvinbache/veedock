import uvicorn
from fastapi import FastAPI, Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from db.posgrest_db import conn

limiter = Limiter(
    key_func=get_remote_address,
)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
@limiter.limit("5/minute") #---> limit of call 
def controller(request:Request):
    try:
       with conn.cursor() as cur: 
    
         cur.execute("SELECT * FROM test")
    
         response = cur.fetchall()

         if response is None:
            raise HTTPException(status_code = 404, detail=f"not found")
        
         else:
           return {"response": response}
    
    except Exception as err:
       raise HTTPException(status_code = 500, detail=f"error{err}")


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
