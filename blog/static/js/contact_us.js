$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal .modal-content").html("");
        $("#modal").modal("show");
      },
      success: function (data) {
        $("#modal .modal-content").html(data.html_form);
        // console.log(data.html_form)
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    console.log(form)
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          // $("#book-table tbody").html(data.html_book_list);
          $("#modal").modal("hide");
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $("#contact-us-nav-button").click(loadForm);
  $("#modal").on("submit", ".contact-us-form", saveForm);

  // $("#create-comment-modal-button").click(loadForm);
  // $("#modal").on("submit", ".comment-form", saveForm);

});