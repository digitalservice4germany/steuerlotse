import styled from "styled-components";
import PropTypes from "prop-types";
import ButtonAnchor from "./ButtonAnchor";
import SecondaryAnchorButton from "./SecondaryAnchorButton";

const Box = styled.div`
  background-color: var(--beige-200);
  padding-top: var(--spacing-09);
  padding-bottom: var(--spacing-09);
  margin-top: var(--spacing-11);
`;
const InnerBox = styled.div`
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  margin: 0 auto;
  max-width: var(--pages-max-width);

  @media (min-width: 768px) {
    display: grid;
    grid-template-columns: 1fr 0.5fr 0.5fr 1fr;
    grid-template-rows: 1fr;
  }

  @media (min-width: 769px) {
    margin: 0 auto;
    padding-left: var(--spacing-06);
    padding-right: var(--spacing-06);
  }

  @media (min-width: 1025px) {
    padding-left: var(--spacing-08);
    padding-right: var(--spacing-08);
    grid-gap: 1rem;
  }
`;

const TextBox = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  @media (min-width: 768px) {
    grid-column: 1 / 4;
    grid-row: 1;
  }

  @media (min-width: 1224px) {
    grid-column: 1 / 3;
  }
`;

const ButtonBox = styled.div`
  display: flex;

  @media (max-width: 576px) {
    flex-direction: column;
  }
`;

const BoxText = styled.span`
  padding-bottom: var(--spacing-06);
`;

export default function ContentPageBox({ boxText, anchor, plausibleDomain }) {
  return (
    <Box>
      <InnerBox>
        <TextBox>
          <BoxText>{boxText.headerOne}</BoxText>
          <ButtonAnchor
            url={anchor.eligibility.url}
            plausibleGoal={anchor.eligibility.plausibleGoal}
            plausibleDomain={plausibleDomain}
          >
            {anchor.eligibility.text}
          </ButtonAnchor>
          <BoxText className="mt-5">{boxText.headerTwo}</BoxText>
          <ButtonBox>
            <SecondaryAnchorButton
              url={anchor.faq.url}
              plausibleGoal={anchor.faq.plausibleGoal}
              text={anchor.faq.text}
              plausibleDomain={plausibleDomain}
            />
            <SecondaryAnchorButton
              url={anchor.contact.url}
              plausibleGoal={anchor.contact.plausibleGoal}
              text={anchor.contact.text}
              plausibleDomain={plausibleDomain}
              className="mt-4 mt-md-0"
            />
          </ButtonBox>
        </TextBox>
      </InnerBox>
    </Box>
  );
}

ContentPageBox.propTypes = {
  boxText: {
    headerOne: PropTypes.string,
    headerTwo: PropTypes.string,
  },
  plausibleDomain: PropTypes.string,
  anchor: {
    url: PropTypes.string,
    text: PropTypes.string,
    plausibleGoal: PropTypes.string,
  },
};

ContentPageBox.defaultProps = {
  boxText: {
    headerOne: null,
    headerTwo: null,
  },
  plausibleDomain: null,
  anchor: {
    url: null,
    text: null,
    plausibleGoal: null,
  },
};
