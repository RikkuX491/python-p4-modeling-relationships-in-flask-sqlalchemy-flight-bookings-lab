# Modeling Relationships in Flask-SQLAlchemy - Flight Bookings Lab

## Learning Goals

- Use Flask-SQLAlchemy to define a data model with relationships
- Implement an association proxy for a model
- Use SQLAlchemy-Serializer to serialize an object with relationships

---

## Setup

Fork and clone the lab repo.

Run `pipenv install` and `pipenv shell` .

```console
$ pipenv install
$ pipenv shell
```

Change into the `server` directory:

```console
$ cd server
```

The file `server/models.py` defines models named `Flight` and `Customer`.

Run the following commands to create the tables for flights and customers.

```console
$ flask db init
$ flask db migrate -m "initial migration"
$ flask db upgrade head
```

## Task # 1 : Add Booking and relationships with Flight and Customer

A customer can book a flight.

- A booking **belongs to** a flight.
- A booking **belongs to** a customer.
- A flight **has many** customers **through** bookings.
- A customer **has many** flights **through** bookings.

Edit `server/models.py` to add a new model class named `Booking` that inherits
from `db.Model`. Add the following attributes to the `Booking` model:

- a string named `__tablename__` assigned to the value `'bookings'`.
- a column named `id` to store an integer that is the primary key.
- a column named `price` to store a float.
- a column named `destination` to store a string.
- a column named `flight_id` that is a foreign key to the `'flights'` table.
- a column named `customer_id` that is a foreign key to the `'customers'` table.
- a relationship named `flight` that establishes a relationship with the `Flight`
  model. Assign the `back_populates` parameter to match the property name
  defined to the reciprocal relationship in `Flight`.
- a relationship named `customer` that establishes a relationship with the
  `Customer` model. Assign the `back_populates` parameter to match the property
  name defined to the reciprocal relationship in `Customer`.

Edit the `Flight` model to add the following:

- a relationship named `bookings` that establishes a relationship with the
  `Booking` model. Assign the `back_populates` parameter to match the property
  name defined to the reciprocal relationship in `Booking`.

Edit the `Customer` model to add the following:

- a relationship named `bookings` that establishes a relationship with the
  `Booking` model. Assign the `back_populates` parameter to match the property
  name defined to the reciprocal relationship in `Booking`.

Save `server/models.py`. Make sure you are in the `server` directory, then type
the following to perform a migration to add the new model:

```console
$ flask db migrate -m 'add booking'
$ flask db upgrade head
```

Run `server/seed.py` to add sample flights, customers, and bookings to the
database.

```
$ python seed.py
```

Then use either Flask shell or SQLite Viewer to confirm the 3 tables are
populated with the seed data.

## Task # 2: Add Association Proxy

Given a customer, we might want to get a list of flights they've booked.
Currently, you would need to iterate through the customer's bookings to get each
flight. Try this in the Flask shell:

```py
>>> from models import *
>>> customer1 = Customer.query.filter_by(id=1).first()
>>> customer1
<Customer 1>
>>> flights = [booking.flight for booking in customer1.bookings]
>>> flights
[<Flight 1, Jetblue>, <Flight 2, Delta>, <Flight 1, Jetblue>]
>>>
```

Update `Customer` to add an association proxy named `flights` to get a list of
flights through the customer's `bookings` relationship.

Once you've defined the association proxy, you can easily get the flights for a
customer as:

```py
>>> customer1.flights
[<Flight 1, Jetblue>, <Flight 2, Delta>, <Flight 1, Jetblue>]
```

## Task # 3: Add Serialization

- Edit `Customer`, `Flight`, and `Bookings` to inherit from `SerializerMixin`.
- Add serialization rules to avoid errors involving recursion depth (be careful
  about tuple commas).
  - `Flight` should exclude `bookings.flight` and `bookings.customer`
  - `Customer` should exclude `bookings.flight` and `bookings.customer`
  - `Booking` should exclude `customer.bookings` and `flight.bookings`

---