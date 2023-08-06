from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class RolesOld(PrimaryBase):
    __tablename__ = 'roles_old'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    role_id = Column(INTEGER, nullable=False, autoincrement=False)
    role_name = Column(VARCHAR(25), autoincrement=False)
