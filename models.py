from pony.orm import Database, Required, Json, Optional

from settings import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserState(db.Entity):
    """User`s state inside the scenario"""
    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)


class Registration(db.Entity):
    """Registration request"""
    departure = Required(str)
    arrival = Required(str)
    chosen_date = Required(str)
    places = Required(str)
    phone_number = Required(str)
    email = Required(str)
    confirmed = Required(bool)
    comment = Optional(str)


db.generate_mapping(create_tables=True)