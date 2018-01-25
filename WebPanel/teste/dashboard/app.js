var app = angular.module('myApp',['ngRoute','basicAuthModule']);




app.controller('MyController', ['$scope', function($scope) {

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
  
  


}]);



app.directive('userPanel', function(){
return {
	restrict: 'E',
	templateUrl: 'user-panel.html' ,
	controller: function(){

	} ,
	controllerAs: 'panels'
	};
});

app.directive('userDomains', function(){
return {
	restrict: 'E',
	templateUrl: 'user-domains.html' ,
	controller: function(){

	} ,
	controllerAs: 'domainsControllerxx'
	};
});

app.directive('userEmails', function(){
return {
	restrict: 'E',
	templateUrl: 'user-emails.html' ,
	controller: function(){

	} ,
	controllerAs: 'emailsControllerxx'
	};
});


app.directive('userLogin', function(){
return {
	restrict: 'E',
	templateUrl: 'login.html' ,
	controller: function(){

	} ,
	controllerAs: 'login'
	};
});

app.directive('userDatabases', function(){
return {
	restrict: 'E',
	templateUrl: 'user-databases.html' ,
	controller: function(){

	} ,
	controllerAs: 'userdatabaes'
	};
});

app.directive('userFtpaccounts', function(){
return {
	restrict: 'E',
	templateUrl: 'user-ftp-accounts.html' ,
	controller: function(){

	} ,
	controllerAs: 'login'
	};
});



app.service('ContactService', function () {
    //to create unique contact id
    var uid = 1;
    
    //contacts array to hold list of all contacts
    var contacts = [{
        id: 0,
        'name': 'Viral',
            'email': 'hello@gmail.com',
            'phone': '123-2343-44'
    }];
    
    //save method create a new contact if not already exists
    //else update the existing object
    this.save = function (contact) {
        if (contact.id == null) {
            //if this is new contact, add it in contacts array
            contact.id = uid++;
            contacts.push(contact);
        } else {
            //for existing contact, find this contact using id
            //and update it.
            for (i in contacts) {
                if (contacts[i].id == contact.id) {
                    contacts[i] = contact;
                }
            }
        }

    }

    //simply search contacts list for given id
    //and returns the contact object if found
    this.get = function (id) {
        for (i in contacts) {
            if (contacts[i].id == id) {
                return contacts[i];
            }
        }

    }
    
    //iterate through contacts list and delete 
    //contact if found
    this.delete = function (id) {
        for (i in contacts) {
            if (contacts[i].id == id) {
                contacts.splice(i, 1);
            }
        }
    }

    //simply returns the contacts list
    this.list = function () {
        return contacts;
    }
});

app.controller('UserController', function ($scope, ContactService) {

    $scope.contacts = ContactService.list();

    $scope.saveContact = function () {
        ContactService.save($scope.newcontact);
        $scope.newcontact = {};
    }


    $scope.delete = function (id) {

        ContactService.delete(id);
        if ($scope.newcontact.id == id) $scope.newcontact = {};
    }


    $scope.edit = function (id) {
        $scope.newcontact = angular.copy(ContactService.get(id));
    }
});

app.config(function($routeProvider){
	$routeProvider.when('/login', {
		controller:'ContactController',
		templateUrl: 'login.html'
	})
	.when('/books', {
		controller:'BooksController',
		templateUrl: 'views/books.html'
	})
	.when('/books/details/:id',{
		controller:'BooksController',
		templateUrl: 'views/book_details.html'
	})
	.when('/books/add',{
		controller:'BooksController',
		templateUrl: 'views/add_book.html'
	})
	.when('/books/edit/:id',{
		controller:'BooksController',
		templateUrl: 'views/edit_book.html'
	})
	.otherwise({
		redirectTo: '/'
	});
});


app.controller('userLoginCtrl', function($scope, $http, basicAuthService) {

$scope.LoginData = {};


   $scope.processLogin = function () {
     console.log('login = ' + $scope.LoginData.username);
	  console.log('password = ' + $scope.LoginData.password);
	  localStorage.username = $scope.LoginData.username;
	  localStorage.password  = $scope.LoginData.password;
   };

});

