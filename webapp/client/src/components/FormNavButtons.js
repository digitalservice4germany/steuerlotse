import PropTypes from "prop-types";
import styled from "styled-components";

const Row = styled.div`
  margin-top: var(--spacing-09);
`;

// TODO: tidy this up (turn into a proper Button component as per Nadine's designs?)
const Button = styled.button`
  padding: 1rem 1.25rem calc(1rem - 4px) 1.25rem;

  font-size: var(--text-base);
  letter-spacing: var(--tracking-wide);
  text-decoration: none;
  color: var(--inverse-text-color);
  background: var(--link-color);
  display: inline-block;
  position: relative;
  border: none;
  border-radius: 0;
  border-bottom: 4px solid var(--link-color);

  &:not(:disabled):not(.disabled):active {
    background: var(--link-color) !important;
    border: none !important;
    border-bottom: 4px solid var(--link-color) !important;
  }

  &:hover {
    background: var(--link-hover-color);
    border: none;
    border-bottom: 4px solid var(--link-hover-color);
  }

  &:focus {
    color: var(--focus-text-color);

    background: var(--focus-color);

    outline: none;
    box-shadow: none;
    border: 0;
    border-bottom: 4px solid var(--focus-border-color);
  }
`;

const OutlineButton = styled.button`
  padding: 1rem 1.25rem calc(1rem - 4px) 1.25rem; /* The calculation subtracts the border-bottom height. We need a border-bottom for the focus state. */

  font-weight: var(--font-bold);
  letter-spacing: var(--tracking-wide);
  text-decoration: none;
  color: var(--link-color);

  background: white;
  background-clip: padding-box;

  border: 0;
  border-radius: 0;
  border: 1px solid var(--border-color);

  :not(:disabled):not(.disabled):active {
    color: var(--link-active-color);
    background-color: inherit;
    border: 1px solid var(--link-active-color);
  }

  :hover {
    color: var(--link-hover-color);
    background: white;
    border: 1px solid var(--link-hover-color);
  }

  :focus {
    color: var(--focus-color);

    outline: none;
    box-shadow: none;
    border: 1px solid var(--focus-border-color);
  }
`;

const ExplanatoryText = styled.small`
  margin-bottom: 0;
  margin-left: var(--spacing-02);

  & a {
    color: var(--text-color);
    font-weight: var(--font-bold);
  }
`;

export default function FormNavButtons({
  explanatoryButtonText,
  overviewButton,
  nextButtonLabel,
}) {
  // TODO intl
  const backToOverviewText = "form.back_to_overview";
  // TODO intl
  nextButtonLabel = nextButtonLabel || "form.next";

  return (
    <Row className="form-row">
      {overviewButton && (
        <OutlineButton
          type="submit"
          className="btn mr-2"
          name="overview_button"
        >
          {backToOverviewText}
        </OutlineButton>
      )}

      <Button type="submit" className="btn btn-primary" name="next_button">
        {nextButtonLabel}
      </Button>

      {explanatoryButtonText && (
        // The one (!) place this is being used contains HTML tags, so we need to render as unsafe HTML.
        <ExplanatoryText
          dangerouslySetInnerHTML={{ __html: explanatoryButtonText }}
        ></ExplanatoryText>
      )}
    </Row>
  );
}

FormNavButtons.propTypes = {
  nextButtonLabel: PropTypes.string,
  overviewButton: PropTypes.bool,
  explanatoryButtonText: PropTypes.string,
};
