$(document).ready(function() {
	$("#id_fecha").datepicker({
		dateFormat: 'yy-mm-dd',
        changeMonth: true,
        changeYear: true,
        showAnim: ''
    });
    $('#id_hora_inicio').timepicker();
    $('#id_hora_fin').timepicker();
});