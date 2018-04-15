var chartData1 = [];
var chartData2 = [];
var chartData3 = [];
var chartData4 = [];
var index = 501;
// Create a basic chart object
chart = new AmCharts.AmStockChart();

//Function to load initial data after page loads
function generateChartData(chart){
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 21);
    firstDate.setHours(0, 0, 0, 0);
        //console.log(index);
        var val = null;
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'http://192.168.43.164:5000/getInitial', false);
        xhr.onload = function() {
        if (xhr.status === 200) {
         vals =  JSON.parse(xhr.responseText);
         console.log(xhr.responseText);
        console.log('asdasdas');
        for (var i = 0; i < 500; i++) {
                console.log(i);
                 var newDate = new Date(firstDate);
                 var newDate2 = new Date(firstDate);
                 newDate.setDate(newDate.getDate());
                 newDate2.setDate(newDate.getDate());
                 newDate.setHours(i,0,0,0);
                 newDate2.setHours(i+1,0,0,0);
                 console.log(newDate, newDate2);
                chartData1.push({
                    date: newDate2,
                    value: vals.actualDataStock2[i],
                    volume: vals.percentChange[i],
                    trend: vals.isCorrectlyPredicted[i]
                });
                chartData2.push({
                    date: newDate,
                    value: vals.actualDataStock2[i],
                    volume: vals.percentChange[i],
                    trend: vals.isCorrectlyPredicted[i]
                });
                chartData3.push({
                    date: newDate2,
                    value: vals.actualDataStock2[i],
                    volume: vals.percentChange[i],
                    trend: vals.isCorrectlyPredicted[i]
                });
                chartData4.push({
                    date: newDate,
                    value: vals.actualDataStock2[i],
                    volume: vals.percentChange[i],
                    trend: vals.isCorrectlyPredicted[i]
                });
    }
}
};
xhr.send();
}

//Function to execute on page load
AmCharts.ready(function() {
    generateChartData(chart);
    createStockChart(chart);
});

//Makes repeat AJAX Calls to server to fetch new data
setInterval(function(){ getnewdata(chart);},5000);

//Creates actual stock chart from the ojects
function createStockChart() {
    //chart.glueToTheEnd = true;
    chart.chartCursorSettings = {
      "valueBalloonsEnabled": true,
      "fullWidth": true,
      "cursorAlpha": 0.1,
      "valueLineBalloonEnabled": true,
      "valueLineEnabled": true,
      "valueLineAlpha": 0.5
};
    // DATASETS //////////////////////////////////////////
    // create data sets first
    var dataSet1 = new AmCharts.DataSet();
    dataSet1.title = "American Airlines Prediction";
    dataSet1.fieldMappings = [{
        fromField: "value",
        toField: "value"},
    {
        fromField: "volume",
        toField: "volume"},
        {
            fromField: "trend",
            toField: "trend"}];
    dataSet1.dataProvider = chartData1;
    dataSet1.categoryField = "date";

    var dataSet2 = new AmCharts.DataSet();
    dataSet2.title = "American Airlines";
    dataSet2.fieldMappings = [{
        fromField: "value",
        toField: "value"},
    {
        fromField: "volume",
        toField: "volume"},
        {
            fromField: "trend",
            toField: "trend"}];
    dataSet2.dataProvider = chartData2;
    dataSet2.categoryField = "date";

    var dataSet3 = new AmCharts.DataSet();
    dataSet3.title = "Amazon Predicion";
    dataSet3.fieldMappings = [{
        fromField: "value",
        toField: "value"},
    {
        fromField: "volume",
        toField: "volume"},
        {
            fromField: "trend",
            toField: "trend"}];
    dataSet3.dataProvider = chartData3;
    dataSet3.categoryField = "date";

    var dataSet4 = new AmCharts.DataSet();
    dataSet4.title = "Amazon";
    dataSet4.fieldMappings = [{
        fromField: "value",
        toField: "value"},
    {
        fromField: "volume",
        toField: "volume"},
        {
            fromField: "trend",
            toField: "trend"}];
    dataSet4.dataProvider = chartData4;
    dataSet4.categoryField = "date";

    // set data sets to the chart
    chart.dataSets = [dataSet1, dataSet2, dataSet3, dataSet4];
    chart.mainDataSet = dataSet1;

    // PANELS ///////////////////////////////////////////
    // first stock panel
    var stockPanel1 = new AmCharts.StockPanel();
    stockPanel1.showCategoryAxis = false;
    stockPanel1.title = "Price in Dollars";
    stockPanel1.percentHeight = 100;
    stockPanel1.recalculateToPercents="never";

    // graph of first stock panel
    var graph1 = new AmCharts.StockGraph();
    graph1.valueField = "value";
    graph1.comparable = true;
    graph1.compareField = "value";
    stockPanel1.addStockGraph(graph1);

    // create stock legend
    stockPanel1.stockLegend = new AmCharts.StockLegend();


    // second stock panel
    var stockPanel2 = new AmCharts.StockPanel();
    stockPanel2.title = "Prediction Difference";
    stockPanel2.percentHeight = 50;
    var graph2 = new AmCharts.StockGraph();
    graph2.valueField = "volume";
    graph2.type = "smoothedLine";
    graph2.showBalloon = false;
    graph2.fillAlphas = 1;
    stockPanel2.addStockGraph(graph2);
    stockPanel2.stockLegend = new AmCharts.StockLegend();

    var stockPanel3 = new AmCharts.StockPanel();
    stockPanel3.title = "Trend Accuracy";
    stockPanel3.percentHeight = 50;
    var graph3 = new AmCharts.StockGraph();
    graph3.valueField = "trend";
    graph3.type = "column";
    graph3.showBalloon = false;
    graph3.fillAlphas = 1;
    stockPanel3.addStockGraph(graph3);
    stockPanel3.stockLegend = new AmCharts.StockLegend();

    // set panels to the chart
    chart.panels = [stockPanel1, stockPanel2, stockPanel3];


    // OTHER SETTINGS ////////////////////////////////////
    var sbsettings = new AmCharts.ChartScrollbarSettings();
    sbsettings.graph = graph1;
    sbsettings.usePeriod = "DD";
    chart.chartScrollbarSettings = sbsettings;


    // PERIOD SELECTOR ///////////////////////////////////
    var periodSelector = new AmCharts.PeriodSelector();
    periodSelector.position = "left";
    periodSelector.periods = [    {
            period: "HH",
            selected: true,
            count: 5,
            label: "5 hour"},
     {
        period: "DD",
        count: 10,
        label: "10 days"},

    {
        period: "MM",
        count: 1,
        label: "1 month"},
    {
        period: "YYYY",
        count: 1,
        label: "1 year"},
    {
        period: "MAX",
        label: "MAX"}];
    chart.periodSelector = periodSelector;


    // DATA SET SELECTOR
    var dataSetSelector = new AmCharts.DataSetSelector();
    dataSetSelector.position = "left";
    dataSetSelector.selectText = "Select Stock or Prediction";
    chart.dataSetSelector = dataSetSelector;


    chart.addListener("rendered", function(event) {
        chart.mouseDown = false;
        chart.containerDiv.onmousedown = function() {
            chart.mouseDown = true;
    };
        chart.containerDiv.onmouseup = function() {
            chart.mouseDown = false;
    };
    });

    chart.write('chartdiv');
 //   return chart;
}
    // set up the chart to update every second

