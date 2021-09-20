from xml.etree.ElementTree import ParseError

from erica.elster_xml.xml_parsing.erica_xml_parsing import get_elements_text_from_xml, remove_declaration_and_namespace

_ERIC_SUCCESS_CODE = {
    0: "ERIC_OK"
}

_ERIC_CUSTOM_ERROR_CODES = {
    1: "NULL_POINTER_RETURNED",
    2: "NO_MATCHING_IDENTIFIER_FOR_UNLOCK_REQUEST",
    3: "ALREADY_OPEN_UNLOCK_CODE_REQUEST",
    5: "ELSTER_REQUEST_ID_UNKNOWN",
    6: "INVALID_BUFA_NUMBER",
    7: "INVALID_TAX_NUMBER",
}

_ERIC_GLOBAL_VALIDATION_ERRORS = {
    610001002: "ERIC_GLOBAL_PRUEF_FEHLER"
}

_FSC_ALREADY_REQUESTED_ERRORS = {
    610101292: "ERIC_TRANSFER_ERR_XML_NHEADER"  # has no special error message
}

_NO_ANTRAG_FOUND_ERRORS = {
    610101292: "ERIC_TRANSFER_ERR_XML_NHEADER"  # has no special error message
}

_ERIC_GLOBAL_INITIALISATION_ERRORS = {
    610001081: "ERIC_GLOBAL_NICHT_INITIALISIERT",
    610001082: "ERIC_GLOBAL_MEHRFACHE_INITIALISIERUNG",
    610001083: "ERIC_GLOBAL_FEHLER_INITIALISIERUNG"
}

_ERIC_GLOBAL_TAX_NUMBER_INVALID_ERRORS = {
    610001034: "ERIC_GLOBAL_STEUERNUMMER_UNGUELTIG",
}

