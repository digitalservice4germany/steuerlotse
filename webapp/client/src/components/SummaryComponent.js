import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";

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

const BoxText = styled.p`
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

const ValueText = styled.p`
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

export default function SummaryComponent({ data, label, url }) {
  const { t } = useTranslation();

  const mapping =
    data &&
    data.map((item) => (
      <Wrapper key={item.name}>
        <Column>
          <BoxText>{item.name}</BoxText>
        </Column>
        <Column>
          <ValueText>{item.value}</ValueText>
        </Column>
      </Wrapper>
    ));

  return (
    <Box>
      <LabelBox>
        <BoxLabelText>{label}</BoxLabelText>
        <BoxLink
          href={url}
          aria-label={`${label} ${t("lotse.summary.changeAlt")}`}
        >
          {t("lotse.summary.change")}
        </BoxLink>
      </LabelBox>
      <ValueBox>{mapping}</ValueBox>
    </Box>
  );
}

SummaryComponent.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string,
      value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    })
  ).isRequired,
  label: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
};
