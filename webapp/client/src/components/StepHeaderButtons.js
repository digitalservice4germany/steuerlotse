import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
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
  // render_info.prev_url
  url: PropTypes.string,
  // render_info.back_link_text if render_info.back_link_text else _('form.back')
  text: PropTypes.string,
};

StepHeaderButtons.defaultProps = {
  url: undefined,
  text: undefined,
};
