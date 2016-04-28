$(function () {
    'use strict';

    var $btnScheduleLoad = $('#btn-schedule-load');

    var handleScheduleLoadSubmit = function (event) {
        event.preventDefault();
        var scheduleId = $('#schedule-select').val();

        window.location = '/scheduling/' + scheduleId;
    };

    $btnScheduleLoad.on('click', handleScheduleLoadSubmit);
});