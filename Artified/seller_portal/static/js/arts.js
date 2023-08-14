$(document).on('click', '.edit_button_seller', function () {

    var current = $(this);
    current.parent().addClass("inactive");
    current.parent().next().removeClass("inactive");
    var curr_data = current.data("pid");
    var arr = ["name", "price", "desc", "category", "subcat"];
    for (let val of arr){
        var temp_input = $("input[name = "+curr_data+"_"+val+"]");
        temp_input.prop("disabled", false);        
        temp_input.attr("data-value", temp_input.val());
    }
});

$(document).on('click', '.cancel_button_seller', function () {

    var current = $(this);
    current.parent().addClass("inactive");
    current.parent().prev().removeClass("inactive");
    var curr_data = current.data("pid");
    var arr = ["name", "price", "desc", "category", "subcat"];
    for (let val of arr){
        var temp_input = $("input[name = "+curr_data+"_"+val+"]");
        temp_input.val(temp_input.data("value"));        
        temp_input.removeData("data-value");
        temp_input.prop("disabled", true);
    }
});

$(document).on('click', '.save_button_seller', function () {

    var current = $(this);
    current.parent().addClass("inactive");
    current.parent().prev().removeClass("inactive");
    var curr_data = current.data("pid");
    var arr = ["name", "price", "desc", "category", "subcat"];
    var jsondata = {"pid":curr_data}
    for (let val of arr){
        jsondata[val] = $("input[name = "+curr_data+"_"+val+"]").val();
    }
    $.ajax({
        type:"POST",
        url : "/seller/update_data_arts/",
        data:jsondata,
        success:function(){
            alert("Done");
        }
    }); 
});









