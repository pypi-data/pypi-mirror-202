export default {
  title: "Streamsync",
  description:
    "Create data apps using a drag-and-drop UI editor, while retaining the full power of Python in the backend.",
  themeConfig: {
    logo: "/logo.svg",
    nav: [
      { text: "Guide", link: "/guide" },
      { text: "Configs", link: "/configs" },
      { text: "Changelog", link: "https://github.com/..." },
    ],
    sidebar: [
      {
        text: "Guide",
        items: [
          { text: "Introduction", link: "/introduction" },
          { text: "Getting started", link: "/getting-started" },
          { text: "Builder basics", link: "/builder-basics" },
          { text: "Components", link: "/components" },
          { text: "Application state", link: "/application-state" },
          { text: "Event handlers", link: "/event-handlers" },
          { text: "Run and share", link: "/run-and-share" },
        ],
      },
      {
        text: "Advanced",
        items: [
          { text: "Routing", link: "/routing" },
          { text: "Custom server", link: "/custom-server" },
        ],
      },
    ],
  },
};
