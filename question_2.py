def get_largest_possible_loss(pricesLst: list[float]) -> dict:
    current_loss = 0
    index_1 = None
    index_2 = None
    try:
        for price in pricesLst:
            for next_price in pricesLst[pricesLst.index(price) + 1 :]:
                loss = next_price - price
                if loss < current_loss:
                    current_loss = loss
                    index_1 = pricesLst.index(price)
                    index_2 = pricesLst.index(next_price)

        biggest_loss = round(-current_loss, 2)

        return {
            "Biggest Loss": biggest_loss,
            "Index 1": index_1,
            "Index 2": index_2,
        }
    except TypeError:
        return {"Error": "The supplied prices are of the wrong type"}
