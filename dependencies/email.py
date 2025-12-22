from fastapi_mail import ConnectionConfig , FastMail, MessageSchema, MessageType
from fastapi import HTTPException


async def model_email(user, token):
    try: 
        conf = ConnectionConfig(
            MAIL_USERNAME = "kelvinabache12@gmail.com",
            MAIL_PASSWORD = "msjz gawa uwkq lgjd",
            MAIL_FROM = "kelvinabache12@gmail.com",
            MAIL_PORT = 587,
            MAIL_SERVER = "smtp.gmail.com",
            MAIL_STARTTLS = True,
            MAIL_SSL_TLS = False,
            USE_CREDENTIALS = True,
            VALIDATE_CERTS = True
        )
        
        message = MessageSchema(
        subject="Confirmación de Cuenta",
        recipients=[user.get("email")],
        body=f"Hola {user.get("email")}!, Haz clic en este link para confirmar tu cuenta: http://localhost:8090/token/confirmar/{token}",
        subtype=MessageType.plain
        )
    
        fm = FastMail(conf)
        
        await fm.send_message(message)
            
        return {"message":"ok"}
    
    except Exception as err:
          print(err)
          raise HTTPException(status_code=500,detail="Server error")
          