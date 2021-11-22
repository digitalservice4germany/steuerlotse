import PropTypes from "prop-types";
import React, { useState } from "react";
import { Trans, useTranslation } from "react-i18next";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import FormFieldDropDown from "../components/FormFieldDropDown";
import FormFieldYesNo from "../components/FormFieldYesNo";
import FormFieldTaxNumber from "../components/FormFieldTaxNumber";
import FormHeader from "../components/FormHeader";
import FormRowCentered from "../components/FormRowCentered";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import SubHeading from "../components/SubHeading";
import {
  checkboxPropType,
  fieldPropType,
  selectionFieldPropType,
} from "../lib/propTypes";

const TAX_NUMBER_FORM_STATES = {
  NothingSelected: "NothingSelected",
  StateSelectionTaxNumberExists: "StateSelectionTaxNumberExists",
  StateSelectionNoTaxNumberExists: "StateSelectionNoTaxNumberExists",
  TaxOfficeSelection: "TaxOfficeSelection",
  TaxNumberInput: "TaxNumberInput",
  RequestNewTaxNumber: "RequestNewTaxNumber",
};

function currentState(fields) {
  if (fields.steuernummerExists.value === "yes") {
    if (fields.bundesland.selectedValue) {
      return TAX_NUMBER_FORM_STATES.TaxNumberInput;
    }
    return TAX_NUMBER_FORM_STATES.StateSelectionTaxNumberExists;
  }
  if (fields.steuernummerExists.value === "no") {
    if (fields.bundesland.selectedValue) {
      if (fields.bufaNr.selectedValue) {
        return TAX_NUMBER_FORM_STATES.RequestNewTaxNumber;
      }
      return TAX_NUMBER_FORM_STATES.TaxOfficeSelection;
    }
    return TAX_NUMBER_FORM_STATES.StateSelectionNoTaxNumberExists;
  }

  return TAX_NUMBER_FORM_STATES.NothingSelected;
}

function extractCorrespondingTaxOffices(
  selectedStateAbbreviation,
  taxOfficeList
) {
  const selectedState = taxOfficeList.find(
    (taxOffice) => taxOffice.stateAbbreviation === selectedStateAbbreviation
  );

  if (selectedState) {
    const selectedTaxOffices = selectedState.taxOffices;
    if (selectedTaxOffices) {
      selectedTaxOffices.sort((a, b) => String(a.name).localeCompare(b.name));
      return selectedTaxOffices.map((taxOffice) => ({
        value: taxOffice.bufaNr,
        displayName: taxOffice.name.replace("Finanzamt ", ""),
      }));
    }
  }

  return [];
}

