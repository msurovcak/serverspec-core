"use strict";

var reportResultsApp = angular.module("reportResultsApp", ['ui.bootstrap']);


// We use this service to pass data between upoadCtrl and reportResultCtrl
reportResultsApp.factory("ResultData", function() {
    var current = null;
    return {
        "save": function(data) { current = data; return current; },
        "fetch": function() { return current }
    };
});

reportResultsApp.controller("uploadCtrl", [ "$scope", "$location", "ResultData", "files", function($scope, $location, ResultData, files) {
    // Select a file
    $scope.files = files;
    $scope.visit = function(file) {
        $location.path("/url/" + file);
    };

    // Upload a file
    $scope.onFileSelect = function($files) {
        var reader = new FileReader();
        var file = $files[0];
        reader.addEventListener("loadend", function() {
            $scope.$apply(function(scope) {
                var input = JSON.parse(reader.result);
                ResultData.save(input);
                $location.path("/file/" + file.name);
            });
        });
        reader.readAsBinaryString($files[0]);
    };

    // Load an URL
    $scope.load = function() {
        var target = "/url/" + encodeURI($scope.url);
        $location.path("/url/" + $scope.url);
    }
}]);

reportResultsApp.controller("reportResultCtrl", [ "$scope", "$modal", "$location", "data", "filename", function($scope, $modal, $location, data, filename) {
    if (data === null) {
        console.warn("No data available, go back to upload");
        $location.path("/");
    } else {
        $scope.results = data.tests;
        $scope.sources = data.sources;
        $scope.filename = filename;
    }

    // Transform a status in a mark
    $scope.mark = function(status) {
        return {
            "failed": "✗",
            "passed": "✓"
        }[status] || "";
    };

    // Text for tooltip
    $scope.tooltip = function(test) {
        if (!test.full_description) {
            return "";
        }
        return test.full_description.replace(/\//g, "/\u200d");
    };

    // Tabs handling
    $scope.select = function(rs) { rs.active = true; }
    $scope.deselect = function(rs) { rs.active = false; }

    // Details of a test
    $scope.details = function (hostname, result) {
        var modalInstance = $modal.open({
            templateUrl: "details.html",
            windowClass: "wider-modal",
            controller: [ "$scope", "$modalInstance", "result", "hostname", "source",
                          function ($scope, $modalInstance, result, hostname, source) {
                              $scope.hostname = hostname;
                              $scope.file_path = result.test.file_path;
                              $scope.line_number = result.test.line_number;
                              $scope.description = result.test.full_description;
                              $scope.status = result.test.status;
                              $scope.exception = result.test.exception;
                              $scope.source_start = source.start;
                              $scope.source_snippet = source.snippet.join("\n");

                              $scope.ok = function () {
                                  $modalInstance.dismiss('ok');
                              };
                          }],
            resolve: {
                result: function() { return result; },
                hostname: function() { return hostname; },
                source: function() {
                    // Extract the appropriate source snippet.
                    var file = result.test.file_path;
                    var start = result.test.line_number;
                    var end = result.test.line_number;
                    var source = $scope.sources[file];
                    // We search for the first blank lines followed by a non-idented line
                    while (start > 1 &&
                           (source[start - 1] !== "" ||
                            (source[start] || "").match(/^\s/) !== null)) start--;
                    while (source[end - 1] !== undefined &&
                           (source[end - 1] !== "" ||
                            (source[end - 2] || "").match(/^\s/) !== null)) end++;
                    start++; end--;
                    return {
                        "start": start,
                        "snippet": source.slice(start - 1, end)
                    }
                }
            }
        });
    };

}]);

reportResultsApp.directive(
    'fastscroll', function($window, $timeout) {
        return {
            scope: false,
            replace: false,
            restrict: 'A',
            link: function($scope, $element) {
                var timer;
                angular.element($window).on('scroll', function() {
                    if (timer) {
                        $timeout.cancel(timer);
                        timer = null;
                    }
                    $element.addClass('disable-hover');
                    timer = $timeout(function() {
                        $element.removeClass('disable-hover');
                    }, 500);
                });
            }
        };
    });

reportResultsApp.directive(
    "prettyprint", function() {
        return {
            scope: false,
            replace: true,
            restrict: 'E',
            template: '<pre class="prettyprint"></pre>',
            controller: function($scope, $element) {
                $element.html(prettyPrintOne($scope.source_snippet,
                                             "ruby",
                                             $scope.source_start));
                angular.element($element
                                .removeClass("highlighted")
                                .find("li")[$scope.line_number - $scope.source_start])
                    .addClass("highlighted");
            }
        };
    });

/* Local variables: */
/* js2-basic-offset: 4 */
/* End: */
