from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, JSONB
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT, SMALLINT
from neer.base import PrimaryBase

class ArcgisFeatures(PrimaryBase):
    __tablename__ = 'arcgis_features'
    __table_args__ = {'schema': 'aqueduct'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    team_id = Column(INTEGER, nullable=False, autoincrement=False)
    server_url = Column(TEXT, nullable=False, autoincrement=False)
    service_name = Column(TEXT, nullable=False, autoincrement=False)
    service_type = Column(TEXT, nullable=False, autoincrement=False)
    layer_id = Column(INTEGER, nullable=False, autoincrement=False)
    layer_name = Column(TEXT, nullable=False, autoincrement=False)
    layer_category = Column(TEXT, autoincrement=False)
    fid = Column(INTEGER, nullable=False, autoincrement=False)
    geometry = Column(TEXT, autoincrement=False)
    properties = Column(JSONB, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False, autoincrement=False)