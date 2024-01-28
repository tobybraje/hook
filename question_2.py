def get_largest_possible_loss(pricesLst: list[float]) -> dict:
    try:
        biggest_loss = 0
        index_1 = None
        index_2 = None

        pricesLstSorted = sorted(pricesLst)

        pricesAndIndexes = [
            (price, pricesLst.index(price)) for price in pricesLstSorted
        ]

        for sell_price_tuple in pricesAndIndexes:
            sell_price = sell_price_tuple[0]
            index_2 = sell_price_tuple[1]

            for buy_price_tuple in reversed(pricesAndIndexes):
                if buy_price_tuple[1] < index_2:
                    biggest_loss = buy_price_tuple[0] - sell_price
                    index_1 = buy_price_tuple[1]
                    break
            else:
                continue
            break

        if biggest_loss < 0:
            biggest_loss = 0
            index_1 = None
            index_2 = None

        return_dict = {
            "Biggest Loss": round(biggest_loss, 2),
            "Index 1": index_1,
            "Index 2": index_2,
        }

        return return_dict
    except TypeError:
        return {"Error": "The supplied prices are of the wrong type"}
