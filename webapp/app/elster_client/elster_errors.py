from flask_babel import lazy_gettext as _l
from requests import RequestException


ERIC_GLOBAL_INITIALISATION_ERRORS = ["ERIC_GLOBAL_NICHT_INITIALISIERT", "ERIC_GLOBAL_MEHRFACHE_INITIALISIERUNG",
                                     "ERIC_GLOBAL_FEHLER_INITIALISIERUNG"]

ERIC_GLOBAL_ERRORS = ["ERIC_GLOBAL_UNKNOWN", "ERIC_GLOBAL_HINWEISE", "ERIC_GLOBAL_FEHLERMELDUNG_NICHT_VORHANDEN",
                      "ERIC_GLOBAL_KEINE_DATEN_VORHANDEN", "ERIC_GLOBAL_NICHT_GENUEGEND_ARBEITSSPEICHER",
                      "ERIC_GLOBAL_DATEI_NICHT_GEFUNDEN",
                      "ERIC_GLOBAL_HERSTELLER_ID_NICHT_ERLAUBT", "ERIC_GLOBAL_ILLEGAL_STATE",
                      "ERIC_GLOBAL_FUNKTION_NICHT_ERLAUBT",
                      "ERIC_GLOBAL_ECHTFALL_NICHT_ERLAUBT", "ERIC_GLOBAL_NO_VERSAND_IN_BETA_VERSION",
                      "ERIC_GLOBAL_TESTMERKER_UNGUELTIG",
                      "ERIC_GLOBAL_DATENSATZ_ZU_GROSS", "ERIC_GLOBAL_VERSCHLUESSELUNGS_PARAMETER_NICHT_ERLAUBT",
                      "ERIC_GLOBAL_NUR_PORTALZERTIFIKAT_ERLAUBT", "ERIC_GLOBAL_ABRUFCODE_NICHT_ERLAUBT",
                      "ERIC_GLOBAL_ERROR_XML_CREATE",
                      "ERIC_GLOBAL_TEXTPUFFERGROESSE_FIX", "ERIC_GLOBAL_INTERNER_FEHLER",
                      "ERIC_GLOBAL_ARITHMETIKFEHLER",
                      "ERIC_GLOBAL_STEUERNUMMER_FALSCHE_LAENGE", "ERIC_GLOBAL_STEUERNUMMER_NICHT_NUMERISCH",
                      "ERIC_GLOBAL_LANDESNUMMER_UNBEKANNT", "ERIC_GLOBAL_BUFANR_UNBEKANNT",
                      "ERIC_GLOBAL_LANDESNUMMER_BUFANR",
                      "ERIC_GLOBAL_PUFFER_ZUGRIFFSKONFLIKT", "ERIC_GLOBAL_PUFFER_UEBERLAUF",
                      "ERIC_GLOBAL_DATENARTVERSION_UNBEKANNT",
                      "ERIC_GLOBAL_DATENARTVERSION_XML_INKONSISTENT", "ERIC_GLOBAL_COMMONDATA_NICHT_VERFUEGBAR",
                      "ERIC_GLOBAL_LOG_EXCEPTION",
                      "ERIC_GLOBAL_TRANSPORTSCHLUESSEL_NICHT_ERLAUBT", "ERIC_GLOBAL_OEFFENTLICHER_SCHLUESSEL_UNGUELTIG",
                      "ERIC_GLOBAL_TRANSPORTSCHLUESSEL_TYP_FALSCH", "ERIC_GLOBAL_PUFFER_UNGLEICHER_INSTANZ",
                      "ERIC_GLOBAL_VORSATZ_UNGUELTIG",
                      "ERIC_GLOBAL_DATEIZUGRIFF_VERWEIGERT", "ERIC_GLOBAL_UNGUELTIGE_INSTANZ",
                      "ERIC_GLOBAL_UNKNOWN_PARAMETER_ERROR", "ERIC_GLOBAL_CHECK_CORRUPTED_NDS",
                      "ERIC_GLOBAL_VERSCHLUESSELUNGS_PARAMETER_NICHT_ANGEGEBEN", "ERIC_GLOBAL_SEND_FLAG_MEHR_ALS_EINES",
                      "ERIC_GLOBAL_UNGUELTIGE_FLAG_KOMBINATION", "ERIC_GLOBAL_ERSTE_SEITE_DRUCK_NICHT_UNTERSTUETZT",
                      "ERIC_GLOBAL_UNGUELTIGER_PARAMETER", "ERIC_GLOBAL_DRUCK_FUER_VERFAHREN_NICHT_ERLAUBT",
                      "ERIC_GLOBAL_VERSAND_ART_NICHT_UNTERSTUETZT", "ERIC_GLOBAL_UNGUELTIGE_PARAMETER_VERSION",
                      "ERIC_GLOBAL_TRANSFERHANDLE", "ERIC_GLOBAL_PLUGININITIALISIERUNG",
                      "ERIC_GLOBAL_INKOMPATIBLE_VERSIONEN",
                      "ERIC_GLOBAL_VERSCHLUESSELUNGSVERFAHREN_NICHT_UNTERSTUETZT",
                      "ERIC_GLOBAL_MEHRFACHAUFRUFE_NICHT_UNTERSTUETZT",
                      "ERIC_GLOBAL_UTI_COUNTRY_NOT_SUPPORTED", "ERIC_GLOBAL_IBAN_FORMALER_FEHLER",
                      "ERIC_GLOBAL_IBAN_LAENDERCODE_FEHLER",
                      "ERIC_GLOBAL_IBAN_LANDESFORMAT_FEHLER", "ERIC_GLOBAL_IBAN_PRUEFZIFFER_FEHLER",
                      "ERIC_GLOBAL_BIC_FORMALER_FEHLER",
                      "ERIC_GLOBAL_BIC_LAENDERCODE_FEHLER", "ERIC_GLOBAL_ZULASSUNGSNUMMER_ZU_LANG",
                      "ERIC_GLOBAL_IDNUMMER_UNGUELTIG",
                      "ERIC_GLOBAL_NULL_PARAMETER", "ERIC_GLOBAL_EWAZ_UNGUELTIG",
                      "ERIC_GLOBAL_EWAZ_LANDESKUERZEL_UNBEKANNT",
                      "ERIC_GLOBAL_UPDATE_NECESSARY", "ERIC_GLOBAL_EINSTELLUNG_NAME_UNGUELTIG",
                      "ERIC_GLOBAL_EINSTELLUNG_WERT_UNGUELTIG",
                      "ERIC_GLOBAL_ERR_DEKODIEREN", "ERIC_GLOBAL_FUNKTION_NICHT_UNTERSTUETZT",
                      "ERIC_GLOBAL_NUTZDATENTICKETS_NICHT_EINDEUTIG",
                      "ERIC_GLOBAL_NUTZDATENHEADERVERSIONEN_UNEINHEITLICH", "ERIC_GLOBAL_BUNDESLAENDER_UNEINHEITLICH",
                      "ERIC_GLOBAL_ZEITRAEUME_UNEINHEITLICH", "ERIC_GLOBAL_NUTZDATENHEADER_EMPFAENGER_NICHT_KORREKT"]

