import PropTypes from "prop-types";
import React from "react";
import styled from "styled-components";
import Details from "./Details";

const DetailsDiv = styled.div`
  margin-bottom: var(--spacing-04);

  @media (max-width: 500px) {
    margin-bottom: 0;
  }
`;

function DetailsSeparated({ children, title, detailsId }) {
  return (
    <DetailsDiv>
      <Details title={title} detailsId={detailsId}>
        {children}
      </Details>
    </DetailsDiv>
  );
}

DetailsSeparated.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]).isRequired,
  title: PropTypes.string.isRequired,
  detailsId: PropTypes.string.isRequired,
};

export default DetailsSeparated;
