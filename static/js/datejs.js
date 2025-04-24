$(document).ready(function () {
  // Initialize DataTable with buttons and custom length menu
  $("#plist").dataTable({
    responsive: true, // Ensures responsiveness
    lengthChange: true, // Allows changing page length
    autoWidth: false, // Prevents automatic column width
    buttons: ["excel", "print"], // Adds export buttons
    lengthMenu: [5] // Sets the page length to 5
  }).buttons().container().appendTo("#plist_wrapper .col-md-6:eq(0)");

  // Fade out alert messages after 2 seconds
  setTimeout(function () {
    $(".alert").fadeOut("fast");
  }, 2000);

  // Initialize select2 with placeholder and clear option
  $("#id_drug_id").select2({
    placeholder: "Dispense Drug Here",
    allowClear: true,
    width: "100%" // Ensures full-width dropdown
  });

  // Handle select2 open and value change events
  $("#id_drug_id").on("select2:open", function () {
    $("#id_drug_id").change(function () {
      var data = $(this).val();
      $("#id_taken").val(data); // Sets the value in another input
    });
  });

  // Filter table rows based on user input in #filter2
  $("#filter2").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#plist > tbody > tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });

  // Fade out the theme loader
  $(".theme-loader").fadeOut(500);
});


  // $(function(){
    //     $('#id_drug_id').change(function(){
    //     var data= $(this).val();
    //     alert(data);       
    //     $("#id_sto").val(data)
         
    //   });
     
    //  $('#select2-search__field')
    //      .text(drugname)
    //      .trigger('change');
    
    //   });


    // $("#select2-search__field").on("click", function() {

    //   $('#id_drug_id').change(function(){
    //         var data= $(this).val();
    //         alert(data);       
    //         $("#id_sto").val(data)
             
    //       });
         
    //      $('#select2-search__field')
    //          .text(drugname)
    //          .trigger('change');
    
    //     });