const CACHE_STATIC_NAME     = 'staticBaseTheme-v1';
const CACHE_DYNAMIC_NAME    = 'dynamicBaseTheme-v1';
const CACHE_INMUTABLE_NAME  = 'inmutableBaseTheme-v1';
const CACHE_DYNAMIC_LIMIT   = 50;

const listadoCache = [
    /* CSS Inmutables */
    "/static/codeFrontEnd/assets/libs/jquery-ui/jquery-ui.css",
    "/static/codeFrontEnd/assets/libs/bootstrap-datepicker/bootstrap-datepicker.css",
    "/static/codeFrontEnd/assets/libs/fancybox/jquery.fancybox.min.css",
    "/static/codeFrontEnd/assets/libs/aos/aos.css",
    "/static/codeFrontEnd/assets/libs/selling/style.css",
    "/static/codeFrontEnd/assets/rexy/style.css",
    "/static/codeFrontEnd/assets/libs/fonts/flaticon/font/flaticon.css",
    "/static/codeFrontEnd/assets/libs/fonts/icomoon/style.css",

    /* JS Inmutables */
    "/static/codeFrontEnd/assets/libs/jquery-ui/jquery-ui.js",
    "/static/codeFrontEnd/assets/libs/stellar/jquery.stellar.min.js",
    "/static/codeFrontEnd/assets/libs/countdown/jquery.countdown.min.js",
    "/static/codeFrontEnd/assets/libs/bootstrap-datepicker/bootstrap-datepicker.min.js",
    "/static/codeFrontEnd/assets/libs/aos/aos.js",
    "/static/codeFrontEnd/assets/libs/fancybox/jquery.fancybox.min.js",
    "/static/codeFrontEnd/assets/libs/easing/jquery.easing.1.3.js",
    "/static/codeFrontEnd/assets/libs/selling/main.js",
    "https://kit.fontawesome.com/0265b153d4.js",

    /* Fuentes Inmutables */
    "/static/codeFrontEnd/assets/libs/fonts/icomoon/fonts/icomoon.ttf?10si43",

    /* CSS static */

    /* JS static */

    /* Img static */

];

self.addEventListener('install', e => {
    const cache_inmutable = caches.open(CACHE_INMUTABLE_NAME)
    .then(appCache => {
        return appCache.addAll(listadoCache)
    });

    e.waitUntil(Promise.all([cache_inmutable]))
    self.skipWaiting()
});

self.addEventListener('fetch', e => {
    /* 
        Cache with Network Fallback
        primero se fija en la cache sino va a internet
    */
    const respuesta = caches.match(e.request)
    .then( res => {
        if(res) return res

        /* no existe el archivo y va a la web */
        console.log(`No existe ${e.request.url}`)

        return fetch( e.request ).then(newResp => {

            /* caches.open(CACHE_DYNAMIC_NAME).then(appCache => {
                appCache.put(e.request, newResp)
                limpiarCache(CACHE_DYNAMIC_NAME, CACHE_DYNAMIC_LIMIT)
            }) */
            return newResp.clone()
        })
    })
    e.respondWith( respuesta )
});