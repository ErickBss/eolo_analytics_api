from config.database import db


class DateTime(db.Model):
    __tablename__ = "date_time"

    date_time_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    target_date = db.Column(db.Date)
    target_time = db.Column(db.Integer)


class Geolocation(db.Model):
    __tablename__ = "geolocation"

    geo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(255))
    state = db.Column(db.String(255))
    city = db.Column(db.String(255))
    neighborhood = db.Column(db.String(255))


class DataAggregate(db.Model):
    __tablename__ = "data_aggregate"

    geo_id = db.Column(
        db.Integer, db.ForeignKey("geolocation.geo_id"), primary_key=True
    )
    date_time_id = db.Column(
        db.Integer, db.ForeignKey("date_time.date_time_id"), primary_key=True
    )
    mid_temp = db.Column(db.Float)
    mid_wind_speed = db.Column(db.Float)
    mid_wind_direction = db.Column(db.String(255))
    mid_real_feal = db.Column(db.Float)
    mid_humidity = db.Column(db.Float)
    mid_precipitation = db.Column(db.Float)

    date_time = db.relationship("DateTime", backref="data_aggregate", uselist=False)
    geolocation = db.relationship("Geolocation", backref="data_aggregate")
