OPTIONS = ["Water", "Methanol", "Acetone", "Specific"]

// $( document ).ready(function() {
//     window.table = new Table(5);
// });

function addOptions(select){
    OPTIONS.forEach((item, index)=>{
        let option;
        option = $("<option></option>").text(item).attr("val",item);
        select.append(option)
    })
}

class Table {
    constructor(number_of_rows, url) {
        Table.removeRows();
        this.number_of_rows = number_of_rows;
        this.addRow();
        this.urlGetData = url;

    }

    addRow() {
        for (let i = 0; i < this.number_of_rows; i++) {
            let request = $.ajax({
                method: 'GET',
                url: "/table/",
                dataType: 'html',
                async: false,
                success: dispatch,
            });

            function dispatch(data, textStatus, jqXHR){
                Table.createRowFromHtml(data, i+1);
            }
        }
    }

    static loadCalculationValues(dataForEachRow){
        dataForEachRow.forEach(function (values,index){
            let calc_cell = $("#calculation-cell-"+(index+1))
            values.forEach(function(val, index){
                val = parseFloat(val).toFixed(3)
                switch (index){
                    case 0:
                        calc_cell.find('.estimated-drop').text(val)
                        break;
                    case 1:
                        calc_cell.find('.estimated-volume').text(val)
                        break;
                    case 2:
                        break;
                    case 3:
                        calc_cell.find('.minimum-volume').text(val)
                        break;
                }
            })
        });
    }


    static getTableValues(toString){
        let row = $(".band_row")
        let tablevalues = [];
        row.each(function (index){
            let item = {}
            item['band'] = $(this).find(".band_column").text()
            item['description'] = $(this).find(".description_column").text()
            item['volume (ul)'] = $(this).find(".volume").val()
            item['type'] = $(this).find(".solvent_select").val()
            item['density'] = $(this).find(".density").val()
            item['viscosity'] =$(this).find(".viscosity").val()
            tablevalues.push(item)
        })
        if(toString==true){
            tablevalues = '&table='+JSON.stringify(tablevalues)
        }
        return tablevalues
    }

    static createRowFromHtml(data, i){
        let body = $('#tbody_band');
        let row = jQuery(data)
        let select = row.find('select')
        let bandColumn = row.find('.band_column')
        let form = row.find('form')
        bandColumn.text(i)

        let calculation_cell = row.find('.calculation-cell')
        let volume_cell = row.find('.volume-cell')
        calculation_cell.attr('id',"calculation-cell-"+i)
        volume_cell.attr('id',"volume-cell-"+i)
        addOptions(select);

        // If Selection is "Specific"
        select.on("change", function () {
            let specific_options = $(this).closest('form').find('.specific-options')
            if ($(this).val() == "Specific") {
                specific_options.show()
            } else {
                specific_options.hide()
            }
        })

        // If Something change in the row
        form.on("change", function () {
            let formData = new FormData(this);
            calcVol()
        })
        body.append(row);
    }

    static removeRows(){
        let body = $('#tbody_band');
        body.empty();
    }
}


