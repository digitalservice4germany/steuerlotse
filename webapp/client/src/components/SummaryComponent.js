import React from "react";
import styled from "styled-components";
// import { propTypes } from "react-bootstrap/esm/Image";

const Box = styled.div``;
const LabelBox = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 0 0 var(--spacing-02);
`;
const ValueBox = styled.div`
  display: flex;
  justify-content: space-between;
  border: 1px solid var(--border-color);
  padding: var(--spacing-04);
  background-color: var(--white);
`;

const BoxText = styled.h3`
  font-size: var(--text-medium-big);
  margin: 0;
`;

const ValueText = styled.h5`
  font-size: var(--text-medium);
  font-weight: 400;
`;

const Column = styled.div`
  display: flex;
  flex-direction: column;
  flex-basis: 100%;
  flex: 1;
`;

export default function SummaryComponent() {
  return (
    <Box>
      <LabelBox>
        <BoxText>Angabe zu weiteren Einkünften</BoxText>
        <BoxText>Andern</BoxText>
      </LabelBox>
      <ValueBox>
        <Column>
          <BoxText>Keine weiteren Einkünfte vorhanden:</BoxText>
        </Column>
        <Column>
          <ValueText>Ja</ValueText>
        </Column>
      </ValueBox>
    </Box>
  );
}

SummaryComponent.propTypes = {
  //   stepLabel: propTypes.string.isRequired,
};

SummaryComponent.defaultProps = {};
