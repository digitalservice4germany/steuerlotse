import PropTypes from "prop-types";
import React, { useState, useReducer } from "react";
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

const TAX_NUMBER_FORM_STATE_CHANGES = {
  NothingSelected: "NothingSelected",
  TaxNumberExistsSelected: "TaxNumberExistsSelected",
  BundeslandSelected: "BundeslandSelected",
  TaxOfficeSelected: "TaxOfficeSelected",
};

function reduceTaxNumberPageData(state, action) {
  switch (action.type) {
    case TAX_NUMBER_FORM_STATE_CHANGES.TaxNumberExistsSelected:
      return {
        ...state,
        taxNumberExists: action.value,
        steuernummer:
          action.value === "yes" && state.bundesland
            ? state.steuernummer
            : [""],
        bufaNr:
          action.value !== "yes" && state.bundesland ? state.bufaNr : undefined,
        requestNewTaxNumber: undefined,
        showTaxNumberExists: true,
        showBundesland: true,
        showSteuernummer: action.value === "yes" && state.bundesland,
        showBufaNr: action.value !== "yes" && state.bundesland,
        showRequestNewTaxNumber: false,
      };
    case TAX_NUMBER_FORM_STATE_CHANGES.BundeslandSelected:
      if (!action.value) {
        return {
          ...state,
          bundesland: action.value,
          bufaNr: undefined,
          requestNewTaxNumber: undefined,
          showTaxNumberExists: true,
          showBundesland: true,
          showBufaNr: false,
          showSteuernummer: false,
          showRequestNewTaxNumber: false,
        };
      }

      if (state.taxNumberExists === "yes") {
        return {
          ...state,
          bundesland: action.value,
          bufaNr: undefined,
          requestNewTaxNumber: undefined,
          showTaxNumberExists: true,
          showBundesland: true,
          showBufaNr: false,
          showSteuernummer: true,
          showRequestNewTaxNumber: false,
        };
      }
      return {
        ...state,
        bundesland: action.value,
        steuernummer: [""],
        requestNewTaxNumber: undefined,
        showTaxNumberExists: true,
        showBundesland: true,
        showBufaNr: true,
        showSteuernummer: false,
        showRequestNewTaxNumber: false,
      };
    case TAX_NUMBER_FORM_STATE_CHANGES.TaxOfficeSelected:
      return {
        ...state,
        bufaNr: action.value,
        requestNewTaxNumber: undefined,
        showTaxNumberExists: true,
        showBundesland: true,
        showBufaNr: true,
        showSteuernummer: false,
        showRequestNewTaxNumber: true,
      };
    default:
      return {
        ...state,
        taxNumberExists: undefined,
        bundesland: undefined,
        bufaNr: undefined,
        steuernummer: [""],
        requestNewTaxNumber: undefined,
        showTaxNumberExists: true,
        showBundesland: false,
        showBufaNr: false,
        showSteuernummer: false,
        showRequestNewTaxNumber: false,
      };
  }
}

function getSplitTypeForState(selectedStateAbbreviation) {
  switch (selectedStateAbbreviation) {
    case "bw":
    case "be":
    case "hb":
    case "hh":
    case "nd":
    case "rp":
    case "sh":
      return "0";
    case "by":
    case "bb":
    case "mv":
    case "sl":
    case "sn":
    case "st":
    case "th":
      return "1";
    case "nw":
      return "2";
    default:
      return "3";
  }
}

