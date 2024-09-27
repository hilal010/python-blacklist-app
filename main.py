import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import models
import schemas

# Logging yapılandırması
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = FastAPI()

# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add user to blacklist
@app.post("/blacklist/add", response_model=schemas.BlacklistInDB)
def add_user_to_blacklist(user_id: int, reason: str, db: Session = Depends(get_db)):
    logging.info(f"Attempting to add user {user_id} to blacklist with reason: {reason}")
    
    # Kullanıcıyı bul
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # Kullanıcı mevcut değilse hata döndür
    if not user:
        logging.warning(f"User {user_id} not found for blacklist addition")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Kullanıcı `status=False` ise kara listeye eklemeyi engelle
    if not user.status:
        logging.warning(f"User {user_id} has a status of False and cannot be added to the blacklist")
        raise HTTPException(status_code=400, detail="User status is False, cannot be added to the blacklist")
    
    # Kara listeye ekle
    blacklist_entry = crud.add_user_to_blacklist(db, user_id, reason)
    
    logging.info(f"User {user_id} added to blacklist successfully")
    return blacklist_entry

# Remove user from blacklist
@app.delete("/blacklist/remove/{user_id}", response_model=schemas.BlacklistInDB)
def remove_user_from_blacklist(user_id: int, db: Session = Depends(get_db)):
    logging.info(f"Attempting to remove user {user_id} from blacklist")
    blacklist_entry = crud.remove_user_from_blacklist(db, user_id)
    if not blacklist_entry:
        logging.warning(f"Blacklist entry for user {user_id} not found")
        raise HTTPException(status_code=404, detail="Blacklist entry not found")
    logging.info(f"User {user_id} removed from blacklist successfully")
    return blacklist_entry

# Check if user is in blacklist
@app.get("/blacklist/check/{user_id}", response_model=schemas.BlacklistInDB)
def check_user_in_blacklist(user_id: int, db: Session = Depends(get_db)):
    logging.info(f"Checking if user {user_id} is in blacklist")
    blacklist_entry = crud.check_user_in_blacklist(db, user_id)
    if not blacklist_entry:
        logging.warning(f"User {user_id} not found in blacklist")
        raise HTTPException(status_code=404, detail="User not found in blacklist")
    logging.info(f"User {user_id} found in blacklist")
    return blacklist_entry

