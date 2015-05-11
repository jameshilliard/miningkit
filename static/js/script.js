var app = angular.module('miningkit', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.controller('SummaryController', function($scope, $http) {
    $scope.summary = {};

    function update() {
        $http.get('/summary.json').success(function(data) {
            $scope.summary = data.summary;
        });
    }

    update();
    setInterval(update, 5000);
});

app.controller('DevicesController', function($scope, $http) {
    $scope.devices = [];
    $scope.selectedTab = 0;

    $scope.selectTab = function(index) {
        $scope.selectedTab = index;
    };

    function update() {
        $http.get('/devices.json').success(function(data) {
            $scope.devices = data.devices;
            if (data.devices.length < $scope.selectedTab + 1) {
                $scope.selectedTab = 0;
            }
        });
    }

    update();
    setInterval(update, 5000);
});
