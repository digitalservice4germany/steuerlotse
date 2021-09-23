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
          {label.optional && <OptionalHint />}
          {label.help && <HelpModal title={label.text} body={label.help} />}
        </>,
        labelClassNames
      )}
      {/* This content becomes a _sibling_ of the label / legend. */}
      {label.exampleInput && (
        <ExampleFieldInput {...{ exampleInput: label.exampleInput, fieldId }} />
      )}
      {details && !details.positionAfterField && (
        <Details title={details.title} detailsId={fieldId}>
          {{
            paragraphs: [details.text],
          }}
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
    optional: PropTypes.bool,
    help: PropTypes.string, // field.render_kw['help']
    exampleInput: PropTypes.string, // field.render_kw["example_input"]
  }),
  details: PropTypes.exact({
    title: PropTypes.string,
    text: PropTypes.string,
    positionAfterField: PropTypes.bool, // False unless using 'form_full_width' template (which some pages do)
  }),
};

FieldLabelScaffolding.defaultProps = {
  label: {
    text: undefined,
    optional: false,
    help: undefined,
    exampleInput: undefined,
  },
  details: undefined,
};
