
AS.container.set('fade', function(options) {

    AS.assertTrue(options, ['type'], 'fade');

    if (options.type != 'in' && options.type != 'out') {
        throw new SyntaxError('Fade type must be in or out');
    }

    if (typeof options.target == 'undefined') {
        options.target = options.dom;
    }
    if (typeof options.duration == 'undefined') {
        options.duration = 300;
    }

    var oldComplete = options.complete,
        type = options.type,
        $target
    ;

    delete options.type;

    options.complete = function() {
        AS.log({
            msg: 'AS - fadeIn - complete',
            options: options
        });
        if (oldComplete) {
            AS.execute(options.dom, oldComplete);
        }
    };

    $target = AS.assertSelector(options.target, 'fade empty target');

    if (type == 'in') {
        $target.fadeIn(options);
    } else {
        $target.fadeOut(options);
    }
});
