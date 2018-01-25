/**
 * Angular Module provided to access remote services using basic authentication.
 * This module relies on angular-base64-codec library (http://github.com/xelita/angular-base64) to encode / decode data to / from base64.
 *
 * @author Xelita (http://github.com/xelita)
 */
var basicAuthModule = angular.module('basicAuthModule', ['base64Module']);

// Constants

/**
 * Constants service used in the whole module.
 */
basicAuthModule.constant('basicAuthConstants', {
    basicHeaderPrefix: 'Basic '
});

// Services

/**
 * Main service of the module.
 */
basicAuthModule.factory('basicAuthService', ['$log', '$http', 'base64Service', 'basicAuthConstants', function ($log, $http, base64Service, basicAuthConstants) {

    return {
        /**
         * Generate a basic authorization header based on the given username and password.
         * @param username the user name
         * @param password the user password
         * @return a basic authorization header (eg. 'Basic dGVzdA==')
         */
        generateAuthorizationHeader: function (username, password) {
            $log.debug('basicAuthService.authorizationHeader.');
            var authData = base64Service.encode(username + ':' + password);
            return basicAuthConstants.basicHeaderPrefix + authData;
        },

        /**
         * Perform a login request (POST) to validate user credentials with the backend server.
         * @param url the login url
         * @param authData the authentication data. Must contain at least {username: 'username here', password: 'password here'}
         * @param successCallback the callback invoked in case of a successfull login (optional)
         * @param failureCallback the callback invoked in case of a failed login attempt (optional)
         */
        login: function (url, authData, successCallback, failureCallback) {
            $log.debug('basicAuthService.login.');

            // Compute authorisation header: 'Basic dGVzdA=='
            var authorizationHeader = this.generateAuthorizationHeader(authData.username, authData.password);
            // coloquei a linha abaixo, pois o backend requerer que ja exista a header de basic auth
            $http.defaults.headers.common.Authorization = authorizationHeader;
            // Post the login request to the backend server in order to validate them
//            $http.post(url, authData).then(function (response) { nao envia o authdata
            $http.post(url).then(function (response) {
                // Store authorization header as default authorization header for further queries
                $http.defaults.headers.common.Authorization = authorizationHeader;

                // Delegate response to the caller (afterSuccess hook)
                if (successCallback) {
                    successCallback(authorizationHeader, response);
                }
            }, function (error) {
                // Delegate response to the caller (afterFailure hook)
                if (failureCallback) {
                    failureCallback(error);
                }
            });
        },

        /**
         * Perform a logout request (POST) to the backend server.
         * @param url the logout url
         * @param successCallback the callback invoked in case of a successfull logout (optional)
         * @param failureCallback the callback invoked in case of a failed logout attempt (optional)
         */
        logout: function (url, successCallback, failureCallback) {
            $log.debug('basicAuthService.logout.');

            // Post the logout request to the backend server
            $http.post(url).then(function (response) {
                // Clear authorization header
                $http.defaults.headers.common.Authorization = basicAuthConstants.basicHeaderPrefix;

                // Delegate response to the caller (afterSuccess hook)
                if (successCallback) {
                    successCallback(response);
                }
            }, function (error) {
                // Delegate response to the caller (afterFailure hook)
                if (failureCallback) {
                    failureCallback(error);
                }
            });
        }
    };
}]);
