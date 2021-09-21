// TODO: get rid of bootstrap (or use react-bootstrap, reactstrap, etc.)
import "bootstrap"; // For the data-toggle=collapse functionality
import React from "react";
import PropTypes from "prop-types";

function Details({ children, title, detailsId }) {
  const outerDivId = `details-${detailsId}`;
  const detailsBodyId = `details-body-${detailsId}`;
  const headingId = `heading-${detailsId}`;
  return (
    // TODO: styled-components
    <div id={outerDivId} className="details-card ml-0 pl-0">
      <div className="card">
        <div className="card-header unstyled-card-header d-sm-flex justify-content-between align-items-center cursor-pointer mb-0">
          <div
            className="collapsed w-100"
            id={headingId}
            data-toggle="collapse"
            data-target={`#${detailsBodyId}`}
            role="button"
            aria-expanded="false"
            aria-controls={detailsBodyId}
          >
            <div className="row details-row">
              <button
                className="btn details-icon control-show-more"
                type="button"
                tabIndex="-1"
                aria-hidden="true"
              />
              <button
                className="btn details-icon control-show-less"
                type="button"
                tabIndex="-1"
                aria-hidden="true"
              />
              <button className="btn" type="button">
                <span className="mb-0">{title}</span>
              </button>
            </div>
          </div>
        </div>
        <div
          id={detailsBodyId}
          className="collapse"
          aria-labelledby={headingId}
          data-parent={`#${outerDivId}`}
        >
          <div className="card-body container pt-0">
            <div className="details-row row">
              <div className="block-quote-line" />
              <div className="details-content">
                {children.paragraphs.map((paragraph, index) => (
                  // There is no natural key and the list is completely static, so using the index is fine.
                  // eslint-disable-next-line
                  <p key={index}>{paragraph}</p>
                ))}
                {children.listItems && (
                  <ul>
                    {children.listItems.map((listItem, index) => (
                      // There is no natural key and the list is completely static, so using the index is fine.
                      // eslint-disable-next-line
                      <li key={index} className="mb-2">
                        {listItem}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

Details.propTypes = {
  children: PropTypes.exact({
    paragraphs: PropTypes.arrayOf(PropTypes.node),
    listItems: PropTypes.arrayOf(PropTypes.node),
  }).isRequired,
  title: PropTypes.string.isRequired,
  detailsId: PropTypes.string.isRequired,
};

export default Details;
