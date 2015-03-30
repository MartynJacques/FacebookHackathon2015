var chart;

$(document).ready ( function(){
       document.getElementById("clear").style.visibility = "hidden";
       document.getElementById("graphbit").style.visibility = "hidden";
});

$("#go").click(function(){
    $("#go").addClass('loadinggif');
    $.getJSON("http://46.101.46.176:5000/api/" + $("#name").val() , function(data){
        $("#go").removeClass('loadinggif');
        var gap = document.getElementById("gap");
        gap.innerHTML=""

        var title = document.getElementById("resultsTitle");
        title.innerHTML = "<br>Results: <br>" + "<h4>" + $("#name").val() + "</h4>"; 

        var table = document.getElementById("resultsTable");
        table.innerHTML = "";
        var row = table.insertRow(0);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        cell1.innerHTML = "<h3>Facebook</h3>";
        cell2.innerHTML = "";

        row = table.insertRow(1);
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell1.innerHTML = "Likes: ";
        cell2.innerHTML = JSON.stringify(data.interactions.facebook.likes);

        row = table.insertRow(2);
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell1.innerHTML = "Facebook Shares: ";
        cell2.innerHTML = JSON.stringify(data.interactions.facebook.shares);

        row = table.insertRow(3);
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell1.innerHTML = "<h3>Twitter</h3>";
        cell2.innerHTML = "";

        row = table.insertRow(4);
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell1.innerHTML = "Tweets:";
        cell2.innerHTML = JSON.stringify(data.interactions.twitter.count);

        row = table.insertRow(5);
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell1.innerHTML = "<h3>Google+</h3>";
        cell2.innerHTML = "";

        row = table.insertRow(6);
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell1.innerHTML = "Google +1's:";
        cell2.innerHTML = JSON.stringify(data.interactions.google.plus_ones);
 
        document.getElementById("clear").style.visibility = "visible";
        if(data.showGraph) {
            document.getElementById("graphbit").style.visibility = "visible";
        }

        //$('html,body').animate({scrollTop: $(document).height()}, 600);
        $('html, body').animate({ scrollTop: ($("#resultsTitle").offset().top -50)}, 600);

        gap.innerHTML = "<br><br><br><br><br>"; 
    });
});

$("#clear").click(function(){
    //$.getJSON("http://46.101.46.176:5000/api/" + $("#name").val() , function(data){
        var gap = document.getElementById("gap");
        gap.innerHTML=""

        var title = document.getElementById("resultsTitle");
        title.innerHTML = ""; 

        var table = document.getElementById("resultsTable");
        table.innerHTML = "";

        var graphTitle = document.getElementById("graphTitle");
        graphTitle.innerHTML = "";

        //var canvas = document.getElementById('myChart');
        chart.destroy();
        //canvas.remove();
        //$('#main').append('<canvas id="myChart"><canvas>');

        document.getElementById("clear").style.visibility = "hidden";
        document.getElementById("graphbit").style.visibility = "hidden";

        $('html, body').animate({ scrollTop: ($("#main").offset().top)-100}, 600);
    //});
});

$("#graphbit").click(function(){
    $("#graphbit").addClass('loadinggif');
    $.getJSON("http://46.101.46.176:5000/api/history/" + $("#name").val() , function(data){
        var graphTitle = document.getElementById("graphTitle");
        graphTitle.innerHTML = "<br>Total Interactions vs Time: <br>" + "<h4>" + $("#name").val() + "</h4>";

        $("#graphbit").removeClass('loadinggif');
        var labels = []
        var ydata = []
        data = data['data']
        for(var i = 0; i < data.length; i++) {
            var obj = data[i]['interactions'];
            var total = 0;
            total += obj['facebook']['total_interactions'];
            total += obj['twitter']['count'];
            ydata.push(total);
            var date = data[i]['timestamp'];
            console.log(millisecondsToTime(date));
            labels.push(millisecondsToTime(date));
        }

        var buyerData = {
        labels : labels,
        datasets : [
                {
                    fillColor : "#3f67d7",
                    strokeColor : "#000000",
                    pointColor : "#4664d2",
                    pointStrokeColor : "#000000",
                    data : ydata
                }
            ]
        }

        var buyers = document.getElementById('myChart').getContext('2d');
        chart = new Chart(buyers).Line(buyerData);
    });
$('html, body').animate({ scrollTop: ($("#graphTitle").offset().top -50)}, 600);

});

function millisecondsToTime(milli)
{
      var milliseconds = milli % 1000;
      var seconds = Math.floor((milli / 1000) % 60);
      var minutes = Math.floor((milli / (60 * 1000)) % 60);
      var hours = Math.floor((milli / (3660 * 1000)) % 24);

      return hours + ":" + minutes;
}


