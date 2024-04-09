from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app import crud, models, schemas, database, auth
from dotenv import load_dotenv
from .schemas import UsuarioInDB

load_dotenv()  # Isso carrega as variáveis de ambiente do arquivo .env



models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=schemas.Token)
async def login_para_acessar_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud.obter_usuario_por_email(db, email=form_data.username)
    if not usuario or not auth.verificar_senha(form_data.password, usuario.SenhaHash.decode('utf-8')):
  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.criar_access_token(
        data={"sub": usuario.Email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UsuarioInDB)
async def read_users_me(current_user: UsuarioInDB = Depends(auth.get_current_user)):
    return current_user

##############################################################################
@app.post("/usuarios/", response_model=schemas.UsuarioInDB, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.obter_usuario_por_email(db, email=usuario.Email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud.criar_usuario(db=db, usuario=usuario)

@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioInDB)
def ler_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.obter_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    sucesso = crud.deletar_usuario(db, usuario_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"ok": True}

@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioInDB)
def atualizar_usuario(usuario_id: int, usuario: schemas.UsuarioBase, db: Session = Depends(get_db)):
    db_usuario = crud.atualizar_usuario(db, usuario_id, usuario.dict())
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario


@app.get("/usuarios/email/{email}", response_model=schemas.UsuarioInDB)
def ler_usuario_por_email(email: str, db: Session = Depends(get_db)):
    db_usuario = crud.obter_usuario_por_email(db, email=email)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario
