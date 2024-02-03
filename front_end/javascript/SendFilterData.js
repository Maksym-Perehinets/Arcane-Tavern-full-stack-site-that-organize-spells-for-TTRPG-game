let filterList = [];

async function sendFilters(filters) {
  res = await ApplyFilters(filters);
  insertData(res, true);
}

function collectFilters(){
    var elms = document.querySelectorAll("[id='actionDropdown']");
    var filters = ""
    for(var i = 0; i < elms.length; i++){ 
      filters += elms[i].value;
    }
    sendFilters(filters);
    filterList = [];
}

