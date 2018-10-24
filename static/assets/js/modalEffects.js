var ModalEffects = (function() {

	function init() {

	    $(document).on('click', '.md-trigger', function(){
	        var modal = $(this);
	        var id_modal = '#' + $(this).attr('data-modal');

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



	}

	init();

})();