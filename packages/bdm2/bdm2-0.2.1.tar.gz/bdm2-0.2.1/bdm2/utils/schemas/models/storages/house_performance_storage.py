from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String, Boolean, Float, Date, DateTime

from bdm2.utils.schemas.components.sqlhelpers.helpers import SQLABase


# ============================================
# Target weights
# ============================================


class WeightSourceTypes(SQLABase):
    __tablename__ = "weight_source_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    comment = Column(String)


class WeightSources(SQLABase):
    __tablename__ = "weight_sources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_type_id = Column(
        Integer, ForeignKey("weight_source_types.id"), nullable=False
    )
    postfix = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("source_type_id", "postfix", name="weight_sources_un"),
    )


class ChickenWeights(SQLABase):
    __tablename__ = "chicken_weights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cycle_house_id = Column(Integer, ForeignKey("cycle_houses.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("weight_sources.id"), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    confidence = Column(Float)
    updated = Column(DateTime, nullable=False)
    comment = Column(String)
    __table_args__ = (
        UniqueConstraint(
            "cycle_house_id", "age", "source_id", name="weights_table_un_2_1"
        ),
    )


class SLTTimetable(SQLABase):
    __tablename__ = "slt_timetable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cycle_house_id = Column(Integer, ForeignKey("cycle_houses.id"), nullable=False)
    date = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    stop_feed_dt = Column(DateTime)
    lifting_dt = Column(DateTime)
    harvest_dt = Column(DateTime)
    slt_dt = Column(DateTime)
    # fasting_start_dt = Column(DateTime)
    bird_count = Column(Integer)
    # fasting_time = Column(Float)
    # weight_loss = Column(Float)
    updated = Column(DateTime)
    comment = Column(String)
    weight = Column(Float)

    __table_args__ = (
        UniqueConstraint("cycle_house_id", "age", name="slt_timetable_un_2"),
    )


# class PIWFHATable(SQLABase):
#     __tablename__ = "piwfha_new"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     slt_id = Column(Integer, ForeignKey("slt_timetable.id"), nullable=False)
#     src_id = Column(Integer, ForeignKey("weight_sources.id"), nullable=False)
#     weight = Column(Float)
#     fasting_start_dt = Column(DateTime)
#     piwfha_dt = Column(DateTime)
#     fasting_time = Column(Float)
#     weight_loss = Column(Float)
#     comment = Column(String)
#     updated = Column(DateTime, nullable=False)
#     user_id = Column(DateTime, nullable=False)
#
#     __table_args__ = (UniqueConstraint("slt_id", "src_id", name="piwfha_new_un"),)


# class PIWFHATableOLD(SQLABase):
#     __tablename__ = "piwfha"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     cycle_house_id = Column(Integer, ForeignKey("cycle_houses.id"), nullable=False)
#     src_id = Column(Integer, ForeignKey("weight_sources.id"), nullable=False)
#     age = Column(Integer, nullable=False)
#     fasting_start_dt = Column(DateTime)
#     piwfha_dt = Column(DateTime)
#     piwfha_weight = Column(Float)
#     fasting_time = Column(Float)
#     weight_loss = Column(Float)
#     comment = Column(String)
#     updated = Column(DateTime, nullable=False)
#     user_id = Column(DateTime, nullable=False)
#     to_delete = Column(Boolean, nullable=False)
