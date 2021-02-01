
AS.container.set('block', function(options) {
    var $target;

    if (typeof options.target != 'undefined') {
        $target = $(options.target);
        if (typeof $target.block == 'function') {
            $target.block(options.options);
        }
    } else {
        if (typeof $.blockUI == 'function') {
            $.blockUI();
        }
    }
});
