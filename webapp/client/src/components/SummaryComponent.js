import React from "react";
import styled from "styled-components";
// import PropTypes from "prop-types";

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
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  border: 1px solid var(--border-color);
  padding: var(--spacing-04);
  padding-top: 0.5rem;
  background-color: var(--white);
`;

const BoxText = styled.h3`
  font-size: var(--text-medium-big);
  margin: 0;
  font-weight: 700;
  padding: 0 15px;
`;

const BoxLabelText = styled(BoxText)`
  padding: 0;
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
`;

const Column = styled.div`
  display: flex;
  flex-direction: column;
  flex-basis: 100%;
`;

const Wrapper = styled.div`
  display: flex;
  flex-direction: row;
  margin-top: var(--spacing-04);
`;

export default function SummaryComponent({ data }) {
  const mapping =
    data.data &&
    Object.entries(data.data).map(([key, value]) => (
      <Wrapper>
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
  data: {},
};

SummaryComponent.defaultProps = {
  data: null,
};
