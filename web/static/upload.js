$(document).ready(function () {
  $("#classify-button").click(function () {
    const url = $("#url").val();

    if (!url) {
      alert("Please enter a URL.");
      return;
    }

    $("#result").text("Please wait...").show();

    $.ajax({
      url: "/api/classify",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ url: url }),
      success: function (response) {
        const formattedResponse = formatResponse(response);
        $("#result")
          .removeClass("negative")
          .addClass("positive")
          .html(formattedResponse)
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

  function formatResponse(response) {
    let resultHtml = "<ul>";
    const categories = [];

    for (const key in response) {
      if (response.hasOwnProperty(key)) {
        const [count, totalPercentage] = response[key];
        categories.push({ key, count, totalPercentage });
      }
    }

    categories.sort((a, b) => b.totalPercentage - a.totalPercentage);

    categories.forEach((category, index) => {
      const { key, count, totalPercentage } = category;
      const average = (totalPercentage / count).toFixed(2);
      const highlightClass = index === 0 ? "highlight" : "";
      resultHtml += `<li class="${highlightClass}"><strong>${key}:</strong> Count: ${count}, Total Percentage: ${totalPercentage}, Average Percentage: ${average}%</li>`;
    });

    resultHtml += "</ul>";
    return resultHtml;
  }
});
