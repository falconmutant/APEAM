function {prefix}_addCards(process){
    $.post('{url}', {
       target: 'candidate',
	   category: 'visualize',
	   process: process,
	   csrfmiddlewaretoken: token
   }, function(data){
       if($("#row2").length){
           $("#row2").html('');
           $("#row2").attr('data', process);
       }
       else{
           $(".page-body").append('<div class="row" id="row2" data="'+process+'"></div>');
       }
       data.forEach(function(candidate){
           $("#row2").append('<div class="col-md-6 col-xl-4">'+
	           '<div class="card client-map">' +
	           '    <div class="card-header borderless">' +
	           '        <div class="card-header-right">' +
               '            <a style="color: red;" class="candidate_delete" data="'+candidate.id+'"><i class="feather open-card-option icon-x"></i></a>' +
	           '        </div>' +
	           '    </div>' +
	           '    <div class="card-block">' +
	           '        <div class="client-detail">' +
	           '            <div class="client-profile">' +
	           '                <img src="'+candidate.image+'">' +
	           '            </div>'+
	           '            <div class="client-contain">' +
	           '                <h5>'+candidate.name+'</h5>' +
	           '                <p class="text-muted">'+candidate.appointment+'</p>' +
	           '                <p class="text-muted">'+candidate.category+'</p>' +
	           '                <p class="text-muted">'+candidate.entity+'</p>' +
	           '            </div>' +
	           '        </div>' +
	           '    </div>' +
	           '</div>'
           );
       });
       $("#row2").append('<div class="col-md-6 col-xl-4">'+
	       '<div class="card client-map waves-effect md-trigger" data-modal="{prefix}_modal">' +
	       '    <div class="card-header borderless">' +
           '        <div class="card-header-right">' +
           '        </div>' +
           '    </div>' +
           '    <div class="card-block">' +
           '        <div class="client-detail">' +
           '            <div class="client-profile">' +
           '                <img src="/static/assets/images/new-candidate.png">' +
           '            </div>'+
           '            <div class="client-contain">' +
           '                <h5>NOMBRE</h5>' +
           '                <p class="text-muted">CARGO</p>' +
           '                <p class="text-muted">CATEGORIA</p>' +
           '                <p class="text-muted">DISTRITO, ESTADO, MUNICIPIO</p>' +
           '            </div>' +
           '        </div>' +
           '    </div>' +
           '</div>'
       );
   });
}

$(document).on('click', '.visualize_candidate', function(e){
   e.preventDefault();
   {prefix}_addCards($(this).attr('data'));
   $.post('{url}', {
       target: 'form',
	   category: 'initialize',
	   form: 'new_candidate',
	   csrfmiddlewaretoken: token
   }, function(data){
       data.politic_party.forEach(function(pp){
           $('#{prefix}_new_candidate_form #politic_party').append('<option value="'+pp.id+'">'+pp.name+'</option>');
       });

       data.category.forEach(function(category){
           $('#{prefix}_new_candidate_form #category').append('<option value="'+category[0]+'">'+category[1]+'</option>');
       });

       data.appointment.forEach(function(appointment){
           $('#{prefix}_new_candidate_form #appointment').append('<option value="'+appointment[0]+'">'+appointment[1]+'</option>');
       });

       data.entity.forEach(function(entity){
           $('#{prefix}_new_candidate_form #entity').append('<option value="'+entity.id+'">'+entity.name+'</option>');
       });

   });
});

