import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

// SILENT CACHE CLEANUP - No reloading, just cleanup
(() => {
  // 1. Unregister ALL service workers (non-blocking)
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.getRegistrations()
      .then((registrations) => {
        registrations.forEach((registration) => {
          registration.unregister().catch(() => {});
        });
      })
      .catch(() => {});
  }

  // 2. Clear Cache API (non-blocking)
  if ("caches" in window) {
    caches.keys()
      .then((cacheNames) => {
        cacheNames.forEach((cacheName) => {
          caches.delete(cacheName).catch(() => {});
        });
      })
      .catch(() => {});
  }

  // 3. Clear IndexedDB (non-blocking)
  if ("indexedDB" in window) {
    try {
      if (window.indexedDB.databases) {
        window.indexedDB.databases()
          .then((dbs) => {
            dbs.forEach((db) => {
              if (db.name) {
                window.indexedDB.deleteDatabase(db.name).catch(() => {});
              }
            });
          })
          .catch(() => {});
      }
    } catch (e) {}
  }

  // 4. Clear storage
  try {
    localStorage.clear();
    sessionStorage.clear();
  } catch (e) {}
})();

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
