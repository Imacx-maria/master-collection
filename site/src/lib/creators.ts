export type Creator = {
  slug: string;
  name: string;
  shortName: string;
  title: string;
  location: string;
  initials: string;
  websiteLabel: string;
  websiteUrl: string;
  badges: string[];
  stats: Array<{
    value: string;
    label: string;
  }>;
  bio: string[];
  skills: string[];
  clients: string[];
  roles: Array<{
    title: string;
    company: string;
  }>;
  knownFor: string[];
};

export const creators: Creator[] = [
  {
    slug: "joseph-berry",
    name: "Joe Berry",
    shortName: "Joe",
    title: "Experience Designer",
    location: "London",
    initials: "JB",
    websiteLabel: "jbstudio.co",
    websiteUrl: "https://jbstudio.co",
    badges: [
      "Awwwards Jury 2025",
      "Webflow Professional Partner",
      "Awwwards Site of the Year",
      "Webflow Conf 2023 Speaker",
    ],
    stats: [
      { value: "4", label: "Templates" },
      { value: "£400+", label: "Total value" },
      { value: "12+", label: "Years" },
    ],
    bio: [
      "Hey, I'm Joe. I run JB Studio LDN, a small independent studio out of London making digital experiences for brands, startups, and the occasional ambitious side project. 12+ years deep, ex-Digitas, Awwwards Jury, Webflow Professional Partner. Proper Londoner, proud dad, creative thinker, in that order, mostly.",
      "I work end-to-end: brand, UX/UI, interaction design, and build. Webflow is home, GSAP is the playground. I like sites that move with intent, feel considered, and actually ship.",
    ],
    skills: [
      "Branding",
      "Visual Identity",
      "Art Direction",
      "UX/UI",
      "Web & App Design",
      "Interaction Design",
      "Design Systems",
      "Webflow",
      "Shopify",
    ],
    clients: ["1820", "Cartier", "Redchurch", "Desktronic", "Fates", "Light Factory", "Vergo Bank", "HF-11", "The Flow Party"],
    roles: [
      { title: "Founder & Experience Designer", company: "JB Studio LDN" },
      { title: "Founder & Creative Director", company: "SkinGame Media" },
      { title: "Senior Digital Designer", company: "Digitas (previously)" },
    ],
    knownFor: [
      "Awwwards Site of the Year and Users Choice with 1820",
      "Multiple Sites of the Day",
      "Webflow Conf 2023 speaker",
      "Awwwards Jury 2025",
      "Webflow Professional Partner",
      "Widely cloned community resources including Bark Studio and Dribbble Workshop",
    ],
  },
];

export function getCreatorBySlug(slug: string) {
  return creators.find((creator) => creator.slug === slug);
}
