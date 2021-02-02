
AS.container.set('if', function(options) {

    AS.assertTrue(options, ['arg'], 'if');

    options.then = typeof options.then == 'undefined' ? {} : options.then;
    options.else = typeof options.else == 'undefined' ? {} : options.else;

    var target = AS.execute(options.dom, options.arg)
        ? options.then
        : options.else
    ;

    return AS.execute(options.dom, target);

});
