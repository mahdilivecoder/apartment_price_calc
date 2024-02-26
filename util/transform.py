class transform:
    """
    Transform entered with regex to get suitable data for saving data into houses.csv file
    """
    def make_trans_price(price):
        if "میلیارد تومان" in price:
            price=price.replace("میلیارد تومان","")
            price=round(float(price)*1000000000,2)
            return price
        elif "میلیون تومان" in price:
            price=price.vreplace("میلیون تومان","")
            price=round(float(price)*1000000,2)
            return price
        
    def make_trans_parking(parking):
        parking=parking.replace("پارکینگ","")
        return int(parking)
    def make_trans_type(type):
        if "مسکونی" in type:
            return 0
        else:
            raise TypeError("The field type is wrong!")
        
    def make_trans_bedroom(bedroom):
        bedroom=bedroom.replace("خواب","")
        return int(bedroom)
    
    def make_trans_metraj(metr):
        metr=metr.replace("متر","")
        return int(metr)
    
    def make_trans_location(location):
        if "سعادت اباد" in location:
            return 2
        if "دریا" in location:
            return 3
        else:
            raise NameError("Name of location is not right")