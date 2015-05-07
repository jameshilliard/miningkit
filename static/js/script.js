var app = angular.module('miningkit', [])

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.controller('DevicesController', function($scope, $http) {
    $scope.devices = null;
    $scope.selectedTab = 0;

    $scope.selectTab = function(index) {
        $scope.selectedTab = index;
    };

    function update() {
        $http.get('/devs.json').success(function(data) {
            $scope.devices = data.devices;
        });
    }

    update();
    setInterval(update, 5000);
});
