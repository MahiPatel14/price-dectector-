def make_decision(current_price, predicted_price):
    if predicted_price > current_price:
        return " Wait (Price may increase)"
    else:
        return " Buy Now (Price is low)"