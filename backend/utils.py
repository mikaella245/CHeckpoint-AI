reference_rates = {
    2019: 1.5,
    2020: 1.25,
    2021: 1.25,
    2022: 1.25,
    2023: 1.75,
    2024: 2.0
    }

def get_reference_rate(year: int):
    return reference_rates.get(year, 1.25)

