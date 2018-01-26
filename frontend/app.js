var app = angular.module('myApp',['ngRoute','basicAuthModule']);

app.controller('MyController', function($scope,$http,basicAuthService) {

var ApiUrl = "http://127.0.0.1:5000/api/";

$scope.alo="buceta";

$scope.showurl = function(url){
    $scope.template_url = url;
};

$scope.redirect = function(url){
    window.location = url;
};


$scope.Login = function() {
  localStorage.username = $scope.username;
  localStorage.password  = $scope.password;
  //if $scope.showurl('login.html');
 console.log($scope.username);
 console.log($scope.password);
   var authData = {username: $scope.username, password: $scope.password};
   var successCB = function(response) {
       // Work with extra data coming from the remote server
       //$scope.generatedKey = response.data.generatedKey;
      $scope.template_url = "user-panel.html";
      $scope.alo="BUCETAO";

     // alert('ok');
   };
   var failureCB = function(error) {
      $scope.showurl('login.html');

   };
   var x = ApiUrl + "login";
   basicAuthService.login(x , authData, successCB, failureCB);
};

//$scope.Login();



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


});

