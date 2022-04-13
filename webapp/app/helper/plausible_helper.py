from flask_babel import lazy_gettext as _l


def get_plausible_data(step_name, config):
    plausible_data = {
        'plausible_domain': config,
        'plausible_target': _l('plausible.target.goal'),
        'plausible_source': ''
    }

    if step_name == 'familienstand':
        plausible_data['plausible_source'] = _l('plausible.source.step.familienstand')
        return plausible_data

    if step_name == 'iban':
        plausible_data['plausible_source'] = _l('plausible.source.step.iban')
        return plausible_data

    if step_name == 'person_a':
        plausible_data['plausible_source'] = _l('plausible.source.step.person_a')
        return plausible_data

    if step_name == 'person_b':
        plausible_data['plausible_source'] = _l('plausible.source.step.person_b')
        return plausible_data

    if step_name == 'vorsorge':
        plausible_data['plausible_source'] = _l('plausible.source.step.vorsorge')
        return plausible_data

    if step_name == 'ausserg_bela':
        plausible_data['plausible_source'] = _l('plausible.source.step.ausserg_bela')
        return plausible_data

    if step_name == 'haushaltsnahe_handwerker':
        plausible_data['plausible_source'] = _l('plausible.source.step.haushaltsnahe_handwerker')
        return plausible_data

    if step_name == 'gem_haushalt':
        plausible_data['plausible_source'] = _l('plausible.source.step.gem_haushalt')
        return plausible_data

    if step_name == 'religion':
        plausible_data['plausible_source'] = _l('plausible.source.step.religion')
        return plausible_data

    if step_name == 'spenden':
        plausible_data['plausible_source'] = _l('plausible.source.step.spenden')
        return plausible_data
