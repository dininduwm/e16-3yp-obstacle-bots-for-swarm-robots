
AS.container.set('bs.modal.load', function(options) {

    AS.assertTrue(options, ['url'], 'bs.modal.load');

    var arg = $.extend(true, {}, options);
    if (typeof arg.success == 'undefined') {
        arg.success = {};
    }
    arg.success.html = {
        success: {
            'bs.modal.show': null
        }
    };

    AS.execute(options.dom, {
        load: arg
    }, options.domEvent);

});