ERIC_TRANSFER_ERRORS = ["ERIC_TRANSFER_COM_ERROR", "ERIC_TRANSFER_VORGANG_NICHT_UNTERSTUETZT",
                        "ERIC_TRANSFER_ERR_XML_THEADER",
                        "ERIC_TRANSFER_ERR_PARAM", "ERIC_TRANSFER_ERR_DATENTEILENDNOTFOUND",
                        "ERIC_TRANSFER_ERR_BEGINDATENLIEFERANT",
                        "ERIC_TRANSFER_ERR_ENDDATENLIEFERANT", "ERIC_TRANSFER_ERR_BEGINTRANSPORTSCHLUESSEL",
                        "ERIC_TRANSFER_ERR_ENDTRANSPORTSCHLUESSEL",
                        "ERIC_TRANSFER_ERR_BEGINDATENGROESSE", "ERIC_TRANSFER_ERR_ENDDATENGROESSE",
                        "ERIC_TRANSFER_ERR_SEND", "ERIC_TRANSFER_ERR_NOTENCRYPTED",
                        "ERIC_TRANSFER_ERR_PROXYCONNECT", "ERIC_TRANSFER_ERR_CONNECTSERVER",
                        "ERIC_TRANSFER_ERR_NORESPONSE", "ERIC_TRANSFER_ERR_PROXYAUTH", "ERIC_TRANSFER_ERR_SEND_INIT",
                        "ERIC_TRANSFER_ERR_TIMEOUT", "ERIC_TRANSFER_ERR_PROXYPORT_INVALID", "ERIC_TRANSFER_ERR_OTHER",
                        "ERIC_TRANSFER_ERR_XML_NHEADER",
                        "ERIC_TRANSFER_ERR_XML_ENCODING", "ERIC_TRANSFER_ERR_ENDSIGUSER",
                        "ERIC_TRANSFER_ERR_XMLTAG_NICHT_GEFUNDEN", "ERIC_TRANSFER_ERR_DATENTEILFEHLER",
                        "ERIC_TRANSFER_EID_ZERTIFIKATFEHLER", "ERIC_TRANSFER_EID_KEINKONTO",
                        "ERIC_TRANSFER_EID_IDNRNICHTEINDEUTIG",
                        "ERIC_TRANSFER_EID_SERVERFEHLER", "ERIC_TRANSFER_EID_KEINCLIENT",
                        "ERIC_TRANSFER_EID_CLIENTFEHLER", "ERIC_TRANSFER_EID_FEHLENDEFELDER",
                        "ERIC_TRANSFER_EID_IDENTIFIKATIONABGEBROCHEN", "ERIC_TRANSFER_EID_NPABLOCKIERT"
                        ]

