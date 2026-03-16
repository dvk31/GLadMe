import type { PageProps } from "@inertiajs/core";
import { Head, usePage } from "@inertiajs/react";

type FlashLevel = "success" | "error" | "warning" | "info";

interface SharedUser {
  id: string;
  email: string;
  display_name: string;
}

type SharedPageProps = PageProps & {
  auth: {
    user: SharedUser | null;
  };
  flash: Record<FlashLevel, string | null>;
};

interface ProjectSummary {
  id: string;
  name: string;
  description: string;
  created_at: string;
}

interface HomePageProps {
  siteName: string;
  siteUrl: string;
  openrouterConfigured: boolean;
  defaultModel: string;
  projects: ProjectSummary[];
}

const features = [
  {
    title: "Base models",
    body: "UUID primary keys, timestamps, audit fields, and soft delete without tenant or ACL coupling.",
  },
  {
    title: "Lightweight service contracts",
    body: "A small ABC + Protocol + registry layer that stays easy to understand and extend.",
  },
  {
    title: "OpenRouter gateway",
    body: "A focused sync client for commands and app services, without billing or orchestration baggage.",
  },
];

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export default function HomeIndex({
  siteName,
  siteUrl,
  openrouterConfigured,
  defaultModel,
  projects,
}: HomePageProps) {
  const { auth, flash } = usePage<SharedPageProps>().props;
  const activeFlash = Object.entries(flash).find(([, value]) => value);

  return (
    <>
      <Head title="Starter" />

      <main className="page-shell">
        <section className="hero">
          <p className="eyebrow">Open-source Django starter</p>
          <h1>{siteName}</h1>
          <p className="hero-copy">
            Django, React, Inertia, and a minimal OpenRouter gateway with the heavy platform
            pieces removed.
          </p>

          <div className="hero-meta">
            <span className={`pill ${openrouterConfigured ? "pill--success" : "pill--muted"}`}>
              {openrouterConfigured ? "OpenRouter configured" : "OpenRouter not configured"}
            </span>
            <span className="pill pill--muted">default model: {defaultModel}</span>
            <span className="pill pill--muted">site: {siteUrl}</span>
          </div>

          {auth.user ? (
            <p className="signed-in">Signed in as {auth.user.display_name || auth.user.email}.</p>
          ) : (
            <p className="signed-in">Anonymous session. Shared Inertia auth props are still wired.</p>
          )}

          {activeFlash ? (
            <div className={`flash flash--${activeFlash[0]}`}>{activeFlash[1]}</div>
          ) : null}
        </section>

        <section className="card-grid">
          {features.map((feature) => (
            <article className="card" key={feature.title}>
              <h2>{feature.title}</h2>
              <p>{feature.body}</p>
            </article>
          ))}
        </section>

        <section className="panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Example model</p>
              <h2>Projects</h2>
            </div>
            <code>manage.py ai_chat \"hello\"</code>
          </div>

          {projects.length === 0 ? (
            <p className="empty-state">
              No sample projects yet. Create one in the admin or shell to see the base model in
              action.
            </p>
          ) : (
            <ul className="project-list">
              {projects.map((project) => (
                <li className="project-row" key={project.id}>
                  <div>
                    <h3>{project.name}</h3>
                    <p>{project.description || "No description yet."}</p>
                  </div>
                  <time dateTime={project.created_at}>{formatDate(project.created_at)}</time>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </>
  );
}
