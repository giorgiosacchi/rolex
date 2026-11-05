// Rolex Live · classical and JB edition
'use strict';
const CACHE='rolex-live-dual-jb-v13';
const ASSETS=['./','./index.html','./manifest.webmanifest','./assets/rolex.png','./assets/jb.webp','./assets/crown-classic.png','./assets/crown-back-classic.png','./assets/crown-jb.png','./assets/crown-back-jb.png','./icons/icon-192.png','./icons/icon-512.png','./icons/icon-maskable-512.png','./icons/apple-touch-icon.png'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(ASSETS)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(Promise.all([
  caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('rolex-live-')&&key!==CACHE).map(key=>caches.delete(key)))),
  self.clients.claim()
])));
self.addEventListener('fetch',event=>{
 const request=event.request;
 if(request.method!=='GET'||new URL(request.url).origin!==self.location.origin)return;
 if(request.mode==='navigate'){
  event.respondWith(fetch(request).then(response=>{
    if(response.ok){const copy=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(request,copy)))}
    return response;
  }).catch(()=>caches.match(request).then(hit=>hit||caches.match('./index.html'))));
  return;
 }
 event.respondWith(caches.match(request).then(hit=>hit||fetch(request)));
});
