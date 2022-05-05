$(document).ready(function() {

    $('#converter').on('change', function() {
        console.log("Changed");
        $('#unit-in').selectpicker('destroy')
        $('#unit-out').selectpicker('destroy');
        $("#input").val("");
        $("#output").val("");
        $('#unit-in').empty();
        $("#unit-out").empty();
        $('#unit-in').selectpicker()
        $('#unit-out').selectpicker();

        var unit_type = this.value;
        postData({"unit_type": unit_type}, "update-units", function(result) {
            console.log(result);
            var data;
            if (unit_type == "CURR") {
                for(let i of Object.keys(result["units"])) {
                    console.log(result[i]);
                    data = "<option value=" + i + ">" + result["units"][i] + "</option>"
                     $('#unit-in').append(data)
                    $('#unit-out').append(data)
                }
            }
            else {
                for(let i of result.units) {
                    data = "<option value=" + i + ">" + i + "</option>"
                     $('#unit-in').append(data)
                     $('#unit-out').append(data)
                }
            }
            $('#unit-out').selectpicker('refresh');
            $('#unit-in').selectpicker('refresh');

        });
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
        $("#unit-in").selectpicker('val', bottom);
        $("#unit-out").selectpicker('val', top);

        if($("#input").val() != "") {
            $("#convert").trigger("click");
        }


    });

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