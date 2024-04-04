#!/usr/bin/env python3

from app import app
from models import db, Flight, Customer, Booking

with app.app_context():
    Flight.query.delete()
    Customer.query.delete()
    Booking.query.delete()

    flight1 = Flight(airline="Jetblue")
    flight2 = Flight(airline="Delta")
    flight3 = Flight(airline="American Airlines")
    
    db.session.add_all([flight1, flight2, flight3])
    db.session.commit()

    customer1 = Customer(first_name="Alice", last_name="Baker")
    customer2 = Customer(first_name="Bob", last_name="Carris")
    customer3 = Customer(first_name="Cynthia", last_name="Jones")

    db.session.add_all([customer1, customer2, customer3])
    db.session.commit()

    booking1 = Booking(price=1000.99, destination="Honolulu, Hawaii", flight=flight1, customer=customer1)
    booking2 = Booking(price=3334.74, destination="New Zealand", flight=flight1, customer=customer2)
    booking3 = Booking(price=523.33, destination='Puerto Vallarta, Mexico', flight=flight2, customer=customer1)
    booking4 = Booking(price=643.45, destination="Nassau, Bahamas", flight=flight1, customer=customer1)

    db.session.add_all([booking1, booking2, booking3, booking4])
    db.session.commit()

    print("🌱 Flights, Customers, and Bookings successfully seeded! 🌱")