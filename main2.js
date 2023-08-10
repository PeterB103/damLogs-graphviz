//Input selectors
const startInputSimulated = document.querySelector("#startInputSimulated");
const endInputSimulated = document.querySelector("#endInputSimulated");
const startInputReal = document.querySelector("#startInputReal");
const endInputReal = document.querySelector("#endInputReal");

//Text & Time Selectors
const tableContainerSim = document.querySelector("#tableContainerSim");
const tableContainerReal = document.querySelector("#tableContainerReal");
const timeDisplaySimulated = document.querySelector("#timeDisplaySimulated");
const timeDisplayReal = document.querySelector("#timeDisplayReal");

//File Input element
const fileInput = document.getElementById('fileInput');

//dataTypes
const simulatedStates = "states";
const realStates = "realTimes"

// Get the file input element and Event listener for file selection
fileInput.addEventListener('change', handleFileSelect);
function handleFileSelect(event) {
    const file = event.target.files[0]; // Get the selected file

    const reader = new FileReader();

    reader.onload = function(e) {
        const fileContents = e.target.result; // Get the file contents

        // Fill the Ace Editor instance with the file contents
        const editor = ace.edit('editor');
        editor.setValue(fileContents);
        editor.clearSelection();
    };
    reader.readAsText(file);
}

// Download the Proto Text 
document.getElementById('saveBtn').addEventListener('click', function() {
  // Get the editor content
  const editor = ace.edit('editor');
  const text = editor.getValue();

  // Create a Blob object from the text
  const textFile = new Blob([text], { type: 'text/plain' });

  // Create a URL for the Blob object
  const url = URL.createObjectURL(textFile);

  // Create a temporary link and click it to start the download
  const downloadLink = document.createElement('a');
  downloadLink.href = url;
  downloadLink.download = 'protoText.txt';

  // Append the link to the body (required for Firefox)
  document.body.appendChild(downloadLink);

  // Simulate clicking the link
  downloadLink.click();

  // Remove the link after the download starts
  document.body.removeChild(downloadLink);
});

startInputSimulated.addEventListener('input', validateNumberInput);
endInputSimulated.addEventListener('input', validateNumberInput);
startInputReal.addEventListener('input', validateNumberInput);
endInputReal.addEventListener('input', validateNumberInput);

function validateNumberInput(event) {
    const inputText = event.target.value;
    const isValidNumber = /^\d*$/.test(inputText);

    if (!isValidNumber) {
        event.target.value = '';
    }
}

//Data Fetching
function handleDataFetch(dataType, tableContainer, startInput, endInput, timeDisplay) {
  const url = `http://localhost:5000/all_data`;
  fetch(url)
  .then(response => response.json())
  .then(data => {
    const table = createTable(data);
    tableContainer.innerHTML = ''; // Clear the previous content of the table container
    tableContainer.appendChild(table);
    //textArea.textContent = JSON.stringify(data, null, 2); // Format JSON with 2-space indentation

    // Get the last key from the states data
    let lastKey = 0;
    for (let key in data) {
      if (Number(key) > lastKey) {
        lastKey = Number(key);
      }
    }

    // Set default values for input boxes
    startInput.value = 0;
    endInput.value = lastKey;
    timeDisplay.textContent = `Start Time: ${startInput.value}, End Time: ${endInput.value}`;
  });
}

// Display updating
startInputSimulated.addEventListener('input', () => updateDisplay(simulatedStates, tableContainerSim, startInputSimulated, endInputSimulated, timeDisplaySimulated));
endInputSimulated.addEventListener('input', () => updateDisplay(simulatedStates, tableContainerSim, startInputSimulated, endInputSimulated, timeDisplaySimulated));
startInputReal.addEventListener('input', () => updateDisplay(realStates, tableContainerReal, startInputReal, endInputReal, timeDisplayReal));
endInputReal.addEventListener('input', () => updateDisplay(realStates, tableContainerReal, startInputReal, endInputReal, timeDisplayReal));

// Function to update the content in the timeDisplayDiv and make new fetch call when inputs change
function updateDisplay(dataType, tableContainer, startInput, endInput, timeDisplay) {
  const startTime = startInput.value;
  const endTime = endInput.value;
  timeDisplay.textContent = `Start Time: ${startTime}, End Time: ${endTime}`;
  const url = `http://localhost:5000/data/${dataType}?start=${startTime}&end=${endTime}`

  // Displaying the parsed information in text area
  fetch(url)
  .then(response => response.json())
  .then(data => {
    // textArea.textContent = JSON.stringify(data, null, 2); // Format JSON with 2-space indentation
    const table = createTable(data);
    tableContainer.innerHTML = ''; // Clear the previous content of the table container
    tableContainer.appendChild(table);
  });
}

function createTable(data) {
  const table = document.createElement('table');

  // Create table header
  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  const headers = ['Node#', 'Trait', 'RealT', 'Data', 'SimTime']; // Replace with your column names
  headers.forEach(headerText => {
    const th = document.createElement('th');
    th.textContent = headerText;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Create table body
  const tbody = document.createElement('tbody');
  data.forEach(row => {
    const tr = document.createElement('tr');
    row.forEach(cell => {
      const td = document.createElement('td');
      td.textContent = cell;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  return table;
}


//Initalize the Screen

document.addEventListener("DOMContentLoaded", function() {
  //Initalize the Splitting
  Split(['#controlPanel', '#graph'], {
    sizes: [50, 50],
    minSize: [200, 200], // Minimum size of panels in pixels
    gutterSize: 10, // Size of the gutter in pixels
    cursor: 'col-resize' // CSS cursor value to display while dragging
  });

  //simulatedStates data fetch
  handleDataFetch(simulatedStates, tableContainerSim, startInputSimulated, endInputSimulated, timeDisplaySimulated);
  //realStates data fetch
  handleDataFetch(realStates, tableContainerReal, startInputReal, endInputReal, timeDisplayReal);

});
