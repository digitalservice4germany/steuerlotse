import unittest

from werkzeug.datastructures import MultiDict
from flask_babel import _
from app.forms.validations.date_validations import ValidDateOfBirth, ValidDateOfDeath, ValidDateOfDivorce, ValidDateOfMarriage
from app.forms.fields import SteuerlotseDateField
from app.forms import SteuerlotseBaseForm


class DateForm(SteuerlotseBaseForm):
    date_field = SteuerlotseDateField()
    
class TestValidDateOfBirth(unittest.TestCase):
    def setUp(self):
        self.form = DateForm()
        self.validator = ValidDateOfBirth()
        
    
    def test_date_of_birth_is_valid(self):
        """
        GIVEN a valid date 1.1.2020
        WHEN validation executed
        THEN no ValueErrors expected
        """
                
        # Arrange
        self.is_valid = False
        self.wrong_date_input = ['1', '1', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        self.validation_error = ''
        
        # Act      
        try:                      
            self.validator(self.form, self.form.date_field)
            self.is_valid = True
        except Exception as ex:
            self.validation_error = str(ex)
            
        # Assert
        self.assertTrue(self.is_valid, f'Error raised:{self.validation_error}') 
        
    
    def test_date_of_birth_to_far_in_past_throws_ValueError(self):
        """
        GIVEN a date before 1.1.1900
        WHEN validation executed
        THEN ValueError with message validate.date-of-to-far-in-past expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['1', '1', '1899']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-to-far-in-past'))
        
    
    def test_date_of_birth_in_the_future_throws_ValueError(self):
        """
        GIVEN a date in the future 9.9.9999
        WHEN validation executed
        THEN ValueError with message validate.date-of-in-the-future expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['1', '1', '9999']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-in-the-future'))
        
    
    def test_invalid_date_of_birth_throws_ValueError(self):
        """
        GIVEN a invalid date 99.99.2020
        WHEN validation executed
        THEN ValueError with message validate.validate.date-of-incorrect expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['99', '99', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-incorrect'))
        
    def test_incomplete_date_of_birth_throws_ValueError(self):
        """
        GIVEN a incomplete date __.__.2020
        WHEN validation executed
        THEN ValueError with message validate.validate.date-of-birth-incomplete expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['', '', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-birth-incomplete'))
    
class TestValidDateOfMarriage(unittest.TestCase):
    def setUp(self):
        self.form = DateForm()
        self.validator = ValidDateOfMarriage()
        
    
    def test_date_of_marriage_is_valid(self):
        """
        GIVEN a valid date 1.1.2020
        WHEN validation executed
        THEN no ValueErrors expected
        """
                
        # Arrange
        self.is_valid = False
        self.wrong_date_input = ['1', '1', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        self.validation_error = ''
        
        # Act      
        try:                      
            self.validator(self.form, self.form.date_field)
            self.is_valid = True
        except Exception as ex:
            self.validation_error = str(ex)
            
        # Assert
        self.assertTrue(self.is_valid, f'Error raised:{self.validation_error}') 
        
    
    def test_date_of_marriage_to_far_in_past_throws_ValueError(self):
        """
        GIVEN a date before 1.1.1900
        WHEN validation executed
        THEN ValueError with message validate.date-of-to-far-in-past expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['1', '1', '1899']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-to-far-in-past'))
        
    
    def test_date_of_marriage_in_the_future_throws_ValueError(self):
        """
        GIVEN a date in the future 9.9.9999
        WHEN validation executed
        THEN ValueError with message validate.date-of-in-the-future expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['1', '1', '9999']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-in-the-future'))
        
    
    def test_invalid_date_of_marriage_throws_ValueError(self):
        """
        GIVEN a invalid date 99.99.2020
        WHEN validation executed
        THEN ValueError with message validate.validate.date-of-incorrect expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['99', '99', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-incorrect'))
        
    def test_incomplete_date_of_marriage_throws_ValueError(self):
        """
        GIVEN a incomplete date __.__.2020
        WHEN validation executed
        THEN ValueError with message validate.validate.date-of-marriage-incomplete expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['', '', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-marriage-incomplete'))
    
class TestValidDateOfDivorce(unittest.TestCase):
    def setUp(self):
        self.form = DateForm()
        self.validator = ValidDateOfDivorce()
        
    
    def test_date_of_divorce_is_valid(self):
        """
        GIVEN a valid date 1.1.2020
        WHEN validation executed
        THEN no ValueErrors expected
        """
                
        # Arrange
        self.is_valid = False
        self.wrong_date_input = ['1', '1', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        self.validation_error = ''
        
        # Act      
        try:                      
            self.validator(self.form, self.form.date_field)
            self.is_valid = True
        except Exception as ex:
            self.validation_error = str(ex)
            
        # Assert
        self.assertTrue(self.is_valid, f'Error raised:{self.validation_error}') 
        
    
    def test_date_of_divorce_to_far_in_past_throws_ValueError(self):
        """
        GIVEN a date before 1.1.1900
        WHEN validation executed
        THEN ValueError with message validate.date-of-to-far-in-past expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['1', '1', '1899']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-to-far-in-past'))
        
    
    def test_date_of_divorce_in_the_future_throws_ValueError(self):
        """
        GIVEN a date in the future 9.9.9999
        WHEN validation executed
        THEN ValueError with message validate.date-of-in-the-future expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['1', '1', '9999']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-in-the-future'))
        
    
    def test_invalid_date_of_divorce_throws_ValueError(self):
        """
        GIVEN a invalid date 99.99.2020
        WHEN validation executed
        THEN ValueError with message validate.validate.date-of-incorrect expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['99', '99', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-incorrect'))
        
    def test_incomplete_date_of_divorce_throws_ValueError(self):
        """
        GIVEN a incomplete date __.__.2020
        WHEN validation executed
        THEN ValueError with message validate.validate.date-of-incomplete expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['', '', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-incomplete'))
    
class TestValidDateOfDeath(unittest.TestCase):    
    def setUp(self):
        self.form = DateForm()
        self.validator = ValidDateOfDeath()
        
    
    def test_date_of_death_is_valid(self):
        """
        GIVEN a valid date 1.1.2020
        WHEN validation executed
        THEN no ValueErrors expected
        """
                
        # Arrange
        self.is_valid = False
        self.wrong_date_input = ['1', '1', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        self.validation_error = ''
        
        # Act      
        try:                      
            self.validator(self.form, self.form.date_field)
            self.is_valid = True
        except Exception as ex:
            self.validation_error = str(ex)
            
        # Assert
        self.assertTrue(self.is_valid, f'Error raised:{self.validation_error}') 
        
    
    def test_date_of_death_to_far_in_past_throws_ValueError(self):
        """
        GIVEN a date before 1.1.1900
        WHEN validation executed
        THEN ValueError with message validate.date-of-to-far-in-past expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['1', '1', '1899']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-to-far-in-past'))
        
    
    def test_date_of_death_in_the_future_throws_ValueError(self):
        """
        GIVEN a date in the future 9.9.9999
        WHEN validation executed
        THEN ValueError with message validate.date-of-in-the-future expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['1', '1', '9999']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-in-the-future'))
        
    
    def test_invalid_date_of_death_throws_ValueError(self):
        """
        GIVEN a invalid date 99.99.2020
        WHEN validation executed
        THEN ValueError with message validate.validate.date-of-incorrect expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['99', '99', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-incorrect'))
        
    def test_incomplete_date_of_death_throws_ValueError(self):
        """
        GIVEN a incomplete date __.__.2020
        WHEN validation executed
        THEN ValueError with message validate.validate.date-of-death-incomplete expected
        """
                
        # Arrange
        self.is_valid = True
        self.wrong_date_input = ['', '', '2020']
        self.form.process(formdata=MultiDict({'date_field': self.wrong_date_input}))
        
        # Act
        try:                      
            self.validator(self.form, self.form.date_field)
        except ValueError as ex:
            self.is_valid = False
            self.validation_error = str(ex)
            
        # Assert        
        self.assertFalse(self.is_valid, 'ValueError expected')
        self.assertEqual(self.validation_error, _('validate.date-of-death-incomplete'))