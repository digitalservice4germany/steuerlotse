import PropTypes from "prop-types";
import styled from "styled-components";

const FailureAlertArea = styled.div`
  margin-top: var(--spacing-11);

  &.alert {
    border-radius: 0;
    border: 0;
    padding: var(--spacing-05);
  }

  &.alert-danger {
    background-color: var(--error-color);
    color: var(--inverse-text-color);
  }

  @media (max-width: 1024px) {
    margin-top: var(--spacing-05);
  }
`;

const Intro = styled.p`
  font-size: var(--text-medium);
`;

export default function FormFailureHeader({ title, intro, hideIntro }) {
  return (
    <>
      <FailureAlertArea className="alert alert-danger" role="alert">
        <h1>{title}</h1>
      </FailureAlertArea>
      {intro && !hideIntro && <Intro>{intro}</Intro>}
    </>
  );
}

FormFailureHeader.propTypes = {
  title: PropTypes.string.isRequired,
  intro: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
  hideIntro: PropTypes.bool,
};

FormFailureHeader.defaultProps = {
  intro: undefined,
  hideIntro: false,
};
