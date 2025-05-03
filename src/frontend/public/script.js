// ==============================
// SVG Update Logic
// ==============================

// Variables for path and obstacle status
let currentPath = 'left';  // Possible values: 'forward', 'left', 'right', 'backward'
let predictedPath = 'forward';  // Possible values: 'forward', 'left', 'right', 'backward'
let obstacleDetected = false;  // true for red, false for green






// Function to determine the correct SVG file and update the panel content
function updateSVG() {
    let svgFile = '';
    let safetyStatus = '';
    let safetyMessage = '';
    let safetyColor = '';  // Variable for safety status color
    let messageColor = '';  // Variable for safety message color

    // Check if obstacles are detected
    if (obstacleDetected) {
        if (currentPath === 'left') {
            imgFile = 'images/paths/left-notsafe.png';  // Updated path and file extension
            safetyStatus = 'Not Safe!';
            safetyMessage = 'Obstacles detected ahead while Turning Left. <br>Smart Wheelchair has been automatically stopped.';
            safetyColor = '#DA3B3B';  // Color for Not Safe
            messageColor = '#D63F3F';  // Color for safety message
        } else if (currentPath === 'right') {
            imgFile = 'images/paths/right-notsafe.png';  // Updated path and file extension
            safetyStatus = 'Not Safe!';
            safetyMessage = 'Obstacles detected ahead while Turning Right. <br>Smart Wheelchair has been automatically stopped.';
            safetyColor = '#DA3B3B';  // Color for Not Safe
            messageColor = '#D63F3F';  // Color for safety message
        } else if (currentPath === 'backward') {
            imgFile = 'images/paths/straight-notsafe.png';  // Updated path and file extension
            safetyStatus = 'Not Safe!';
            safetyMessage = 'Obstacles detected behind you while moving backward. <br>Smart Wheelchair has been automatically stopped.';
            safetyColor = '#DA3B3B';  // Color for Not Safe
            messageColor = '#D63F3F';  // Color for safety message
        } else {
            imgFile = 'images/paths/straight-notsafe.png';  // Updated path and file extension
            safetyStatus = 'Not Safe!';
            safetyMessage = 'Obstacles detected ahead. <br>Smart Wheelchair has been automatically stopped.';
            safetyColor = '#DA3B3B';  // Color for Not Safe
            messageColor = '#D63F3F';  // Color for safety message
        }
    } else {
        if (currentPath === 'left') {
            imgFile = 'images/paths/leftpath.png';  // Updated path and file extension
            safetyStatus = 'Safe';
            safetyMessage = 'No obstacles detected while Turning Left. <br>You may proceed left.';
            safetyColor = '';  // Default color for Safe
            messageColor = '';  // Default color for Safe message
        } else if (currentPath === 'right') {
            imgFile = 'images/paths/rightpath.png';  // Updated path and file extension
            safetyStatus = 'Safe';
            safetyMessage = 'No obstacles detected while Turning Right. <br>You may proceed right.';
            safetyColor = '';  // Default color for Safe
            messageColor = '';  // Default color for Safe message
        } else if (currentPath === 'backward') {
            imgFile = 'images/paths/straightpath.png';  // Updated path and file extension
            safetyStatus = 'Safe';
            safetyMessage = 'No obstacles detected behind you while moving backward. <br>You may proceed backward.';
            safetyColor = '';  // Default color for Safe
            messageColor = '';  // Default color for Safe message
        } else {
            imgFile = 'images/paths/straightpath.png';  // Updated path and file extension
            safetyStatus = 'Safe';
            safetyMessage = 'No obstacles detected ahead. <br>You may proceed forward.';
            safetyColor = '';  // Default color for Safe
            messageColor = '';  // Default color for Safe message
        }
    }

    const svgElement = document.querySelector('.svg-container img');  // Change this if you're using <image> tag
    if (svgElement) {
        svgElement.src = imgFile;  // Use src for <img> or xlink:href for <image>
    } else {
        console.error('Image element not found in the SVG container.');
    }

    // Update the current path and safety status text
    const displayPath = (currentPath === 'left') ? 'Turning Left' :
                        (currentPath === 'right') ? 'Turning Right' :
                        currentPath.charAt(0).toUpperCase() + currentPath.slice(1); // Default case for forward and backward

    document.getElementById('current-path').textContent = displayPath; // Update the displayed path
    const safetyStatusElement = document.getElementById('safety-status');
    safetyStatusElement.textContent = safetyStatus;
    safetyStatusElement.style.color = safetyColor;  // Set the color for safety status
    const safetyMessageElement = document.getElementById('safety-message');
    safetyMessageElement.innerHTML = safetyMessage;
    safetyMessageElement.style.color = messageColor;  // Set the color for safety message

    updatePredictedPathSegment();
    updateSegmentColors();
    
}

