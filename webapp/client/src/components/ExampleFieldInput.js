import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";

const Example = styled.div`
  &.example-input {
    color: var(--secondary-text-color);
    margin-bottom: var(--spacing-02);
  }
`;
function ExampleFieldInput({ exampleInput, fieldId }) {
  return (
    <Example className="example-input" htmlFor={fieldId}>
      {exampleInput}
    </Example>
  );
}

ExampleFieldInput.propTypes = {
  exampleInput: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
};

export default ExampleFieldInput;
