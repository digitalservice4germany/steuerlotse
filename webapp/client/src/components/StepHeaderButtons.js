import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import BackLink from "./BackLink";

const HeaderNavigation = styled.div`
  position: absolute;
  top: var(--spacing-05);
`;

export default function StepHeaderButtons({ url, text }) {
  const { t } = useTranslation();

  const linkText = text || t("form.back");

  return (
    <HeaderNavigation>
      {url && (
        <div className="mt-3">
          <BackLink text={linkText} url={url} />
        </div>
      )}
    </HeaderNavigation>
  );
}

StepHeaderButtons.propTypes = {
  url: PropTypes.string,
  text: PropTypes.string,
};

StepHeaderButtons.defaultProps = {
  url: undefined,
  text: undefined,
};
