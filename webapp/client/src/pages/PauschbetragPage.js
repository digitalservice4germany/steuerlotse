import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormFieldRadioGroup from "../components/FormFieldRadioGroup";
import DetailsSeparated from "../components/DetailsSeparated";
import {
  extendedSelectionFieldPropType,
  stepHeaderPropType,
} from "../lib/propTypes";

export default function PauschbetragPage({
  stepHeader,
  form,
  fields,
  pauschbetrag,
  prevUrl,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader
        title={stepHeader.title}
        intro={
          <Trans
            t={t}
            i18nKey="lotse.pauschbetrag.intro"
            components={{
              bold: <b />,
            }}
          />
        }
      />
      <DetailsSeparated
        title={t("lotse.pauschbetrag.details.title")}
        detailsId="pauschbetrag_details"
      >
        {[
          <p key={0}>{t("lotse.pauschbetrag.details.p1")}</p>,
          <ul key={1}>
            <li key={0}>{t("lotse.pauschbetrag.details.list.listItem1")}</li>
            <li key={1}>{t("lotse.pauschbetrag.details.list.listItem2")}</li>
            <li key={2}>{t("lotse.pauschbetrag.details.list.listItem3")}</li>
          </ul>,
          <p key={2}>{t("lotse.pauschbetrag.details.p2")}</p>,
          <p key={3}>
            <Trans
              t={t}
              i18nKey="lotse.pauschbetrag.details.p3"
              components={{
                bold: <b />,
              }}
            />
          </p>,
          <p key={4}>{t("lotse.pauschbetrag.details.p4")}</p>,
        ]}
      </DetailsSeparated>
      <StepForm {...form}>
        <FormFieldRadioGroup
          fieldName={fields.requestsPauschbetrag.name}
          fieldId={fields.requestsPauschbetrag.name}
          options={[
            {
              value: "yes",
              displayName: (
                <Trans
                  t={t}
                  i18nKey="lotse.pauschbetrag.requestPauschbetrag.yes"
                  components={{
                    bold: <b />,
                  }}
                  values={{ pauschbetrag }}
                />
              ),
            },
            {
              value: "no",
              displayName: t("lotse.pauschbetrag.requestPauschbetrag.no"),
            },
          ]}
          value={fields.requestsPauschbetrag.selectedValue}
          errors={fields.requestsPauschbetrag.errors}
        />
      </StepForm>
    </>
  );
}

PauschbetragPage.propTypes = {
  stepHeader: stepHeaderPropType.isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    requestsPauschbetrag: extendedSelectionFieldPropType,
  }).isRequired,
  pauschbetrag: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
