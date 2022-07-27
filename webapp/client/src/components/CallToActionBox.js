import styled from "styled-components";
import PropTypes from "prop-types";
import ButtonAnchor from "./ButtonAnchor";
import { Headline2 } from "./ContentPagesGeneralStyling";

const Box = styled.div`
  padding: 60px 0px 90px 0px;
  background-color: ${(props) =>
    props.colorVariant ? "var(--beige-100)" : "var(--beige-200)"};
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-height: 274px;
`;

const Row = styled.div`
  display: flex;

  & .left-button {
    margin-right: var(--spacing-05);

    @media (max-width: 767px) {
      margin-bottom: var(--spacing-03);
      margin-right: 0;
    }
  }

  @media (max-width: 767px) {
    flex-direction: column;
    align-items: center;
  }
`;

export default function CallToActionBox({
  headline,
  anchor,
  plausibleDomain,
  plausibleGoal,
  variant,
  buttonText,
  colorVariant,
  multipleButtons,
  plausibleProps,
  firstButtonText,
  firstButtonUrl,
  firstButtonPlausibleGoal,
  firstButtonPlausibleProps,
  secondButtonText,
  secondButtonUrl,
  secondButtonPlausibleProps,
  secondButtonPlausibleGoal,
}) {
  return !multipleButtons ? (
    <Box colorVariant={colorVariant}>
      <Headline2 marginVariant paddingVariant>
        {headline}
      </Headline2>
      <ButtonAnchor
        variant={variant}
        url={anchor}
        plausibleGoal={plausibleGoal}
        plausibleDomain={plausibleDomain}
        plausibleProps={plausibleProps}
      >
        {buttonText}
      </ButtonAnchor>
    </Box>
  ) : (
    <Box colorVariant={colorVariant}>
      <Headline2 marginVariant paddingVariant>
        {headline}
      </Headline2>
      <Row>
        <ButtonAnchor
          url={firstButtonUrl}
          plausibleGoal={firstButtonPlausibleGoal}
          plausibleDomain={plausibleDomain}
          plausibleProps={firstButtonPlausibleProps}
          className="left-button"
        >
          {firstButtonText}
        </ButtonAnchor>
        <ButtonAnchor
          variant={variant}
          url={secondButtonUrl}
          plausibleGoal={secondButtonPlausibleGoal}
          plausibleDomain={plausibleDomain}
          plausibleProps={secondButtonPlausibleProps}
        >
          {secondButtonText}
        </ButtonAnchor>
      </Row>
    </Box>
  );
}

CallToActionBox.propTypes = {
  headline: PropTypes.string,
  anchor: PropTypes.shape({
    url: PropTypes.string,
    text: PropTypes.string,
  }),
  plausibleDomain: PropTypes.string,
  plausibleGoal: PropTypes.string,
  variant: PropTypes.string,
  buttonText: PropTypes.string,
  colorVariant: PropTypes.string,
  multipleButtons: PropTypes.bool,
  firstButtonText: PropTypes.string,
  secondButtonText: PropTypes.string,
  secondButtonUrl: PropTypes.string,
  firstButtonUrl: PropTypes.string,
  firstButtonPlausibleGoal: PropTypes.string,
  firstButtonPlausibleProps: PropTypes.string,
  secondButtonPlausibleGoal: PropTypes.string,
  secondButtonPlausibleProps: PropTypes.string,
  plausibleProps: PropTypes.shape({ method: PropTypes.string }),
};

CallToActionBox.defaultProps = {
  headline: null,
  anchor: null,
  plausibleDomain: null,
  plausibleGoal: null,
  variant: null,
  buttonText: null,
  colorVariant: null,
  multipleButtons: false,
  firstButtonText: null,
  secondButtonText: null,
  secondButtonUrl: null,
  firstButtonUrl: null,
  secondButtonPlausibleGoal: null,
  firstButtonPlausibleGoal: null,
  firstButtonPlausibleProps: null,
  secondButtonPlausibleProps: null,
  plausibleProps: null,
};
