import PropTypes from "prop-types";
import StepHeaderButtons from "../components/StepHeaderButtons";

export default function LoginPage({ prevUrl, backLinkText }) {
  return (
    <StepHeaderButtons backLinkUrl={prevUrl} backLinkText={backLinkText} />
  );
}

LoginPage.propTypes = {
  prevUrl: PropTypes.string,
  backLinkText: PropTypes.string,
};

LoginPage.defaultProps = {
  prevUrl: null,
  // TODO: intl
  backLinkText: "form.back",
};
