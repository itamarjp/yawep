var app = angular.module('myApp',['ngRoute','basicAuthModule']);

app.controller('MyController', function($scope,$http,basicAuthService) {

var ApiUrl = "http://127.0.0.1:5000/api/";

$scope.showurl = function(url){
    $scope.template = url;
    if (url==0){this.getUsers();}
    if (url==1){this.getDomains();}
    if (url==2){this.getEmails();}
    if (url==3){this.getDatabases();}
    if (url==4){this.getFTP();}
    if (url==5){
    this.getDomains();
    
    }
    
};

$scope.Logged = 0;

$scope.Login = function() {
  localStorage.username = $scope.username;
  localStorage.password = $scope.password;
 console.log($scope.username);
 console.log($scope.password);
   var authData = {username: $scope.username, password: $scope.password};
   var successCB = function(response) {
      $scope.Logged = 1;
      $scope.template = 'login'
   };
   var failureCB = function(error) {
      $scope.Logged = 0;
      $scope.template = 'login'
   };
   var x = ApiUrl + "login";
   basicAuthService.login(x , authData, successCB, failureCB);
};


$scope.Logout = function() {
  localStorage.username = "";
  localStorage.password = "";
  $scope.username ="";
  $scope.password ="";
  $scope.Logged = 0;
  $scope.template = -1;
};


  $scope.getDomains = function () {  
     $http.get(ApiUrl + "domains" ).then(function (response) {$scope.domains = response.data;});
     console.log($scope.domains);
  };

  $scope.selectDomain = function (domain,template) {
     alert(domain.name);
     $scope.selectedDomain=domain;
     $scope.template=template;
     console.log(domain.name);
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


  $scope.getDatabases = function () {  
     $http.get(ApiUrl + "databases" ).then(function (response) {$scope.databases = response.data;});
     console.log($scope.databases);
  };

    $scope.editDatabase = function (id) {
          $http.get(ApiUrl + "databases/" + id ).then(function (response) {$scope.newdb = response.data;});
    };


    $scope.deleteDatabase = function (id) {
        $http.delete(ApiUrl + "databases/" + id ).then(function (response) {$scope.newdb = {};$scope.getDatabases();});
    };

    $scope.saveDatabase = function () {
         console.log($scope.newdb);
            if ($scope.newdb.id === null) {  
             $http.post(ApiUrl + "databases",$scope.newdb.id).then(function (response) {$scope.newdb = {};$scope.getDatabases();});
         } else {
            $http.put(ApiUrl + "databases/" + $scope.newdb.id ,$scope.newdb).then(function (response) {$scope.newdb = {};$scope.getDatabases();});
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
1    };

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

    $scope.editUser = function (id) {
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



  $scope.getFTP = function () {  
     $http.get(ApiUrl + "ftpaccounts" ).then(function (response) {$scope.ftpaccounts = response.data;});
  };

    $scope.editFTP = function (id) {
          $http.get(ApiUrl + "ftpaccounts/" + id ).then(function (response) {$scope.newftp = response.data;});
    };


    $scope.deleteFTP = function (id) {
        $http.delete(ApiUrl + "ftpaccounts/" + id ).then(function (response) {$scope.newftp = {};$scope.getFTP();});
    };

    $scope.saveUser = function () {
         console.log($scope.ftpaccounts);
            if ($scope.newftp.id === null) {  
             $http.post(ApiUrl + "ftpaccounts",$scope.newftp).then(function (response) {$scope.newuser = {};$scope.getFTP();});                      
         } else {
            $http.put(ApiUrl + "ftpaccounts/" + $scope.newftp.id ,$scope.newftp).then(function (response) {$scope.newftp = {};$scope.getFTP();});
            }
        };

});
