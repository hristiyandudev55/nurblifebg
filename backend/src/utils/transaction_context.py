from contextlib import contextmanager


@contextmanager
def transaction_context(db):
    try:
        yield
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
