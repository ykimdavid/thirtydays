$(document).ready( function() {
  $('.datepicker').datepicker();
  $('select').formSelect();
});


// $('#complete_btn').click(function(){
//   var habit_id;
//   habit_id = $(this).attr("habit_id");
//   $.get('/complete_habit/', {id: habit_id}, function(data){
//     $('#complete_btn').addClass("disabled");
//     $('#complete_btn').html(data);
//     });
// });
