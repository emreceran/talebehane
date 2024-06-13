odoo.define('talebehane.signup', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;

    $(document).ready(function () {
        $('#il_id').change(function () {
            var il_id = $(this).val();
            console.log("Selected il_id: " + il_id);
            ajax.jsonRpc('/get_ilce', 'call', {'il_id': il_id})
                .then(function (data) {
                    console.log("Received ilceler data: ", data);
                    var $ilceSelect = $('#ilce_id');
                    $ilceSelect.empty();
                    $ilceSelect.append('<option value="">İlçe Seçin</option>');
                    $.each(data, function (id, name) {
                        $ilceSelect.append('<option value="' + id + '">' + name + '</option>');
                    });
                });
        });

        $('#ilce_id').change(function () {
            var ilce_id = $(this).val();
            console.log("Selected ilce_id: " + ilce_id);
            ajax.jsonRpc('/get_lise', 'call', {'ilce_id': ilce_id})
                .then(function (data) {
                    console.log("Received liseler data: ", data);
                    var $liseSelect = $('#lise_id');
                    $liseSelect.empty();
                    $liseSelect.append('<option value="">Lise Seçin</option>');
                    $.each(data, function (id, name) {
                        $liseSelect.append('<option value="' + id + '">' + name + '</option>');
                    });
                });
        });
    });
});
