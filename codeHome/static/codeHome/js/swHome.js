const CACHE_STATIC_NAME     = 'staticHome-v1';
const CACHE_DYNAMIC_NAME    = 'dynamicHome-v1';
const CACHE_INMUTABLE_NAME  = 'inmutableHome-v1';
const CACHE_DYNAMIC_LIMIT   = 50;

const listadoCache = [
    /* CSS Inmutables */
    "/static/codeHome/css/bootstrap.min.css",
    "/static/codeHome/css/elegant-icons.css",
    "/static/codeHome/css/flaticon.css",
    "/static/codeHome/css/owl.carousel.min.css",
    "/static/codeHome/css/slicknav.min.css",
    "/static/codeHome/css/style.css",

    /* JS Inmutables */
    "/static/codeHome/js/jquery-3.3.1.min.js",
    "/static/codeHome/js/bootstrap.min.js",
    "/static/codeHome/js/jquery.slicknav.js",
    "/static/codeHome/js/owl.carousel.min.js",
    "/static/codeHome/js/main.js",

    /* Fuentes Inmutables */
    "https://fonts.googleapis.com/css?family=Montserrat:400,500,600,700,800,900&display=swap",
    "https://fonts.gstatic.com/s/montserrat/v15/JTUSjIg1_i6t8kCHKm459Wlhyw.woff2",
    "https://fonts.gstatic.com/s/montserrat/v15/JTURjIg1_i6t8kCHKm45_ZpC3gnD_g.woff2",
    "https://fonts.gstatic.com/s/montserrat/v15/JTURjIg1_i6t8kCHKm45_dJE3gnD_g.woff2",
    "https://ka-f.fontawesome.com/releases/v5.15.3/webfonts/free-fa-solid-900.woff2",
    "https://ka-f.fontawesome.com/releases/v5.15.3/webfonts/free-fa-regular-400.woff2",
    "https://ka-f.fontawesome.com/releases/v5.15.3/webfonts/free-fa-solid-900.woff2",
    "https://ka-f.fontawesome.com/releases/v5.15.3/css/free-v4-font-face.min.css?token=0265b153d4",
    "https://ka-f.fontawesome.com/releases/v5.15.3/css/free-v4-shims.min.css?token=0265b153d4",

    /* CSS static */

    /* JS static */
    "https://kit.fontawesome.com/0265b153d4.js",

    /* Img static */
    "/static/codeHome/img/favicon.png",
    "/static/codeHome/img/logoHorizontal.png",
    "/static/codeHome/img/logo.png",
    "/static/codeHome/img/svg/check.svg",
    "/static/codeHome/img/svg/cancel.svg",
    "/static/codeHome/img/line.png",
    "/static/codeHome/img/footer-bg.png",
    "/static/codeHome/img/hero/hero-1.jpg",
    "/static/codeHome/img/assets/faq.jpg",
    "/static/codeHome/img/assets/fotografia.png",
    "/static/codeHome/img/assets/productos.png",
    "/static/codeHome/img/assets/chef.png",
    "/static/codeHome/img/assets/emprendedor.jpg",
    
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