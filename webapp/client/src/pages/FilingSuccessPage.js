import PropTypes from "prop-types";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormHeader from "../components/FormHeader";
import DownloadLink from "../components/DownloadLink";
import StepNavButtons from "../components/StepNavButtons";

export default function FilingSuccessPage({
  nextUrl,
  transferTicket,
  downloadUrl,
  taxNumberProvided,
  plausibleDomain,
}) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("filing.success.title"),
    intro: t("filing.success.intro"),
  };

  // Add custom plausible goal if tax number provided and plausible domain active
  // Hook is called after component is rendered and will only run once after component is rendered
  useEffect(() => {
    if (taxNumberProvided !== null && plausibleDomain !== null) {
      window.plausible("summary_submitted", {
        props: { tax_number_provided: { taxNumberProvided } },
      });
    }
    return null;
  }, [taxNumberProvided, plausibleDomain]);

  return (
    <>
      <StepHeaderButtons />
      <FormHeader {...stepHeader} />
      <h2 className="h4 mt-5">{t("filing.success.transfer_ticket.heading")}</h2>
      <p>{t("filing.success.transfer_ticket.text")}</p>
      <span className="font-weight-bolder">
        {t("filing.success.transfer_ticket.your")} {transferTicket}
      </span>
      <h2 className="h4 mt-5">{t("filing.success.pdf.heading")}</h2>
      <p className="mb-4">{t("filing.success.pdf.text")}</p>
      <DownloadLink text={t("filing.success.pdf.download")} url={downloadUrl} />
      <StepNavButtons nextUrl={nextUrl} isForm={false} />
    </>
  );
}

FilingSuccessPage.propTypes = {
  nextUrl: PropTypes.string.isRequired,
  transferTicket: PropTypes.string.isRequired,
  downloadUrl: PropTypes.string.isRequired,
  taxNumberProvided: PropTypes.bool,
  plausibleDomain: PropTypes.string,
};

FilingSuccessPage.defaultProps = {
  taxNumberProvided: false,
  plausibleDomain: null,
};