function getInitialTaxNumberPageData(fields) {
  const currentState = {
    taxNumberExists: fields.steuernummerExists.value,
    bundesland: fields.bundesland.selectedValue,
    bufaNr: fields.bufaNr.selectedValue,
    steuernummer: fields.steuernummer.value,
    requestNewTaxNumber: fields.requestNewTaxNumber.checked,
    showTaxNumberExists: true,
    showBundesland: false,
    showBufaNr: false,
    showSteuernummer: false,
    showRequestNewTaxNumber: false,
  };
  if (fields.steuernummerExists.value === "yes") {
    if (fields.bundesland.selectedValue) {
      return {
        ...currentState,
        showBundesland: true,
        showSteuernummer: true,
      };
    }
    return {
      ...currentState,
      showBundesland: true,
    };
  }
  if (fields.steuernummerExists.value === "no") {
    if (fields.bundesland.selectedValue) {
      if (fields.bufaNr.selectedValue) {
        return {
          ...currentState,
          showBundesland: true,
          showBufaNr: true,
          showRequestNewTaxNumber: true,
        };
      }
      return {
        ...currentState,
        showBundesland: true,
        showBufaNr: true,
      };
    }
    return {
      ...currentState,
      showBundesland: true,
    };
  }
  return currentState;
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

  const [taxNumberPageData, changeTaxNumberPageData] = useReducer(
    reduceTaxNumberPageData,
    getInitialTaxNumberPageData(fields)
  );

  const [selectedStateAbbreviation, setSelectedStateAbbreviation] = useState(
    () => {
      if (fields.bundesland.selectedValue) {
        return fields.bundesland.selectedValue.toLowerCase();
      }
      return undefined;
    }
  );

  const stateDropDown = (
    <FormRowCentered key="bundeslandRow">
      <FormFieldDropDown
        fieldName="bundesland"
        fieldId="bundesland"
        key="bundesland"
        selectedValue={taxNumberPageData.bundesland}
        options={fields.bundesland.options}
        label={{
          text: t("lotseFlow.taxNumber.bundesland.labelText"),
        }}
        errors={fields.bundesland.errors}
        onChangeHandler={(event) => {
          const currentSelectedStateAbbreviation =
            event.target.options[
              event.target.selectedIndex
            ].value.toLowerCase();
          setSelectedStateAbbreviation(currentSelectedStateAbbreviation);
          changeTaxNumberPageData({
            value: event.target.value,
            type: TAX_NUMBER_FORM_STATE_CHANGES.BundeslandSelected,
          });
        }}
      />
    </FormRowCentered>
  );

  const bufaNrDropdown = (
    <FormRowCentered key="bufaNrRow">
      <FormFieldDropDown
        fieldName="bufa_nr"
        fieldId="bufa_nr"
        key="bufa_nr"
        selectedValue={taxNumberPageData.bufaNr}
        options={extractCorrespondingTaxOffices(
          selectedStateAbbreviation,
          taxOfficeList
        )}
        label={{
          text: t("lotseFlow.taxNumber.taxOffices.labelText"),
        }}
        errors={fields.bufaNr.errors}
        onChangeHandler={(event) => {
          changeTaxNumberPageData({
            value: event.target.value,
            type: TAX_NUMBER_FORM_STATE_CHANGES.TaxOfficeSelected,
          });
        }}
      />
    </FormRowCentered>
  );

  const taxNumberInput = (
    <FormRowCentered key="steuernummerRow">
      <FormFieldTaxNumber
        required
        fieldName="steuernummer"
        fieldId="steuernummer"
        values={taxNumberPageData.steuernummer}
        label={{
          text: t("lotseFlow.taxNumber.taxNumberInput.labelText"),
          exampleInput: t("lotseFlow.taxNumber.taxNumberInput.labelText"),
        }}
        errors={fields.steuernummer.errors}
        key={selectedStateAbbreviation}
        splitType={getSplitTypeForState(selectedStateAbbreviation)} // Do not split field for Hessen
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
        checked={taxNumberPageData.requestNewTaxNumber}
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

  const shownFields = [];

  if (taxNumberPageData.showBundesland) {
    shownFields.push(stateDropDown);
  }
  if (taxNumberPageData.showBufaNr) {
    shownFields.push(bufaNrDropdown);
  }
  if (taxNumberPageData.showRequestNewTaxNumber) {
    shownFields.push(requestNewTaxNumberCheckbox);
  }
  if (taxNumberPageData.showSteuernummer) {
    shownFields.push(taxNumberInput);
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
            value={taxNumberPageData.taxNumberExists}
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
            onChangeHandler={(event) => {
              changeTaxNumberPageData({
                value: event.target.value,
                type: TAX_NUMBER_FORM_STATE_CHANGES.TaxNumberExistsSelected,
              });
            }}
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
