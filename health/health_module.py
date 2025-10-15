def check_vitals(vitals:dict)->str:
    """
    check vitals of the system
    """
    hr=vitals.get("heart_rate",80)
    if hr>100:
        return "Aaram se saas lo balak"
    else:
        return "mast ho balak, chill rho"
