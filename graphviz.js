//Button handler to download graphic as SVG
document.getElementById('downloadBtn').addEventListener('click', function() {
  var svgElement = document.querySelector('#graph svg'); // Select the SVG element
  var svgData = new XMLSerializer().serializeToString(svgElement); // Serialize the SVG to a string
  var blob = new Blob([svgData], {type: 'image/svg+xml'}); // Create a Blob from the SVG string
  var url = URL.createObjectURL(blob); // Create a URL from the Blob

  // Create a new <a> element, set its href to the Blob URL, and programmatically click it to initiate download
  var link = document.createElement('a');
  link.href = url;
  link.download = 'graph.svg';
  link.click();

  // Clean up by revoking the Blob URL
  URL.revokeObjectURL(url);
});


var margin = 40; // to avoid scrollbars
var graphviz; // Declare the graphviz variable

function attributer(datum, index, nodes) {
    var selection = d3.select(this);
    if (datum.tag == "svg") {
        var parentWidth = document.getElementById("controlPanel").clientWidth; // Get the width of the parent element
        var width = Math.min(window.innerWidth - parentWidth, window.innerHeight) - margin; // Calculate the width to fit within the remaining space
        var height = window.innerHeight;
        selection
            .attr("width", width)
            .attr("height", height);
        datum.attributes.width = width - margin;
        datum.attributes.height = height - margin;
    }
}

function resetZoom() {
    console.log('Resetting zoom');
    graphviz
        .resetZoom(d3.transition().duration(1000));
}

function resizeSVG() {
    console.log('Resize');
    var parentWidth = document.getElementById("controlPanel").clientWidth; // Get the width of the parent element
    var width = Math.min(window.innerWidth - parentWidth, window.innerHeight) - margin; // Calculate the width to fit within the remaining space
    var height = window.innerHeight;
    d3.select("#graph").selectWithoutDataPropagation("svg")
        .transition()
        .duration(700)
        .attr("width", width - margin)
        .attr("height", height - margin);
}

d3.select(window).on("resize", resizeSVG);
d3.select(window).on("click", resetZoom);

function renderGraph() {
  fetch('http://localhost:5000/dotCode')
      .then(response => response.text())
      .then(dotCodeSource => {
          if (graphviz) {
            console.log(dotCodeSource)
              graphviz
                  .attributer(attributer)
                  .renderDot(dotCodeSource);
          } else {
              graphviz = d3.select("#graph").graphviz()
                  .zoomScaleExtent([0.5, 2])
                  .attributer(attributer)
                  .renderDot(dotCodeSource);
          }
      })
      .catch(error => {
          // Handle any errors that occurred during fetching or generating dotCode
          console.error(error);
      });
}

  

// Initial rendering
renderGraph();

// // Reload the graph when the file changes
// function watchFileChanges() {
//     renderGraph(); // Render the graph on each check
//     setTimeout(watchFileChanges, 1000); // Check for file changes every second
// }

// watchFileChanges();