app.controller('DomainCtrl', function($scope, $http, basicAuthService) {


   var authData = {username: localStorage.username, password: localStorage.password};
   
   var successCB = function(response) {
      		console.log('ok x');
   };
   
   var failureCB = function(error) {
       		console.log('falhou');
   };
   
   basicAuthService.login('http://127.0.0.1:5000/api/login', authData, successCB, failureCB);

  $scope.getDomains = function () {  
     $http.get("http://127.0.0.1:5000/api/domains" ).then(function (response) {$scope.domains = response.data});
     console.log($scope.domains);
  }     
   $scope.getDomains();

   
    $scope.edit = function (id) {
          $http.get("http://127.0.0.1:5000/api/domains/" + id ).then(function (response) {$scope.newdomain = response.data});
    }


    $scope.delete = function (id) {
        $http.delete("http://127.0.0.1:5000/api/domains/" + id ).then(function (response) {$scope.newdomain = {};$scope.getDomains();});
    }

    $scope.saveDomain = function () {
         console.log($scope.newdomain);
			if ($scope.newdomain.id == null) {  
             $http.post("http://127.0.0.1:5000/api/domains",$scope.newdomain).then(function (response) {$scope.newdomain = {};$scope.getDomains();});                      
         } else {
            $http.put("http://127.0.0.1:5000/api/domains/" + $scope.newdomain.id ,$scope.newdomain).then(function (response) {$scope.newdomain = {};$scope.getDomains();});
            }
        }
        
});



app.controller('EmailsCtrl', function($scope, $http, basicAuthService) {

  $scope.emails = {};

   var authData = {username: localStorage.username, password: localStorage.password};
   
   var successCB = function(response) {
      		console.log('ok x');
   };
   
   var failureCB = function(error) {
       		console.log('falhou');
   };
   
   basicAuthService.login('http://127.0.0.1:5000/api/login', authData, successCB, failureCB);

  $scope.getEmails = function () {  
     $http.get("http://127.0.0.1:5000/api/emails" ).then(function (response) {$scope.emails = response.data});
     console.log($scope.emails);
  }     
   $scope.getEmails();

   
    $scope.edit = function (id) {
          $http.get("http://127.0.0.1:5000/api/emails/" + id ).then(function (response) {$scope.newemail = response.data});
    }


    $scope.delete = function (id) {
        $http.delete("http://127.0.0.1:5000/api/emails/" + id ).then(function (response) {$scope.newemail = {};$scope.getEmails();});
    }

    $scope.saveEmail = function () {
         console.log($scope.newemail);
			if ($scope.newemail.id == null) {  
             $http.post("http://127.0.0.1:5000/api/emails",$scope.newemail).then(function (response) {$scope.newemail = {};$scope.getEmails();});                      
         } else {
            $http.put("http://127.0.0.1:5000/api/emails/" + $scope.newemail.id ,$scope.newemail).then(function (response) {$scope.newemail = {};$scope.getEmails();});
            }
        }
        
});



app.controller('customersCtrl', function($scope, $http, basicAuthService) {
//{ headers: {'Authorization': 'Basic eDp4'}}

   var authData = {username: localStorage.username, password: localStorage.password};
   
   var successCB = function(response) {
      		console.log('ok x');
		//console.log($scope.users);
   };
   
   var failureCB = function(error) {
       		console.log('falhou');
   };
   
   basicAuthService.login('http://127.0.0.1:5000/api/login', authData, successCB, failureCB);
     //$http.get("http://127.0.0.1:5000/api/users" ).then(function (response) {$scope.users = response.data});

  $scope.getUsers = function () {  
     $http.get("http://127.0.0.1:5000/api/users" ).then(function (response) {$scope.users = response.data});
  }     
   $scope.getUsers();

   
    $scope.edit = function (id) {
          $http.get("http://127.0.0.1:5000/api/users/" + id ).then(function (response) {$scope.newuser = response.data});
    }


    $scope.delete = function (id) {
        $http.delete("http://127.0.0.1:5000/api/users/" + id ).then(function (response) {$scope.newcontact = {};$scope.getUsers();});
    }

    $scope.saveUser = function () {
         console.log($scope.newuser);
			if ($scope.newuser.id == null) {  
             $http.post("http://127.0.0.1:5000/api/users",$scope.newuser).then(function (response) {$scope.newuser = {};$scope.getUsers();});                      
         } else {
            $http.put("http://127.0.0.1:5000/api/users/" + $scope.newuser.id ,$scope.newuser).then(function (response) {$scope.newuser = {};$scope.getUsers();});
            }
        }
        
});



