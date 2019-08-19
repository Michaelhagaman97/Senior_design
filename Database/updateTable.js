function updateTable() {
	var dateval = document.getElementById("dateval").value;
	var dateupp = document.getElementById("dateupp").value;

	if (dateval == "") {
        document.getElementById("selection").innerHTML = "";
        return;
    } else {
        if (window.XMLHttpRequest) {
            // code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp = new XMLHttpRequest();
        } else {
            // code for IE6, IE5
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("selection").innerHTML = this.responseText;
            }
        };
//	date
        xmlhttp.open("GET","dateSelect.php?date="+dateval+"&upper="+dateupp+"&submit=View+Images",true);
        xmlhttp.send();
    }
}
/* this is an incomplete function to update the metadata panel
function updateMetaD(){
	var dateval = document.getElementById("dateval").value;
	if (dateval == "") {
        document.getElementById("currentSel").innerHTML = "";
        return;
    } else {
        if (window.XMLHttpRequest) {
            // code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp = new XMLHttpRequest();
        } else {
            // code for IE6, IE5
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("currentSel").innerHTML = this.responseText;
            }
        };
//	date
        xmlhttp.open("GET","",true);
        xmlhttp.send();
    }
}
*/
function getImage(str) {
	var x = document.getElementById("image");
	if(str != null){
		image.src = str;
	}
	else{
		image.src = "";
	}
}