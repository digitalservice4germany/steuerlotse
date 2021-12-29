import PropTypes from "prop-types";
import styled from "styled-components";

const Intro = styled.p`
  font-size: var(--text-medium);
`;

export default function FormHeaderParagraphs({ title, intros }) {
  return (
    <div>
      <h1 className="my-4">{title}</h1>
      {intros.map((intro, index) => (
        <Intro key={`intro_${index}`}>{intro}</Intro>
      ))}
    </div>
  );
}

FormHeaderParagraphs.propTypes = {
  title: PropTypes.string.isRequired,
  intros: PropTypes.arrayOf(
    PropTypes.oneOfType([PropTypes.string, PropTypes.element, PropTypes.object])
  ),
};

FormHeaderParagraphs.defaultProps = {
  intros: [],
};
