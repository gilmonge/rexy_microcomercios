const CACHE_STATIC_NAME     = 'staticmalefashion-v1';
const CACHE_DYNAMIC_NAME    = 'dynamicmalefashion-v1';
const CACHE_INMUTABLE_NAME  = 'inmutablemalefashion-v1';
const CACHE_DYNAMIC_LIMIT   = 50;

const listadoCache = [
    /* CSS Inmutables */
    "/static/codeFrontEnd/themes/malefashion/css/bootstrap.min.css",
    "/static/codeFrontEnd/themes/malefashion/css/elegant-icons.css",
    "/static/codeFrontEnd/themes/malefashion/css/magnific-popup.css",
    "/static/codeFrontEnd/themes/malefashion/css/nice-select.css",
    "/static/codeFrontEnd/themes/malefashion/css/slicknav.min.css",
    "/static/codeFrontEnd/themes/malefashion/css/style.css",
    "/static/codeFrontEnd/themes/malefashion/css/owl.carousel.min.css",

    /* JS Inmutables */
    "/static/codeFrontEnd/themes/malefashion/js/jquery-3.3.1.min.js",
    "/static/codeFrontEnd/themes/malefashion/js/bootstrap.min.js",
    "/static/codeFrontEnd/themes/malefashion/js/jquery.nice-select.min.js",
    "/static/codeFrontEnd/themes/malefashion/js/jquery.nicescroll.min.js",
    "/static/codeFrontEnd/themes/malefashion/js/jquery.countdown.min.js",
    "/static/codeFrontEnd/themes/malefashion/js/jquery.magnific-popup.min.js",
    "/static/codeFrontEnd/themes/malefashion/js/jquery.slicknav.js",
    "/static/codeFrontEnd/themes/malefashion/js/owl.carousel.min.js",
    "/static/codeFrontEnd/themes/malefashion/js/mixitup.min.js",
    "/static/codeFrontEnd/themes/malefashion/js/main.js",
    "/static/codeFrontEnd/themes/malefashion/js/swmalefashion.js",

    /* Fuentes Inmutables */
    "/static/codeFrontEnd/themes/malefashion/fonts/ElegantIcons.woff",

    /* CSS static */

    /* JS static */

    /* Img static */
    "/static/codeFrontEnd/themes/malefashion/img/icon/search.png",

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