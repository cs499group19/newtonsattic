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

//All of the following functions use jQuery
$(function() {
//variables that store the data and the calendar weeks
var $data = $( 'ul[id^=data]' ), $calendar = $( 'div[id^=week]' );
//variable that sets up tabs
var tabs = $( "#tabs" ).tabs();

//Declares which ids are draggable and how they will be implemented
$( "li" , $data ).draggable({
      revert: "invalid", // when not dropped, the item will revert back to its initial position
      containment: "calendar",
      helper: "clone",
      cursor: "move",
});

//Declares which ids are droppable and how they will be implemented
$( 'div[id^=week]' ).droppable({
      accept: "ul[id^=data] > li",
      //activeClass: "ui-state-highlight",  ---highlight the droppable that is being dropped into
      drop: function( event, ui ) {
           //alert( "dropped" );  --popup in the browser for testing purposes
           deleteGroup( ui.draggable , event.target );

      }
});

//Function to delete the draggable from the list and add it to the droppable when dropped
//Called from the previous function
function deleteGroup( $item, $week ) {
      /* ---testing purposes---
      console.log($item);
      console.log("\n");
      console.log($week);*/
      $item.fadeOut(function() {
          var $list = $( "ul", $week ).length ?
            $( "ul", $week ) :
            $( "<ul class='data ui-helper-reset'/>" ).appendTo( $week );
          $item.appendTo( $list ).fadeIn(function() {
            /* --optional animation to modify later if we choose
            $item
              .animate({ width: "48px" })
              .find ( "li" )
                .animate({ height: "36px" });*/
          });

      });
}
});