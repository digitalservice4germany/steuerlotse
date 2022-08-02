import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import BackLink from "./BackLink";

export default function StepHeaderButtons({ url, text, disable }) {
  const { t } = useTranslation();

  const linkText = text || t("form.back");

  let content = null;

  if (url) {
    content = (
      <div className="header-navigation">
        <div className="mt-3">
          <BackLink disable={disable} text={linkText} url={url} />
        </div>
      </div>
    );
  }

  return content;
}

StepHeaderButtons.propTypes = {
  url: PropTypes.string,
  text: PropTypes.string,
  disable: PropTypes.bool,
};

StepHeaderButtons.defaultProps = {
  url: undefined,
  text: undefined,
  disable: false,
};