_ERIC_GLOBAL_ERRORS = {
    610001001: "ERIC_GLOBAL_UNKNOWN",
    610001003: "ERIC_GLOBAL_HINWEISE",
    610001007: "ERIC_GLOBAL_FEHLERMELDUNG_NICHT_VORHANDEN",
    610001008: "ERIC_GLOBAL_KEINE_DATEN_VORHANDEN",
    610001013: "ERIC_GLOBAL_NICHT_GENUEGEND_ARBEITSSPEICHER",
    610001014: "ERIC_GLOBAL_DATEI_NICHT_GEFUNDEN",
    610001016: "ERIC_GLOBAL_HERSTELLER_ID_NICHT_ERLAUBT",
    610001017: "ERIC_GLOBAL_ILLEGAL_STATE",
    610001018: "ERIC_GLOBAL_FUNKTION_NICHT_ERLAUBT",
    610001019: "ERIC_GLOBAL_ECHTFALL_NICHT_ERLAUBT",
    610001020: "ERIC_GLOBAL_NO_VERSAND_IN_BETA_VERSION",
    610001025: "ERIC_GLOBAL_TESTMERKER_UNGUELTIG",
    610001026: "ERIC_GLOBAL_DATENSATZ_ZU_GROSS",
    610001027: "ERIC_GLOBAL_VERSCHLUESSELUNGS_PARAMETER_NICHT_ERLAUBT",
    610001028: "ERIC_GLOBAL_NUR_PORTALZERTIFIKAT_ERLAUBT",
    610001029: "ERIC_GLOBAL_ABRUFCODE_NICHT_ERLAUBT",
    610001030: "ERIC_GLOBAL_ERROR_XML_CREATE",
    610001031: "ERIC_GLOBAL_TEXTPUFFERGROESSE_FIX",
    610001032: "ERIC_GLOBAL_INTERNER_FEHLER",
    610001033: "ERIC_GLOBAL_ARITHMETIKFEHLER",
    610001035: "ERIC_GLOBAL_STEUERNUMMER_FALSCHE_LAENGE",
    610001036: "ERIC_GLOBAL_STEUERNUMMER_NICHT_NUMERISCH",
    610001037: "ERIC_GLOBAL_LANDESNUMMER_UNBEKANNT",
    610001038: "ERIC_GLOBAL_BUFANR_UNBEKANNT",
    610001039: "ERIC_GLOBAL_LANDESNUMMER_BUFANR",
    610001040: "ERIC_GLOBAL_PUFFER_ZUGRIFFSKONFLIKT",
    610001041: "ERIC_GLOBAL_PUFFER_UEBERLAUF",
    610001042: "ERIC_GLOBAL_DATENARTVERSION_UNBEKANNT",
    610001044: "ERIC_GLOBAL_DATENARTVERSION_XML_INKONSISTENT",
    610001045: "ERIC_GLOBAL_COMMONDATA_NICHT_VERFUEGBAR",
    610001046: "ERIC_GLOBAL_LOG_EXCEPTION",
    610001047: "ERIC_GLOBAL_TRANSPORTSCHLUESSEL_NICHT_ERLAUBT",
    610001048: "ERIC_GLOBAL_OEFFENTLICHER_SCHLUESSEL_UNGUELTIG",
    610001049: "ERIC_GLOBAL_TRANSPORTSCHLUESSEL_TYP_FALSCH",
    610001050: "ERIC_GLOBAL_PUFFER_UNGLEICHER_INSTANZ",
    610001051: "ERIC_GLOBAL_VORSATZ_UNGUELTIG",
    610001053: "ERIC_GLOBAL_DATEIZUGRIFF_VERWEIGERT",
    610001080: "ERIC_GLOBAL_UNGUELTIGE_INSTANZ",
    610001102: "ERIC_GLOBAL_UNKNOWN_PARAMETER_ERROR",
    610001108: "ERIC_GLOBAL_CHECK_CORRUPTED_NDS",
    610001206: "ERIC_GLOBAL_VERSCHLUESSELUNGS_PARAMETER_NICHT_ANGEGEBEN",
    610001209: "ERIC_GLOBAL_SEND_FLAG_MEHR_ALS_EINES",
    610001218: "ERIC_GLOBAL_UNGUELTIGE_FLAG_KOMBINATION",
    610001220: "ERIC_GLOBAL_ERSTE_SEITE_DRUCK_NICHT_UNTERSTUETZT",
    610001222: "ERIC_GLOBAL_UNGUELTIGER_PARAMETER",
    610001224: "ERIC_GLOBAL_DRUCK_FUER_VERFAHREN_NICHT_ERLAUBT",
    610001225: "ERIC_GLOBAL_VERSAND_ART_NICHT_UNTERSTUETZT",
    610001226: "ERIC_GLOBAL_UNGUELTIGE_PARAMETER_VERSION",
    610001227: "ERIC_GLOBAL_TRANSFERHANDLE",
    610001228: "ERIC_GLOBAL_PLUGININITIALISIERUNG",
    610001229: "ERIC_GLOBAL_INKOMPATIBLE_VERSIONEN",
    610001230: "ERIC_GLOBAL_VERSCHLUESSELUNGSVERFAHREN_NICHT_UNTERSTUETZT",
    610001231: "ERIC_GLOBAL_MEHRFACHAUFRUFE_NICHT_UNTERSTUETZT",
    610001404: "ERIC_GLOBAL_UTI_COUNTRY_NOT_SUPPORTED",
    610001501: "ERIC_GLOBAL_IBAN_FORMALER_FEHLER",
    610001502: "ERIC_GLOBAL_IBAN_LAENDERCODE_FEHLER",
    610001503: "ERIC_GLOBAL_IBAN_LANDESFORMAT_FEHLER",
    610001504: "ERIC_GLOBAL_IBAN_PRUEFZIFFER_FEHLER",
    610001510: "ERIC_GLOBAL_BIC_FORMALER_FEHLER",
    610001511: "ERIC_GLOBAL_BIC_LAENDERCODE_FEHLER",
    610001519: "ERIC_GLOBAL_ZULASSUNGSNUMMER_ZU_LANG",
    610001525: "ERIC_GLOBAL_IDNUMMER_UNGUELTIG",
    610001526: "ERIC_GLOBAL_NULL_PARAMETER",
    610001851: "ERIC_GLOBAL_UPDATE_NECESSARY",
    610001860: "ERIC_GLOBAL_EINSTELLUNG_NAME_UNGUELTIG",
    610001861: "ERIC_GLOBAL_EINSTELLUNG_WERT_UNGUELTIG",
    610001862: "ERIC_GLOBAL_ERR_DEKODIEREN",
    610001863: "ERIC_GLOBAL_FUNKTION_NICHT_UNTERSTUETZT",
    610001865: "ERIC_GLOBAL_NUTZDATENTICKETS_NICHT_EINDEUTIG",
    610001866: "ERIC_GLOBAL_NUTZDATENHEADERVERSIONEN_UNEINHEITLICH",
    610001867: "ERIC_GLOBAL_BUNDESLAENDER_UNEINHEITLICH",
    610001868: "ERIC_GLOBAL_ZEITRAEUME_UNEINHEITLICH",
    610001869: "ERIC_GLOBAL_NUTZDATENHEADER_EMPFAENGER_NICHT_KORREKT"
}

