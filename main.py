import car_booking

app = car_booking.create_app()

if __name__ == "__main__":
    app.run(debug=True)
