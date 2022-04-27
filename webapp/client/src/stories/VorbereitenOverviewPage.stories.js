import React from "react";
import VorbereitenOverviewPage from "../pages/VorbereitenOverviewPage";

export default {
  title: "Pages/VorbereitenOverviewPage",
  component: VorbereitenOverviewPage,
};

function Template(args) {
  return <VorbereitenOverviewPage {...args} />;
}

export const Default = Template.bind({});

Default.args = {
  downloadPreparationLink: "/downloadPreparationLink",
  vorsorgeaufwendungenUrl: "/vorsorgeaufwendungenUrl",
  krankheitskostenUrl: "/krankheitskostenUrl",
  pflegekostenUrl: "/pflegekostenUrl",
  angabenBeiBehinderungUrl: "/angabenBeiBehinderungUrl",
  bestattungskostenUrl: "/bestattungskostenUrl",
  wiederbeschaffungskostenUrl: "/wiederbeschaffungskostenUrl",
  haushaltsnaheDienstleistungenUrl: "/haushaltsnaheDienstleistungenUrl",
  handwerkerleistungenUrl: "/handwerkerleistungenUrl",
  spendenUndMitgliedsbeitraegeUrl: "/spendenUndMitgliedsbeitraegeUrl",
  kirchensteuerUrl: "/kirchensteuerUrl",
};
