$(function(){

  var text_input = $("#u3");
  var submit_button = $("#u104");
  var your_word = $("#u4");
  var their_word = $("#u7");
  var input_touched = false;

  text_input.prop('disabled', true);

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
        if(!input_touched)
          text_input.val("your turn");
        text_input.prop('disabled', false);
      } else {
        if(!input_touched)
          text_input.val("waiting for opponent");
        text_input.prop('disabled', true);
      }      

      if(isMyTurn(data)) {
        if( data.gamestate.moves.len > 1 )
          your_word.html(data.gamestate.moves.slice(-2)[0]);
        their_word.html(data.gamestate.moves.slice(-1)[0]);
      } else {
        your_word.html(data.gamestate.moves.slice(-1)[0]);
        if( data.gamestate.moves.len > 1 )
          their_word.html(data.gamestate.moves.slice(-2)[0]);
      }
    });
  };

  text_input.click(function(){
    input_touched = true;
    text_input.val('');
  });

  submit_button.click(function(){
    input_touched = false;
    $.post('/move', { 'word' : text_input.val() }, function(data) {
      if(data != "") {
        //  if there was an error, the server will return it in the response
        //  and we'll just print it out as an alert dialog
        alert(data);
      } else {
        //  display your submitted word in the appropriate area
        //your_word.html( text_input.val() ); 
      }
    });
  });

  setInterval(loop, 1000);

});
