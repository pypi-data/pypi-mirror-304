from typing import Optional
import pandas as pd
from pymongo import MongoClient, errors
from bdm2.constants.global_setup.env import (
    MONGO_SERVER, MONGO_PORT, MONGO_USERNAME, MONGO_PASSWORD,
    MONGO_AUTH_DB, MONGO_CONNECTION_NAME)
from bdm2.logger import build_logger
from pathlib import Path


class MongoConnectionParams:
    """
    Stores MongoDB connection parameters, such as server, port, username, password,
    authentication database, and connection name. It also constructs the MongoDB URI for connection.
    """
    server = MONGO_SERVER
    port = MONGO_PORT
    username = MONGO_USERNAME
    password = MONGO_PASSWORD
    auth_db = MONGO_AUTH_DB
    connection_name = MONGO_CONNECTION_NAME

    uri = (f'mongodb://{username}:{password}@{server}:{port}/?'
           f'serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource={auth_db}&authMechanism=SCRAM-SHA-1')


class MongoDBConnection:
    """
    Establishes a connection to the MongoDB database and provides context management for connection handling.

    Attributes:
        client: The MongoClient instance for managing the connection.
        database: The MongoDB database object.
        logger: Logger to track connection status and errors.

    Methods:
        get_database(): Returns the MongoDB database object.
    """

    def __init__(self):
        """
        Initializes the MongoDB connection, logs the connection status, and raises an exception on connection failure.
        """
        self.logger = build_logger(Path(__file__), save_log=False)
        try:
            self.client = MongoClient(MongoConnectionParams.uri)
            self.database = self.client[MongoConnectionParams.auth_db]
            self.logger.info(f"Connected to MongoDB: {MongoConnectionParams.auth_db}")
        except errors.ConnectionFailure as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def __enter__(self):
        """
        Context manager enter method to return the database object for use within a `with` statement.
        """
        return self.database

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit method to close the MongoDB connection and log the closure status.
        """
        self.client.close()
        self.logger.info("MongoDB connection closed")

    def get_database(self):
        """
        Returns the MongoDB database object.

        Returns:
            database: The MongoDB database object.
        """
        return self.database


class MongoCollection:
    """
    Provides utility functions for interacting with a MongoDB collection, including inserting, querying, updating, and deleting documents.

    Attributes:
        collection: The MongoDB collection object.
        logger: Logger to track operations and errors within the collection.

    Methods:
        insert_document(document): Inserts a document into the collection.
        find_document(query, gby): Finds a single document based on the query and optional projection.
        find_all_documents(query, gby): Finds all documents matching the query and returns a DataFrame.
        update_document(query, update): Updates a document based on the query.
        delete_document(query): Deletes a document from the collection based on the query.
        get_unique_fields(sample_size): Retrieves unique fields from a sample of documents in the collection.
    """

    def __init__(self, db, collection_name: str):
        """
        Initializes the MongoCollection by assigning the collection from the given database.

        Args:
            db: The MongoDB database object.
            collection_name: The name of the collection to access.
        """
        self.collection = db[collection_name]
        self.logger = build_logger(Path(__file__), save_log=False)
        self.logger.info(f"Accessed collection: {collection_name}")

    def insert_document(self, document: dict):
        """
        Inserts a document into the collection.

        Args:
            document: A dictionary representing the document to insert.

        Returns:
            The result of the insert operation or None if the insertion fails.
        """
        try:
            return self.collection.insert_one(document)
        except errors.PyMongoError as e:
            self.logger.error(f"Failed to insert document: {e}")
            return None

    def find_document(self, query: dict, gby: Optional[dict] = None):
        """
        Finds a single document from the collection based on the query.

        Args:
            query: A dictionary specifying the search criteria.
            gby: Optional. A dictionary specifying the projection of fields to return.

        Returns:
            The first document that matches the query or None if no document is found.
        """
        try:
            if gby:
                return self.collection.find_one(query, gby)
            return self.collection.find_one(query)
        except errors.PyMongoError as e:
            self.logger.error(f"Failed to find document: {e}")
            return None

    def find_all_documents(self, query: dict = {}, gby: Optional[dict] = None):
        """
        Finds all documents in the collection that match the query and returns them as a DataFrame.

        Args:
            query: A dictionary specifying the search criteria. Default is an empty dictionary.
            gby: Optional. A dictionary specifying the projection of fields to return.

        Returns:
            A DataFrame containing the matching documents or an empty DataFrame if no documents are found.
        """
        try:
            if gby:
                return pd.DataFrame(list(self.collection.find(query, gby)))
            return pd.DataFrame(list(self.collection.find(query)))
        except errors.PyMongoError as e:
            self.logger.error(f"Failed to find documents: {e}")
            return pd.DataFrame()

    def update_document(self, query: dict, update: dict):
        """
        Updates a document in the collection based on the query.

        Args:
            query: A dictionary specifying the search criteria.
            update: A dictionary specifying the fields to update.

        Returns:
            The result of the update operation or None if the update fails.
        """
        try:
            return self.collection.update_one(query, {'$set': update})
        except errors.PyMongoError as e:
            self.logger.error(f"Failed to update document: {e}")
            return None

    def delete_document(self, query: dict):
        """
        Deletes a document from the collection based on the query.

        Args:
            query: A dictionary specifying the search criteria.

        Returns:
            The result of the delete operation or None if the deletion fails.
        """
        try:
            return self.collection.delete_one(query)
        except errors.PyMongoError as e:
            self.logger.error(f"Failed to delete document: {e}")
            return None

    def get_unique_fields(self, sample_size: int = 100) -> set:
        """
        Retrieves unique fields (keys) from a sample of documents in the collection.

        Args:
            sample_size: The number of documents to sample. Default is 100.

        Returns:
            A set of unique field names found in the sampled documents.
        """
        fields = set()
        try:
            for document in self.collection.find().limit(sample_size):
                fields.update(document.keys())
        except errors.PyMongoError as e:
            self.logger.error(f"Failed to fetch unique fields: {e}")
        return fields
