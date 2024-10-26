# from dataclasses import dataclass
# from pathlib import Path
#
# import pandas as pd
# import sqlalchemy
# from brddb.constants import PgColumns
# from brddb.models.postgres import (
#     Clients,
#     BreedTypes,
#     Genders,
#     WeightSources,
#     ChickenWeights,
#     ActualClientsInfoTable as ActualClientsInfo,
# )
# from sqlalchemy import (
#     Column,
#     Integer,
#     ForeignKey,
#     String,
#     UniqueConstraint,
#     PrimaryKeyConstraint,
# )
# from sqlalchemy.orm import sessionmaker
#
# from bdm2.logger import build_logger
# from bdm2.utils.schemas.components.sqlhelpers.helpers import SQLABase
# from bdm2.utils.schemas.connection import postgres_engine
#
#
# # class PIWFHAMethodsDescription(SQLABase):
# #     __tablename__ = "piwfha_methods_description"
# #     id = Column(Integer, primary_key=True)
# #     method_name = Column(String)
# #     description = Column(String)
# #     __table_args__ = (UniqueConstraint("id", name="piwfha_methods_description_fk"),)
#
#
# class PIWFHACalculationMethods(SQLABase):
#     __tablename__ = "piwfha_calculation_methods"
#     id = Column(Integer, primary_key=True)
#     method_id = Column(Integer, ForeignKey("piwfha_methods_description.id"))
#     specific_client_id = Column(Integer, ForeignKey("clients.id"))
#     __table_args__ = (
#         UniqueConstraint(
#             "specific_client_id", "method_id", name="specific_client_fk_d"
#         ),
#         PrimaryKeyConstraint("id", name="piwfha_calculation_methods_pk"),
#     )
#
#
# # ============================================
#
#
# class PIWFHAMethodsCommon:
#     @dataclass
#     class PIWFHAMethodsDescriptionColumns:
#         id: str = "id"
#         method_name: str = "method_name"
#         description: str = "description"
#
#     @dataclass
#     class PIWFHACalculationMethodsColumns:
#         id: str = "id"
#         method_name: str = "method_id"
#         specific_client_id: str = "specific_client_id"
#
#     @staticmethod
#     def get_method_for_client(client):
#         logger = build_logger(Path(__file__), save_log=False)
#         statement = (
#             sqlalchemy.select(
#                 PIWFHACalculationMethods.id.label("calculation_id"),
#                 Clients.name.label(PgColumns.client_name),
#                 PIWFHACalculationMethods.specific_client_id.label("specific_client_id"),
#                 PIWFHAMethodsDescription.method_name.label("method_name"),
#                 PIWFHAMethodsDescription.id.label("method_id"),
#                 PIWFHAMethodsDescription.description.label("description"),
#             )
#             .join(Clients, PIWFHACalculationMethods.specific_client_id == Clients.id)
#             .join(
#                 PIWFHAMethodsDescription,
#                 PIWFHACalculationMethods.method_id == PIWFHAMethodsDescription.id,
#             )
#         )
#         session = sessionmaker(bind=postgres_engine)()
#         statement = statement.filter(Clients.name == client)
#         res = pd.DataFrame(session.execute(statement).all())
#         session.close()
#
#         if not res.empty:
#             logger.info(
#                 f"\nhave found specific method for {res.iloc[0].client_name}\n"
#                 f"{res.iloc[0].method_name}\n"
#                 f"description: {res.iloc[0].description}\n"
#             )
#             return res.iloc[0].method_id
#         else:
#             logger.info(
#                 f"\nno found specific method for {client}\n"
#                 f"will be used one of default\n"
#             )
#             return None
#
#
# def get_avg_piwfha_age_for_client(client_name):
#     statement = (
#         sqlalchemy.select(
#             ActualClientsInfo.gender_id.label("gender_id"),
#             Clients.name.label(PgColumns.client_name),
#             BreedTypes.name.label(PgColumns.breed_type_name),
#             Genders.name.label(PgColumns.gender_name),
#             Clients.id.label(PgColumns.client_id),
#             BreedTypes.id.label(PgColumns.breed_type_id),
#             Genders.id.label(PgColumns.gender_id),
#             WeightSources.id.label(PgColumns.weight_sources_id),
#             ChickenWeights.age.label("piwfha_ages"),
#         )
#         .join(Clients, ActualClientsInfo.client_id == Clients.id)
#         .join(BreedTypes, ActualClientsInfo.breed_type_id == BreedTypes.id)
#         .join(Genders, ActualClientsInfo.gender_id == Genders.id)
#         .join(
#             WeightSources, ActualClientsInfo.piwfha_weights_src_id == WeightSources.id
#         )
#         .join(ChickenWeights, ChickenWeights.source_id == WeightSources.id)
#         .filter(Clients.name == client_name)
#     )
#
#     session = sessionmaker(bind=postgres_engine)()
#     res = pd.DataFrame(session.execute(statement).all())
#     mean_age_for_client = int(res.piwfha_ages.mean())
#     session.close()
#     return mean_age_for_client
