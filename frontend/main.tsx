import "./styles/app.css";

import React from "react";
import { createInertiaApp } from "@inertiajs/react";
import { createRoot } from "react-dom/client";

createInertiaApp({
  title: (title) => (title ? `${title} | Open DJ6` : "Open DJ6"),
  resolve: async (name) => {
    const pages = import.meta.glob<{ default: React.ComponentType<any> }>("./pages/**/*.tsx");
    const importPage = pages[`./pages/${name}.tsx`];

    if (!importPage) {
      throw new Error(`Page not found: ${name}`);
    }

    const page = await importPage();
    return page.default;
  },
  setup({ el, App, props }) {
    createRoot(el).render(
      <React.StrictMode>
        <App {...props} />
      </React.StrictMode>,
    );
  },
});
