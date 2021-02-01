
AS.container.set('bs.modal.hide', function(options) {
    AS.assertTrue(options, ['selector'], 'bs.modal.close');

    $(options.selector).modal('hide');
});
