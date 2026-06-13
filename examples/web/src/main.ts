import "./style.css";
import { greet, isOnline } from "./greet";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) {
  throw new Error("App root element not found");
}
const root = app;

function render(): void {
  const online = isOnline();
  root.innerHTML = `
    <main>
      <h1>${greet("FOSS")}</h1>
      <p class="status" data-testid="status">
        ${online ? "Online" : "Offline"} - Golden Path PWA stub
      </p>
    </main>
  `;
}

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
