var app = angular.module("myApp",["ngRoute","basicAuthModule"]);

app.controller("MyController", ["$scope", function($scope, $http, basicAuthService) {

var ApiUrl = "http://127.0.0.1:5000/api/";

$scope.userPanel = 0;
$scope.userLogin = 0;
$scope.userDomains = 0;
$scope.userEmails = 0; 
$scope.userFtpAccounts = 0;

$scope.showLogin = function() {
    $scope.userLogin = 1;
    $scope.userPanel = 0;
    $scope.userDomains = 0;
    $scope.userEmails = 0;
    $scope.userFtpAccounts = 0;
    $scope.userDatabases = 0;
};

$scope.showUser = function() {
    $scope.userLogin = 0;
    $scope.userPanel = 1;
    $scope.userDomains = 0;
    $scope.userEmails = 0;
    $scope.userFtpAccounts = 0;
    $scope.userDatabases = 0;
};

$scope.showDomains = function() {
    $scope.userLogin = 0;
    $scope.userPanel = 0;
    $scope.userDomains = 1;
    $scope.userEmails = 0;
    $scope.userFtpAccounts = 0;   
    $scope.userDatabases = 0;
};

$scope.showEmails = function() {
    $scope.userLogin = 0;
    $scope.userPanel = 0;
    $scope.userDomains = 0;
    $scope.userEmails = 1;
    $scope.userFtpAccounts = 0;   
    $scope.userDatabases = 0;  
};

$scope.showFtpAccounts = function() {
    $scope.userLogin = 0;
    $scope.userPanel = 0;
    $scope.userDomains = 0;
    $scope.userEmails = 0;
    $scope.userFtpAccounts = 1;
    $scope.userDatabases = 0;   
};
  
$scope.showDatabases = function() {
    $scope.userLogin = 0;
    $scope.userPanel = 0;
    $scope.userDomains = 0;
    $scope.userEmails = 0;
    $scope.userFtpAccounts = 0;
    $scope.userDatabases = 1;   
};



$scope.LoginData = {};


$scope.processLogin = function () {
 console.log("login = " + $scope.LoginData.username);
 console.log("password = " + $scope.LoginData.password);
 localStorage.username = $scope.LoginData.username;
 localStorage.password  = $scope.LoginData.password;
};


   var authData = {username: localStorage.username, password: localStorage.password};
   var successCB = function(response) {
            console.log("ok x");
   };
   var failureCB = function(error) {
            console.log("falhou");
   };
   x = ApiUrl + "login";
   
   //basicAuthService.login(x, authData, successCB, failureCB);

  $scope.getDomains = function () {  
     $http.get(ApiUrl + "domains" ).then(function (response) {$scope.domains = response.data;});
     console.log($scope.domains);
  };     

   
    $scope.editDomain = function (id) {
          $http.get(ApiUrl + "domains/" + id ).then(function (response) {$scope.newdomain = response.data;});
    };


    $scope.deleteDomain = function (id) {
        $http.delete(ApiUrl + "domains/" + id ).then(function (response) {$scope.newdomain = {};$scope.getDomains();});
    };

    $scope.saveDomain = function () {
         console.log($scope.newdomain);
            if ($scope.newdomain.id === null) {  
             $http.post(ApiUrl + "domains",$scope.newdomain).then(function (response) {$scope.newdomain = {};$scope.getDomains();});                      
         } else {
            $http.put(ApiUrl + "domains/" + $scope.newdomain.id ,$scope.newdomain).then(function (response) {$scope.newdomain = {};$scope.getDomains();});
            }
        };
        



  $scope.getEmails = function () {  
     $http.get(ApiUrl + "emails" ).then(function (response) {$scope.emails = response.data;});
     console.log($scope.emails);
  };
    $scope.editEmail = function (id) {
          $http.get(ApiUrl + "emails/" + id ).then(function (response) {$scope.newemail = response.data;});
    };


    $scope.deleteEmail = function (id) {
        $http.delete(ApiUrl + "emails/" + id ).then(function (response) {$scope.newemail = {};$scope.getEmails();});
    };

    $scope.saveEmail = function () {
         console.log($scope.newemail);
    if ($scope.newemail.id === null) {  
             $http.post(ApiUrl + "emails",$scope.newemail).then(function (response) {$scope.newemail = {};$scope.getEmails();});                      
         } else {
            $http.put(ApiUrl + "emails/" + $scope.newemail.id ,$scope.newemail).then(function (response) {$scope.newemail = {};$scope.getEmails();});
            }
        };


  $scope.getUsers = function () {  
     $http.get(ApiUrl + "users" ).then(function (response) {$scope.users = response.data;});
  };

    $scope.editUsers = function (id) {
          $http.get(ApiUrl + "users/" + id ).then(function (response) {$scope.newuser = response.data;});
    };


    $scope.deleteUser = function (id) {
        $http.delete(ApiUrl + "users/" + id ).then(function (response) {$scope.newcontact = {};$scope.getUsers();});
    };

    $scope.saveUser = function () {
         console.log($scope.newuser);
            if ($scope.newuser.id === null) {  
             $http.post(ApiUrl + "users",$scope.newuser).then(function (response) {$scope.newuser = {};$scope.getUsers();});                      
         } else {
            $http.put(ApiUrl + "users/" + $scope.newuser.id ,$scope.newuser).then(function (response) {$scope.newuser = {};$scope.getUsers();});
            }
        };
        


app.directive("userPanel", function(){
return {
    restrict: "E",
    templateUrl: "user-panel.html"
    };
});

app.directive("userDomains", function(){
return {
    restrict: "E",
    templateUrl: "user-domains.html" ,
    controllerAs: "MyController"
    };
});

app.directive("userEmails", function(){
return {
    restrict: "E",
    templateUrl: "user-emails.html" ,
    };
});


app.directive("userLogin", function(){
return {
    restrict: "E",
    templateUrl: "login.htm" ,
    };
});

app.directive("userDatabases", function(){
return {
    restrict: "E",
    templateUrl: "user-databases.html" ,
    };
});

app.directive("userFtpaccounts", function(){
return {
    restrict: "E",
    templateUrl: "user-ftp-accounts.html" ,
    };
});

app.config(function($routeProvider){
    $routeProvider.when("/login", {
        controller:"ContactController",
        templateUrl: "login.html"
    })
    .when("/books", {
        controller:"BooksController",
        templateUrl: "views/books.html"
    })
    .when("/books/details/:id",{
        controller:"BooksController",
        templateUrl: "views/book_details.html"
    })
    .when("/books/add",{
        controller:"BooksController",
        templateUrl: "views/add_book.html"
    })
    .when("/books/edit/:id",{
        controller:"BooksController",
        templateUrl: "views/edit_book.html"
    })
    .otherwise({
        redirectTo: "/"
    });
});


}]);

