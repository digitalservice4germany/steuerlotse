import React from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";

const Hint = styled.span`
  font-size: var(--text-medium);
  font-weight: var(--font-normal);
`;

function OptionalHint() {
  const { t } = useTranslation();

  return <Hint>{t("form.optional")}</Hint>;
}

OptionalHint.propTypes = {};

export default OptionalHint;
