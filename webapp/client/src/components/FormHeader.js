import PropTypes from "prop-types";
import styled from "styled-components";

const Intro = styled.p`
  font-size: var(--text-medium);
`;

export default function FormHeader({ title, intro, hideIntro }) {
  return (
    <div>
      <h1 className="my-4">{title}</h1>
      {intro && !hideIntro && <Intro>{intro}</Intro>}
    </div>
  );
}

FormHeader.propTypes = {
  title: PropTypes.string.isRequired,
  intro: PropTypes.string,
  hideIntro: PropTypes.bool,
};

FormHeader.defaultProps = {
  intro: undefined,
  hideIntro: false,
};
