from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class RatingLookup(PrimaryBase):
    __tablename__ = 'rating_lookup'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    circumstance = Column(VARCHAR(191), nullable=False, autoincrement=False)
    rating = Column(VARCHAR(191), nullable=False, autoincrement=False)
