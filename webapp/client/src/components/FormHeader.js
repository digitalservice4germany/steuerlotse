import PropTypes from "prop-types";
import FormHeaderParagraphs from "./FormHeaderParagraphs";

export default function FormHeader({ title, intro, hideIntro }) {
  const intros = !hideIntro ? [intro] : [];
  return <FormHeaderParagraphs title={title} intros={intros} />;
}

FormHeader.propTypes = {
  title: PropTypes.string.isRequired,
  intro: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.element,
    PropTypes.object,
  ]),
  hideIntro: PropTypes.bool,
};

FormHeader.defaultProps = {
  intro: undefined,
  hideIntro: false,
};
