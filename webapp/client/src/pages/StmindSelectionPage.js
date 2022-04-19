import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import SelectableCard from "../components/SelectableCard";
import vorsorgeIcon from "../assets/icons/vorsorge_icon.svg";
import aussergBelaIcon from "../assets/icons/ausserg_bela_icon.svg";
import handwerkerIcon from "../assets/icons/handwerker_icon.svg";
import spendenIcon from "../assets/icons/spenden_icon.svg";
import religionIcon from "../assets/icons/religion_icon.svg";
import { checkboxPropType } from "../lib/propTypes";

export default function StmindSelectionPage({
  stepHeader,
  form,
  fields,
  prevUrl,
  plausibleDomain,
}) {
  const { t } = useTranslation();
  const plausibleProps = { method: "CTA Steuermindernde Aufwendungen" };

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader {...stepHeader} />
      <StepForm
        plausibleDomain={plausibleDomain}
        plausibleProps={plausibleProps}
        {...form}
      >
        <SelectableCard
          autofocus
          fieldName="stmind_select_vorsorge"
          fieldId="stmind_select_vorsorge"
          checked={fields.stmindSelectVorsorge.checked}
          title={t("lotse.stmindSelection.selectVorsorge.label.title")}
          body={t("lotse.stmindSelection.selectVorsorge.label.text")}
          icon={vorsorgeIcon}
          errors={fields.stmindSelectVorsorge.errors}
        />
        <SelectableCard
          fieldName="stmind_select_ausserg_bela"
          fieldId="stmind_select_ausserg_bela"
          checked={fields.stmindSelectAussergBela.checked}
          title={t("lotse.stmindSelection.selectAussergBela.label.title")}
          body={t("lotse.stmindSelection.selectAussergBela.label.text")}
          icon={aussergBelaIcon}
          errors={fields.stmindSelectAussergBela.errors}
        />
        <SelectableCard
          fieldName="stmind_select_handwerker"
          fieldId="stmind_select_handwerker"
          checked={fields.stmindSelectHandwerker.checked}
          title={t("lotse.stmindSelection.selectHandwerker.label.title")}
          body={t("lotse.stmindSelection.selectHandwerker.label.text")}
          icon={handwerkerIcon}
          errors={fields.stmindSelectHandwerker.errors}
        />
        <SelectableCard
          fieldName="stmind_select_spenden"
          fieldId="stmind_select_spenden"
          checked={fields.stmindSelectSpenden.checked}
          title={t("lotse.stmindSelection.selectSpenden.label.title")}
          body={t("lotse.stmindSelection.selectSpenden.label.text")}
          icon={spendenIcon}
          errors={fields.stmindSelectSpenden.errors}
        />
        <SelectableCard
          fieldName="stmind_select_religion"
          fieldId="stmind_select_religion"
          checked={fields.stmindSelectReligion.checked}
          title={t("lotse.stmindSelection.selectReligion.label.title")}
          body={t("lotse.stmindSelection.selectReligion.label.text")}
          icon={religionIcon}
          errors={fields.stmindSelectReligion.errors}
        />
      </StepForm>
    </>
  );
}

StmindSelectionPage.propTypes = {
  stepHeader: PropTypes.exact({
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    explanatoryButtonText: PropTypes.string,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    stmindSelectVorsorge: checkboxPropType,
    stmindSelectAussergBela: checkboxPropType,
    stmindSelectHandwerker: checkboxPropType,
    stmindSelectSpenden: checkboxPropType,
    stmindSelectReligion: checkboxPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
  plausibleDomain: PropTypes.string,
};

StmindSelectionPage.defaultProps = {
  plausibleDomain: null,
};
