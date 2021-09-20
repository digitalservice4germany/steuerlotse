import styled from "styled-components";

const FormRowCentered = styled.div`
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  margin-top: var(--spacing-03);
  /* This moved the border further outside to allow for the children to fill that space with margin,
  allowing the children to have space between them. See the bootstrap row/column technique. */
  margin-left: calc(-1 * var(--spacing-02));
  margin-right: calc(-1 * var(--spacing-02));

  & > * {
    margin: 0 var(--spacing-02);
  }

  /* TODO: adapt to make sure this keeps working when adding grouped fields component */
  .grouped-input-fields > & {
    margin-top: 0;
  }
`;

export default FormRowCentered;
