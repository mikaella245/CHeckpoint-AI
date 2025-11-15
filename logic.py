from utils import get_reference_rate
from models import RentInput

def calculate_faireness(data):

    contract_rate = get_reference_rate(data.contract_year)
    current_rate = get_reference_rate(data.increase_year)

    # Taux de référence
    rate_diff = current_rate - contract_rate
    hypo_adjust = rate_diff * 0.025 #Check if it's actual legal coeff

    allowed_rent = RentInput.original_rent * (1 + hypo_adjust)

    # Inflation adjustment
    inflation_adjust = RentInput.inflation_rate * 0.40 #Check if it's actual percentage of inflation that can be passed to tenants
    allowed_rent *= (1 + inflation_adjust)

    # Renovation adjustment

    if RentInput.renovations == True:
        allowed_rent *= 1.10
    
    # Compare current rent with maximum allowed rent:
    diff = abs(RentInput.current_rent - allowed_rent)

    if diff == 0:
        flag = "The rent is fair."
    elif 0 < diff <= 150:
        flag = "There is very low probability of the rent being abusive."
    elif 150 < diff <= 300:
        flag = "There is low probability of the rent being abusive."
    elif 300 < diff <= 600:
        flag = "There is considerable probability of the rent being abusive."
    else:
        flag = "There is high probability of the rent being abusive."

    return {
        "allowed_rent_estimate": round(allowed_rent, 2),
        "difference": round(diff, 2),
        "analysis": flag
    }
