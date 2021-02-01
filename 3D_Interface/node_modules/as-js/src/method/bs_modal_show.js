
AS.container.set('bs.modal.show', function(options) {

    if (!options.target) {
        options.target = $(options.dom);
    }

    var $modal = $(options.target);

    if ($modal.length == 0) {
        throw new SyntaxError('bs.modal.show missing content or not html');
    }

    AS.bind($modal);

    if (typeof $modal.modal != 'function') {
        throw new SyntaxError('bs.modal.show missing modal function - bootstrap not loaded?');
    }

    if ($modal.closest('body').length == 0) {
        $('body').append($modal);
    }

    $modal.modal('show');

    if (options.removeOnClose || typeof options.removeOnClose == 'undefined') {
        $modal.on('hidden.bs.modal', function() {
            $(this).remove();
        });
    }
});
