/*
QUnit.test( "hello test", function( assert ) {
  assert.ok( 1 == "1", "Passed!" );
});
*/

var metricData1 =   [
                        {
                            "keyName" : "SOG",
                            "displayName" : "SOG",
                            "value": 6.5,
                            "targetValue" : 6.4
                        },
                        {
                            "keyName" : "COG",
                            "displayName" : "COG",
                            "value" : 135.8,
                            "targetValue" : "None"
                        }
                    ];


var metricData2 =   [
                        {
                            "displayName" : "SOG",
                            "keyName" : "SOG",
                            "value" : 6.8,
                            "targetValue" : 6.4
                        },
                        {
                            "displayName" : "COG",
                            "keyName" : "COG",
                            "value" : 141.3,
                            "targetValue" : "None"
                        }
                    ];



QUnit.test( "Controller Metric Referesh", function( assert ) {
    var readoutDiv = document.createElement("div");
    var targetReadoutDiv = document.createElement("div");
    var instNameDiv = document.createElement("div");
    var controller = new instrumentController(instNameDiv, readoutDiv, targetReadoutDiv);  
    controller.updateMetricData(metricData1);
    controller.selectMetric("SOG");

    assert.ok("6.5" === readoutDiv.textContent, "Check that instrument value is set to match metricData1");
    controller.updateMetricData(metricData2);
    assert.ok("6.8" === readoutDiv.textContent, "After metric update, check that instrument value matches metricData2.")
});

QUnit.test( "Select a new metric", function( assert ) {
    var readoutDiv = document.createElement("div");
    var instNameDiv = document.createElement("div");
    var targetReadoutDiv = document.createElement("div");
    var controller = new instrumentController(instNameDiv, readoutDiv, targetReadoutDiv);  
    controller.updateMetricData(metricData1);
    controller.selectMetric("SOG");
    assert.ok("6.5" === readoutDiv.textContent, "Check that instrument value is set to match selected metric");
    assert.ok("SOG" === instNameDiv.textContent, "Check that instrument name is set to match selected metric");
});

QUnit.test( "Initialize controller with null divs", function( assert ) {
    var assertMessage = "Expect an exception for invalid constructor arguments.";

    var controller = null;
    try{
        controller = new instrumentController(null, null, null);
        assert.ok(false, "Expected an exception, but it didn't occure");      
    }
    catch(e){
        assert.ok(e == "You must initialize the controller with valid dom element objects", assertMessage);
    }

});



//TODO - Error Handling and NULLs
    //handled Null on constructor
    //Select a metric that doesn't exist in the data field
    //Set an update for data af
//Change div instrument name when metric name changes
//Toggle display of target metric