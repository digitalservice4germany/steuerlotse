def calculate_fahrkostenpauschbetrag(has_pflegegrad: str = None, disability_degree: int = None,
                                     has_merkzeichen_bl: bool = False, has_merkzeichen_tbl: bool = False,
                                     has_merkzeichen_h: bool = False, has_merkzeichen_ag: bool = False,
                                     has_merkzeichen_g: bool = False):
    if has_pflegegrad == 'yes' or has_merkzeichen_bl or has_merkzeichen_tbl or has_merkzeichen_tbl \
            or has_merkzeichen_h or has_merkzeichen_ag:
        return 4500
    elif disability_degree and (disability_degree >= 80 or (has_merkzeichen_g and disability_degree >= 70)):
        return 900
    else:
        return 0