_ERIC_TRANSFER_ERRORS = {
    610101200: "ERIC_TRANSFER_COM_ERROR",
    610101201: "ERIC_TRANSFER_VORGANG_NICHT_UNTERSTUETZT",
    610101210: "ERIC_TRANSFER_ERR_XML_THEADER",
    610101251: "ERIC_TRANSFER_ERR_PARAM",
    610101253: "ERIC_TRANSFER_ERR_DATENTEILENDNOTFOUND",
    610101255: "ERIC_TRANSFER_ERR_BEGINDATENLIEFERANT",
    610101256: "ERIC_TRANSFER_ERR_ENDDATENLIEFERANT",
    610101257: "ERIC_TRANSFER_ERR_BEGINTRANSPORTSCHLUESSEL",
    610101258: "ERIC_TRANSFER_ERR_ENDTRANSPORTSCHLUESSEL",
    610101259: "ERIC_TRANSFER_ERR_BEGINDATENGROESSE",
    610101260: "ERIC_TRANSFER_ERR_ENDDATENGROESSE",
    610101271: "ERIC_TRANSFER_ERR_SEND",
    610101274: "ERIC_TRANSFER_ERR_NOTENCRYPTED",
    610101276: "ERIC_TRANSFER_ERR_PROXYCONNECT",
    610101278: "ERIC_TRANSFER_ERR_CONNECTSERVER",
    610101279: "ERIC_TRANSFER_ERR_NORESPONSE",
    610101280: "ERIC_TRANSFER_ERR_PROXYAUTH",
    610101282: "ERIC_TRANSFER_ERR_SEND_INIT",
    610101283: "ERIC_TRANSFER_ERR_TIMEOUT",
    610101284: "ERIC_TRANSFER_ERR_PROXYPORT_INVALID",
    610101291: "ERIC_TRANSFER_ERR_OTHER",
    610101292: "ERIC_TRANSFER_ERR_XML_NHEADER",
    610101293: "ERIC_TRANSFER_ERR_XML_ENCODING",
    610101294: "ERIC_TRANSFER_ERR_ENDSIGUSER",
    610101295: "ERIC_TRANSFER_ERR_XMLTAG_NICHT_GEFUNDEN",
    610101297: "ERIC_TRANSFER_ERR_DATENTEILFEHLER",
    610101500: "ERIC_TRANSFER_EID_ZERTIFIKATFEHLER",
    610101510: "ERIC_TRANSFER_EID_KEINKONTO",
    610101511: "ERIC_TRANSFER_EID_IDNRNICHTEINDEUTIG",
    610101512: "ERIC_TRANSFER_EID_SERVERFEHLER",
    610101520: "ERIC_TRANSFER_EID_KEINCLIENT",
    610101521: "ERIC_TRANSFER_EID_CLIENTFEHLER",
    610101522: "ERIC_TRANSFER_EID_FEHLENDEFELDER",
    610101523: "ERIC_TRANSFER_EID_IDENTIFIKATIONABGEBROCHEN",
    610101524: "ERIC_TRANSFER_EID_NPABLOCKIERT"
}

