from main_app.models import Car

def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        discount = 1 - (sum(int(e) for e in str(car.year))/100)
        discounted_price = car.price * discount
        car.price_with_discount = discounted_price
        car.save()



