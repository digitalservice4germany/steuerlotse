def calculate_pauschbetrag(pflegegrad=False, beh_grad=None, merkzeichen_bl=False, merkzeichen_tbl=False, merkzeichen_h=False,
                           merkzeichen_ag=False, merkzeichen_g=False):
    if pflegegrad:
        return 7400
    if merkzeichen_bl:
        return 7400
    if merkzeichen_tbl:
        return 7400
    if merkzeichen_h:
        return 7400

    beh_grad_to_pauschal_betrag_mapping = {
        20: 384,
        30: 620,
        40: 860,
        50: 1140,
        60: 1440,
        70: 1780,
        80: 2120,
        90: 2460,
        100: 2840,
    }

    return beh_grad_to_pauschal_betrag_mapping[beh_grad]