_ERIC_CRYPT_ERRORS = {
    610201016: "ERIC_CRYPT_ERROR_CREATE_KEY",
    610201101: "ERIC_CRYPT_E_INVALID_HANDLE",
    610201102: "ERIC_CRYPT_E_MAX_SESSION",
    610201103: "ERIC_CRYPT_E_BUSY",
    610201104: "ERIC_CRYPT_E_OUT_OF_MEM",
    610201105: "ERIC_CRYPT_E_PSE_PATH",
    610201106: "ERIC_CRYPT_E_PIN_WRONG",
    610201107: "ERIC_CRYPT_E_PIN_LOCKED",
    610201108: "ERIC_CRYPT_E_P7_READ",
    610201109: "ERIC_CRYPT_E_P7_DECODE",
    610201110: "ERIC_CRYPT_E_P7_RECIPIENT",
    610201111: "ERIC_CRYPT_E_P12_READ",
    610201112: "ERIC_CRYPT_E_P12_DECODE",
    610201113: "ERIC_CRYPT_E_P12_SIG_KEY",
    610201114: "ERIC_CRYPT_E_P12_ENC_KEY",
    610201115: "ERIC_CRYPT_E_P11_SIG_KEY",
    610201116: "ERIC_CRYPT_E_P11_ENC_KEY",
    610201117: "ERIC_CRYPT_E_XML_PARSE",
    610201118: "ERIC_CRYPT_E_XML_SIG_ADD",
    610201119: "ERIC_CRYPT_E_XML_SIG_TAG",
    610201120: "ERIC_CRYPT_E_XML_SIG_SIGN",
    610201121: "ERIC_CRYPT_E_ENCODE_UNKNOWN",
    610201122: "ERIC_CRYPT_E_ENCODE_ERROR",
    610201123: "ERIC_CRYPT_E_XML_INIT",
    610201124: "ERIC_CRYPT_E_ENCRYPT",
    610201125: "ERIC_CRYPT_E_DECRYPT",
    610201126: "ERIC_CRYPT_E_P11_SLOT_EMPTY",
    610201127: "ERIC_CRYPT_E_NO_SIG_ENC_KEY",
    610201128: "ERIC_CRYPT_E_LOAD_DLL",
    610201129: "ERIC_CRYPT_E_NO_SERVICE",
    610201130: "ERIC_CRYPT_E_ESICL_EXCEPTION",
    610201144: "ERIC_CRYPT_E_TOKEN_TYPE_MISMATCH",
    610201146: "ERIC_CRYPT_E_P12_CREATE",
    610201147: "ERIC_CRYPT_E_VERIFY_CERT_CHAIN",
    610201148: "ERIC_CRYPT_E_P11_ENGINE_LOADED",
    610201149: "ERIC_CRYPT_E_USER_CANCEL",
    610201200: "ERIC_CRYPT_ZERTIFIKAT",
    610201201: "ERIC_CRYPT_SIGNATUR",
    610201203: "ERIC_CRYPT_NICHT_UNTERSTUETZTES_PSE_FORMAT",
    610201205: "ERIC_CRYPT_PIN_BENOETIGT",
    610201206: "ERIC_CRYPT_PIN_STAERKE_NICHT_AUSREICHEND",
    610201208: "ERIC_CRYPT_E_INTERN",
    610201209: "ERIC_CRYPT_ZERTIFIKATSPFAD_KEIN_VERZEICHNIS",
    610201210: "ERIC_CRYPT_ZERTIFIKATSDATEI_EXISTIERT_BEREITS",
    610201211: "ERIC_CRYPT_PIN_ENTHAELT_UNGUELTIGE_ZEICHEN",
    610201212: "ERIC_CRYPT_E_INVALID_PARAM_ABC",
    610201213: "ERIC_CRYPT_CORRUPTED",
    610201214: "ERIC_CRYPT_EIDKARTE_NICHT_UNTERSTUETZT",
    610201215: "ERIC_CRYPT_E_SC_SLOT_EMPTY",
    610201216: "ERIC_CRYPT_E_SC_NO_APPLET",
    610201217: "ERIC_CRYPT_E_SC_SESSION",
    610201218: "ERIC_CRYPT_E_P11_NO_SIG_CERT",
    610201219: "ERIC_CRYPT_E_P11_INIT_FAILED",
    610201220: "ERIC_CRYPT_E_P11_NO_ENC_CERT",
    610201221: "ERIC_CRYPT_E_P12_NO_SIG_CERT",
    610201222: "ERIC_CRYPT_E_P12_NO_ENC_CERT",
    610201223: "ERIC_CRYPT_E_SC_ENC_KEY",
    610201224: "ERIC_CRYPT_E_SC_NO_SIG_CERT",
    610201225: "ERIC_CRYPT_E_SC_NO_ENC_CERT",
    610201226: "ERIC_CRYPT_E_SC_INIT_FAILED",
    610201227: "ERIC_CRYPT_E_SC_SIG_KEY"
}

