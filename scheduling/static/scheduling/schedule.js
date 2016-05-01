// This file contains the javascript that is necessary for the
//   scheduling.html page

var Week = function () {
    return {
        morning: [],
        afternoon: []
    };
};

var Schedule = function () {
    var rv = {weeks: []};

    for (var i = 1; i <= 12; i++) {
        rv.weeks.push(Week());
    }

    return rv;
};


var Course = function (id, title, instructors, rooms) {
    var rv = {};

    rv.id = id;
    rv.title = title;
    rv.instructors = instructors;
    rv.rooms = rooms;

    return rv;
};


var Instructor = function (id, name, availabilities, specialties) {
    var rv = {};

    rv.id = id;
    rv.name = name;
    rv.availabilities = availabilities;
    rv.specialties = specialties;

    return rv;
};


var Classroom = function (id, name, capacity) {
    var rv = {};

    rv.id = id;
    rv.name = name;
    rv.capacity = capacity;

    return rv;
};

var parseDatabaseData = function (data) {
    var rv = {};
    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            rv[key] = JSON.parse(data[key]);
        }
    }

    return rv;
};

var createDraggable = function (course, age, instructor, classroom) {
    var rv = {};

    rv.course = course;
    rv.age = age;
    rv.instructor = instructor;
    rv.classroom = classroom;

    return rv;
}

// Function to generate the draggables based on what instructor, class, classroom, age group
//   combinations are available.
function generateAvailable(data, schedule, week, time) {
    var available = [];
    //var t = time.charAt(0).toLowerCase();
    if (data[week] == null) {
        return available;
    }
    if (data[week][time] == null) {
        return available;
    }
    for (var pair in data[week][time]) {
        var course = data[week][time][pair][0];
        var instructor = data[week][time][pair][1];

        /*var used = false;
        if (schedule != "") {
            for (var pair in schedule[week][time]) {
                if ( pair[0]==course && pair[1]==instructor ) {
                    used = true;
                    break;
                }
            }
        }*/


        for (var room in course.room_requirement) {
            var courseItem = document.createElement('div');
            courseItem.setAttribute('class', 'box box-primary collapsed-box course');

            var div1 = document.createElement('div');
            div1.setAttribute('class', 'box-header with-border');
            courseItem.appendChild(div1);

            var h3 = document.createElement('h3');
            h3.setAttribute('class', 'box-title');
            h3.setAttribute('id', 'courseName');
            h3.innerHTML = course.name;
            div1.appendChild(h3);

            var div2 = document.createElement('div');
            div2.setAttribute('class', 'box-tools pull-right');
            div1.appendChild(div2);

            var button = document.createElement('button');
            button.setAttribute('class', 'btn btn-box-tool');
            button.setAttribute('data-widget', 'collapse');
            div2.appendChild(button);

            var i = document.createElement('i');
            i.setAttribute('class', 'fa fa-minus');
            button.appendChild(i);

            var div3 = document.createElement('div');
            div3.setAttribute('class', 'box-body');
            courseItem.appendChild(div3);

            var ul = document.createElement('ul');
            ul.setAttribute('id', 'course');
            ul.setAttribute('style', 'list-style-type: circle');
            div3.appendChild(ul);

            var li1 = document.createElement('li');
            li1.setAttribute('id', 'ageGroup');
            li1.innerHTML = "Age Group: " + course.age_group;
            ul.appendChild(li1);

            var li2 = document.createElement('li');
            li2.setAttribute('id', 'instructorName');
            li2.innerHTML = "Instructor: " + instructor.user.full_name;
            ul.appendChild(li2);

            var li3 = document.createElement('li');
            li3.setAttribute('id', 'classroomName');
            li3.innerHTML = "Classroom: " + course.room_requirement[room].name;
            ul.appendChild(li3);

            var allCourses = document.getElementById('availCourses-'+week+time);
            allCourses.appendChild(courseItem);
        }
    }
}

