function sortTable(n) {
    var spellListTable, i, x, y, switchcount;
    switchcount = 0;
    var dir = "asc";
    var switching = true;
    spellListTable = document.getElementById("spellList");

    while (switching) {
        switching = false;
        var rows = spellListTable.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            var Switch = false;

            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    Switch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    Switch = true;
                    break;
                }
            }
        }

        if (Switch) { 
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++;
        } 
        
        else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            } 
        }
    }
}