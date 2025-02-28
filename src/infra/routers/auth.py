
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.usuario_repositorio import RepositorioUsuario

SECRET_KEY = "b39e739fde4f2fa586826d9777751cd94d504b4a01c05d1e809b28df56b0366d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 50


oauth_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

router = APIRouter(prefix="/auth", tags=["Autenticação"])

def criar_token_acesso(email: str, expires_in: int = 50):
    exp = datetime.utcnow() + timedelta(minutes=expires_in)
    payload = {"sub": email, "exp": exp}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token invalido"
            )

def verificador_token(
    db_session: Session = Depends(get_db),
    token: str = Depends(oauth_scheme)
):     #Verifica o token e retorna o usuário autenticado
    try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         email: str = payload.get("sub")

         if email is None:
              raise HTTPException(
                   status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido")
         usuario = RepositorioUsuario(db_session).buscar_por_email(email)

         if usuario is None:
              raise HTTPException(
                   status_code=status.HTTP_401_UNAUTHORIZED,
                   detail="Usuário não encontrado"
              )
         return usuario  #Retorna usuário autenticado
    
    except JWTError:
         raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Token inválido"
         )

@router.post("/token", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    repo = RepositorioUsuario(db)

    usuario = repo.verificar_nome(form_data.username)

    if not usuario or not repo.verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciais inválidas"
        )

    access_token = criar_token_acesso(usuario.email)

    return {"access_token": access_token, "token_type": "bearer"}




