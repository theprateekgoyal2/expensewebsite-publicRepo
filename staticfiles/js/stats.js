document.addEventListener('DOMContentLoaded', function () {
    let myChart; // Define the chart object

    const renderChart = (data, labels) => {
        const ctx = document.getElementById('myChart');
        if (myChart) {
            myChart.destroy(); // Destroy the existing chart
        }
        myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Expenses per category',
                    data: data,
                    backgroundColor: [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)",
                        "rgba(75, 192, 192, 1)",
                        "rgba(153, 102, 255, 1)",
                        "rgba(255, 159, 64, 1)",
                    ]
                }]
            },
            options: {
                title: {
                    display: true,
                    text: "Expenses per category",
                },
                plugins: {
                    legend: {
                        display: true,
                    },
                    datalabels: {
                        color: '#fff',
                        formatter: (value, context) => {
                            return `${context.chart.data.labels[context.dataIndex]}: $${value}`;
                        },
                    },
                },
            },
        });

    };

    const getChartData = (timeInterval) => {
        console.log('fetching', timeInterval);
        console.log(timeInterval)
        console.log(`Fetching data for time interval:`, timeInterval);
        const url = `/expense_category_summary/${timeInterval}`;
        console.log(url)
        fetch(url)
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`HTTP error! Status: ${res.status}`);
                }
                return res.json();
            })
            .then((results) => {
                console.log("Results:", results);
                const category_data = results.expense_category_data;
                const [labels, data] = [Object.keys(category_data), Object.values(category_data)];
                renderChart(data, labels); // Update the chart with the new data
            })
            .catch((error) => {
                console.error("Fetch error:", error);
            });
    };

    const timeIntervalDropdown = document.getElementById('time-interval');
    const selectedTimeInterval = document.getElementById('selected-time-interval');
    
    timeIntervalDropdown.addEventListener('change', function () {
        const selectedOption = this.options[this.selectedIndex];
        selectedTimeInterval.textContent = selectedOption.text;
        document.onload = getChartData(selectedOption.value);
    });
    

    // Initialize the chart with the default time interval (e.g., '1m')
    document.onload = getChartData('1m');

    // document.onload = getChartData();
});
