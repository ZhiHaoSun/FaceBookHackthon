var profileEditApp = angular.module('profileEditApp', []);


profileEditApp.config(['$httpProvider', '$interpolateProvider',
    function($httpProvider, $interpolateProvider) {
    /* for compatibility with django teplate engine */
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
    /* csrf */
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
}]);


var uploader = new qq.FileUploader({
    element: document.getElementById('file-uploader'),
    action: vars.photoUploadUrl,
    allowedExtensions: ['jpg', 'jpeg', 'png', 'gif'],
    sizeLimit: 4194304,
    multiple: false,
    template: '<div class="qq-uploader">' +
        '<div class="qq-upload-drop-area"><span>Drop files here to upload</span></div>' +
        '<div class="qq-upload-button pure-button">Add photo</div>' +
        '<div class="qq-uploads-wrap"><ul class="qq-upload-list"></ul></div>' +
    '</div>',
    onComplete: function(id, fileName, responseJson) {
        var scope = angular.element(document.getElementById('file-uploader')).scope();
        scope.$apply(function(){
            scope.data.photos.push({url: responseJson.url});
        });
    },
});


profileEditApp.controller('profileEditCtrl', function ($scope, $http) {
    $scope.data = {success: false};

    /* get profile data list */
    $http({method: 'GET', url: vars.profileUrl}).
    success(function(data, status, headers, config) {
        $scope.data.name = data['name'];
        $scope.data.photos = data['photos']
    })

    $scope.updateProfile = function() {
        $http({method: 'PATCH', url: vars.profileUrl, data: {
            name: $scope.data['name']}}).
        success(function(data, status, headers, config) {
            $scope.data['success'] = true;
        }).
        error(function(data, status, headers, config) {
            $scope.data['success'] = false;
        });
    }
});