ERIC_CRYPT_ERRORS = ["ERIC_CRYPT_ERROR_CREATE_KEY", "ERIC_CRYPT_E_INVALID_HANDLE", "ERIC_CRYPT_E_MAX_SESSION",
                     "ERIC_CRYPT_E_BUSY", "ERIC_CRYPT_E_OUT_OF_MEM", "ERIC_CRYPT_E_PSE_PATH", "ERIC_CRYPT_E_PIN_WRONG",
                     "ERIC_CRYPT_E_PIN_LOCKED",
                     "ERIC_CRYPT_E_P7_READ", "ERIC_CRYPT_E_P7_DECODE",
                     "ERIC_CRYPT_E_P7_RECIPIENT", "ERIC_CRYPT_E_P12_READ", "ERIC_CRYPT_E_P12_DECODE",
                     "ERIC_CRYPT_E_P12_SIG_KEY",
                     "ERIC_CRYPT_E_P12_ENC_KEY", "ERIC_CRYPT_E_P11_SIG_KEY", "ERIC_CRYPT_E_P11_ENC_KEY",
                     "ERIC_CRYPT_E_XML_PARSE",
                     "ERIC_CRYPT_E_XML_SIG_ADD", "ERIC_CRYPT_E_XML_SIG_TAG", "ERIC_CRYPT_E_XML_SIG_SIGN",
                     "ERIC_CRYPT_E_ENCODE_UNKNOWN",
                     "ERIC_CRYPT_E_ENCODE_ERROR", "ERIC_CRYPT_E_XML_INIT", "ERIC_CRYPT_E_ENCRYPT",
                     "ERIC_CRYPT_E_DECRYPT", "ERIC_CRYPT_E_P11_SLOT_EMPTY", "ERIC_CRYPT_E_NO_SIG_ENC_KEY",
                     "ERIC_CRYPT_E_LOAD_DLL", "ERIC_CRYPT_E_NO_SERVICE", "ERIC_CRYPT_E_ESICL_EXCEPTION",
                     "ERIC_CRYPT_E_TOKEN_TYPE_MISMATCH", "ERIC_CRYPT_E_P12_CREATE", "ERIC_CRYPT_E_VERIFY_CERT_CHAIN",
                     "ERIC_CRYPT_E_P11_ENGINE_LOADED", "ERIC_CRYPT_E_USER_CANCEL", "ERIC_CRYPT_ZERTIFIKAT",
                     "ERIC_CRYPT_SIGNATUR", "ERIC_CRYPT_NICHT_UNTERSTUETZTES_PSE_FORMAT", "ERIC_CRYPT_PIN_BENOETIGT",
                     "ERIC_CRYPT_PIN_STAERKE_NICHT_AUSREICHEND", "ERIC_CRYPT_E_INTERN",
                     "ERIC_CRYPT_ZERTIFIKATSPFAD_KEIN_VERZEICHNIS",
                     "ERIC_CRYPT_ZERTIFIKATSDATEI_EXISTIERT_BEREITS", "ERIC_CRYPT_PIN_ENTHAELT_UNGUELTIGE_ZEICHEN",
                     "ERIC_CRYPT_E_INVALID_PARAM_ABC", "ERIC_CRYPT_CORRUPTED", "ERIC_CRYPT_EIDKARTE_NICHT_UNTERSTUETZT",
                     "ERIC_CRYPT_E_SC_SLOT_EMPTY",
                     "ERIC_CRYPT_E_SC_NO_APPLET", "ERIC_CRYPT_E_SC_SESSION",
                     "ERIC_CRYPT_E_P11_NO_SIG_CERT", "ERIC_CRYPT_E_P11_INIT_FAILED", "ERIC_CRYPT_E_P11_NO_ENC_CERT",
                     "ERIC_CRYPT_E_P12_NO_SIG_CERT", "ERIC_CRYPT_E_P12_NO_ENC_CERT",
                     "ERIC_CRYPT_E_SC_ENC_KEY", "ERIC_CRYPT_E_SC_NO_SIG_CERT",
                     "ERIC_CRYPT_E_SC_NO_ENC_CERT", "ERIC_CRYPT_E_SC_INIT_FAILED", "ERIC_CRYPT_E_SC_SIG_KEY"
                     ]

