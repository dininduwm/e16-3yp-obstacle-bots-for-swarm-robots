
AS.container.set('trigger', function(options) {

    AS.assertTrue(options, ['event'], 'trigger');

    var $obj, arr;

    if (options.selector) {
        $obj = $(options.selector);
        $obj.trigger(options.event);
        return $obj.length;
    } else {
        arr = AS.container.getEventListeners(options.event);
        $(arr).each(function() {
            $(this).trigger(options.event);
        });
    }

});