export default function TaxNumberPage({
  stepHeader,
  form,
  fields,
  taxOfficeList,
  numberOfUsers,
}) {
  const { t } = useTranslation();

  const [taxNumberFormState, setTaxNumberFormState] = useState(
    currentState(fields)
  );

  const [selectedStateAbbreviation, setSelectedStateAbbreviation] = useState(
    () => {
      if (fields.bundesland.selectedValue) {
        return fields.bundesland.selectedValue.toLowerCase();
      }
      return undefined;
    }
  );

  const changeTaxNumberExists = (event) => {
    switch (taxNumberFormState) {
      case TAX_NUMBER_FORM_STATES.NothingSelected:
      case TAX_NUMBER_FORM_STATES.StateSelectionTaxNumberExists:
      case TAX_NUMBER_FORM_STATES.StateSelectionNoTaxNumberExists:
        if (event.target.value === "yes") {
          setTaxNumberFormState(
            TAX_NUMBER_FORM_STATES.StateSelectionTaxNumberExists
          );
        } else if (event.target.value === "no") {
          setTaxNumberFormState(
            TAX_NUMBER_FORM_STATES.StateSelectionNoTaxNumberExists
          );
        }
        break;
      default:
        if (event.target.value === "yes") {
          setTaxNumberFormState(TAX_NUMBER_FORM_STATES.TaxNumberInput);
        } else if (event.target.value === "no") {
          setTaxNumberFormState(TAX_NUMBER_FORM_STATES.TaxOfficeSelection);
        }
        break;
    }
  };

  const changeStateSelection = (event) => {
    const currentSelectedStateAbbreviation =
      event.target.options[event.target.selectedIndex].value.toLowerCase();
    setSelectedStateAbbreviation(currentSelectedStateAbbreviation);

    if (currentSelectedStateAbbreviation) {
      switch (taxNumberFormState) {
        case TAX_NUMBER_FORM_STATES.StateSelectionTaxNumberExists:
          setTaxNumberFormState(TAX_NUMBER_FORM_STATES.TaxNumberInput);
          break;
        case TAX_NUMBER_FORM_STATES.StateSelectionNoTaxNumberExists:
        case TAX_NUMBER_FORM_STATES.TaxOfficeSelection:
        case TAX_NUMBER_FORM_STATES.RequestNewTaxNumber:
          setTaxNumberFormState(TAX_NUMBER_FORM_STATES.TaxOfficeSelection);
          break;
        default:
          break;
      }
    } else if (taxNumberFormState === TAX_NUMBER_FORM_STATES.TaxNumberInput) {
      setTaxNumberFormState(
        TAX_NUMBER_FORM_STATES.StateSelectionTaxNumberExists
      );
    } else {
      setTaxNumberFormState(
        TAX_NUMBER_FORM_STATES.StateSelectionNoTaxNumberExists
      );
    }
  };

  const changeTaxOffices = (event) => {
    if (
      event.target.value &&
      taxNumberFormState === TAX_NUMBER_FORM_STATES.TaxOfficeSelection
    ) {
      setTaxNumberFormState(TAX_NUMBER_FORM_STATES.RequestNewTaxNumber);
    } else if (
      !event.target.value &&
      taxNumberFormState === TAX_NUMBER_FORM_STATES.RequestNewTaxNumber
    ) {
      setTaxNumberFormState(TAX_NUMBER_FORM_STATES.TaxOfficeSelection);
    }
  };

  const stateDropDown = (
    <FormRowCentered key="bundeslandRow">
      <FormFieldDropDown
        fieldName="bundesland"
        fieldId="bundesland"
        key="bundesland"
        selectedValue={fields.bundesland.selectedValue}
        options={fields.bundesland.options}
        label={{
          text: t("lotseFlow.taxNumber.bundesland.labelText"),
        }}
        errors={fields.bundesland.errors}
        onChangeHandler={changeStateSelection}
      />
    </FormRowCentered>
  );

  const bufaNrDropdown = (
    <FormRowCentered key="bufaNrRow">
      <FormFieldDropDown
        fieldName="bufa_nr"
        fieldId="bufa_nr"
        key="bufa_nr"
        selectedValue={fields.bufaNr.selectedValue}
        options={extractCorrespondingTaxOffices(
          selectedStateAbbreviation,
          taxOfficeList
        )}
        label={{
          text: t("lotseFlow.taxNumber.taxOffices.labelText"),
        }}
        errors={fields.bufaNr.errors}
        onChangeHandler={changeTaxOffices}
      />
    </FormRowCentered>
  );

  const taxNumberInput = (
    <FormRowCentered key="steuernummerRow">
      <FormFieldTaxNumber
        required
        fieldName="steuernummer"
        fieldId="steuernummer"
        values={fields.steuernummer.value}
        label={{
          text: t("lotseFlow.taxNumber.taxNumberInput.labelText"),
          exampleInput: t("lotseFlow.taxNumber.taxNumberInput.labelText"),
        }}
        errors={fields.steuernummer.errors}
        key={selectedStateAbbreviation}
        isSplit={selectedStateAbbreviation !== "he"} // Do not split field for Hessen
      />
    </FormRowCentered>
  );

  const requestNewTaxNumberCheckbox = (
    <FormRowCentered key="requestNewTaxNumberRow">
      <SubHeading>
        {t("lotseFlow.taxNumber.requestNewTaxNumber.headline")}
      </SubHeading>
      <p>{t("lotseFlow.taxNumber.requestNewTaxNumber.intro")}</p>
      <FormFieldConsentBox
        required
        fieldName="request_new_tax_number"
        fieldId="request_new_tax_number"
        checked={fields.requestNewTaxNumber.checked}
        labelText={
          <Trans
            t={t}
            i18nKey="lotseFlow.taxNumber.requestNewTaxNumber.labelText"
            count={numberOfUsers}
          />
        }
        errors={fields.requestNewTaxNumber.errors}
      />
    </FormRowCentered>
  );

  let shownFields;

  switch (taxNumberFormState) {
    case TAX_NUMBER_FORM_STATES.NothingSelected:
      break;
    case TAX_NUMBER_FORM_STATES.StateSelectionTaxNumberExists:
      shownFields = [stateDropDown];
      break;
    case TAX_NUMBER_FORM_STATES.StateSelectionNoTaxNumberExists:
      shownFields = [stateDropDown];
      break;
    case TAX_NUMBER_FORM_STATES.TaxOfficeSelection:
      shownFields = [stateDropDown, bufaNrDropdown];
      break;
    case TAX_NUMBER_FORM_STATES.TaxNumberInput:
      shownFields = [stateDropDown, taxNumberInput];
      break;
    case TAX_NUMBER_FORM_STATES.RequestNewTaxNumber:
      shownFields = [
        stateDropDown,
        bufaNrDropdown,
        requestNewTaxNumberCheckbox,
      ];
      break;
    default:
  }

  return (
    <>
      <StepHeaderButtons />
      <FormHeader {...stepHeader} />
      <StepForm {...form}>
        <FormRowCentered>
          <FormFieldYesNo
            fieldName="steuernummer_exists"
            fieldId="steuernummer_exists"
            value={fields.steuernummerExists.value}
            label={{
              text: t("lotseFlow.taxNumber.taxNumberExists.labelText", {
                count: numberOfUsers,
              }),
            }}
            details={{
              title: t("lotseFlow.taxNumber.taxNumberExists.help.title"),
              text: t("lotseFlow.taxNumber.taxNumberExists.help.text"),
            }}
            errors={fields.steuernummerExists.errors}
            onChangeHandler={changeTaxNumberExists}
          />
        </FormRowCentered>
        {shownFields}
      </StepForm>
    </>
  );
}

TaxNumberPage.propTypes = {
  stepHeader: PropTypes.exact({
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    steuernummerExists: fieldPropType,
    steuernummer: fieldPropType,
    bundesland: selectionFieldPropType,
    bufaNr: selectionFieldPropType,
    requestNewTaxNumber: checkboxPropType,
  }).isRequired,
  taxOfficeList: PropTypes.arrayOf(
    PropTypes.exact({
      stateAbbreviation: PropTypes.string,
      name: PropTypes.string,
      taxOffices: PropTypes.arrayOf(
        PropTypes.exact({
          name: PropTypes.string,
          bufaNr: PropTypes.string,
        })
      ),
    })
  ).isRequired,
  numberOfUsers: PropTypes.number.isRequired,
};