_ERIC_IO_ERRORS = {
    610301001: "ERIC_IO_FEHLER",
    610301005: "ERIC_IO_DATEI_INKORREKT",
    610301006: "ERIC_IO_PARSE_FEHLER",
    610301007: "ERIC_IO_NDS_GENERIERUNG_FEHLGESCHLAGEN",
    610301010: "ERIC_IO_MASTERDATENSERVICE_NICHT_VERFUEGBAR",
    610301014: "ERIC_IO_STEUERZEICHEN_IM_NDS",
    610301031: "ERIC_IO_VERSIONSINFORMATIONEN_NICHT_GEFUNDEN",
    610301104: "ERIC_IO_FALSCHES_VERFAHREN",
    610301105: "ERIC_IO_READER_MEHRFACHE_STEUERFAELLE",
    610301106: "ERIC_IO_READER_UNERWARTETE_ELEMENTE",
    610301107: "ERIC_IO_READER_FORMALE_FEHLER",
    610301108: "ERIC_IO_READER_FALSCHES_ENCODING",
    610301109: "ERIC_IO_READER_MEHRFACHE_NUTZDATEN_ELEMENTE",
    610301110: "ERIC_IO_READER_MEHRFACHE_NUTZDATENBLOCK_ELEMENTE",
    610301111: "ERIC_IO_UNBEKANNTE_DATENART",
    610301114: "ERIC_IO_READER_UNTERSACHBEREICH_UNGUELTIG",
    610301115: "ERIC_IO_READER_ZU_VIELE_NUTZDATENBLOCK_ELEMENTE",
    610301150: "ERIC_IO_READER_STEUERZEICHEN_IM_TRANSFERHEADER",
    610301151: "ERIC_IO_READER_STEUERZEICHEN_IM_NUTZDATENHEADER",
    610301152: "ERIC_IO_READER_STEUERZEICHEN_IN_DEN_NUTZDATEN",
    610301200: "ERIC_IO_READER_SCHEMA_VALIDIERUNGSFEHLER",
    610301201: "ERIC_IO_READER_UNBEKANNTE_XML_ENTITY",
    610301252: "ERIC_IO_DATENTEILNOTFOUND",
    610301253: "ERIC_IO_DATENTEILENDNOTFOUND",
    610301300: "ERIC_IO_UEBERGABEPARAMETER_FEHLERHAFT",
    610301400: "ERIC_IO_UNGUELTIGE_UTF8_SEQUENZ",
    610301401: "ERIC_IO_UNGUELTIGE_ZEICHEN_IN_PARAMETER"
}

_ERIC_PRINT_ERRORS = {
    610501001: "ERIC_PRINT_INTERNER_FEHLER",
    610501002: "ERIC_PRINT_DRUCKVORLAGE_NICHT_GEFUNDEN",
    610501004: "ERIC_PRINT_UNGUELTIGER_DATEI_PFAD",
    610501007: "ERIC_PRINT_INITIALISIERUNG_FEHLERHAFT",
    610501008: "ERIC_PRINT_AUSGABEZIEL_UNBEKANNT",
    610501009: "ERIC_PRINT_ABBRUCH_DRUCKVORBEREITUNG",
    610501010: "ERIC_PRINT_ABBRUCH_GENERIERUNG",
    610501011: "ERIC_PRINT_STEUERFALL_NICHT_UNTERSTUETZT",
    610501012: "ERIC_PRINT_FUSSTEXT_ZU_LANG"
}

_ERIC_ERROR_MESSAGES = {**_ERIC_SUCCESS_CODE, **_ERIC_CUSTOM_ERROR_CODES, **_ERIC_GLOBAL_VALIDATION_ERRORS,
                        **_ERIC_GLOBAL_INITIALISATION_ERRORS, **_ERIC_GLOBAL_ERRORS, **_ERIC_TRANSFER_ERRORS,
                        **_ERIC_CRYPT_ERRORS, **_ERIC_IO_ERRORS, **_ERIC_PRINT_ERRORS}


class EricProcessNotSuccessful(Exception):
    """Exception raised in case of an unsuccessful process in the ERiC binaries
    """
    ERROR_CODE = -1

    def __init__(self, res_code=-1):
        self.res_code = res_code
        super().__init__()

    def __str__(self):
        return f"{self.res_code}: {self.get_eric_error_code_message(self.res_code)}"

    @staticmethod
    def get_eric_error_code_message(res_code):
        return _ERIC_ERROR_MESSAGES.get(res_code, "Unknown error message")

    def generate_error_response(self, include_responses=False):
        """
        Generates a dict which is the representation used to send errors outside of Erica.
        """
        error_response = {"code": self.ERROR_CODE,
                          "message": self.get_eric_error_code_message(self.res_code)
                          }
        return error_response


