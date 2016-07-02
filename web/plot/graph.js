var chart = AmCharts.makeChart("chartdiv", {
    "type": "serial",
    "theme": "light",
    "marginRight": 20,
    "marginLeft": 20,
    "autoMarginOffset": 10,
    "mouseWheelZoomEnabled":true,
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
        "backgroundAlpha": 0,
        "selectedBackgroundAlpha": 0.1,
        "selectedBackgroundColor": "#888888",
        "graphFillAlpha": 0,
        "graphLineAlpha": 0.5,
        "selectedGraphFillAlpha": 0,
        "selectedGraphLineAlpha": 1,
        "autoGridCount": true,
        "color": "#AAAAAA"
    },
    "categoryField": "date",
    "export": {
    	"enabled": true,
    }
});

chart.addListener("dataUpdated", zoomChart);

function zoomChart(){
    chart.zoomToDates(new Date(new Date().setDate(new Date().getDate()-2)), new Date());
}
