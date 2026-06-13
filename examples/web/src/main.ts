import "./style.css";
import { createThemeToggle } from "./components/ThemeToggle";
import { isOnline } from "./greet";
import { t } from "./i18n";
import { initTheme } from "./theme";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) {
  throw new Error("App root element not found");
}
const root = app;

function render(): void {
  const online = isOnline();
  const statusKey = online ? "app.status.online" : "app.status.offline";

  root.innerHTML = `
    <main>
      <div class="gp-header">
        <h1 class="gp-title">${t("app.title")}</h1>
      </div>
      <p class="gp-headline">${t("app.greeting")}</p>
      <p class="gp-body" data-testid="status">${t(statusKey)}</p>
    </main>
  `;

  const header = root.querySelector<HTMLDivElement>(".gp-header");
  if (header) {
    header.appendChild(createThemeToggle());
  }
}

initTheme();
render();
window.addEventListener("online", render);
window.addEventListener("offline", render);

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {
      // Service worker registration may fail in dev; acceptable for stub
    });
  });
}