ERIC_IO_ERRORS = ["ERIC_IO_FEHLER", "ERIC_IO_DATEI_INKORREKT", "ERIC_IO_PARSE_FEHLER",
                  "ERIC_IO_NDS_GENERIERUNG_FEHLGESCHLAGEN", "ERIC_IO_MASTERDATENSERVICE_NICHT_VERFUEGBAR",
                  "ERIC_IO_STEUERZEICHEN_IM_NDS",
                  "ERIC_IO_VERSIONSINFORMATIONEN_NICHT_GEFUNDEN", "ERIC_IO_FALSCHES_VERFAHREN",
                  "ERIC_IO_READER_MEHRFACHE_STEUERFAELLE", "ERIC_IO_READER_UNERWARTETE_ELEMENTE",
                  "ERIC_IO_READER_FORMALE_FEHLER", "ERIC_IO_READER_FALSCHES_ENCODING",
                  "ERIC_IO_READER_MEHRFACHE_NUTZDATEN_ELEMENTE", "ERIC_IO_READER_MEHRFACHE_NUTZDATENBLOCK_ELEMENTE",
                  "ERIC_IO_UNBEKANNTE_DATENART", "ERIC_IO_READER_UNTERSACHBEREICH_UNGUELTIG",
                  "ERIC_IO_READER_ZU_VIELE_NUTZDATENBLOCK_ELEMENTE", "ERIC_IO_READER_STEUERZEICHEN_IM_TRANSFERHEADER",
                  "ERIC_IO_READER_STEUERZEICHEN_IM_NUTZDATENHEADER", "ERIC_IO_READER_STEUERZEICHEN_IN_DEN_NUTZDATEN",
                  'ERIC_IO_READER_ZU_VIELE_ANHAENGE', 'ERIC_IO_READER_ANHANG_ZU_GROSS',
                  'ERIC_IO_READER_ANHAENGE_ZU_GROSS', "ERIC_IO_READER_SCHEMA_VALIDIERUNGSFEHLER",
                  "ERIC_IO_READER_UNBEKANNTE_XML_ENTITY", "ERIC_IO_DATENTEILNOTFOUND",
                  "ERIC_IO_DATENTEILENDNOTFOUND", "ERIC_IO_UEBERGABEPARAMETER_FEHLERHAFT",
                  "ERIC_IO_UNGUELTIGE_UTF8_SEQUENZ", "ERIC_IO_UNGUELTIGE_ZEICHEN_IN_PARAMETER"
                  ]

ERIC_PRINT_ERRORS = ["ERIC_PRINT_INTERNER_FEHLER", "ERIC_PRINT_DRUCKVORLAGE_NICHT_GEFUNDEN",
                     "ERIC_PRINT_UNGUELTIGER_DATEI_PFAD",
                     "ERIC_PRINT_INITIALISIERUNG_FEHLERHAFT", "ERIC_PRINT_AUSGABEZIEL_UNBEKANNT",
                     "ERIC_PRINT_ABBRUCH_DRUCKVORBEREITUNG", "ERIC_PRINT_ABBRUCH_GENERIERUNG",
                     "ERIC_PRINT_STEUERFALL_NICHT_UNTERSTUETZT", "ERIC_PRINT_FUSSTEXT_ZU_LANG"
                     ]


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


class EricaRequestTimeoutError(RequestException):
    """Exception raised when a Timeout reached in Erica"""

    def __init__(self, original_exception=None):
        self.message = _l('erica.timeout.error')
        self.original_exception = original_exception
        super(EricaRequestTimeoutError, self).__init__()


class EricaRequestConnectionError(RequestException):
    """Exception raised when a Connection Error reached in Erica"""

    def __init__(self, original_exception=None):
        self.message = _l('erica.connection.error')
        self.original_exception = original_exception
        super(EricaRequestConnectionError, self).__init__()
