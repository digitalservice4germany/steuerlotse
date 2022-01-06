import PropTypes from "prop-types";
import styled from "styled-components";

const Intro = styled.p`
  font-size: var(--text-medium);
`;

export default function FormHeaderIntro({ paragraphs }) {
  return (
    <div>
      {paragraphs.map((intro, index) => (
        <Intro key={`intro_${index}`}>{intro}</Intro>
      ))}
    </div>
  );
}

FormHeaderIntro.propTypes = {
  paragraphs: PropTypes.arrayOf(
    PropTypes.oneOfType([PropTypes.string, PropTypes.element, PropTypes.object])
  ),
};

FormHeaderIntro.defaultProps = {
  paragraphs: [],
};
