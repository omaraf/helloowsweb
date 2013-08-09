$(document).ready(function() {
	if ($('form[data-behavior=confirm]').length >= 1) {
 
        //console.log('run.js: document ready : Applying confirmation, ' + $('form[data-behavior=confirm]').length + ' times');
 
        $('form[data-behavior=confirm] select').click(function() {
            var dataValue = $(this).find(':selected').text();
            $(this).attr('data-value', dataValue);
 
            // Debug console
            //console.log('Adding data-value at: ' + dataValue);
        });
 
        //$('form[data-behavior=confirm] .confirm-toggle').replaceWith('<input id="confirm-submit" type="submit" class="is-hidden"/>' + '<a href="#" class="confirm-toggle btn btn-primary">Continue</a>');
 
        /**
         *  Since we know javascript is executed so far, lets handle it with the confirmation.
         *
         *  That way, no javascript-enabled browsing user will be able to use the form. #progressiveEnhancement
         *
         *  Do the work.
         */
        $('form[data-behavior=confirm] .confirm-toggle').click(function(event) {
            event.preventDefault();
            var id_button = $(this).attr('id');
            console.log(id_button);
            // Get form content
            var form = $('form[data-behavior=confirm]').clone().attr('id', 'cloned'); //.appendTo('body');
            var i = 0;
            form.find(':input:not([type=hidden])').each(function() {
                var field = $(this);
 
 
                if (field.is('select')) {
                    fieldValue = $(this).attr('data-value');
                    if (fieldValue === undefined) {
                        fieldValue = field.find(':selected').html();
 
                        // Debug console
                        //console.log('fieldValue was undefined, setting to : ' + fieldValue);
                    }
 
                    // Debug console
                    //console.log('fieldValue is : ' + fieldValue);
                } else {
                    fieldValue = field.val();
                }
 
                // Remove undefined field (they are useless)
                if (fieldValue === '') {
                    field.parent().parent().addClass('empty-field-resolved');
                }
 
                // Debug console
                //console.log('Field ' + i + ' :' + fieldValue + ' for #' + field.attr('id'));
 
                // Wrap fieldValue in a tag, Tested in IE7!!
                field.after($('<span class="value">' + fieldValue + '</span>'));
 
                // Remove the field itself, we only want to see the resulting
                field.remove();
 
                i++;
            });
 
            // Work stuff out for modal window, copying content, and building modal into the DOM
            var decorate = $("<div id=\"modal-placeholder\"><div class=\"modal-builder\"></div></div>");
            var buildup = decorate.find(".modal-builder").html(form);
 
            buildup.appendTo('body');
 
            // Debug console
            //console.log('Appending #modal-placeholder in body, ready to call dialog2()');
 
            // Remove not needed anymore stuff
            $('.modal-builder .help-block, .modal-builder .input-append, .modal-builder .form-actions').remove();
            if ( id_button == 'updatebutton') {
                $('.modal-builder').dialog2({
                    title: "¿Esta Seguro de Actualizar este Registro?",
                    id: "confirm-modal",
                    modalClass: "modal-wide fade in",
                    closeOnOverlayClick: false,
                    closeOnEscape: false,
                    initialLoadText: "Loading in progress...",
                    buttons: {
                        "Confirmar": {
                            primary: true,
                            click: function() {
                                // Debug
                                console.log('Inside dialog2() clicked Confirm');
                                $.ajax({
                                    type: "POST",
                                    url: '/reservar/sala/update',
                                    data: $("#updatesalaform").serialize(), // serializes the form's elements.
                                    success: showResponse,
                                    error: showError,
                                });
                                $(this).dialog2("close");
                                return false;
                            }
                        },
                        "Cancelar": {
                            click: function() {
                                // Debug
                                console.log('Inside dialog2() clicked cancel');
 
                                $(this).dialog2("close");
                                $('.modal').remove();
                                return false;
                            } 
                        }
                    }
                });
            }

            if ( id_button == 'deletebutton') {
                $('.modal-builder').dialog2({
                    title: "¿Esta Seguro de Borrar este Registro?",
                    id: "confirm-modal",
                    modalClass: "modal-wide fade in",
                    closeOnOverlayClick: false,
                    closeOnEscape: false,
                    initialLoadText: "Loading in progress...",
                    buttons: {
                        "Confirmar": {
                            primary: true,
                            click: function() {
                                // Debug
                                console.log('Inside dialog2() clicked Confirm');
                                $.ajax({
                                    type: "POST",
                                    url: '/reservar/sala/delete',
                                    data: $("#updatesalaform").serialize(), // serializes the form's elements.
                                    success: showResponseDel,
                                    error: showError,
                                });
                                $(this).dialog2("close");
                                return false;
                            }
                        },
                        "Cancelar": {
                            click: function() {
                                // Debug
                                console.log('Inside dialog2() clicked cancel');
 
                                $(this).dialog2("close");
                                $('.modal').remove();
                                return false;
                            } 
                        }
                    }
                });
            }
            // Do my own cleanup. Remove potentially bogus nodes
            $('#modal-placeholder, .modal-header .close, .control-group.empty-field-resolved').remove();
        });
    }
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
    $('#outputform').addClass('alert alert-success').html('Reservacion Actualizada Fecha Inicio: '+responseText.fecha_inicio+',Fecha Fin: '+responseText.fecha_fin).fadeIn('slow'); 
}
function showResponseDel(responseText, statusText, xhr, $form)  {
    window.location = '/reservar/sala';
    window.location.replace = '/reservar/sala'; 
}