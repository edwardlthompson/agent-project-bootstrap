import { Hono } from "hono";

import { aboutPayload } from "./about.js";
import { buildFeedbackUrl, type FeedbackKind, feedbackRepo } from "./feedback.js";
import { greet } from "./greet.js";
import { loadOpenApiSpec } from "./openapi.js";

export function createApp() {
  const app = new Hono();

  app.get("/openapi.json", (c) => c.json(loadOpenApiSpec()));
  app.get("/health", (c) => c.json({ status: "ok" }));
  app.get("/about", (c) => c.json(aboutPayload()));
  app.get("/feedback", (c) => {
    const kind: FeedbackKind = c.req.query("kind") === "feature" ? "feature" : "bug";
    const title = c.req.query("title") ?? "";
    return c.json({ kind, ...buildFeedbackUrl(feedbackRepo(), kind, title) });
  });

  app.get("/greet/:name?", (c) => {
    const name = c.req.param("name") ?? "";
    return c.json({ message: greet(name) });
  });

  return app;
}
