success_card = {
    "order_type": "premium",
    "details": {
        "card_number": "4015042660210714",
        "secure_code": "56456",
        "card_name": "Mary Peterson",
        "card_cvv": "125",
        "card_actual": "12/33",
        "days": 10
    }
}

fail_card = [
    {
        "order_type": "premium",
        "details": {
            "card_number": "4015042660210714",
            "secure_code": "56456",
            "card_name": "Mary Peterson",
            "card_cvv": "300",  # cvv недостатка денег на карте
            "card_actual": "12/33",
            "days": 10
        }
    },
    {
        "order_type": "premium",
        "details": {
            "card_number": "4015042660210714",
            "secure_code": "56450",  # неверный код смс
            "card_name": "Mary Peterson",
            "card_cvv": "125",
            "card_actual": "12/33",
            "days": 10
        }
    },
    {
        "order_type": "premium",
        "details": {
            "card_number": "4015042660210714",
            "secure_code": "56456",
            "card_name": "Mary Peterson",
            "card_cvv": "155",  # неверный cvv
            "card_actual": "12/33",
            "days": 10
        }
    },
    {
        "order_type": "premium",
        "details": {
            "card_number": "4015042660210",  # неверный номер карты
            "secure_code": "56456",
            "card_name": "Mary Peterson",
            "card_cvv": "125",
            "card_actual": "12/33",
            "days": 10
        }
    }
]
