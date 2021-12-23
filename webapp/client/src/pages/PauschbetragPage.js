import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormFieldRadio, { boldifyChoices } from "../components/FormFieldRadio";
import Details from "../components/Details";
import { extendedSelectionFieldPropType } from "../lib/propTypes";

const DetailsDiv = styled.div`
  margin-bottom: var(--spacing-04);
`;

export default function PauschbetragPage({
  stepHeader,
  form,
  fields,
  prevUrl,
}) {
  const { t } = useTranslation();
  const boldChoices = boldifyChoices(fields.wantsPauschbetrag.options);

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
      <DetailsDiv>
        <Details
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
        </Details>
      </DetailsDiv>
      <StepForm {...form}>
        <FormFieldRadio
          fieldName={fields.wantsPauschbetrag.name}
          fieldId={fields.wantsPauschbetrag.name}
          options={boldChoices}
          value={fields.wantsPauschbetrag.selectedValue}
          errors={fields.wantsPauschbetrag.errors}
        />
      </StepForm>
    </>
  );
}

PauschbetragPage.propTypes = {
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
    wantsPauschbetrag: extendedSelectionFieldPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
