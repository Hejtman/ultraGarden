var chart = AmCharts.makeChart("chartdiv", {
    "type": "serial",
    "theme": "light",
    "legend": {
        "useGraphSettings": true
    },
    "dataProvider": chartData,
    "synchronizeGrid": true,
    "valueAxes": [{
        "axisColor": "#FF6600",
        "position": "right"
    }],
    "dashLength": 1,
    "position": "right",
    "guides": [{
            "dashLength": 6,
            "inside": true,
            "label": "permanent damage",
            "lineAlpha": 0.5,
            "value": 30,
        },{
            "dashLength": 6,
            "inside": true,
            "label": "closed",
            "lineAlpha": 0.5,
            "value": 24,
        },{
            "dashLength": 6,
            "inside": true,
            "label": "optimum",
            "lineAlpha": 0.5,
            "value": 21,
        },{
            "dashLength": 6,
            "inside": true,
            "label": "optimum",
            "lineAlpha": 0.5,
            "value": 19,
        },{
            "dashLength": 6,
            "inside": true,
            "label": "closed",
            "lineAlpha": 0.5,
            "value": 16,
        },{
            "dashLength": 6,
            "inside": true,
            "label": "permanent damage",
            "lineAlpha": 0.5,
            "value": 4,
    }],
    "graphs": [{
        "valueAxis": "v1",
        "lineColor": "#000000",
        "title": "temperature inside tube",
        "valueField": "tube",
		  "fillAlphas": 0
    }, {
        "valueAxis": "v2",
        "lineColor": "#00BBBB",
        "title": "barel watter temperature",
        "valueField": "barel",
		  "fillAlphas": 0
    }, {
        "valueAxis": "v3",
        "lineColor": "#FFAA00",
        "title": "balcony temperature in shadow",
        "valueField": "balcony",
		  "fillAlphas": 0
    }],
	 "chartCursor": {
		  "cursorPosition": "mouse"
    },
    "categoryAxis": {
        "parseDates": true,
		  "minPeriod": "mm",
        "axisColor": "#DADADA",
        "minorGridEnabled": true
    },
    "categoryField": "date",
    "export": {
    	"enabled": true,
		"position": "top-right"
    },
});

chart.addListener("dataUpdated", zoomChart);
zoomChart();


function zoomChart(){
    chart.zoomToIndexes(chart.dataProvider.length - 0, chart.dataProvider.length - 0);
}

