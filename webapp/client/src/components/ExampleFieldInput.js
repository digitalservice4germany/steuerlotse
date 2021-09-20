import React from "react";
import PropTypes from "prop-types";

function ExampleFieldInput({ exampleInput, fieldId }) {
  return (
    // TODO: styled-components
    <div className="example-input" htmlFor={fieldId}>
      {exampleInput}
    </div>
  );
}

ExampleFieldInput.propTypes = {
  exampleInput: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
};

export default ExampleFieldInput;
