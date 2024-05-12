var durationIndex = {
    "day": 1,
    "week": 2,
    "month": 3,
    "quarter": 4
}

function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function handleDurationChange() {
    var duration = document.getElementById("data_drn").value;
    var frequency = document.getElementById("data_freq");
    var options = frequency.getElementsByTagName("option");
    var last_selected_freq = frequency.value;
    var last_valid_freq = null;
    var freq_still_valid = false;
    for (var i = 0; i < options.length; i++) {
        if (i < durationIndex[duration] && i >= durationIndex[duration]-2) {
            options[i].disabled = false;
            if(last_selected_freq == options[i].value) freq_still_valid = true;
            last_valid_freq = options[i].value;
        }else {
            options[i].disabled = true;
        }
    }

    if(! freq_still_valid) frequency.value = last_valid_freq;
}

document.getElementById("data_drn").value = getQueryParam('data_drn') || "week";
document.getElementById("data_freq").value = getQueryParam('data_freq') || "daily";
handleDurationChange();


let stepsData = total_data.steps.steps_data_json;
let heartRateData = total_data.heartRate.heart_data_json;
let restingHeartRateData = total_data.restingHeartRate.resting_heart_data_json;
let sleepData = total_data.sleep.sleep_data_json;

console.log(total_data.activity);

// Extract dates and steps count
let stepsDates = stepsData.map(entry => entry.start);
let stepsCount = stepsData.map(entry => entry.count);

// Extract dates and heart rate count
let heartRateDates = heartRateData.map(entry => entry.start);
let heartRateCount = heartRateData.map(entry => entry.count);
let hearRateMin = heartRateData.map(entry => entry.min);
let hearRateMax = heartRateData.map(entry => entry.max);

// Extract dates and resting heart rate count
let restingHeartRateDates = restingHeartRateData.map(entry => entry.start);
let restingHeartRateCount = restingHeartRateData.map(entry => entry.count);

let sleepDates = sleepData.map(entry => entry.start);
let sleepCount = sleepData.map(entry => entry.count);

// Get canvas elements
const stepsCtx = document.getElementById('stepsChart').getContext('2d');
const heartRateCtx = document.getElementById('heartRateChart').getContext('2d');
const sleepCtx = document.getElementById('sleepChart').getContext('2d');

// Create bar plot
const stepsChart = new Chart(stepsCtx, {
    type: 'bar',
    data: {
        labels: stepsDates,
        datasets: [{
            label: 'Steps Count',
            data: stepsCount,
            backgroundColor: '#772014',
            borderWidth: 1
        }]
    },
    options: {
        maintainAspectRatio:true,
        responsive: true,
        scales: {
            x: {
                title: {
                    display: false
                },
                ticks: {
                    color: 'black'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Steps Count',
                    color:'black'
                },
                ticks: {
                    color: 'black'
                }
            }
        }
    }
});
const heartRateChart = new Chart(heartRateCtx, {
    type: 'line',
    data: {
        labels: heartRateDates,
        datasets: [{
            label: 'Min Heart Rate',
            data: hearRateMin,
            borderColor: 'rgba(55, 173, 221, 1.0)',
            backgroundColor: 'rgba(55, 173, 221, 0.6)',
            borderWidth: 2,
            fill: false
        }, {
            label: 'Max Heart Rate',
            data: hearRateMax,
            borderColor: 'rgba(55, 173, 221, 1.0)',
            backgroundColor: 'rgba(55, 173, 221, 0.6)',
            borderWidth: 2,
            fill: '-1'
        }, {
            label: 'Resting Heart Rate',
            data: restingHeartRateCount,
            borderColor: 'blue',
            borderWidth: 2,
            fill: false
        }]
    },
    options: {
        maintainAspectRatio:true,
        responsive: true,
        elements: {
            line: {
                tension: 0.000001
            }
        },
        plugins: {
            filler: {
                propagate: false
            }
        },
        scales: {
            x: {
                title: {
                    display: false
                },
                ticks: {
                    color: 'black' 
                }

            },
            y: {
                title: {
                    display: true,
                    text: 'Heart Rate',
                    color:'black'
                },
                ticks: {
                    color: 'black' 
                }
            }
        }
    }
});
const sleepChart = new Chart(sleepCtx, {
    type: 'pie',
    data: {
        labels: sleepDates,
        datasets: [{
            label: 'Sleep Hours',
            data: sleepCount,
            borderColor: '#990f02',
            borderWidth: 2,
            backgroundColor: '#008000',
            fill: true
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio:false,
        plugins: {
            legend: {
            position: 'top',
            }
        }
    }}
);

document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM fully loaded and parsed");

    var modal = document.getElementById("dataModal");
    var btn = document.getElementById("addDataButton");
    var span = document.getElementsByClassName("close")[0];

    if (btn) {
        btn.onclick = function () {
            console.log("Button clicked");
            modal.style.display = "block";
        };
    } else {
        console.log("Button element not found");
    }

    if (span) {
        span.onclick = function () {
            console.log("Close span clicked");
            modal.style.display = "none";
        };
    } else {
        console.log("Close span element not found");
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            console.log("Click on window outside modal");
            modal.style.display = "none";
        }
    };
});
