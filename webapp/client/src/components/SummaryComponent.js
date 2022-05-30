import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";

const Box = styled.div`
  margin-bottom: var(--spacing-05);
`;
const LabelBox = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 0 0 var(--spacing-02);
`;
const ValueBox = styled.div`
  border: 1px solid var(--border-color);
  padding: var(--spacing-02);
  padding-top: 0;
  background-color: var(--white);
`;

const BoxText = styled.h3`
  font-size: var(--text-medium);
  margin: 0;
  font-weight: 700;
  padding: 0 15px 0 10px;
`;

const BoxLabelText = styled(BoxText)`
  padding: 0;
  font-size: var(--text-medium-big);
`;

const BoxLink = styled.a`
  font-size: var(--text-medium-big);
  margin: 0;
  text-decoration: none;

  &:visited {
    text-decoration-color: var(--link-visited-color);
    color: var(--link-visited-color);
  }
`;

const ValueText = styled.h5`
  font-size: var(--text-medium);
  font-weight: 400;
  margin: 0;
`;

const Column = styled.div`
  display: flex;
  flex-direction: column;
  flex-basis: 100%;
  margin-top: var(--spacing-04);
`;

const Wrapper = styled.div`
  display: flex;
  flex-direction: row;
  margin-top: 0;
  margin-bottom: var(--spacing-02);
`;

export default function SummaryComponent({ data }) {
  const mapping =
    data.data &&
    Object.entries(data.data).map(([key, value]) => (
      <Wrapper key={key}>
        <Column>
          <BoxText>{key}</BoxText>
        </Column>
        <Column>
          <ValueText>{value}</ValueText>
        </Column>
      </Wrapper>
    ));

  return (
    <Box>
      <LabelBox>
        <BoxLabelText>{data.label}</BoxLabelText>
        <BoxLink href={data.url}>Ändern</BoxLink>
      </LabelBox>
      <ValueBox>{mapping}</ValueBox>
    </Box>
  );
}

SummaryComponent.propTypes = {
  data: {
    decl_incomes: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    decl_edaten: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    familienstand: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    steuernummer: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    person_a: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    has_disability_person_a: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    merkzeichen_person_a: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    person_a_requests_pauschbetrag: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    steuperson_a_requests_fahrtkostenpauschaleernummer: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    person_b: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    has_disability_person_b: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    merkzeichen_person_b: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    person_b_requests_pauschbetrag: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
    iban: {
      data: {},
      label: PropTypes.string,
      url: PropTypes.string,
    },
  },
};

SummaryComponent.defaultProps = {
  data: null,
};
