import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import styled, { css, keyframes } from "styled-components";
import ClipLoader from "react-spinners/ClipLoader";
import ButtonAnchor from "./ButtonAnchor";
import addPlausibleGoal from "../lib/helpers";
import { waitingMomentMessagePropType } from "../lib/propTypes";
import { ReactComponent as VectorRight } from "../assets/icons/vector.svg";

const { Text, Icon } = ButtonAnchor;

const ButtonAnchorStyled = styled(ButtonAnchor)`
  font-size: var(--text-base);
  margin-right: var(--spacing-05);
`;

const Row = styled.div`
  margin-top: var(--spacing-09);
  display: flex;
  flex-wrap: wrap;
  row-gap: var(--spacing-05);
`;

const ClipLoaderWithStyle = styled(ClipLoader)`
  margin-right: var(--spacing-03);
`;

// TODO: tidy this up (turn into a proper Button component as per Nadine's designs?)
const sharedButtonLinkStyle = css`
  padding: 1rem 1.25rem calc(1rem - 4px) 1.25rem;
  margin-right: var(--spacing-05);
  font-size: var(--text-base);
  font-family: var(--font-bold);
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
// eslint-disable-next-line no-unused-vars
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
  ${sharedButtonLinkStyle};

  padding: 1rem 1.25rem calc(1rem - 4px) 1.25rem; /* The calculation subtracts the border-bottom height. We need a border-bottom for the focus state. */

  font-family: var(--font-bold);
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
    border: 0;
    border-bottom: 4px solid var(--focus-border-color);
  }
`;

const OutlineButton = styled.button`
  padding: 1rem 1.25rem calc(1rem - 4px) 1.25rem; /* The calculation subtracts the border-bottom height. We need a border-bottom for the focus state. */

  font-family: var(--font-bold);
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
    font-family: var(--font-bold);
  }
`;

const fadeInAndOutAnimation = keyframes`
  0% {
    opacity: 0;
  }
  5% {
    opacity: 1;
  }
  95% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
`;

const fadeInAndOutAnimationSecond = keyframes`
  0% {
    opacity: 0;
  }
  1.82% {
    opacity: 1;
  }
  98.28% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
`;

const ExplanatoryTextSpinner = styled.small`
  margin-bottom: 0;
  font-size: var(--text-medium);
  animation-name: ${fadeInAndOutAnimation};
  animation-duration: 10s;
  -webkit-animation: ${fadeInAndOutAnimation} 10s;
`;

const ExplanatoryTextSpinnerSecond = styled.small`
  margin-bottom: 0;
  font-size: var(--text-medium);
  display: none;
  visibility: hidden;
  animation-name: ${fadeInAndOutAnimationSecond};
  animation-duration: 110s;
  -webkit-animation: ${fadeInAndOutAnimationSecond} 110s;
`;

const HiddenAriaDiv = styled.div`
  position: absolute !important;
  display: block;
  visibility: visible;
  overflow: hidden;
  width: 1px;
  height: 1px;
  margin: -1px;
  border: 0;
  padding: 0;
  clip: rect(0 0 0 0);
`;

export default function StepNavButtons({
  explanatoryButtonText,
  showOverviewButton,
  overviewUrl,
  nextButtonLabel,
  nextUrl,
  isForm,
  plausibleGoal,
  plausibleDomain,
  plausibleProps,
  loading,
  waitingMessages,
}) {
  const { t } = useTranslation();
  const overviewLabel = t("form.backToOverview");
  const nextLabel = nextButtonLabel || t("form.next");
  const handleClick = () => {
    addPlausibleGoal(plausibleDomain, plausibleGoal, { props: plausibleProps });
  };
  // eslint-disable-next-line no-unused-vars
  function announceChange(message) {
    const ariaLiveContainer = document.querySelector("[aria-live]");
    ariaLiveContainer.appendChild(document.createTextNode(message));
  }
  if (loading) {
    announceChange(waitingMessages.firstMessage);
    const interval = setInterval(() => {
      const firstMessage = document.getElementById("firstMessage");
      const secondMessage = document.getElementById("secondMessage");
      firstMessage.style.display = "none";
      firstMessage.style.visibility = "none";
      secondMessage.style.display = "block";
      secondMessage.style.visibility = "visible";
      announceChange(waitingMessages.secondMessage);
      clearInterval(interval);
    }, 10000);
  }

  return (
    <Row className="form-row">
      {isForm && showOverviewButton && (
        <OutlineButton
          type="submit"
          className="btn mr-2"
          name="overview_button"
          onClick={handleClick}
        >
          {overviewLabel}
        </OutlineButton>
      )}

      {!isForm && showOverviewButton && (
        <OutlineLink
          href={overviewUrl}
          className="btn mr-2"
          name="overview_link"
          onClick={handleClick}
        >
          {overviewLabel}
        </OutlineLink>
      )}

      {isForm && !waitingMessages && (
        <Button type="submit" className="btn btn-primary" name="next_button">
          {nextLabel}
        </Button>
      )}

      {isForm && !loading && waitingMessages && (
        <ButtonAnchorStyled type="submit" name="next_button">
          <Text>{nextLabel}</Text>
          <Icon hoverVariant="translate-x">
            <VectorRight />
          </Icon>
        </ButtonAnchorStyled>
      )}
      {!isForm && nextUrl && (
        <Link href={nextUrl} className="btn btn-primary" name="next_button">
          {nextLabel}
        </Link>
      )}

      {explanatoryButtonText && !loading && (
        <ExplanatoryText>{explanatoryButtonText}</ExplanatoryText>
      )}

      {loading && <ClipLoaderWithStyle color="#0B0C0C" size="30px" />}
      {loading && (
        <div>
          <ExplanatoryTextSpinner id="firstMessage">
            {waitingMessages.firstMessage}
          </ExplanatoryTextSpinner>
          <ExplanatoryTextSpinnerSecond id="secondMessage">
            {waitingMessages.secondMessage}
          </ExplanatoryTextSpinnerSecond>
        </div>
      )}
      <HiddenAriaDiv aria-live="assertive" />
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
  plausibleGoal: PropTypes.string,
  plausibleProps: PropTypes.shape({ method: PropTypes.string }),
  plausibleDomain: PropTypes.string,
  loading: PropTypes.bool,
  waitingMessages: waitingMomentMessagePropType,
};

StepNavButtons.defaultProps = {
  nextButtonLabel: undefined,
  showOverviewButton: false,
  overviewUrl: undefined,
  explanatoryButtonText: undefined,
  nextUrl: undefined,
  isForm: true,
  plausibleGoal: "Zurück zur Übersicht",
  plausibleProps: undefined,
  plausibleDomain: null,
  loading: false,
  waitingMessages: undefined,
};
