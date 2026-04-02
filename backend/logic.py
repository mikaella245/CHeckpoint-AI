from utils import get_reference_rate
from models import RentInput

def calculate_faireness(data: RentInput):

    contract_rate = get_reference_rate(data.contract_year)
    current_rate = get_reference_rate(data.increase_year)

    # Allowed initial rent 
    #allowed_initial_rent = 

    # Taux de référence
    rate_diff = current_rate - contract_rate
    hypo_adjust = rate_diff * 0.025 #Check if it's actual legal coeff

    allowed_rent = data.original_rent * (1 + hypo_adjust)

    # Renovation adjustment

    if data.renovations == True:
        allowed_rent *= 1.10
    
    # Compare current rent with maximum allowed rent:
    diff = abs(data.current_rent - allowed_rent)

    if diff == 0:
        flag = "The rent is fair."
    elif 0 < diff <= 150:
        flag = "There is very low probability of your rent being abusive."
    elif 150 < diff <= 300:
        flag = "There is low probability of your rent being abusive."
    elif 300 < diff <= 600:
        flag = "The probability of your rent being abusive is considerable."
    else:
        flag = "The probability of your rent being abusive is high." 

    return {
        "allowed_rent_estimate": round(allowed_rent, 2),
        "difference": round(diff, 2),
        "assessment": flag
    }
