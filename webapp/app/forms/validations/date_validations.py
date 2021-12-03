import datetime

from wtforms import ValidationError
from flask_babel import _
from flask_babel import lazy_gettext as _l


class ValidDateOf:
    """Validates a date between 01.01.1900 and today
           
    Possible validation errors and message parameters:
    - message_missing: Date is missing (__.__.___)
    - message_incomplete: Date is invalid (99.99.2021)
    - message_incorrect: Date is incomplete (__.__.2021)
    - message_in_the_future: Date is in the future
    - message_to_far_in_past: Date is is before 01.01.1990
    
    """
    def __init__(self, message_missing, message_incomplete, message_incorrect, message_in_the_future, message_to_far_in_past) -> None:
        self.message_missing = message_missing
        self.message_incomplete = message_incomplete
        self.message_incorrect = message_incorrect
        self.message_in_the_future = message_in_the_future
        self.message_to_far_in_past = message_to_far_in_past

    def __call__(self, form, field):
        raw_input_date = field._value()
        elster_min_date = datetime.date(1900, 1, 1)
                
        day, month, year = None, None, None

        if isinstance(raw_input_date, list):
            if len(raw_input_date) != 3:
                raise ValidationError(self.message_incomplete)

            day, month, year = raw_input_date
        else:
            raise ValidationError(self.message_incorrect)

        if not day or not month or not year: 
            raise ValidationError(self.message_incomplete)
        
        if len(year) < 4:            
            raise ValidationError(self.message_incomplete)
            
        try:
            input_date = datetime.date(int(year), int(month), int(day))
        except ValueError:
            raise ValidationError(self.message_incorrect)

        if input_date > datetime.date.today():
            raise ValidationError(self.message_in_the_future)

        if input_date < elster_min_date:
            raise ValidationError(self.message_to_far_in_past)


class ValidDateOfBirth(ValidDateOf):
    def __init__(self) -> None:
        super().__init__(
            message_missing = _l('validate.date-of-birth-missing'),
            message_incomplete = _l('validate.date-of-birth-incomplete'), 
            message_incorrect = _l('validate.date-of-incorrect'), 
            message_in_the_future = _l('validate.date-of-in-the-future'), 
            message_to_far_in_past = _l('validate.date-of-to-far-in-past'))
        
class ValidDateOfDeath(ValidDateOf):
    def __init__(self) -> None:
        super().__init__(
            message_missing = _l('validate.date-of-death-missing'),
            message_incomplete = _l('validate.date-of-death-incomplete'), 
            message_incorrect = _l('validate.date-of-incorrect'), 
            message_in_the_future = _l('validate.date-of-in-the-future'), 
            message_to_far_in_past = _l('validate.date-of-to-far-in-past'))
        
class ValidDateOfMarriage(ValidDateOf):
    def __init__(self) -> None:
        super().__init__(
            message_missing = _l('validate.date-of-marriage-missing'),
            message_incomplete = _l('validate.date-of-marriage-incomplete'), 
            message_incorrect = _l('validate.date-of-incorrect'), 
            message_in_the_future = _l('validate.date-of-in-the-future'), 
            message_to_far_in_past = _l('validate.date-of-to-far-in-past'))
        

class ValidDateOfDivorce(ValidDateOf):
    def __init__(self) -> None:
        super().__init__(
            message_missing = _l('validate.date-of-divorce-missing'),
            message_incomplete = _l('validate.date-of-incomplete'), 
            message_incorrect = _l('validate.date-of-incorrect'), 
            message_in_the_future = _l('validate.date-of-in-the-future'), 
            message_to_far_in_past = _l('validate.date-of-to-far-in-past'))
        
        
class ValidDateOfSeparatedSince(ValidDateOf):
    def __init__(self) -> None:
        super().__init__(
            message_missing = _l('validate.date-of-separated-missing'),
            message_incomplete = _l('validate.date-of-incomplete'), 
            message_incorrect = _l('validate.date-of-incorrect'), 
            message_in_the_future = _l('validate.date-of-in-the-future'), 
            message_to_far_in_past = _l('validate.date-of-too-far-in-past'))
