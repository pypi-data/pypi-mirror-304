from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import sqlalchemy
from brddb.constants import PgColumns
from brddb.models.postgres import WeightSources
from brddb.models.postgres.common import Clients
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import sessionmaker

from bdm2.logger import build_logger
from bdm2.utils.schemas.components.sqlhelpers.helpers import SQLABase
from bdm2.utils.schemas.connection import postgres_engine


# Убедитесь, что импорт `declarative_base` только один раз


# Определение модели HarvestDayParams
class HarvestDayParams(SQLABase):
    __tablename__ = "harvest_day_params"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(
        Integer,
        ForeignKey("clients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )
    farm_id = Column(
        Integer,
        ForeignKey("farms.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )
    fatsing_start = Column(String, nullable=False)
    hr_period_1 = Column(Integer, nullable=True)
    hr_period_2 = Column(Integer, nullable=True)
    hr_period_3 = Column(Integer, nullable=True)
    wt_loss_in_period_1 = Column(Float, nullable=True)
    wt_loss_in_period_2 = Column(Float, nullable=True)
    wt_loss_in_period_3 = Column(Float, nullable=True)
    recalculate_lifting = Column(Boolean)

    __table_args__ = (
        UniqueConstraint("client_id", "farm_id", name="harvest_day_params_fk"),
        PrimaryKeyConstraint("id", name="harvest_day_params_pk"),
    )


@dataclass
class HarvestDayParamsColumns:
    id: str = "id"
    client_id: str = "client_id"
    farm_id: str = "farm_id"
    fatsing_start: str = "fatsing_start"
    hr_period_1: str = "hr_period_1"
    hr_period_2: str = "hr_period_2"
    hr_period_3: str = "hr_period_3"
    wt_loss_in_period_1: str = "wt_loss_in_period_1"
    wt_loss_in_period_2: str = "wt_loss_in_period_2"
    wt_loss_in_period_3: str = "wt_loss_in_period_3"
    recalculate_lifting: str = "recalculate_lifting"


class MethodsHarvestDayParams:
    @staticmethod
    def get_info(client):
        logger = build_logger(Path(__file__), save_log=False)
        Session = sessionmaker(bind=postgres_engine)
        with Session() as session:
            try:
                # 5
                # _lifting_final_fix_union
                statement = sqlalchemy.select(
                    HarvestDayParams.id.label("id"),
                    Clients.name.label(PgColumns.client_name),
                    HarvestDayParams.farm_id.label("farm_id"),
                    HarvestDayParams.fatsing_start.label("fatsing_start"),
                    HarvestDayParams.hr_period_1.label("hr_period_1"),
                    HarvestDayParams.hr_period_2.label("hr_period_2"),
                    HarvestDayParams.hr_period_3.label("hr_period_3"),
                    HarvestDayParams.wt_loss_in_period_1.label("wt_loss_in_period_1"),
                    HarvestDayParams.wt_loss_in_period_2.label("wt_loss_in_period_2"),
                    HarvestDayParams.wt_loss_in_period_3.label("wt_loss_in_period_3"),
                    HarvestDayParams.recalculate_lifting.label("recalculate_lifting"),
                ).join(
                    Clients, HarvestDayParams.client_id == Clients.id
                )  # .join(Farms, HarvestDayParams.farm_id == Farms.id)

                # session = sessionmaker(bind=postgres_engine)()
                statement = statement.filter(Clients.name.in_(client))
                res = pd.DataFrame(session.execute(statement).all())
                # session.rollback()
                # session.close()

            except Exception as e:
                logger.info(f"Error occurred: {e}")
            finally:
                session.close()
            return res

    @staticmethod
    def check_postfix_is_registered(pifa_postfix, additional_postfix,
                                    logger=build_logger(Path(__file__), save_log=False)):
        pifa_full_postfix = pifa_postfix + additional_postfix
        Session = sessionmaker(bind=postgres_engine)
        with Session() as session:
            try:
                statement = sqlalchemy.select(
                    WeightSources.id,
                    WeightSources.postfix,
                    WeightSources.source_type_id,
                ).where(
                    WeightSources.source_type_id == 5,
                    WeightSources.postfix == pifa_postfix,
                )

                res = pd.DataFrame(session.execute(statement).all())
            except Exception as e:
                logger.info(f"Error occurred: {e}")
            finally:
                session.close()
                if len(res):
                    return True
                else:
                    return False

    @staticmethod
    def register_postfix(pifa_postfix, additional_postfix,
                         logger=build_logger(Path(__file__), save_log=False)):
        pifa_full_postfix = pifa_postfix + additional_postfix
        Session = sessionmaker(bind=postgres_engine)
        with Session() as session:
            try:
                statement1 = sqlalchemy.insert(WeightSources).values(
                    source_type_id=5, postfix=pifa_full_postfix
                )
                session.execute(statement1)
                session.commit()
                statement2 = sqlalchemy.insert(WeightSources).values(
                    source_type_id=5, postfix=pifa_postfix
                )
                session.execute(statement2)
                session.commit()
            except Exception as e:
                logger.info(f"Error occurred: {e}")
            finally:
                session.close()


if __name__ == "__main__":
    mtest = MethodsHarvestDayParams
    result = mtest.get_info(client="KXSAAF")
    # logger.info(result)
