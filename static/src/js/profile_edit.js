odoo.define('talebehane.profile', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function () {
        var $ilSelect = $('#il_id');
        var $uniSelect = $('#uni_id');
        var $ilceSelect = $('#ilce_id');
        var $fakSelect = $('#fak_id');
        var $bolumSelect = $('#bolum_id');

        function loadIlce(il_id, selectedIlceId) {
            return new Promise(function (resolve) {
                if (il_id) {
                    ajax.jsonRpc('/get_ilce', 'call', {'il_id': il_id}).then(function (data) {
                        $ilceSelect.empty();
                        $ilceSelect.append($('<option>', {value: '', text: 'İlçe Seçin'}));
                        $.each(data, function (index, ilce) {
                            $ilceSelect.append($('<option>', {value: ilce.id, text: ilce.name, selected: ilce.id == selectedIlceId}));
                        });
                        if (selectedIlceId) {
                            $ilceSelect.val(selectedIlceId);
                        }
                        resolve();
                    });
                } else {
                    $ilceSelect.empty().append($('<option>', {value: '', text: 'İlçe Seçin'}));
                    resolve();
                }
            });
        }

        function loadFak(uni_id, selectedFakId) {
            return new Promise(function (resolve) {
                if (uni_id) {
                    ajax.jsonRpc('/get_fak', 'call', {'uni_id': uni_id}).then(function (data) {
                        $fakSelect.empty();
                        $fakSelect.append($('<option>', {value: '', text: 'Fakülte Seçin'}));
                        $.each(data, function (index, fak) {
                            $fakSelect.append($('<option>', {value: fak.id, text: fak.name, selected: fak.id == selectedFakId}));
                        });
                        if (selectedFakId) {
                            $fakSelect.val(selectedFakId);
                        }
                        resolve();
                    });
                } else {
                    $fakSelect.empty().append($('<option>', {value: '', text: 'Fakülte Seçin'}));
                    $bolumSelect.empty().append($('<option>', {value: '', text: 'Bölüm Seçin'}));
                    resolve();
                }
            });
        }

        function loadBolum(fak_id, selectedBolumId) {
            return new Promise(function (resolve) {
                if (fak_id) {
                    ajax.jsonRpc('/get_bolum', 'call', {'fak_id': fak_id}).then(function (data) {
                        $bolumSelect.empty();
                        $bolumSelect.append($('<option>', {value: '', text: 'Bölüm Seçin'}));
                        $.each(data, function (index, bolum) {
                            $bolumSelect.append($('<option>', {value: bolum.id, text: bolum.name, selected: bolum.id == selectedBolumId}));
                        });
                        if (selectedBolumId) {
                            $bolumSelect.val(selectedBolumId);
                        }
                        resolve();
                    });
                } else {
                    $bolumSelect.empty().append($('<option>', {value: '', text: 'Bölüm Seçin'}));
                    resolve();
                }
            });
        }

        $ilSelect.change(function () {
            var il_id = $ilSelect.val();
            loadIlce(il_id, null);
            if (!il_id) {
                $ilceSelect.empty().append($('<option>', {value: '', text: 'İlçe Seçin'}));
            }
        });

        $uniSelect.change(function () {
            var uni_id = $uniSelect.val();
            loadFak(uni_id, null);
            if (!uni_id) {
                $fakSelect.empty().append($('<option>', {value: '', text: 'Fakülte Seçin'}));
                $bolumSelect.empty().append($('<option>', {value: '', text: 'Bölüm Seçin'}));
            }
        });

        $fakSelect.change(function () {
            var fak_id = $fakSelect.val();
            loadBolum(fak_id, null);
            if (!fak_id) {
                $bolumSelect.empty().append($('<option>', {value: '', text: 'Bölüm Seçin'}));
            }
        });

        // Initial load for preselected values
        var selectedIlceId = $ilceSelect.data('selected');
        var selectedFakId = $fakSelect.data('selected');
        var selectedBolumId = $bolumSelect.data('selected');

        (async function initializeSelections() {
            if ($ilSelect.val()) {
                await loadIlce($ilSelect.val(), selectedIlceId);
            }

            if ($uniSelect.val()) {
                await loadFak($uniSelect.val(), selectedFakId);
            }

            if ($fakSelect.val()) {
                await loadBolum($fakSelect.val(), selectedBolumId);
            }
        })();
    });
});
