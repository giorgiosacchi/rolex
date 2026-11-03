/* Rolex Live PWA - offline shell v2 */
'use strict';
const CACHE='rolex-live-offline-v2';
const ASSETS=['./','./index.html','./manifest.webmanifest','./assets/rolex.png','./icons/icon-192.png','./icons/icon-512.png','./icons/icon-maskable-512.png','./icons/apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(Promise.all([caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('rolex-live-offline-')&&k!==CACHE).map(k=>caches.delete(k)))),self.clients.claim()]))});
self.addEventListener('fetch',e=>{const req=e.request;if(req.method!=='GET'||new URL(req.url).origin!==self.location.origin)return;
if(req.mode==='navigate'){e.respondWith(fetch(req).then(r=>{if(r.ok){const clone=r.clone();e.waitUntil(caches.open(CACHE).then(c=>c.put(req,clone)))}return r}).catch(()=>caches.match(req).then(hit=>hit||caches.match('./index.html'))));return}
e.respondWith(caches.match(req).then(hit=>hit||fetch(req)))
});
