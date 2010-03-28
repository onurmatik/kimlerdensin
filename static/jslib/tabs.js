$(document).ready(function(){
   $('#tabs div#tab-1,div#tab-2,div#tab-3').hide(); // Hide all divs
   $('#tabs div#tab-1').show(); // Show the first div
   $('#tabs ul li:first').addClass('active'); // Set the class for active state
   $('#tabs ul li a').click(function(){ // When link is clicked
   $('#tabs ul li').removeClass('active'); // Remove active class from links
   $(this).parent().addClass('active'); //Set parent of clicked link class to active
   var currentTab = $(this).attr('href'); // Set currentTab to value of href attribute
   $('#tabs div#tab-1,div#tab-2,div#tab-3').hide(); // Hide all divs
   $(currentTab).show(); // Show div with id equal to variable currentTab
   return false;
   });
});