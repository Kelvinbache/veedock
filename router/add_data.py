
from fastapi import APIRouter,Request, HTTPException

# local
from db.posgrest_db import conn
from dependencies.limit import limiter


router_add_item = APIRouter()


@router_add_item.post("/")
@limiter.limit("5/minute")
def controller_post(request:Request):
    try:
      #  with conn.cursor() as cur: 
      #    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
      #    conn.commit()  
       
       return {"response":"ok"}
        
    except Exception as err:
       raise HTTPException(status_code = 500, detail=f"error{err}")


