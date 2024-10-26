# import standard libs:
import functools
import gc
import time

# pymongo:
# Requires pymongo 3.6.0+
# from pymongo import MongoClient
from sqlalchemy.orm import sessionmaker

from bdm2.utils.schemas.connection import postgres_engine

# don't forget to add namespice:
# import some db's:
# connection
# from DataBase.utils.table_utils import *

"""
Must use functools.wraps to inherit name of the func/class 
"""


def singlefuncwrapper(func):
    @functools.wraps(func)
    def onCall(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return onCall


def postgre_wrapper(label='', count_time=True):
    def outer_wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            start = time.perf_counter()
            # intercepting self. from the wrapped class instance:
            wrapped_class_instance = args[0]
            # call session here:
            Session = sessionmaker(bind=postgres_engine)
            # try to get posgres_engine from self.object
            # since we call self(instance, *args, **kwargs)
            # in the get
            # Session = sessionmaker(bind=postgres_engine)
            session = Session()
            # wrapped_class_instance.dynamic_session = session
            try:
                # or return func(*args, **kwargs)
                return func(*args, session=session, **kwargs)
            finally:
                # if you use it as a dynamic attribute:
                # delete (!) dynamic attribute
                # del wrapped_class_instance.dynamic_session
                # delete it with delattr (!)
                # delattr(wrapped_class_instance, 'dynamic_session')

                # and collect data
                gc.collect()
                # safely exiting
                session.rollback()
                session.close()
                if count_time:
                    elapsed = time.perf_counter() - start
                    print(label, f"Postgre connection: {elapsed:.3f} sec")

        return inner_wrapper

    return outer_wrapper

# def mongo_wrapper(label='', count_calls=True, count_time=True):
#     def outer_wrapper(func):
#         @functools.wraps(func)
#         def inner_wrapper(*args, **kwargs):
#
#             start = time.perf_counter()
#             wrapped_class_instance = args[0]
#             client = MongoClient(wrapped_class_instance.mongo_uri)
#
#             try:
#                 return func(*args, client = client, **kwargs)
#             finally:
#                 client.close()
#                 if count_time:
#                     elapsed = time.perf_counter() - start
#                     print(label, f"Mongo connection took: {elapsed:.3f} sec")
#         return inner_wrapper
#
#     return outer_wrapper
