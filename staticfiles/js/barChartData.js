window.onload = function () {
    let myBarChart; // Define the bar chart object

    const renderChart = (data, labels) => {
        const ctx = document.getElementById('myBarChart');
        if (myBarChart) {
            myBarChart.destroy(); // Destroy the existing bar chart
        }
    
        myBarChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Expenses',
                        data: data.expenses,
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    },
                    {
                        label: 'Income',
                        data: data.income,
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    },
                ],
            },
            options: {
                indexAxis: 'x', // Display bars on the X-axis
                grouping: true, // Display bars side by side
                scales: {
                    x: {
                        beginAtZero: true, // Start the X-axis from zero
                    },
                    y: {
                        beginAtZero: true, // Start the Y-axis from zero
                    },
                },
            },
        });
    };
    
    const getChartData = () => {
        const url = `/dashboard/get_charts_data/`; // URL to your view
        console.log(url)
        fetch(url)
            .then((res) => {
                if (!res.ok) {
                    // throw an Error(`HTTP error! Status: ${res.status}`);
                }
                return res.json();
            })
            .then((results) => {
                const chartData = results.monthly_data;
                const { labels, data } = chartData;
                renderChart(data, labels); // Update the bar chart with the new data
            })
            .catch((error) => {
                console.error("Fetch error:", error);
            });
    };

    // Initialize the bar chart
    getChartData();
};
