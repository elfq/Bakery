from utils.database import sqlite as db


class Bakery(db.Table):
  user_id = db.Column("BIGINT", nullable=False, primary_key=True)
  bakery_name = db.Column("TEXT", nullable=False)
  bakebucks = db.Column("INT", nullable=False)
  level = db.Column("INT", nullable=False)

class Baked(db.Table):
  user_id = db.Column("BIGINT", nullable=False, primary_key=True)
  cakes = db.Column("INT", nullable=False, primary_key=True)
  


def creation(debug: bool = False):
    failed = False

    for table in db.Table.all_tables():
        try:
            table.create()
        except Exception as e:
            print(f'Could not create {table.__tablename__}.\n\nError: {e}')
            failed = True
        else:
            if debug:
                print(f'[{table.__module__}] Created {table.__tablename__}.')


    return True if not failed else False
