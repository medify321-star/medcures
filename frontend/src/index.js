import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

// COMPREHENSIVE SERVICE WORKER & CACHE CLEANUP
console.log("🔄 Starting comprehensive cache cleanup...");

// 1. Unregister ALL service workers
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.getRegistrations().then((registrations) => {
    console.log(`Found ${registrations.length} service worker(s), unregistering all...`);
    registrations.forEach((registration) => {
      if (registration.uninstall) registration.uninstall();
      registration.unregister().then(() => {
        console.log("✓ Service worker unregistered");
      });
    });
  }).catch((err) => console.error("Error unregistering SW:", err));
}

// 2. Clear IndexedDB (where workbox caches data)
if ("indexedDB" in window) {
  try {
    if (window.indexedDB.databases) {
      window.indexedDB.databases().then((dbs) => {
        dbs.forEach((db) => {
          if (db.name && db.name.includes("workbox")) {
            window.indexedDB.deleteDatabase(db.name);
            console.log(`✓ Deleted IndexedDB: ${db.name}`);
          }
        });
      });
    }
  } catch (e) { console.log("IndexedDB cleanup skipped"); }
}

// 3. Clear Cache API storage
if ("caches" in window) {
  caches.keys().then((cacheNames) => {
    cacheNames.forEach((cacheName) => {
      caches.delete(cacheName).then(() => {
        console.log(`✓ Deleted cache: ${cacheName}`);
      });
    });
  });
}

// 4. Clear LocalStorage and SessionStorage
try {
  localStorage.clear();
  sessionStorage.clear();
  console.log("✓ Cleared LocalStorage and SessionStorage");
} catch (e) { console.log("Storage clear skipped"); }

// 5. Force hard reload on first visit to clear stale content
if (!window.sessionStorage.getItem("hasReloaded")) {
  window.sessionStorage.setItem("hasReloaded", "true");
  setTimeout(() => {
    window.location.reload(true); // true = bypass cache
  }, 500);
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
