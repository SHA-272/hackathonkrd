$(document).ready(function () {
  $("#classify-button").click(function () {
    const url = $("#url").val();

    if (!url) {
      alert("Please enter a URL.");
      return;
    }

    $.ajax({
      url: "/api/classify",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ url: url }),
      success: function (response) {
        $("#result")
          .removeClass("negative")
          .addClass("positive")
          .text(JSON.stringify(response, null, 2))
          .show();
      },
      error: function (xhr) {
        const response = JSON.parse(xhr.responseText);
        $("#result")
          .removeClass("positive")
          .addClass("negative")
          .text(response.error || response.forbidden)
          .show();
      },
    });
  });
});
