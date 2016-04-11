//View controllers for HTML instrument pages


function instrumentController(instReadoutDiv, targetReadoutDiv) {
    var METRICS_DATA_URL = "./data_all/";
    var _instReadoutDiv = instReadoutDiv;
    var _targetReadoutDiv = targetReadoutDiv;
    var _selectedMetricKey = "SOG";
    this.currentMetricData = "";
    this.updateMetricData = function(metricData) {
        this.currentMetricData = metricData; //metricData;
        _instReadoutDiv.innerHTML = "6.5";
    };

    //this.updateViews() {
        
    //};
};

/*

data[1].

[
    {
        "displayName":"SOG",
        "keyName":"SOG",
        "value": 6.5,
        "targetValue":6.4
    },
    {
        "displayName":"SOG",
        "keyName":"COG",
        "value": 135.8,
        "targetValue":"None"
    }
]

populateSelectorMenu
    get the data list from the controller
    for each item in data
        addDataItemToSelector
            selectorName = item.displayName
            selectorDataKey = item.keyName


onclickInstTitle
    
    setInstMenuToVisible

onclickMenuItem
    setcurrentDataItem(selected)

setCurrentDataItem(key)
    setInstViewControllerKey to key

*/
