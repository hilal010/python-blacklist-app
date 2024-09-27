from sqlalchemy.orm import Session
from models import User, Blacklist
from schemas import UserCreate, UserInDB, BlacklistCreate, BlacklistInDB
import models

# Kara listeye kullanıcı ekleme
def add_user_to_blacklist(db: Session, user_id: int, reason: str):
    # Kullanıcıyı kontrol et
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None  # Kullanıcı bulunamadı
    
    # Kullanıcının durumu false ise ekleme yapma
    if not user.status:
        return None  # Kullanıcı durumu aktif değil

    # Kara listeye ekle
    db_blacklist = models.Blacklist(
        user_id=user_id,
        reason=reason
    )
    db.add(db_blacklist)
    db.commit()
    db.refresh(db_blacklist)
    return db_blacklist


# Kara listeden kullanıcıyı çıkarma
def remove_user_from_blacklist(db: Session, user_id: int):
    db_blacklist = db.query(models.Blacklist).filter(models.Blacklist.user_id == user_id).first()
    if db_blacklist:
        db.delete(db_blacklist)
        db.commit()
    return db_blacklist

# Kara listede kullanıcının olup olmadığını kontrol etme
def check_user_in_blacklist(db: Session, user_id: int):
    return db.query(models.Blacklist).filter(models.Blacklist.user_id == user_id).first()

