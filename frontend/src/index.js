import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
// Ensure Tailwind CDN is loaded in the browser at runtime (dev fallback)
if (typeof window !== 'undefined' && !window.tailwind && !document.querySelector('script[src="https://cdn.tailwindcss.com"]')) {
  const tailwindScript = document.createElement('script');
  tailwindScript.src = 'https://cdn.tailwindcss.com';
  tailwindScript.async = false;
  document.head.appendChild(tailwindScript);
}

console.log('bundle executing');
try {
  const rootEl = document.getElementById("root");
  if (rootEl) rootEl.dataset.bundle = 'loaded';
  const root = ReactDOM.createRoot(rootEl);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  );
} catch (err) {
  // show a visible error so users without console can see it
  console.error(err);
  document.body.innerHTML = `<pre style="white-space:pre-wrap;color:#b91c1c;padding:16px">App error: ${err && err.message ? err.message : err}</pre>`;
  throw err;
}
