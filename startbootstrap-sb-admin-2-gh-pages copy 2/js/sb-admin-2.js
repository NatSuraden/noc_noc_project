(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
    
    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });
  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict


const oTableFilter = (function(){

  var input;
  var tables = document.getElementsByTagName('table');
  var table = [];

  for (let i = 0; i < tables.length; i++) {

      table[i] = document.getElementById(tables[i].id);
      table[i].tr = table[i].getElementsByTagName('tr');

      if (table[i].tr.length > 1) {
      
          table[i].td = table[i].tr[1].getElementsByTagName('td');

      } //end if

      for (let j = 0; j < table[i].td.length; j++) {
          
          input = document.getElementById(table[i].id + j.toString());
          table[i].input = [];
          if (input != null) {

              table[i].input[j] = document.getElementById(table[i].id + j.toString());
              table[i].input[j].addEventListener("keyup", function() {
                  runFilter(table[i].id);
              });

          } //end if

      } //end loop

  } //end loop

  function runFilter(parTableName) {
  // Declare variables
  var table, tr, i, td, nMaxCol, nResult, prefixInputId;
  var td = [], input = [], filter = [], txtValue = [];
  var isDisplay = true;

  //Table
  table = document.getElementById(parTableName);
  prefixInputId = parTableName;
  tr = table.getElementsByTagName("tr");

  //Count Table Columns
  if (tr.length > 1) {

      td = tr[1].getElementsByTagName("td")
      nMaxCol = td.length;

  } //end if

  //Re-Count Table Columns
  for (i = 0; i < nMaxCol; i++) {

      if (document.getElementById(prefixInputId+i.toString()) != null) {

          input[i] = document.getElementById(prefixInputId+i.toString());
          filter[i] = input[i].value.toUpperCase();

      } else {
          nMaxCol = i;
      } //end if

  } //end loop

  // TR - Loop through all table rows, and hide those who don't match the search query
  for (i = 1; i < tr.length; i++) {

      //TD
      isDisplay = true;
      for (j = 0; j < nMaxCol; j++) {

          td = tr[i].getElementsByTagName("td")[j];
          txtValue = td.textContent || td.innerText;

          if (filter[j] != "") {

              nResult = txtValue.toUpperCase().indexOf(filter[j]);
              if ( nResult <= -1) {
                  isDisplay = false;
              } //end if

          } //end if

      } //end loop

      if (isDisplay) {
          tr[i].style.display = "";
      } else {
          tr[i].style.display = "none";
      } //end if

  } //end loop

  } //end method

})();
