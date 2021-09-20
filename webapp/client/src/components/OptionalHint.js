import React from "react";
import styled from "styled-components";

const Hint = styled.span`
  font-size: var(--text-medium);
  font-weight: var(--font-normal);
`;

function OptionalHint() {
  return (
    // TODO: intl
    <Hint>form.optional</Hint>
  );
}

OptionalHint.propTypes = {};

export default OptionalHint;
