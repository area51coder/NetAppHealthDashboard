/*
=========================================================
NetApp Health Dashboard
dashboard.js
Part 1
=========================================================
*/

"use strict";

// ======================================================
// Default Chart Configuration
// ======================================================

Chart.defaults.font.family =
    "'Segoe UI', Arial, sans-serif";

Chart.defaults.font.size = 13;

Chart.defaults.color = "#555";

Chart.defaults.plugins.legend.position = "bottom";

Chart.defaults.plugins.legend.labels.boxWidth = 14;

Chart.defaults.plugins.tooltip.enabled = true;


// ======================================================
// Helper
// ======================================================

function chartExists(id)
{
    return document.getElementById(id) !== null;
}


// ======================================================
// Capacity Chart
// ======================================================

function loadCapacityChart()
{
    if (!chartExists("capacityChart"))
        return;

    if (typeof capacityChartData === "undefined")
        return;

    const ctx =
        document
        .getElementById("capacityChart")
        .getContext("2d");

    new Chart(ctx,
    {
        type: "doughnut",

        data:
        {
            labels:
                capacityChartData.labels,

            datasets:
            [
                {

                    data:
                        capacityChartData.values,

                    backgroundColor:
                    [
                        "#2196F3",
                        "#4CAF50"
                    ],

                    borderWidth:1

                }
            ]
        },

        options:
        {
            responsive:true,

            maintainAspectRatio:false,

            cutout:"65%",

            plugins:
            {
                legend:
                {
                    display:true
                }
            }
        }

    });

}


// ======================================================
// Cluster Health Chart
// ======================================================

function loadClusterChart()
{

    if (!chartExists("healthChart"))
        return;

    if (typeof clusterChartData === "undefined")
        return;

    const ctx =
        document
        .getElementById("healthChart")
        .getContext("2d");

    new Chart(ctx,
    {

        type:"doughnut",

        data:
        {

            labels:
                clusterChartData.labels,

            datasets:
            [
                {

                    data:
                        clusterChartData.values,

                    backgroundColor:
                    [

                        "#4CAF50",

                        "#FFC107",

                        "#F44336",

                        "#9E9E9E"

                    ],

                    borderWidth:1

                }

            ]

        },

        options:
        {

            responsive:true,

            maintainAspectRatio:false,

            cutout:"65%",

            plugins:
            {

                legend:
                {

                    display:true

                }

            }

        }

    });

}


// ======================================================
// Dashboard Initialize
// ======================================================

window.addEventListener(

    "load",

    function()
    {

        loadCapacityChart();

        loadClusterChart();

    }

);

/*
=========================================================
dashboard.js
Part 2
Aggregate & Volume Charts
=========================================================
*/


// =====================================================
// Chart Color Palette
// =====================================================

const chartColors = [

    "#4CAF50",
    "#2196F3",
    "#FF9800",
    "#9C27B0",
    "#F44336",
    "#00BCD4",
    "#8BC34A",
    "#3F51B5",
    "#795548",
    "#607D8B"

];


// =====================================================
// Aggregate Bar Chart
// =====================================================

function loadAggregateChart()
{

    if (!chartExists("aggregateChart"))
        return;

    if (typeof aggregateChartData === "undefined")
        return;

    const ctx =
        document
        .getElementById("aggregateChart")
        .getContext("2d");

    new Chart(ctx,
    {

        type: "bar",

        data:
        {

            labels:
                aggregateChartData.labels,

            datasets:
            [
                {

                    label: "Capacity",

                    data:
                        aggregateChartData.values,

                    backgroundColor:
                        chartColors,

                    borderColor:
                        "#1565C0",

                    borderWidth:1,

                    borderRadius:6,

                    hoverBorderWidth:2

                }

            ]

        },

        options:
        {

            responsive:true,

            maintainAspectRatio:false,

            animation:
            {

                duration:1800,

                easing:"easeOutQuart"

            },

            plugins:
            {

                legend:
                {

                    display:false

                },

                tooltip:
                {

                    backgroundColor:"#222",

                    titleColor:"#fff",

                    bodyColor:"#fff",

                    cornerRadius:8,

                    padding:12,

                    callbacks:
                    {

                        label:function(context)
                        {

                            return " Capacity : "
                                + context.raw
                                + " TB";

                        }

                    }

                }

            },

            scales:
            {

                x:
                {

                    ticks:
                    {

                        maxRotation:45,

                        minRotation:30

                    }

                },

                y:
                {

                    beginAtZero:true,

                    grid:
                    {

                        color:"#eeeeee"

                    }

                }

            }

        }

    });

}



// =====================================================
// Volume Pie Chart
// =====================================================

function loadVolumeChart()
{

    if (!chartExists("volumeChart"))
        return;

    if (typeof volumeChartData === "undefined")
        return;

    const ctx =
        document
        .getElementById("volumeChart")
        .getContext("2d");

    new Chart(ctx,
    {

        type:"doughnut",

        data:
        {

            labels:
                volumeChartData.labels,

            datasets:
            [
                {

                    data:
                        volumeChartData.values,

                    backgroundColor:
                        chartColors,

                    hoverOffset:18,

                    borderWidth:1

                }

            ]

        },

        options:
        {

            responsive:true,

            maintainAspectRatio:false,

            cutout:"58%",

            animation:
            {

                animateRotate:true,

                animateScale:true,

                duration:2000,

                easing:"easeOutBounce"

            },

            plugins:
            {

                legend:
                {

                    position:"bottom"

                },

                tooltip:
                {

                    backgroundColor:"#222",

                    cornerRadius:8,

                    padding:12,

                    callbacks:
                    {

                        label:function(context)
                        {

                            return context.label
                                + " : "
                                + context.raw;

                        }

                    }

                }

            }

        }

    });

}



// =====================================================
// Update Dashboard Initialize
// =====================================================

window.addEventListener(

    "load",

    function()
    {

        loadCapacityChart();

        loadClusterChart();

        loadAggregateChart();

        loadVolumeChart();

    }

);