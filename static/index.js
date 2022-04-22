$(document).ready(function() {
    $('#converter').on('change', function() {
        console.log("Changed");
        $("#input").val("");
        $("#output").val("");
        $("#unit-in").empty();
        $("#unit-out").empty();
        var unit_type = this.value;
        postData({"unit_type": unit_type}, "update-units", function(result) {
            console.log(result);
            for(let i of result.units) {
                var data = "<option value=" + i + ">" + i + "</option>"
                $('#unit-in').append(data)
                $('#unit-out').append(data)
            }
        });
    $('#convert').click(function(e) {
        e.stopImmediatePropagation();
        console.log("clicked");
        if($("#input").val() == "") {
            alert("Enter a value");
            return;
        }
        var val = $("#input").val();
        var unit_in = $("#unit-in").val();
        var unit_out = $("#unit-out").val();
        var unit_type = $("#converter").val();
        postData({"unit-in": unit_in, "unit-out": unit_out, "unit-type": unit_type, "val": val}, "convert", function(result) {
            console.log(result);
            $("#output").val(result.converted)

        });
    });

    $('#switch').click(function(e) {
        e.stopImmediatePropagation();
        console.log("clicked");
        var top = $("#unit-in").val();
        var bottom = $("#unit-out").val();
        $("#unit-in option[value=" + bottom + "]").prop("selected", true);
        $("#unit-out option[value=" + top + "]").prop("selected", true);
        if($("#input").val() != "") {
            $("#convert").trigger("click");
        }


    });

    })
});

function postData(send, link, callback) {

    $.ajax ({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(send),
        dataType: 'json',
        url: link,


    }).done(function(data){
        callback(data);
    });
}