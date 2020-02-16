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
        return $.get("api/table/"+table_name);
    },

    load_table_data: function(table_name){
        var self = this;
        this.get_table_data(table_name).then(function(rows){
            if(!rows) return;
            self.data_table.destroy();
            self._clean_table();
            var $table = self.$table_wrapper.find("table");
            var $header = $table.find("thead");
            $table.find("tbody").remove();
            for(key in rows[0]){
                var th = document.createElement("th");
                th.appendChild(document.createTextNode(key));
                $header.append(th);
            }
            self.data_table = $table.DataTable({
                data: rows,
                columns: Object.keys(rows[0]).map(function(key){
                    return { data: key};
                })
            });
        });
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
