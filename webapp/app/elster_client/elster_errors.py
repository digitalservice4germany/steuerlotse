from flask_babel import lazy_gettext as _l


class ElsterProcessNotSuccessful(Exception):
    """Exception raised in case of an unsuccessful process in the ERiC binaries
    """

    def __init__(self, message=None):
        self.message = message
        super().__init__()

    def __str__(self):
        return self.message


class ElsterGlobalError(ElsterProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries due to any of the global error codes.
    """
    pass


class ElsterGlobalValidationError(ElsterGlobalError):
    """Exception raised in case of any global validation error detected by ERiC binaries
    """

    # Overwrite initaliser to add special properties. Elster_response needs to be written to file at a higher level
    def __init__(self, message=None, eric_response=None, validation_problems=None):
        self.eric_response = eric_response
        self.validation_problems = validation_problems
        super().__init__(message)


class ElsterGlobalInitialisationError(ElsterGlobalError):
    """Exception raised in case of any error during initialisation
    """
    pass


class ElsterTransferError(ElsterProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries due to an error with the transfer
    """
    def __init__(self, message=None, eric_response=None, server_response=None):
        self.eric_response = eric_response
        self.server_response = server_response
        if message is None:
            message = ''
        super().__init__(message)


class ElsterCryptError(ElsterProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries due to an error with the crypting
    """
    pass


class ElsterIOError(ElsterProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries due to an error with IO processes
    """
    pass


class ElsterPrintError(ElsterProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries due to an error with the print process
    """
    pass


class ElsterNullReturnedError(ElsterGlobalError):
    """Exception raised in case None was returned by the ERiC binaries. This indicates that a null pointer was returned.
    """
    pass


class ElsterAlreadyRequestedError(ElsterTransferError):
    """Exception raised in case an unlock_code for one idnr is requested multiple times.
    """
    pass


class ElsterRequestIdUnkownError(ElsterTransferError):
    """Exception raised in case for an IdNr no unlock code request can be found and therefore the unlock_code
    activation was unsuccessful.
    """
    pass


class ElsterRequestAlreadyRevoked(ElsterTransferError):
    """Exception raised in case for an request with a specific request_code already has been revoked.
    """
    pass


class ElsterInvalidBufaNumberError(ElsterProcessNotSuccessful):
    """Exception raised in case Erica found the combination of tax office and tax number (the BuFa number)
    to be invalid
    """

    def __init__(self):
        self.message = _l('form.lotse.input_invalid.InvalidBufaNumber')


class ElsterInvalidTaxNumberError(ElsterGlobalValidationError):
    """Exception raised in case Erica found the tax number to be invalid"""

    def __init__(self, message=None, eric_response=None):
        super().__init__(message, eric_response, validation_problems=[_l('form.lotse.input_invalid.InvalidTaxNumber')])


class ElsterResponseUnexpectedStructure(ElsterProcessNotSuccessful):
    """Exception raised in case an IdNr no unlock code request can be found and therefore the unlock_code
    activation was unsuccessful.
    """
    pass


class ElsterUnknownError(ElsterProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries.
    The error code of the binary does not map to any of the other errors.
    """
    pass


class GeneralEricaError(Exception):
    """Exception raised when an error occurred in Erica that is not an
    expected ElsterProcessNotSuccessfulError"""
    def __init__(self, message=None):
        self.message = message
        super().__init__()

    def __str__(self):
        return str(self.message)


class EricaIsMissingFieldError(GeneralEricaError):
    """Exception raised when an error occurred in Erica because a required field was not set"""

    def __init__(self):
        self.message = _l('form.lotse.input_invalid.MissingFieldsInputValidationError')
