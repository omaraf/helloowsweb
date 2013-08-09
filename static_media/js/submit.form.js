$(document).ready(function() { 
    var options = { 
        target:        '#outputform', 
        //beforeSubmit:  showRequest, 
        success:       showResponse,
        dataType:      'json',
        resetForm:      true,
        error:          showError,
    };
    // bind to the form's submit event 
    $('#salaform').submit(function() {  
        $(this).ajaxSubmit(options);  
        return false; 
    });
});
function showError(xhr, textStatus, errorThrown){
    if(xhr.responseText){
        var err = $.parseJSON(xhr.responseText);
        $('#outputform').removeClass();
        $('#outputform').addClass('alert alert-error').html('Error: '+err).fadeIn('slow');  
    }else{
        console.log("No");
        $('#outputform').removeClass();
        $('#outputform').addClass('alert alert-error').html('Error: '+errorThrown).fadeIn('slow'); 
    }
}
function showResponse(responseText, statusText, xhr, $form)  { 
    $('#outputform').removeClass();
    $('#outputform').addClass('alert alert-success').html('Reservacion Creada Fecha Inicio: '+responseText.fecha_inicio+',Fecha Fin: '+responseText.fecha_fin).fadeIn('slow');
    $('#calendar').fullCalendar('refetchEvents');
} 