ckan.module('tweaks-toogle-tooltip', function ($, _) {
    'use strict';
    if (typeof bootstrap === "undefined") {
        $('[data-toggle="tooltip"]').tooltip();
    } else {
        // bye-bye, jQuery
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(
            el => new bootstrap.Tooltip(el)
        );
    }
});