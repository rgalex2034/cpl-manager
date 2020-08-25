function Cpl(){
    this.$table_selector = $("#table-select");
    this.$table_wrapper = $("#data-table-wrapper")
    this.table_template = document.getElementById("data-table-template");
    this.$table = $("#data-table");
    this.data_table = this.$table.DataTable();
}

Cpl.prototype = {

    init: function(){
        var self = this;
        this.$table_selector.on("change", function(){
            if(!this.value) return;
            self.load_table_data(this.value);
        });
    },

    get_tables: function(){
        return $.get("/api/tables");
    },

    load_table_selector: function(){
        var self = this;
        this.get_tables().then(function(tables){
            var $table_options = self.$table_selector.find("#table-options").empty();
            tables.forEach(function(table){
                var option = document.createElement("option");
                option.appendChild(document.createTextNode(table));
                option.value = table;
                $table_options.append(option);
            });
        });
    },

    get_table_data: function(table_name){
        return $.get("api/table/" + table_name);
    },

    load_table_data: function(table_name){
        var self = this;
        this.get_table_data(table_name).then(function(rows){
            if(!rows) return;

            //Preprocess rows
            for(var idx in rows){
                rows[idx] = self._pre_process_row(rows[idx]);
            }

            //Delete and recreate the initial empty table
            self.data_table.destroy();
            self._clean_table();

            var $table = self.$table_wrapper.find("table");
            var $header = $table.find("thead");
            $table.find("tbody").remove();

            //Append header
            for(key in rows[0]){
                var th = document.createElement("th");
                th.appendChild(document.createTextNode(key));
                $header.append(th);
            }

            //Fill the data of the edit cell dialog
            $table.on("click", "tbody > tr > td > div", function(){

                //Get html elements
                var $row = $(this).closest("tr");
                var $modal = $("#modal-edit-cell");
                var $td = $(this).closest("td");

                //Get data
                var id = $row.find("td").first().text();
                var value = this.innerHTML;
                var column_name = $td.closest('table').find('th').eq($td.index()).text();
                
                //Set the data into the dialog
                $modal.find("form > [name=id]").val(id);
                $modal.modal().find("form > [name=value]").val(value);

                //Get row/col indexs
                var row_index = $(this).closest("tr").index();
                var col_index = $(this).parent().index();

                //Set save button onclick event function
                document.getElementById("modal-edit-save-button").onclick = function(){

                    var new_value = document.getElementById("modal-edit-value").value
                        
                    //Check if it is actually necessary to update the database (there are changes)
                    if(value != new_value){

                        //Make the update to the database
                        ajax_res = $.ajax("api/update/" + table_name + "/" + column_name + "/" + id, {
                            method: "POST",
                            contentType: "application/json",
                            data: `{ "data": "${new_value}" }`,
                            success: function(){

                                //Update html data from this element
                                $table.find('tr:eq(' + row_index + ') t' + (row_index == 0 ?  "h" : "d") + ':eq(' + col_index + ')').html('').append(new_value);
                            
                            }
                        });

                    }

                    //Hide modal
                    $modal.modal("hide")

                }

            });

            //Load datatable with rows
            self.data_table = $table.DataTable({
                data: rows,
                columns: Object.keys(rows[0]).map(function(key){
                    return { data: key };
                })
            });

        });
    },

    _pre_process_row(row){
        for(var key in row){
            row[key] = "<div>" + row[key] + "</div>";
        }
        return row;
    },

    _clean_table: function(){
        var new_table = document.importNode(this.table_template.content, true);
        this.$table_wrapper.empty().append(new_table);
    }

};

document.addEventListener("DOMContentLoaded", function(){
    var cpl = new Cpl();
    cpl.init();
    cpl.load_table_selector();
});
