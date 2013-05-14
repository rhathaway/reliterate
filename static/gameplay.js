$(function(){

  var text_input = $("#u3");
  var submit_button = $("#u104");
  var your_word = $("#u4");
  var their_word = $("#u7");


  function isMyTurn(data) {
    if( data.you == data.gamestate.players[data.gamestate.turn] ) 
      return true;
    return false;
  }

  var loop = function() {
    console.log("foo");
    $.getJSON('/gamestate', function(data) {
      console.log(data);
      
      if(isMyTurn(data)) {
        $("#turn").html("it's your turn");
      } else {
        $("#turn").html("waiting for opponent");
      }      
      
      if(isMyTurn(data)) {
        their_word.html(data.gamestate.the_last_word);
      }
    });
  };

  text_input.click(function(){
    text_input.val('');
  });

  submit_button.click(function(){
    $.post('/move', { 'word' : text_input.val() }, function(data) {
      if(data != "") {
        //  if there was an error, the server will return it in the response
        //  and we'll just print it out as an alert dialog
        alert(data);
      } else {
        //  display your submitted word in the appropriate area
        your_word.html( text_input.val() ); 
      }
    });
  });

  setInterval(loop, 1000);

});
