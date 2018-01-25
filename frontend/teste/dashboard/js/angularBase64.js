/**
 * Angular Module provided to deal with Base64 (relies on modern browsers).
 *
 * @author Xelita (http://github.com/xelita)
 */
var base64Module = angular.module('base64Module', []);

// Services

/**
 * Main service of the module.
 */
base64Module.factory('base64Service', ['$log', '$window', function ($log, $window) {

    return {
        /**
         * Encode the given parameter to Base64 (relies on modern browsers).
         * @param param the parameter to encode
         * @return the encoded parameter
         */
        encode: function (param) {
            $log.debug('base64Service.encode.');
            return $window.btoa(unescape(encodeURIComponent(param)));
        },

        /**
         * Decode the given parameter from Base64 (relies on modern browsers).
         * @param param the parameter to decode
         * @return the decoded parameter
         */
        decode: function (param) {
            $log.debug('base64Service.decode.');
            return decodeURIComponent(escape($window.atob(param)));
        }
    };
}]);