$(document).on('change', '#{prefix}_new_candidate_form #appointment', function(e){
   $('#{prefix}_new_candidate_form #municipality').empty();
   $('#{prefix}_new_candidate_form #district').empty();

   e.preventDefault();
   if($(this).val() == 'A'){
       $('#{prefix}_new_candidate_form').append(
           '<div class="form-group form-success">' +
	       '<select name="municipality" id="municipality" class="form-control form-control-default">' +
	       '<option value="-1">Municipio</option>' +
	       '</select>' +
	       '</div>');
       $.post('{url}', {
           target: 'form',
	       category: 'select',
	       select: 'municipality',
	       entity: $('#{prefix}_new_candidate_form #entity').val(),
	       csrfmiddlewaretoken: token
	   }, function(data){
           data.forEach(function(municipality){
               $('#{prefix}_new_candidate_form #municipality').append('<option value="'+municipality.id+'">'+municipality.name+'</option>');
           });
	   });
   }
   else if($(this).val() == 'M' || $(this).val() == 'R'){
       $('#{prefix}_new_candidate_form').append(
           '<div class="form-group form-success">' +
	       '<select name="district" id="district" class="form-control form-control-default select-municipality">' +
	       '<option value="-1">Distrito</option>' +
	       '</select>' +
	       '</div>');
       var data = {
           target: 'form',
	       category: 'select',
	       select: 'district',
	       entity: $('#{prefix}_new_candidate_form #entity').val(),
	       category2: $('#{prefix}_new_candidate_form #category').val(),
	       csrfmiddlewaretoken: token
       }
       $.post('{url}', data, function(data){
           data.forEach(function(district){
               $('#{prefix}_new_candidate_form #district').append('<option value="'+district.id+'">'+district.name+'</option>');
           });
       });
   }
});

$(document).on('click', '#{prefix}_new_candidate_cancel', function(e){
   e.preventDefault();
   $('#{prefix}_new_candidate_form')[0].reset();
   $('.md-overlay').click();
});

$(document).on('click', '#{prefix}_new_candidate_add', function(e){
    e.preventDefault();
    var {prefix}_formData = new FormData($('#{prefix}_new_candidate_form')[0]);
    {prefix}_formData.append('process',$('#row2').attr('data'));
    {prefix}_formData.append('target','candidate');
    {prefix}_formData.append('category','add');
    {prefix}_formData.append('csrfmiddlewaretoken', token);
    $.ajax({
		url: '{url}',
		type: 'POST',
		data: {prefix}_formData,
		async: false,
		success: function (data) {
		    {prefix}_addCards($('#row2').attr('data'));
		    $('#{prefix}_new_candidate_form')[0].reset();
		    $('.md-overlay').click();
		    $('#{prefix} table').DataTable().ajax.reload();
		    notify('top', 'center', 'fa fa-success', 'success', null, null,'¡Exito! ', ' Candidato Creado');
		},
	    error: function(XMLHttpRequest, textStatus, errorThrown) {
			notify('top', 'center', 'fa fa-danger', 'danger', null, null,'¡Error! ', ' Información incompleta');
		},
		cache: false,
		contentType: false,
		processData: false
	});
});

$(document).on('click', '.candidate_delete', function(e){
    e.preventDefault();
    $.post('{url}',{
        target: 'candidate',
        category: 'delete',
        candidate: $(this).attr('data'),
        csrfmiddlewaretoken: token
    },function(data){
        {prefix}_addCards($('#row2').attr('data'));
        $('#{prefix} table').DataTable().ajax.reload();
        notify('top', 'center', 'fa fa-success', 'success', null, null,'¡Exito! ', ' Candidato Eliminado');
    });
});

$(document).on('click', '.edit_process', function(e){
    e.preventDefault();
    $.post('{url}', {
        target: 'process',
        category: 'show',
        process: $(this).attr('data'),
        csrfmiddlewaretoken: token
    }, function(data){
        $('#{prefix}_modify_process_modal #name').val(data.name);
        $('#{prefix}_modify_process_modal #date').attr('data-default-date', data.date);
        $('#{prefix}_modify_process').attr('data', data.id);
        $("#{prefix}_modify_process_form #date").dateDropper();
    });

    var modal = $(this);
    var id_modal = '#{prefix}_modify_process_modal';

    function removeModal( hasPerspective ) {
        $(id_modal).removeClass('md-show');

        if( hasPerspective ) {
            $(document.documentElement).removeClass('md-perspective');
        }
    }

    function removeModalHandler() {
        removeModal( $(modal).hasClass('md-setperspective') );
    }

    function closeModal(){
        removeModalHandler();
        if($(modal).hasClass('md-setperspective')) {
            setTimeout( function() {
                $(document.documentElement).addClass('md-perspective');
            }, 25 );
        }
    }

    $(id_modal).addClass('md-show');

    $(document).on('click', '.md-overlay', function(){
        closeModal();
    });
});

