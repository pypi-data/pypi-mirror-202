from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class StructureReplacementUnitLookup(PrimaryBase):
    __tablename__ = 'structure_replacement_unit_lookup'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    esri_oid = Column(INTEGER, nullable=False, autoincrement=False)
    structure_type = Column(VARCHAR(191), nullable=False, autoincrement=False)
    replacement_unit_name = Column(VARCHAR(191), nullable=False, autoincrement=False)
