//View controllers for HTML instrument pages

function isDomElement(obj){
    if(obj == null || obj.innerHTML === undefined)
        return false;
    return true;
};

function hideElement(el){
    el.style.display = 'none';  
    
}

function unhideElement(el){
    el.style.display = 'inline'; 
}


function instrumentController(instNameDiv, instReadoutDiv, targetReadoutDiv, menuDiv) {
    if(!isDomElement(instNameDiv) || !isDomElement(instReadoutDiv) || !isDomElement(targetReadoutDiv) || !isDomElement(menuDiv))
        throw "You must initialize the controller with valid dom element objects";

    


    var myThis = this; // preserve context within object methods.
    var INST_DECIMAL_PRECISION = 1;
    var _instReadoutDiv = instReadoutDiv;
    var _instNameDiv = instNameDiv;
    var _menuDiv = menuDiv;
    var _targetReadoutDiv = targetReadoutDiv;
    var _selectedMetricKey = "SOG";
    var _currentMetricData = "";

    //jam the proper menu div into the instNameDiv
    _instNameDiv.menuDiv = _menuDiv;
    var instNamceOnclick = "unhideElement(this.menuDiv);";
    _instNameDiv.setAttribute('onclick', instNamceOnclick);



    function getSelectedMetric() {
        for(var i=0; i<_currentMetricData.length; i++){
            if (_currentMetricData[i].keyName == _selectedMetricKey){
                return _currentMetricData[i];
            }
        }
    }

    function getMetricByKeyName(keyName, metrics) {
        for(var i=0; i<metrics.length; i++){
            if (metrics[i].keyName == keyName){
                return metrics[i];
            }
        }
    }

    function refreshInstrument(){
        var selectedMetric = getSelectedMetric();
        if (selectedMetric.value == null)
            return;

        if(_instReadoutDiv.firstChild)
            _instReadoutDiv.removeChild(_instReadoutDiv.firstChild);
        _instReadoutDiv.appendChild(_instReadoutDiv.ownerDocument.createTextNode(selectedMetric.value.toFixed(INST_DECIMAL_PRECISION)));

        if(_instNameDiv.firstChild)
            _instNameDiv.removeChild(_instNameDiv.firstChild);
        _instNameDiv.appendChild(_instReadoutDiv.ownerDocument.createTextNode(selectedMetric.displayName)); 
    }

   this.selectMetric = function (keyName) {
        _selectedMetricKey = keyName;
        //let's also hide the menu, since we've selected an item
        hideElement(_menuDiv);
        if(_currentMetricData != "")
            refreshInstrument();
    }

    function populateMenu(){
        while (_menuDiv.firstChild) {
            _menuDiv.removeChild(_menuDiv.firstChild);
        }
        for(var i=0; i<_currentMetricData.length; i++){

            var selectedMetricLinkDiv = document.createElement("div");
            var selectMetricLink = document.createElement("a");
            var link = document.createTextNode(_currentMetricData[i].displayName);
            selectMetricLink.appendChild(link);
            selectedMetricLinkDiv.appendChild(selectMetricLink);
            //OMG is this actually going to work?? This is quite a hack a doodle doo.
            //Let's jam the point to the this instance method, and a reference to the 
            //keyname associated with this metric. When onclick is call 'this' should 
            //reference the link element, and should be able to reference this 
            //jammed in members.
            selectMetricLink.keyName = _currentMetricData[i].keyName;
            selectMetricLink.selectMetricPtr = myThis.selectMetric;
            var onclickFunction = "this.selectMetricPtr(this.keyName);";
            //var onclickFunction = "debugMe(this);";
            selectMetricLink.setAttribute('onclick', onclickFunction);
            _menuDiv.appendChild(selectedMetricLinkDiv);

        }
    }

    this.updateMetricData = function(metricData) {
        _currentMetricData = metricData; //metricData;
        refreshInstrument();
        populateMenu();
        if(window.console && window.console.log){
            window.console.log("Processed MetricData with start time of: " + getMetricByKeyName("MetricTime", metricData).value)
        }
    };


    this.displayMetricMenu = function(){
        //unhid the menu when the _instNameDiv is clicked
        unhideElement(_menuDiv);
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
