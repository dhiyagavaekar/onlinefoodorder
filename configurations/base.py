from . import database as db_config

def initialize_db_if_not_created():
    # Create the database
    db_config.BASE.metadata.create_all(db_config.ENGINE)