class EricGlobalError(EricProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries due to any of the global error codes.
    """
    ERROR_CODE = 1


class EricGlobalValidationError(EricGlobalError):
    """Exception raised in case of any global validation error detected by ERiC binaries
    """
    ERROR_CODE = 2

    # Overwrite initaliser to add special properties. Eric_response needs to be written to file at a higher level
    def __init__(self, res_code=-1, eric_response=None):
        self.eric_response = eric_response
        self.work_dir = None
        super().__init__(res_code)

    def __str__(self):
        if self.work_dir:
            return f"{self.res_code}: {self.get_eric_error_code_message(self.res_code)} in: {self.work_dir}"
        else:
            return f"{self.res_code}: {self.get_eric_error_code_message(self.res_code)}"

    def generate_error_response(self, include_responses=False):
        """
        Generates a dict which is the representation used to send errors outside of Erica.
        """
        error_response = super().generate_error_response(include_responses)

        if include_responses:
            error_response['eric_response'] = self.eric_response.decode()
        if self.eric_response:
            error_response['validation_problems'] = get_elements_text_from_xml(self.eric_response.decode(), 'Text')
        return error_response


class EricGlobalInitialisationError(EricGlobalError):
    """Exception raised in case of any error during initialisation
    """
    ERROR_CODE = 3


class EricTransferError(EricProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries due to an error with the transfer
    """
    ERROR_CODE = 4

    # Overwrite initaliser to add special properties
    def __init__(self, res_code=-1, eric_response=None, server_response=None, server_err_msg=None):
        self.eric_response = eric_response
        self.server_response = server_response
        self.work_dir = None
        self.server_err_msg = server_err_msg
        super().__init__(res_code)

    def __str__(self):
        if self.work_dir:
            return f"{self.res_code}: {self.get_eric_error_code_message(self.res_code)} in: {self.work_dir}; " \
                   f"server_err_msg: {self.server_err_msg} "
        else:
            return f"{self.res_code}: {self.get_eric_error_code_message(self.res_code)}; " \
                   f"server_err_msg: {self.server_err_msg} "

    def generate_error_response(self, include_responses=False):
        """
        Generates a dict which is the representation used to send errors outside of Erica.
        """
        error_response = super().generate_error_response(include_responses)
        error_response['server_err_msg'] = self.server_err_msg

        if include_responses:
            error_response['eric_response'] = self.eric_response.decode()
            error_response['server_response'] = self.server_response.decode()
        return error_response


class EricCryptError(EricProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries due to an error with the crypting
    """
    ERROR_CODE = 5


class EricIOError(EricProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries due to an error with IO processes
    """
    ERROR_CODE = 6


class EricPrintError(EricProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries due to an error with the print process
    """
    ERROR_CODE = 7


class EricNullReturnedError(EricGlobalError):
    """Exception raised in case None was returned by the ERiC binaries. This indicates that a null pointer was returned.
    """
    ERROR_CODE = 8


class EricAlreadyRequestedError(EricTransferError):
    """Exception raised in case the unlock code was already requested.
    """
    ERROR_CODE = 9

    # Overwrite initaliser to set custom res_code
    def __init__(self, eric_response=None, server_response=None, server_err_msg=None):
        # This error always has the res_code 3
        super().__init__(3, eric_response, server_response, server_err_msg)


class EricAntragNotFoundError(EricTransferError):
    """Exception raised in case an Antrag can not be found by Elster"""
    ERROR_CODE = 10

    def __init__(self, eric_response=None, server_response=None, antrag_id=-1, server_err_msg=None):
        # This error always has the res_code 5
        super().__init__(5, eric_response, server_response, server_err_msg)
        self.antrag_id = antrag_id

    def __str__(self):
        return 'The identifier of the request does not have a representation in the stored data.'


class EricAlreadyRevokedError(EricTransferError):
    """Exception raised in case the unlock code was already revoked.
    """
    ERROR_CODE = 11

    def __str__(self):
        return "The request for the request code has already been revoked"


class InvalidBufaNumberError(EricProcessNotSuccessful):
    """Exception raised in case the entered bufa is invalid"""
    ERROR_CODE = 12

    # Overwrite initaliser to set custom res_code
    def __init__(self, res_code=6):
        # This error always has the res_code 6
        super().__init__(res_code)

    def __str__(self):
        return 'The BuFa number is invalid'


class EricWrongTaxNumberError(EricGlobalValidationError):
    """Exception raised in case the entered tax number is invalid"""
    ERROR_CODE = 13

    # Overwrite initaliser to set custom res_code
    def __init__(self, res_code=7, eric_response=None):
        # This error always has the res_code 7
        super().__init__(res_code, eric_response)

    def __str__(self):
        return 'The tax number is invalid'


class EricInvalidXmlReturnedError(EricProcessNotSuccessful):
    """Exception raised in case an invalid xml is returned by the ERiC binaries.
    """
    pass


class EricUnknownError(EricProcessNotSuccessful):
    """Exception raised in case of an unsuccessful process in the ERiC binaries.
    The error code of the binary does not map to any of the other errors.
    """
    ERROR_CODE = 100


def check_result(rescode, eric_response=None, server_response=None, server_err_msg=None):
    """Checks if a result code indicates an error and raises the corresponding exception.
    If result code is ERIC_OK, no error is raised."""
    if rescode is None:
        raise EricNullReturnedError()
    elif rescode in _ERIC_GLOBAL_VALIDATION_ERRORS:
        raise _create_validation_error(rescode, eric_response)
    elif rescode in _ERIC_GLOBAL_INITIALISATION_ERRORS:
        raise EricGlobalInitialisationError(rescode)
    elif rescode in _ERIC_GLOBAL_TAX_NUMBER_INVALID_ERRORS:
        raise EricWrongTaxNumberError(rescode)
    elif rescode in _ERIC_GLOBAL_ERRORS:
        raise EricGlobalError(rescode)
    elif rescode in _ERIC_TRANSFER_ERRORS:
        raise _create_transfer_error(rescode, eric_response, server_response, server_err_msg)
    elif rescode in _ERIC_CRYPT_ERRORS:
        raise EricCryptError(rescode)
    elif rescode in _ERIC_IO_ERRORS:
        raise EricIOError(rescode)
    elif rescode in _ERIC_PRINT_ERRORS:
        raise EricPrintError(rescode)
    elif rescode in _ERIC_SUCCESS_CODE:
        return
    else:
        raise EricUnknownError


def _create_validation_error(rescode, eric_response):
    if eric_response and 'ungültige Steuernummer' in eric_response.decode():
        raise EricWrongTaxNumberError(eric_response=eric_response)
    else:
        raise EricGlobalValidationError(rescode, eric_response)


def _create_transfer_error(rescode, eric_response, server_response, server_err_msg=None):
    if rescode == 610101292 and server_err_msg and is_error_in_server_err_msg(server_err_msg.get('NDH_ERR_XML'), '371015213'):
        raise EricAlreadyRevokedError(rescode, eric_response, server_response, server_err_msg)
    elif server_response and rescode in _FSC_ALREADY_REQUESTED_ERRORS and \
            ("Es besteht bereits ein offener Antrag auf Erteilung einer Berechtigung zum Datenabruf"
             in server_response.decode() or
             "Es besteht bereits eine Berechtigung mit der gleichen Gültigkeitsdauer"
             in server_response.decode()):
        raise EricAlreadyRequestedError(eric_response, server_response, server_err_msg)
    elif server_response and rescode in _NO_ANTRAG_FOUND_ERRORS and \
            "Es ist kein Antrag auf Erteilung einer Berechtigung zum Datenabruf bzw. keine Berechtigung zum Widerruf " \
            "vorhanden." in server_response.decode():
        raise EricAntragNotFoundError(eric_response, server_response, server_err_msg)
    elif rescode in _ERIC_TRANSFER_ERRORS:
        raise EricTransferError(rescode, eric_response, server_response, server_err_msg)


def check_handle(handle):
    """Checks if a handle is a Null pointer and raises the coresponding exception."""
    if handle is None:
        raise EricNullReturnedError()


def is_error_in_server_err_msg(error_xml_str, error):
    """Checks if a specific error occurs in the <Fehler> tag of the error xml"""
    return any([elem.text == error for elem in remove_declaration_and_namespace(error_xml_str).findall('.//Fehler/Code')])


def check_xml(xml):
    """Checks if xml is a valid xml"""
    if xml != '' and xml != b'':
        import xml.etree.ElementTree as ET
        try:
            ET.fromstring(xml)
        except ParseError:
            raise EricInvalidXmlReturnedError()
        except TypeError:
            raise EricInvalidXmlReturnedError()