// Function to save the schedule as a JSON object.
var saveSchedule = function() {
    var schedule = Schedule();

    for (var i = 1; i <= 12; i++) {
        var weekm = document.getElementById('scheduled-'+i+'Morning').children;
        for (var j = 0; j < weekm.length; j++) {
            var obj = {};

            var allText = weekm[j]['textContent'];
            var patt1 = /Group:\s/g;
            patt1.exec(allText);
            var patt2 = /Instructor:\s/g;
            patt2.exec(allText);
            var patt3 = /Classroom:\s/g;
            patt3.exec(allText);

            var titleEndIndex = allText.indexOf("Age");
            var ageGroupStartIndex = patt1.lastIndex;
            var ageGroupEndIndex = allText.indexOf("Instructor");
            var instructorStartIndex = patt2.lastIndex;
            var instructorEndIndex = allText.indexOf("Classroom");
            var classroomStartIndex = patt3.lastIndex;


            obj.course = allText.slice(0,titleEndIndex);
            obj.instructor = allText.slice(instructorStartIndex, instructorEndIndex);
            obj.ageGroup = allText.slice(ageGroupStartIndex, ageGroupEndIndex);
            obj.classroom = allText.slice(classroomStartIndex);

            schedule.weeks[i-1].morning.push(obj);
        }

        var weeka = getElementById('scheduled-'+i+'Afternoon');
        for (var j = 0; j < weeka.length; j++) {
            var obj = {};

            var allText = weeka[j]['textContent'];
            var patt1 = /Group:\s/g;
            patt1.exec(allText);
            var patt2 = /Instructor:\s/g;
            patt2.exec(allText);
            var patt3 = /Classroom:\s/g;
            patt3.exec(allText);

            var titleEndIndex = allText.indexOf("Age");
            var ageGroupStartIndex = patt1.lastIndex;
            var ageGroupEndIndex = allText.indexOf("Instructor");
            var instructorStartIndex = patt2.lastIndex;
            var instructorEndIndex = allText.indexOf("Classroom");
            var classroomStartIndex = patt3.lastIndex;


            obj.course = allText.slice(0,titleEndIndex);
            obj.instructor = allText.slice(instructorStartIndex, instructorEndIndex);
            obj.ageGroup = allText.slice(ageGroupStartIndex, ageGroupEndIndex);
            obj.classroom = allText.slice(classroomStartIndex);

            schedule.weeks[i-1].afternoon.push(obj);
        }
    }

    return JSON.stringify(schedule);
}

var confirmConflictingAction = function () {
    return confirm('The instructor for this class is ' +
        'not available for this time of day. Are you ' +
        'sure you want to do this?');
};

//All of the following functions use jQuery
$(function () {
    var current_schedule = Schedule();

    //Declares which classes are draggable and how they will be implemented
    $('.course').draggable({
        revert: "invalid", // when not dropped, the item will revert back to its initial position
        //containment: "calendar", //does not need to be contained to anything
        helper: "clone",
        cursor: "move"
    });

    //Declares which classes are droppable and how they will be implemented
    //From list to schedule
    $('.time').droppable({
        accept: $('.course'),
        //activeClass: "ui-state-highlight",  ---highlight the droppable that is being dropped into
        drop: function (event, ui) {
            //alert( "dropped" );  ---popup in the browser for testing purposes
            addToCalendar(ui.draggable, event.target);

        }
    });

    //Function to delete the draggable from the list and add it to the droppable when dropped
    //Called from the previous function
    function addToCalendar($item, $week) {
        /* ---testing purposes---
         console.log($item);
         console.log("\n");
         console.log($week);*/
        $item.fadeOut(function () {
            var $list = $("ul[class='timeOfDay']", $week);
            var r = new RegExp('.+(Build).+');
            var s = new RegExp('.+(Morning).+');

            if (r.test($($item).context.innerText) && s.test($($week).context.innerHTML)) {
                if (!confirmConflictingAction()) {
                    removeFromCalendar($item, $('.allCourses'));
                    return;
                }
            }
            $item.appendTo($list).fadeIn(function () {
                /* --optional animation to modify later if we choose
                 $item
                 .animate({ width: "48px" })
                 .find ( "li" )
                 .animate({ height: "36px" });*/
            });

        });
    }

    //From schedule to list
    //$("ul[id='allCourses']").droppable({
    $(".allCourses").droppable({
        accept: $('.course'),
        //activeClass: "ui-state-highlight",  ---highlight the droppable that is being dropped into
        drop: function (event, ui) {
            //alert( "dropped" );  ---popup in the browser for testing purposes
            removeFromCalendar(ui.draggable, event.target);

        }
    });

    //Function to delete the draggable from the calendar and add it back to the list of draggables when dropped
    //Called from the previous function
    function removeFromCalendar($item, $choices) {
        /*---testing purposes---
         console.log($item);
         console.log("\n");
         console.log($choices);*/
        $item.fadeOut(function () {
            $item.appendTo($choices).fadeIn(function () {
                /* --optional animation to modify later if we choose
                 $item
                 .animate({ width: "48px" })
                 .find ( "li" )
                 .animate({ height: "36px" });*/
            });

        });
    }

});
