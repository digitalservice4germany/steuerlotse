import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import ExampleFieldInput from "./ExampleFieldInput";
import HelpModal from "./HelpModal";
import Details from "./Details";
import OptionalHint from "./OptionalHint";

export default function FieldLabelScaffolding({
  render,
  fieldId,
  label,
  details,
  disable,
}) {
  // Only show label if there is text to show.
  if (!label.text) {
    return null;
  }

  const labelClassNames = classNames("text-input-field-label", {
    "field-label": !label.exampleInput,
    "field-label-example": label.exampleInput,
  });
  return (
    <>
      {/* This content goes _inside_ the label / legend. */}
      {render(
        <>
          {label.text}
          {label.showOptionalTag && <OptionalHint />}
          {label.help && <HelpModal title={label.text} body={label.help} />}
        </>,
        labelClassNames
      )}
      {/* This content becomes a _sibling_ of the label / legend. */}
      {label.exampleInput && (
        <ExampleFieldInput {...{ exampleInput: label.exampleInput, fieldId }} />
      )}
      {details && !details.positionAfterField && (
        <Details disable={disable} title={details.title} detailsId={fieldId}>
          <p>{details.text}</p>
        </Details>
      )}
    </>
  );
}

FieldLabelScaffolding.propTypes = {
  render: PropTypes.func.isRequired,
  fieldId: PropTypes.string.isRequired,
  label: PropTypes.exact({
    text: PropTypes.string,
    showOptionalTag: PropTypes.bool,
    help: PropTypes.string, // field.render_kw['help']
    exampleInput: PropTypes.string, // field.render_kw["example_input"]
  }),
  details: PropTypes.exact({
    title: PropTypes.string,
    text: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
    positionAfterField: PropTypes.bool, // False unless using 'form_full_width' template (which some pages do)
  }),
  disable: PropTypes.bool,
};

FieldLabelScaffolding.defaultProps = {
  label: {
    text: undefined,
    showOptionalTag: false,
    help: undefined,
    exampleInput: undefined,
  },
  details: undefined,
  disable: false,
};
