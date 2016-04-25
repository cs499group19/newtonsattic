function parseDatabaseData(data) 
{
    var rv = {};
    for (var key in data)
    {
        if (data.hasOwnProperty(key))
        {
            rv[key] = JSON.parse(data[key]);
        }
    }
    
    return rv;
}


function alert()
{

}

//All of the following functions use jQuery
$(function() {
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
    function addToCalendar( $item, $week ) {
          /* ---testing purposes---
          console.log($item);
          console.log("\n");
          console.log($week);*/
          $item.fadeOut(function() {
              var $list = $( "ul[id='time']", $week );
              var r = new RegExp('.+(Build).+');
              var s = new RegExp('.+(Morning).+');

              if (r.test($($item).context.innerText) && s.test($($week).context.innerHTML))
              {
                  var result = confirm('The instructor for this class is not available for this time of day. Are you sure you want to do this?');
                  if (!result)
                  {
                      removeFromCalendar($item, $('#allCourses'));
                      return;
                  }
              }
              $item.appendTo( $list ).fadeIn(function() {
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
    $("#allCourses").droppable({
        accept: $('.course'),
        //activeClass: "ui-state-highlight",  ---highlight the droppable that is being dropped into
        drop: function (event, ui) {
            //alert( "dropped" );  ---popup in the browser for testing purposes
            removeFromCalendar(ui.draggable, event.target);

        }
    });

    //Function to delete the draggable from the calendar and add it back to the list of draggables when dropped
    //Called from the previous function
    function removeFromCalendar( $item, $choices ) {
          /*---testing purposes---
          console.log($item);
          console.log("\n");
          console.log($choices);*/
          $item.fadeOut(function() {
              $item.appendTo( $choices ).fadeIn(function() {
                /* --optional animation to modify later if we choose
                $item
                  .animate({ width: "48px" })
                  .find ( "li" )
                    .animate({ height: "36px" });*/
              });

          });
    }

});


// function handleDragStart(e)
// {
//     this.style.opacity = '0.4';
// }
//
// var courseBoxes = document.querySelectorAll('.course');
// [].forEach.call(courseBoxes, function (courseBox) {
//     courseBox.addEventListener('dragstart', handleDragStart, false);
// });