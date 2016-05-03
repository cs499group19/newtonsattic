// This file contains the javascript that is necessary for the
//   scheduling.html page

// Global variable that will store which instructors and classrooms are
//    available when in order to determine conflicts to warn about
var conflicts = {
    1: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    2: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    3: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    4: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    5: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    6: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    7: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    8: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    9: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    10: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    11: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } },
    12: { m: { instructor: [], classroom:[] },
         a: { instructor: [], classroom:[] } }
}

var Week = function () {
    return {
        m: [],
        a: []
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
    if (data[week] == null) {
        return;
    }
    if (data[week][time] == null) {
        return;
    }
    for (var pair in data[week][time]) {
        var course = data[week][time][pair][0];
        var instructor = data[week][time][pair][1];

        for (var room in course.room_requirement) {
            var used = false;
            if (schedule != null) {
                for (var item in schedule['weeks'][week-1][time]) {
                    var info = schedule['weeks'][week-1][time][item];
                    if ( info.course==course.name
                            && info.instructor==instructor.user.full_name
                            && info.classroom==course.room_requirement[room].name
                            && info.ageGroup==course.age_group) {
                        used = true;
                        break;
                    }
                }
            }
            if (used == true) { continue; }

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

// Function to generate the draggables that are already in the schedule
function generateSchedule(schedule, week, time) {
    var t = time.charAt(0).toLowerCase();
    if (schedule == null) {
        return;
    }
    for (var item in schedule['weeks'][week-1][t]) {
        var info = schedule['weeks'][week-1][t][item];

        var courseItem = document.createElement('div');
        courseItem.setAttribute('class', 'box box-primary collapsed-box course');

        var div1 = document.createElement('div');
        div1.setAttribute('class', 'box-header with-border');
        courseItem.appendChild(div1);

        var h3 = document.createElement('h3');
        h3.setAttribute('class', 'box-title');
        h3.setAttribute('id', 'courseName');
        h3.innerHTML = info.course;
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
        li1.innerHTML = "Age Group: " + info.ageGroup;
        ul.appendChild(li1);

        var li2 = document.createElement('li');
        li2.setAttribute('id', 'instructorName');
        li2.innerHTML = "Instructor: " + info.instructor;
        ul.appendChild(li2);

        var li3 = document.createElement('li');
        li3.setAttribute('id', 'classroomName');
        li3.innerHTML = "Classroom: " + info.classroom;
        ul.appendChild(li3);

        var allCourses = document.getElementById('scheduled-'+week+time);
        allCourses.appendChild(courseItem);

        conflicts[week][t]['instructor'].push(info.instructor);
        conflicts[week][t]['classroom'].push(info.classroom);
    }
}

// Function to generate the full schedule
function generateFullSchedule(schedule) {
    for (var i = 0; i < 12; i++) {
        var fullSchedule = document.createElement('tr');
        var weekLabel = document.createElement('th');
        weekLabel.innerHTML = "Week "+(i+1);
        fullSchedule.appendChild(weekLabel);
        for (var item in schedule['weeks'][i]['m']) {
            var info = schedule['weeks'][i]['m'][item];
            var scheduleItem = document.createElement('td');
            scheduleItem.innerHTML = info.course+'<br>'
                                        + info.ageGroup+'<br>'
                                        + info.instructor+'<br>'
                                        + info.classroom+'<br>'
                                        + "Morning";
            fullSchedule.appendChild(scheduleItem);
        }
        for (var item in schedule['weeks'][i]['a']) {
            var info = schedule['weeks'][i]['a'][item];
            var scheduleItem = document.createElement('td');
            scheduleItem.innerHTML = info.course+'<br>'
                                        + info.ageGroup+'<br>'
                                        + info.instructor+'<br>'
                                        + info.classroom+'<br>'
                                        + "Afternoon";
            fullSchedule.appendChild(scheduleItem);
        }
        var fullScheduleBody = document.getElementById('fullScheduleBody');
        fullScheduleBody.appendChild(fullSchedule);
    }
}

// Function that will parse the course, instructor, age group, classroom information
var parseTextContent = function(allText) {
    var obj = {};

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

    return obj;
}

// Function to save the schedule as a JSON object
var saveSchedule = function() {
    var schedule = Schedule();

    for (var i = 1; i <= 12; i++) {
        var weekm = document.getElementById('scheduled-'+i+'Morning').children;
        for (var j = 1; j < weekm.length; j++) {
            var allText = weekm[j]['textContent'];
            var obj = parseTextContent(allText);

            schedule.weeks[i-1].m.push(obj);
        }

        var weeka = document.getElementById('scheduled-'+i+'Afternoon').children;
        for (var j = 1; j < weeka.length; j++) {
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

            schedule.weeks[i-1].a.push(obj);
        }
    }

    return JSON.stringify(schedule);
}

// Function to generate the full schedule that can be printed
function printSchedule(schedule) {
    var html = document.createElement('html');
    var head = document.createElement('head');
    var style = document.createElement('style');
    style.innerHTML = "table, th, td { border: 1px solid black; border-collapse: collapse; }";
    head.appendChild(style);
    var title = document.createElement('title');
    title.innerHTML = "Full Schedule";
    head.appendChild(title);
    html.appendChild(head);
    var body = document.createElement('body');
    var table = document.createElement('table');

    for (var i = 0; i < 12; i++) {
        var fullSchedule = document.createElement('tr');
        var weekLabel = document.createElement('th');
        weekLabel.innerHTML = "Week "+(i+1);
        fullSchedule.appendChild(weekLabel);
        for (var item in schedule['weeks'][i]['m']) {
            var info = schedule['weeks'][i]['m'][item];
            var scheduleItem = document.createElement('td');
            scheduleItem.innerHTML = info.course+'<br>'
                                        + info.ageGroup+'<br>'
                                        + "Morning";
            fullSchedule.appendChild(scheduleItem);
        }
        for (var item in schedule['weeks'][i]['a']) {
            var info = schedule['weeks'][i]['a'][item];
            var scheduleItem = document.createElement('td');
            scheduleItem.innerHTML = info.course+'<br>'
                                        + info.ageGroup+'<br>'
                                        + "Afternoon";
            fullSchedule.appendChild(scheduleItem);
        }
        table.appendChild(fullSchedule);
    }
    body.appendChild(table);
    html.appendChild(body);

    return html.outerHTML;
}

// Function to popup confirm box when there is an instructor conflict
var confirmConflictingInstructor = function () {
    return confirm('The instructor for this class is ' +
        'already scheduled for a class at this time of day. ' +
        'Are you sure you want to do this?');
};

// Function to popup confirm box when there is a classroom conflict
var confirmConflictingClassroom = function () {
    return confirm('The classroom for this class is ' +
        'already scheduled for a class at this time of day. ' +
        'Are you sure you want to do this?');
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

            var allText = ($item).context.innerText;
            var obj = parseTextContent(allText);

            var weekTime = ($item).context.parentNode.id;
            var index = weekTime.indexOf('-');
            var w = weekTime.slice(index+1, (weekTime.length)-1);
            var t = weekTime.slice((weekTime.length)-1);

            if (conflicts[w][t]['instructor'].indexOf(obj.instructor) != -1) {
                if (!confirmConflictingInstructor()) {
                    removeFromCalendar($item, $('.allCourses'));
                    return;
                }
            }

            if (conflicts[w][t]['classroom'].indexOf(obj.classroom) != -1) {
                if (!confirmConflictingClassroom()) {
                    removeFromCalendar($item, $('.allCourses'));
                    return;
                }
            }

            conflicts[w][t]['instructor'].push(obj.instructor);
            conflicts[w][t]['classroom'].push(obj.classroom);

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
