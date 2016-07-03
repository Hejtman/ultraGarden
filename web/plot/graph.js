var chart = AmCharts.makeChart("chartdiv", {
    "type": "serial",
    "theme": "dark",
	 "backgroundColor": "#282828",
	 "backgroundAlpha": 1,
    "legend": {
        "useGraphSettings": true,
	     "backgroundColor": "#282828",
	     "backgroundAlpha": 1
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
        "lineColor": "#FF0000",
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
        "id": "v3",
        "valueAxis": "v3",
        "lineColor": "#FFAA00",
        "title": "balcony temperature in shadow",
        "valueField": "balcony",
		  "fillAlphas": 0
    }],
    "trendLines": [{
        "finalDate": "2099",
        "finalValue": 30,
        "initialDate": "2000",
        "initialValue": 30,
        "lineColor": "#CC0000"
    }, {
        "finalDate": "2099",
        "finalValue": 4,
        "initialDate": "2000",
        "initialValue": 4,
        "lineColor": "#CC0000"
    }],
	 "chartCursor": {
		 "categoryBalloonDateFormat": "MM-DD JJ:NN",
		  "cursorPosition": "mouse",
		  "showNextAvailable": true
    },
    "categoryAxis": {
        "parseDates": true,
		  "minPeriod": "mm",
        "axisColor": "#DADADA",
        "minorGridEnabled": true
    },
    "valueScrollbar": {
        "oppositeAxis": false,
        "offset": 50,
        "scrollbarHeight": 10
    },
	 "chartScrollbar": {
        "graph": "v3",
        "scrollbarHeight": 80,
        "autoGridCount": true
    },
    "mouseWheelZoomEnabled":true,
    "categoryField": "date",
    "export": {
    	"enabled": true
    }
});

chart.addListener("dataUpdated", zoomChart);

function zoomChart(){
//    chart.zoomToDates(new Date(new Date().setDate(new Date().getDate()-2)), new Date());
    chart.zoomToIndexes(chart.dataProvider.length - 2500, chart.dataProvider.length)
}
