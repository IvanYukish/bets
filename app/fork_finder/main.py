sample_data = {
    "coefficients": {
        "1": 1.19,
        "X2": 6.60
    }
}


def find_fork(data: dict) -> dict:
    profit = .0
    for val in data["coefficients"]:
        profit += 1 / data["coefficients"][val]

    if profit >= 1:
        raise Exception
    data["result"] = {
        "profit": 100 - (profit * 100)
    }
    for val in data["coefficients"]:
        data["result"][val] = (1 / data["coefficients"][val] / profit) * 100

    return data


def calculate_fork_amount(amount: float, profit: float, *coefficients) -> dict:
    res = {}
    for coeff in coefficients:
        res[coeff] = (1 / coeff / profit) * amount

    return res
