from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate) -> models.Usuario:
    senha_hash = pwd_context.hash(usuario.Senha)
    db_usuario = models.Usuario(Nome=usuario.Nome, Email=usuario.Email, SenhaHash=senha_hash, Role=usuario.Role)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obter_usuario(db: Session, usuario_id: int) -> models.Usuario:
    return db.query(models.Usuario).filter(models.Usuario.UserID == usuario_id).first()

def deletar_usuario(db: Session, usuario_id: int) -> bool:
    db_usuario = db.query(models.Usuario).filter(models.Usuario.UserID == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True
    return False

def atualizar_usuario(db: Session, usuario_id: int, update_data: dict) -> models.Usuario:
    db.query(models.Usuario).filter(models.Usuario.UserID == usuario_id).update(update_data)
    db.commit()
    return db.query(models.Usuario).filter(models.Usuario.UserID == usuario_id).first()

def obter_usuario_por_email(db: Session, email: str) -> models.Usuario:
    return db.query(models.Usuario).filter(models.Usuario.Email == email).first()

def get_user_by_username(db: Session, username: str) -> models.Usuario:
    """Função adicional para buscar usuário pelo username (email)."""
    return db.query(models.Usuario).filter(models.Usuario.Email == username).first()

