import PropTypes from "prop-types";
import styled from "styled-components";
import BackLink from "./BackLink";

const HeaderNavigation = styled.div`
  height: var(--header-navigation-height);
  margin-bottom: var(--spacing-09);

  @media (max-width: 1024px) {
    height: auto;
    padding-bottom: var(--spacing-02);
    margin-bottom: 0;
  }
`;

export default function StepHeaderButtons({ backLinkUrl, backLinkText }) {
  return (
    <HeaderNavigation>
      {backLinkUrl && (
        <div className="mt-3">
          <BackLink text={backLinkText} url={backLinkUrl} />
        </div>
      )}
    </HeaderNavigation>
  );
}

StepHeaderButtons.propTypes = {
  backLinkUrl: PropTypes.string,
  backLinkText: PropTypes.string,
};
