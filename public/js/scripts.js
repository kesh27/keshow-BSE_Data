$(document).ready(function() {

    let get_equity_data = function(equity_name) {
        if(equity_name){
            equity_name = equity_name.toUpperCase()
        }
        $.ajax({
            type: "GET",
            url: "/generator",
            data: {"equity_name": equity_name},
            success: function(response) {
                response = JSON.parse(response)
                set_values(response)
            }
        })
    }

    get_equity_data()

    let get_equity_data_with_name =  function() {
        value = $('#search').val()
        get_equity_data(value)
    };

    let typing_timer = null;
    $('#search').keydown(function(){
        clearTimeout(typing_timer); 
        typing_timer = setTimeout(get_equity_data_with_name, 500)
    });

    let set_values = function(data) {
        var updated_datetime = new Date(data.last_updated_on)
        updated_datetime = updated_datetime.toString()
        updated_datetime = updated_datetime.split("GMT")
        set_updated_datetime(updated_datetime[0])
        set_equity_cards(data.results_mini)
    }

    let set_updated_datetime = function(updated_datetime) {
        $('#datetime').text(updated_datetime)
    }
    
    let set_equity_cards = function(results_mini) {
        $('#equity-cards').empty()
        set_table_header()
        for(let count = 0; count<results_mini.length; count++) {
            const result = results_mini[count]
            let equity_mini = JSON.parse(result.equity_mini)
            const name = "<div class='equity-card-data first-element'>"+ result.name +"</div>"
            const code = "<div class=equity-card-data>"+ equity_mini.code +"</div>"
            const open_value = "<div class=equity-card-data>&#8377;"+ equity_mini.open_value.toFixed(2) +"</div>"
            const high_value = "<div class=equity-card-data>&#8377;"+ equity_mini.high_value.toFixed(2) +"</div>"
            const low_value = "<div class=equity-card-data>&#8377;"+ equity_mini.low_value.toFixed(2) +"</div>"
            const close_value = "<div class=equity-card-data>&#8377;"+ equity_mini.close_value.toFixed(2) +"</div>"
            const card_elem = "<div class=equity-card>"+ name + code + open_value + high_value + low_value + close_value +"</div>"
            $('#equity-cards').append(card_elem)
        }
    }

    let set_table_header = function() {
        const name = "<div class='equity-card-data first-element'>NAME</div>"
        const code = "<div class=equity-card-data>CODE</div>"
        const open_value = "<div class=equity-card-data>OPEN</div>"
        const high_value = "<div class=equity-card-data>HIGH</div>"
        const low_value = "<div class=equity-card-data>LOW</div>"
        const close_value = "<div class=equity-card-data>CLOSE</div>"
        const card_elem = "<div class='equity-card table-header'>"+ name + code + open_value + high_value + low_value + close_value +"</div>"
        $('#equity-cards').append(card_elem)
    }
});