function getnewdata2(){
                var val = null;
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                   val = xhttp.responseText;
                   console.log(val);
                    }
                };
                xhttp.open('GET','http://localhost:5000/getdata', true);
                xhttp.send();
}

function getnewdata(chart){
        //console.log(index);
        var val = null;
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'http://192.168.43.164:5000/getUpdate?i='+index, true);
        xhr.onload = function() {
        if (xhr.status === 200) {
        vals =  JSON.parse(xhr.responseText);
        console.log(vals);
                var newDate = new Date(chartData1[chartData1.length - 1].date);
                newDate.setDate(newDate.getDate() + 1);
                // if ( chart.mouseDown )
        //         //     return;
                 var i = chartData1.length;
        // //        console.log(index);
                chart.dataSets[0].dataProvider.push({
                    date: newDate,
                    value: vals.predictedDataStock1,
                    volume: Number(vals.percentChange),
                    trend: Number(vals.isCorrectlyPredicted*100)
                });
                console.log(Number(vals.predictedDataStock1));
                chart.dataSets[1].dataProvider.push({
                    date: newDate + 3,
                    value: vals.actualDataStock1,
                    volume: Number(vals.percentChange),
                    trend: Number(vals.isCorrectlyPredicted*100)
                });
                console.log('two');
                chart.dataSets[2].dataProvider.push({
                    date: newDate,
                    value: vals.predictedDataStock2,
                    volume: Number(val.spercentChange),
                    trend: Number(vals.isCorrectlyPredicted*100)
                });
                console.log(vals.isCorrectlyPredicted*100);
                chart.dataSets[3].dataProvider.push({
                    date: newDate + 3,
                    value: vals.actualDataStock2,
                    volume: Number(vals.percentChange),
                    trend: Number(vals.actualDataStock2*100)
                });
                console.log(vals.isCorrectlyPredicted*100);
                chart.validateData();
                index++;
                var newStartDate = new Date(chart.startDate.getTime());
                newStartDate.setDate(newStartDate.getDate());
                var newEndDate = new Date(chart.endDate.getTime());
                newEndDate.setDate(newEndDate.getDate());
                chart.zoom(newStartDate, newEndDate);

        }
        };
xhr.send();
}
