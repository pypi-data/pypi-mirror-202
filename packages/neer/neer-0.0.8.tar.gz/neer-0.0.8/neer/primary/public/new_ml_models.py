from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT, SMALLINT
from neer.base import PrimaryBase

class NewMlModels(PrimaryBase):
    __tablename__ = 'new_ml_models'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    description = Column(TEXT, nullable=False, autoincrement=False)
    s3_model_uri = Column(TEXT, autoincrement=False)
    s3_scalar_url = Column(TEXT, autoincrement=False)
    trained_on = Column(TIMESTAMP(timezone=False), nullable=False, autoincrement=False)