// ==============================
// Update Segment Color Logic
// ==============================
function updateSegmentColors() {
    console.log('Updating segment colors. Obstacle Detected:', obstacleDetected);

    // Array of IDs for segments that can change color
    const segmentIds = ['segment3', 'segment4', 'segment5', 'segment9', 'segment10', 'segment11'];
    
    // Loop through each segment ID
    segmentIds.forEach(id => {
        const segment = document.getElementById(id);
        if (segment) {
            if (obstacleDetected) {
                segment.src = 'images/red-bar.png'; // Change to red if obstacle is detected
            } else {
                segment.src = 'images/green-bar.png'; // Revert back to green if no obstacle
            }
            console.log(`Segment ${id} updated to: ${segment.src}`);
        } else {
            console.warn(`Segment with ID ${id} not found.`);
        }
    });
}

// Function to update the segment color based on predicted path
function updatePredictedPathSegment() {
    const segments = document.querySelectorAll('.right-segment-image');

    segments.forEach((segment) => {
        if (segment.alt.includes(predictedPath)) {
            segment.src = 'images/orange-bar.png';
        } else {
            segment.src = 'images/gray-bar.png';
        }
    });
}
//kag ari
// ==============================
// Battery Update Logic
// ==============================

function updateBatteryLevels(eegBatteryLevel) {
    const eegBatteryElement = document.getElementById('eeg-battery-level');
    eegBatteryElement.textContent = `${eegBatteryLevel}%`; // Update the EEG battery level
}


// ==============================
// Sidebar Toggle Logic
// ==============================

document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', function() {
        const sidebar = document.getElementById('sidebar');
        const logo = document.getElementById('sidebar-logo');

        if (sidebar) {
            // Toggle collapsed class on sidebar
            if (sidebar.classList.contains('collapsed')) {
                sidebar.classList.remove('collapsed');
                logo.src = 'images/logo-neurowarn.png';  // Revert to the full logo when expanded
            } else {
                sidebar.classList.add('collapsed');
                logo.src = 'images/logo-n.png';  // Change to the smaller logo when collapsed
            }

            // Remove highlight from all menu items
            document.querySelectorAll('.menu-item').forEach(menuItem => {
                menuItem.classList.remove('highlight');
            });

            // Highlight the clicked menu item
            item.classList.add('highlight');
        } else {
            console.error('Sidebar element not found.');
        }
    });
});
//muni
function updateStatus(batteryLevel, contactQuality, eegQuality) {
    // Update Battery Level
    const batteryPercentageElement = document.getElementById('battery-percentage');
    const batteryFillElement = document.getElementById('battery-fill');
    batteryPercentageElement.textContent = `${batteryLevel}%`;
    batteryFillElement.style.width = `${batteryLevel}%`;

    // Update Contact Quality
    const contactQualityPercentageElement = document.getElementById('contact-quality-percentage');
    const contactQualityFillElement = document.getElementById('contact-quality-fill');
    contactQualityPercentageElement.textContent = `${contactQuality}%`;
    contactQualityFillElement.style.width = `${contactQuality}%`;

    // Update EEG Quality
    const eegQualityPercentageElement = document.getElementById('eeg-quality-percentage');
    const eegQualityFillElement = document.getElementById('eeg-quality-fill');
    eegQualityPercentageElement.textContent = `${eegQuality}%`;
    eegQualityFillElement.style.width = `${eegQuality}%`;
}


function fetchData() {
    // Fetch data from the server's /api/data endpoint
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            // Set path and obstacle variables
            currentPath = data.actual_command;
            predictedPath = data.predicted_command;
            obstacleDetected = !data.obstacle;
            
            if (data.j_time) {
                alert((Date.now() * 1000) - data.j_time);
            }

            
            // Update the SVG and status values dynamically
            updateSVG();
            
            if (data.eeg_battery_level !== undefined && data.contact_quality !== undefined && data.eeg_quality !== undefined) {
                updateStatus(data.eeg_battery_level, data.contact_quality, data.eeg_quality);
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// Call the function once when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    fetchData();
});

// Call fetchData again periodically
setInterval(fetchData, 100); // Fetch data every 100 milliseconds

updateSVG();
updateBatteryLevels(88);



