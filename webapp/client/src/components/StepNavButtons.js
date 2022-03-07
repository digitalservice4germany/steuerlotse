import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import styled, { css } from "styled-components";

const Row = styled.div`
  margin-top: var(--spacing-09);
  display: flex;
  flex-wrap: wrap;
  row-gap: var(--spacing-05);
`;

// TODO: tidy this up (turn into a proper Button component as per Nadine's designs?)
const sharedButtonLinkStyle = css`
  padding: 1rem 1.25rem calc(1rem - 4px) 1.25rem;
  margin-right: var(--spacing-05);
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

  :focus {
    background-color: var(--link-color);
    border-bottom: 4px solid var(--link-color);
  }

  &:focus-visible {
    color: var(--focus-text-color);
    background-color: var(--focus-color);
    outline: none;
    box-shadow: none;
    border: 0;
    border-bottom: 4px solid var(--focus-border-color);
  }
`;

const Button = styled.button`
  ${sharedButtonLinkStyle}
`;

const Link = styled.a`
  ${sharedButtonLinkStyle}

  &:visited {
    color: var(--inverse-text-color);
  }
`;

const OutlineLink = styled.a`
  ${sharedButtonLinkStyle}

  padding: 1rem 1.25rem calc(1rem - 4px) 1.25rem; /* The calculation subtracts the border-bottom height. We need a border-bottom for the focus state. */

  font-weight: var(--font-bold);
  letter-spacing: var(--tracking-wide);
  text-decoration: none;

  color: var(--link-color);

  background-color: var(--bg-white);
  background-clip: padding-box;
  border: 1px solid var(--border-color);

  &:visited {
    color: var(--link-color);
  }

  :not(:disabled):not(.disabled):active {
    color: var(--link-active-color);
    border: 1px solid var(--link-active-color);
  }

  :hover {
    color: var(--link-hover-color);
    background-color: var(--bg-white);
    border: 1px solid var(--link-hover-color);
  }

  :focus-visible {
    color: var(--focus-color);

    outline: none;
    box-shadow: none;
    border: 1px solid var(--focus-border-color);
  }
`;

const OutlineButton = styled.button`
  padding: 1rem 1.25rem calc(1rem - 4px) 1.25rem; /* The calculation subtracts the border-bottom height. We need a border-bottom for the focus state. */

  font-weight: var(--font-bold);
  letter-spacing: var(--tracking-wide);
  text-decoration: none;
  color: var(--link-color);

  background-color: var(--bg-white);
  background-clip: padding-box;

  border-radius: 0;
  border: 1px solid var(--border-color);

  :not(:disabled):not(.disabled):active {
    color: var(--link-active-color);
    background-color: inherit;
    border: 1px solid var(--link-active-color);
  }

  :hover {
    color: var(--link-hover-color);
    background-color: var(--bg-white);
    border: 1px solid var(--link-hover-color);
  }

  :focus-visible {
    color: var(--focus-text-color);
    background-color: var(--focus-color);
    outline: none;
    box-shadow: none;
    border: 0;
    border-bottom: 4px solid var(--focus-border-color);
  }
`;

const ExplanatoryText = styled.small`
  margin-bottom: 0;

  & a {
    color: var(--text-color);
    font-weight: var(--font-bold);
  }
`;

export default function StepNavButtons({
  explanatoryButtonText,
  showOverviewButton,
  overviewUrl,
  nextButtonLabel,
  nextUrl,
  isForm,
}) {
  const { t } = useTranslation();

  const overviewLabel = t("form.backToOverview");
  const nextLabel = nextButtonLabel || t("form.next");

  return (
    <Row className="form-row">
      {isForm && showOverviewButton && (
        <OutlineButton
          type="submit"
          className="btn mr-2"
          name="overview_button"
        >
          {overviewLabel}
        </OutlineButton>
      )}

      {!isForm && showOverviewButton && (
        <OutlineLink
          href={overviewUrl}
          className="btn mr-2"
          name="overview_link"
        >
          {overviewLabel}
        </OutlineLink>
      )}

      {isForm && (
        <Button type="submit" className="btn btn-primary" name="next_button">
          {nextLabel}
        </Button>
      )}
      {!isForm && nextUrl && (
        <Link href={nextUrl} className="btn btn-primary" name="next_button">
          {nextLabel}
        </Link>
      )}

      {explanatoryButtonText && (
        <ExplanatoryText>{explanatoryButtonText}</ExplanatoryText>
      )}
    </Row>
  );
}

StepNavButtons.propTypes = {
  nextButtonLabel: PropTypes.string,
  showOverviewButton: PropTypes.bool,
  overviewUrl: PropTypes.string,
  explanatoryButtonText: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.element,
  ]),
  nextUrl: PropTypes.string,
  isForm: PropTypes.bool,
};

StepNavButtons.defaultProps = {
  nextButtonLabel: undefined,
  showOverviewButton: false,
  overviewUrl: undefined,
  explanatoryButtonText: undefined,
  nextUrl: undefined,
  isForm: true,
};
