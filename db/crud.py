from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, email: str):
    return db.query(models.Member).filter(models.Member.email == email).first()

def creat_account(db: Session, user_info: schemas.Member):
    db_item = models.Member(**user_info.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def db_add_credit_card(db: Session, credit_card: schemas.CreditCard, member_id: int):
    db_item = models.CreditCard(**credit_card.dict(), member_id = member_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_own_hotels(db: Session, member_id: int):
    return db.query(models.Hotel).filter(models.Hotel.member_id == member_id).all()

def create_hotel(db: Session, hotel_info: schemas.Hotel, member_id: int):
    db_item = models.Hotel(**hotel_info.dict(), member_id=member_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def ensure_user_owns_order(db: Session, member_id: int, order_id: int):
    result = db.query(models.Order).filter(models.Order.id == order_id).first()
    if result is None:
        return False
    else:
        return result.member_id == member_id


def ensure_no_duplicate_rating(db: Session, order_id: int):
    result = db.query(models.Rating).filter(models.Rating.order_id == order_id).first()
    return result is None


def rate_order(db: Session, rate_info: schemas.Rate):
    db_item = models.Rating(**rate_info.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
