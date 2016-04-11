/*
QUnit.test( "hello test", function( assert ) {
  assert.ok( 1 == "1", "Passed!" );
});
*/

var metricData1 =   [
                        "SOG": {
                            "displayName":"SOG",
                            "value": 6.5,
                            "targetValue":6.4
                        },
                        "COG" : {
                            "displayName":"COG",
                            "value": 135.8,
                            "targetValue":"None"
                        }
                    ];


var metricData2 =   [
                        {
                            "displayName":"SOG",
                            "keyName":"SOG",
                            "value": 6.8,
                            "targetValue":6.4
                        },
                        {
                            "displayName":"SOG",
                            "keyName":"COG",
                            "value": 141.3,
                            "targetValue":"None"
                        }
                    ];


QUnit.test( "hello test", function( assert ) {
    var readoutDiv = document.createElement("div");
    var targetReadoutDiv = null;
    var controller = new instrumentController(readoutDiv, targetReadoutDiv);  
    controller.updateMetricData(metricData1);
    assert.ok("SOG" === controller.currentMet ricData[0].keyName, "Update metric data.");
    assert.ok("6.5" === readoutDiv.textContent, "Check that instrument value is set to match metricData1")
    controller.updateMetricData(metricData2);
    assert.ok("6.5" === readoutDiv.textContent, "After metric update, check that instrument value matches metricData2.")
});