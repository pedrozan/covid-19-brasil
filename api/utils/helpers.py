def to_br_date(date):
    return f"{date[6:]}/{date[4:6]}/{date[:4]}"


def calculate_acumulated_values(acc, res):
    acc = {
        "total_new_cases": acc["total_new_cases"] + int(res["new_cases"]),
        "total_acumulated_cases": acc["total_acumulated_cases"]
        + int(res["acumulated_cases"]),
        "total_new_deaths": acc["total_new_deaths"] + int(res["new_deaths"]),
        "total_acumulated_deaths": acc["total_acumulated_deaths"]
        + int(res["acumulated_deaths"]),
    }
    return acc
