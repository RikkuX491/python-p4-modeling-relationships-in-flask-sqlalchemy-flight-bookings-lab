from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

# contains definitions of tables and associated schema constructs
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

# create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# define a model class by inheriting from db.Model.
class Flight(db.Model, SerializerMixin):
    __tablename__ = 'flights'

    # Task # 3 solution code
    serialize_rules = ("-bookings.flight", "-bookings.customer")

    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String)

    # Task # 1 solution code
    bookings = db.relationship('Booking', back_populates='flight')

    # Task # 2 solution code
    customers = association_proxy('bookings', 'customer', creator=lambda c: Booking(customer=c))

    def __repr__(self):
        return f'<Flight {self.id}, {self.airline}>'

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    # Task # 3 solution code
    serialize_rules = ("-bookings.flight", "-bookings.customer")

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    # Task # 1 solution code
    bookings = db.relationship('Booking', back_populates='customer')

    # Task # 2 solution code
    hotels = association_proxy('bookings', 'flight', creator=lambda f: Booking(flight=f))

    def __repr__(self):
        return f'<Customer {self.id}, {self.first_name} {self.last_name}>'
    
# Task # 1 solution code
class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'

    # Task # 3 solution code
    serialize_rules = ('-customer.bookings', '-flight.bookings')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    destination = db.Column(db.String)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    flight = db.relationship('Flight', back_populates='bookings')
    customer = db.relationship('Customer', back_populates='bookings')