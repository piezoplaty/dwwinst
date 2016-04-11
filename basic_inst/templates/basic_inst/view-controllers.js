//View controllers for HTML instrument pages


function instrumentController(instNameDiv, instReadoutDiv, targetReadoutDiv) {
    var METRICS_DATA_URL = "./data_all/";
    var _instReadoutDiv = instReadoutDiv;
    var _instNameDiv = instNameDiv;
    var _targetReadoutDiv = targetReadoutDiv;
    var _selectedMetricKey = "SOG";
    var _currentMetricData = "";


    function getSelectedMetric() {
        for(var i=0; i<_currentMetricData.length; i++){
            if (_currentMetricData[i].keyName == _selectedMetricKey){
                return _currentMetricData[i];
            }
        }
    }

    this.updateMetricData = function(metricData) {
        _currentMetricData = metricData; //metricData;
        var selectedMetric = getSelectedMetric();
        _instReadoutDiv.innerHTML = selectedMetric.value;
        _instNameDiv.innerHTML = selectedMetric.displayName;
    };

    this.selectMetric = function(keyName) {
        _selectedMetricKey = keyName;
    }

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
