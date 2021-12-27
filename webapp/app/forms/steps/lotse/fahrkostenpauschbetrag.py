def calculate_fahrkostenpauschbetrag(has_pflegegrad=False, disability_degree=None, has_merkzeichen_bl=False, has_merkzeichen_tbl=False,
                                     has_merkzeichen_h=False, has_merkzeichen_ag=False, has_merkzeichen_g=False):
    if has_pflegegrad or has_merkzeichen_bl or has_merkzeichen_tbl or has_merkzeichen_tbl or has_merkzeichen_h or has_merkzeichen_ag:
        return 4500
    elif disability_degree >= 80 or (has_merkzeichen_g and disability_degree >= 70):
        return 900

    else:
        return None
