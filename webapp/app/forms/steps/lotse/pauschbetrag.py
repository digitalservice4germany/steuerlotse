def calculate_pauschbetrag(has_pflegegrad=False, disability_degree=None, has_merkzeichen_bl=False, has_merkzeichen_tbl=False, has_merkzeichen_h=False):
    """
    Calculates the pauschbetrag given some information about the user.

    :param has_pflegegrad: A boolean indicating whether the user has a "Pflegegrad" of 4 or 5
    :param disability_degree: An integer indicating the disability degree of the user. Must be between 20 and 100
    :param has_merkzeichen_bl: A boolean indicating whether the user has the Merkzeichen Bl
    :param has_merkzeichen_tbl: A boolean indicating whether the user has the Merkzeichen TBl
    :param has_merkzeichen_h: A boolean indicating whether the user has the Merkzeichen H
    """
    if has_pflegegrad or has_merkzeichen_bl or has_merkzeichen_tbl or has_merkzeichen_h:
        return 7400
    if disability_degree == 100:
        return 2840
    elif disability_degree >= 90:
        return 2460
    elif disability_degree >= 80:
        return 2120
    elif disability_degree >= 70:
        return 1780
    elif disability_degree >= 60:
        return 1440
    elif disability_degree >= 50:
        return 1140
    elif disability_degree >= 40:
        return 860
    elif disability_degree >= 30:
        return 620
    elif disability_degree >= 20:
        return 384
    