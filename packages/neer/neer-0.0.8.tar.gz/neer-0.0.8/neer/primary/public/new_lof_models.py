from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT, SMALLINT
from neer.base import PrimaryBase

class NewLofModels(PrimaryBase):
    __tablename__ = 'new_lof_models'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    description = Column(TEXT, nullable=False, autoincrement=False)
    project_types = Column(SMALLINT, nullable=False, autoincrement=False)
    is_custom = Column(BOOLEAN, nullable=False, autoincrement=False)
