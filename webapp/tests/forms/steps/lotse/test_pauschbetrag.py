from app.forms.steps.lotse.pauschbetrag import calculate_pauschbetrag


class TestCalculatePauschbetrag:

    def test_if_no_merkzeichen_or_pflegegrad_set_then_return_correct_value_for_beh_grad(self):
        input_output_pairs = [
            (20, 384),
            (30, 620),
            (40, 860),
            (50, 1140),
            (60, 1440),
            (70, 1780),
            (80, 2120),
            (90, 2460),
            (100, 2840),
        ]

        params = {
            'pflegegrad': False,
            'merkzeichen_bl': False,
            'merkzeichen_tbl': False,
            'merkzeichen_h': False,
            'merkzeichen_ag': False,
            'merkzeichen_g': False,
        }

        for beh_grad, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_pauschbetrag(**params, beh_grad=beh_grad)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_ag_and_no_pflegegrad_set_then_return_correct_value_for_beh_grad(self):
        input_output_pairs = [
            (20, 384),
            (30, 620),
            (40, 860),
            (50, 1140),
            (60, 1440),
            (70, 1780),
            (80, 2120),
            (90, 2460),
            (100, 2840),
        ]

        params = {
            'pflegegrad': False,
            'merkzeichen_bl': False,
            'merkzeichen_tbl': False,
            'merkzeichen_h': False,
            'merkzeichen_ag': True,
            'merkzeichen_g': False,
        }

        for beh_grad, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_pauschbetrag(**params, beh_grad=beh_grad)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_g_and_no_pflegegrad_set_then_return_correct_value_for_beh_grad(self):
        input_output_pairs = [
            (20, 384),
            (30, 620),
            (40, 860),
            (50, 1140),
            (60, 1440),
            (70, 1780),
            (80, 2120),
            (90, 2460),
            (100, 2840),
        ]

        params = {
            'pflegegrad': False,
            'merkzeichen_bl': False,
            'merkzeichen_tbl': False,
            'merkzeichen_h': False,
            'merkzeichen_ag': False,
            'merkzeichen_g': True,
        }

        for beh_grad, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_pauschbetrag(**params, beh_grad=beh_grad)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegegrad_set_and_no_merkzeichen_then_return_7400_for_all_beh_grad(self):
        beh_grad_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'pflegegrad': True,
            'merkzeichen_bl': False,
            'merkzeichen_tbl': False,
            'merkzeichen_h': False,
            'merkzeichen_ag': False,
            'merkzeichen_g': False,
        }

        for beh_grad in beh_grad_values:

            calculated_pauschbetrag = calculate_pauschbetrag(**params, beh_grad=beh_grad)

            assert calculated_pauschbetrag == 7400

    def test_if_pflegegrad_set_and_merkzeichen_bl_then_return_7400_for_all_beh_grad(self):
        beh_grad_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'pflegegrad': True,
            'merkzeichen_bl': True,
            'merkzeichen_tbl': False,
            'merkzeichen_h': False,
            'merkzeichen_ag': False,
            'merkzeichen_g': False,
        }

        for beh_grad in beh_grad_values:

            calculated_pauschbetrag = calculate_pauschbetrag(**params, beh_grad=beh_grad)

            assert calculated_pauschbetrag == 7400

    def test_if_pflegegrad_set_and_merkzeichen_tbl_then_return_7400_for_all_beh_grad(self):
        beh_grad_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'pflegegrad': True,
            'merkzeichen_bl': False,
            'merkzeichen_tbl': True,
            'merkzeichen_h': False,
            'merkzeichen_ag': False,
            'merkzeichen_g': False,
        }

        for beh_grad in beh_grad_values:

            calculated_pauschbetrag = calculate_pauschbetrag(**params, beh_grad=beh_grad)

            assert calculated_pauschbetrag == 7400

    def test_if_pflegegrad_set_and_merkzeichen_h_then_return_7400_for_all_beh_grad(self):
        beh_grad_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'pflegegrad': True,
            'merkzeichen_bl': False,
            'merkzeichen_tbl': False,
            'merkzeichen_h': True,
            'merkzeichen_ag': False,
            'merkzeichen_g': False,
        }

        for beh_grad in beh_grad_values:

            calculated_pauschbetrag = calculate_pauschbetrag(**params, beh_grad=beh_grad)

            assert calculated_pauschbetrag == 7400

    def test_if_merkzeichen_bl_and_no_pflegegrad_set_then_return_7400_for_all_beh_grad(self):
        beh_grad_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'pflegegrad': False,
            'merkzeichen_bl': True,
            'merkzeichen_tbl': False,
            'merkzeichen_h': False,
            'merkzeichen_ag': False,
            'merkzeichen_g': False,
        }

        for beh_grad in beh_grad_values:

            calculated_pauschbetrag = calculate_pauschbetrag(**params, beh_grad=beh_grad)

            assert calculated_pauschbetrag == 7400

    def test_if_merkzeichen_tbl_and_no_pflegegrad_set_then_return_7400_for_all_beh_grad(self):
        beh_grad_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'pflegegrad': False,
            'merkzeichen_bl': False,
            'merkzeichen_tbl': True,
            'merkzeichen_h': False,
            'merkzeichen_ag': False,
            'merkzeichen_g': False,
        }

        for beh_grad in beh_grad_values:

            calculated_pauschbetrag = calculate_pauschbetrag(**params, beh_grad=beh_grad)

            assert calculated_pauschbetrag == 7400

    def test_if_merkzeichen_h_and_no_pflegegrad_set_then_return_7400_for_all_beh_grad(self):
        beh_grad_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'pflegegrad': False,
            'merkzeichen_bl': False,
            'merkzeichen_tbl': False,
            'merkzeichen_h': True,
            'merkzeichen_ag': False,
            'merkzeichen_g': False,
        }

        for beh_grad in beh_grad_values:

            calculated_pauschbetrag = calculate_pauschbetrag(**params, beh_grad=beh_grad)

            assert calculated_pauschbetrag == 7400
