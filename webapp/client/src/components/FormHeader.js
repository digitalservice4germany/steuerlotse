import PropTypes from "prop-types";
import FormHeaderIntro from "./FormHeaderIntro";

export default function FormHeader({ title, intro, hideIntro }) {
  const intros = [].concat(intro);
  const paragraphs = !hideIntro ? intros : [];
  return (
    <div>
      <h1 className="my-4">{title}</h1>
      <FormHeaderIntro title={title} paragraphs={paragraphs} />;
    </div>
  );
}

FormHeader.propTypes = {
  title: PropTypes.string.isRequired,
  intro: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.element,
    PropTypes.object,
    PropTypes.arrayOf(
      PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.element,
        PropTypes.object,
      ])
    ),
  ]),
  hideIntro: PropTypes.bool,
};

FormHeader.defaultProps = {
  intro: undefined,
  hideIntro: false,
};