$(document).on('click', '#{prefix}_modify_process', function(e){
    e.preventDefault();
    var {prefix}_formData = new FormData($('#{prefix}_modify_process_form')[0]);
    {prefix}_formData.append('process',$(this).attr('data'));
    {prefix}_formData.append('target','process');
    {prefix}_formData.append('category','modify');
    {prefix}_formData.append('csrfmiddlewaretoken', token);
    $.ajax({
		url: '{url}',
		type: 'POST',
		data: {prefix}_formData,
		async: false,
		success: function (data) {
		    $('#{prefix}_modify_process_form')[0].reset();
		    $('.md-overlay').click();
		    $('#{prefix} table').DataTable().ajax.reload();
		    notify('top', 'center', 'fa fa-info', 'info', null, null,'¡Exito! ', ' Proceso Modificado');
		},
	    error: function(XMLHttpRequest, textStatus, errorThrown) {
			notify('top', 'center', 'fa fa-danger', 'danger', null, null,'¡Error! ', ' Información incompleta');
		},
		cache: false,
		contentType: false,
		processData: false
	});
});

$(document).on('click', '#{prefix}_modify_process_cancel', function(e){
   e.preventDefault();
   $('#{prefix}_modify_process_form')[0].reset();
   $('.md-overlay').click();
});

$(document).on('click', '.delete_process', function(e){
    e.preventDefault();
    $.post('{url}',{
        target: 'process',
        category: 'delete',
        process: $(this).attr('data'),
        csrfmiddlewaretoken: token
    },function(data){
        $('#{prefix} table').DataTable().ajax.reload();
        notify('top', 'center', 'fa fa-info', 'info', null, null,'¡Exito! ', ' Proceso Eliminado');
    });
});

$('#{prefix}_new_candidate_form #image').filer({
	limit: 1,
    extensions: ['jpg', 'jpeg', 'png', 'gif', 'psd'],
    changeInput: true,
    showThumbs: true,
    addMore: false,
	captions: {
        button: "<i class='fa fa-image'></i>",
        feedback: "Selecciona una imagen",
        feedback2: "Selecciona la imagen",
        drop: "Suelta la imagen aqui",
        removeConfirmation: "¿Estas seguro de remover la imagen?",
        errors: {
            filesLimit: "Only {{fi-limit}} files are allowed to be uploaded.",
            filesType: "Only Images are allowed to be uploaded.",
            filesSize: "{{fi-name}} is too large! Please upload file up to {{fi-maxSize}} MB.",
            filesSizeAll: "Files you've choosed are too large! Please upload files up to {{fi-maxSize}} MB."
        }
    }
});



var {prefix}_heads = [];

$.post('{url}', {target: "table", category: "initialize", csrfmiddlewaretoken: token}, function (data) {
	$.each(data.data[0], function(k, v) {
        {prefix}_heads.push(k);
    });

	var {prefix}_columns = [];

    for(var i=0; i< {prefix}_heads.length;i++) {
        var cls = ({prefix}_heads[i] == 'Acciones') ? 'disabled-sorting text-right' : '';
        $('#{prefix} table thead tr').append('<th class="' + cls + '">' + {prefix}_heads[i] + '</th>');
        {prefix}_columns.push({
            data: {prefix}_heads[i]
        });
        if ({prefix}_heads[i] == 'Acciones') {prefix}_columns[i]['className'] = 'text-right';
    }

    $('#{prefix} table').DataTable({
		"processing": true,
        "serverSide": true,
        "bDestroy": true,
        "bJQueryUI": true,
        "ajax": {
            'type': 'POST',
            'url': '{url}',
            'data': {
				target: 'table',
				category: 'load',
				csrfmiddlewaretoken: token
            },
        },
	    "columns": {prefix}_columns,
	    "order": [[0, 'asc']],
	    "scrollX": true,
	    "scrollY": "200px",
		"scrollCollapse": true,
        "paging": false,
	    "info": false,
	    "language": {
	        "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
	    }
    });
});
{js}