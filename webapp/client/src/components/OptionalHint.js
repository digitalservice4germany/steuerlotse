import React from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";

const Hint = styled.span`
  margin-left: var(--spacing-01);
  font-size: var(--text-medium);
`;

function OptionalHint() {
  const { t } = useTranslation();

  return <Hint>{t("form.optional")}</Hint>;
}

OptionalHint.propTypes = {};

export default OptionalHint;
