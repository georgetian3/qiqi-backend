def reset_db(engine: AsyncEngine):
    SQLModel.metadata.create_all(engine)