from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class DrawLayer(PrimaryBase):
    __tablename__ = 'draw_layer'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    geojson_data = Column(TEXT, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
