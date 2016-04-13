//View controllers for HTML instrument pages

function isDomElement(obj){
    if(obj == null || obj.innerHTML === undefined)
        return false;
    return true;
};


function instrumentController(instNameDiv, instReadoutDiv, targetReadoutDiv) {
    if(!isDomElement(instNameDiv) || !isDomElement(instReadoutDiv) || !isDomElement(targetReadoutDiv))
        throw "You must initialize the controller with valid dom element objects";


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
            if(_instReadoutDiv.firstChild)
                _instReadoutDiv.firstChild.nodeValue = selectedMetric.value;
            else
                _instReadoutDiv.appendChild(_instReadoutDiv.ownerDocument.createTextNode(selectedMetric.value));

        _instNameDiv.innerText = selectedMetric.displayName;
    };

    this.selectMetric = function(keyName) {
        _selectedMetricKey = keyName;
    }


    this.displayMetricMenu = function(){


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
