document.addEventListener("DOMContentLoaded", function() {
  //Initalize the Splitting
  Split(['#controlPanel', '#graph'], {
    sizes: [50, 50],
    minSize: [200, 200], // Minimum size of panels in pixels
    gutterSize: 10, // Size of the gutter in pixels
    cursor: 'col-resize' // CSS cursor value to display while dragging
  });

});