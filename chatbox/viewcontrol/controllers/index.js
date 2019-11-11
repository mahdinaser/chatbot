var myApp = angular.module('myApp', []);


console.log('Start of index.js');
myApp.controller('AppCtrl', ['$scope', '$http', function ($scope, $http) {
    console.log("Start controllers, index.js");

    $scope.chatbox_list = []; //used to save chat
    let welc = `Hi, I’m Robo. I'm programmed to help you with questions about this site. What would you like to ask me?`
    $scope.chatbox_list.push({ who: 'r', mention: welc });
    var myscroll_down = function () {
        var objDiv = document.getElementById("chatbox_div");
        console.log('values, objDiv=', objDiv.scrollHeight, objDiv.scrollTop, objDiv.clientHeight);
        objDiv.scrollTop += objDiv.scrollHeight;
        console.log('objDiv.scrollTop', objDiv.scrollTop);
    };


    //Run when start of website and when refresh data from chat API
    var refresh = function () {
        // scroll_down();
        console.log("Start refresh()");
        //
        $scope.customer_question = '';
        document.getElementById("customer_question").focus();
        // myscroll_down();
        setTimeout(function () {
            //do what you need here
            myscroll_down();
        }, 50);


    };
    console.log("start controller index.js :)");
    refresh();

    //header link for more... and less...
    $scope.sendQuestion = function () {
        q = $scope.customer_question;
        $scope.chatbox_list.push({ who: 'c', mention: q });
        // myscroll_down();

        console.log('$scope.chatbox_list', $scope.chatbox_list)
        console.log('Your question is:', q);

        $http.get('/chatbox/sendquestion/' + q + '/')
            // .success(function (response) {
            .then(function (response) {
                console.log("got the data");
                console.log("response", response, "<<<<<");
                var rep = response.data;
                $scope.chatbox_list.push({ who: 'r', mention: rep });
                // myscroll_down();
                refresh();
                //code before the pause
            } //$http.get('/chatbox/sendquestion/').success(function(response)
                , function (error) {
                    console.log(error.message);
                    refresh();
                });
    };

    $scope.sendQuestionByEnterKey = function ($event) {
        //alert('swipe');
        var keyCode = $event.which || $event.keyCode;
        console.log("Q=" + $scope.customer_question + ",keyCode=" + keyCode);
        if (keyCode === 13) {
            //call $scope.sendQuestion
            $scope.sendQuestion();



        }//if
    };//$scope.sendQuestionByEnterKey
}]);