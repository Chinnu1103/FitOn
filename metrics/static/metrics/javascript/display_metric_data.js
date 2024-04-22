let stepsData = total_data.steps.steps_data_json;
let heartRateData = total_data.heartRate.heart_data_json;
let restingHeartRateData = total_data.restingHeartRate.resting_heart_data_json;

// Extract dates and steps count
let stepsDates = stepsData.map(entry => entry.start);
let stepsCount = stepsData.map(entry => entry.count);

// Extract dates and heart rate count
let heartRateDates = heartRateData.map(entry => entry.start);
let heartRateCount = heartRateData.map(entry => entry.count);

// Extract dates and resting heart rate count
let restingHeartRateDates = restingHeartRateData.map(entry => entry.start);
let restingHeartRateCount = restingHeartRateData.map(entry => entry.count);

// Get canvas elements
const stepsCtx = document.getElementById('stepsChart').getContext('2d');
const heartRateCtx = document.getElementById('heartRateChart').getContext('2d');
const restingHeartRateCtx = document.getElementById('restingHeartRateChart').getContext('2d');

// Create bar plot
const stepsChart = new Chart(stepsCtx, {
    type: 'bar',
    data: {
        labels: stepsDates,
        datasets: [{
            label: 'Steps Count',
            data: stepsCount,
            backgroundColor: '#214590',
            borderWidth: 1
        }]
    },
    options: {
        maintainAspectRatio:true,
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Date',
                    color:'white'
                },
                ticks: {
                    color: 'white' 
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Steps Count',
                    color:'white'
                },
                ticks: {
                    color: 'white' 
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
            label: 'Heart Rate',
            data: heartRateCount,
            borderColor: '#229954',
            borderWidth: 1,
            fill: false
        }]
    },
    options: {
        maintainAspectRatio:true,
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Date',
                    color:'white'
                },
                ticks: {
                    color: 'white' 
                }

            },
            y: {
                title: {
                    display: true,
                    text: 'Heart Rate',
                    color:'white'
                },
                ticks: {
                    color: 'white' 
                },
                min:0,
                max:100
            }
        }
    }
});
const restingHeartRateChart = new Chart(restingHeartRateCtx, {
    type: 'line',
    data: {
        labels: restingHeartRateDates,
        datasets: [{
            label: 'Resting Heart Rate',
            data: restingHeartRateCount,
            borderColor: '#229954',
            borderWidth: 1,
            fill: true
        }]
    },
    options: {
        maintainAspectRatio:true,
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Date',
                    color:'white'
                },
                ticks: {
                    color: 'white' 
                },
            },
            y: {
                title: {
                    display: true,
                    text: 'Resting Heart Rate',
                    color:'white'
                },
                min:0,
                max:100,
                ticks: {
                    color: 'white' 
                }
                }
            }
        }
    }
);