import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import translations from "./translations";

i18n.use(initReactI18next).init({
  resources: {
    de: {
      translation: translations,
    },
  },
  lng: "de",
  fallbackLng: "de",

  interpolation: {
    escapeValue: false, // react already safes from xss => https://www.i18next.com/translation-function/interpolation#unescape
  },
});

export default i18n;
