
AS.container.set('data.set', function(options) {
    AS.assertTrue(options, ['data'], 'data.set');

    var $dom = options.selector ? $(options.selector) : options.$dom,
        name, value
        ;

    if (typeof options.data != 'object') {
        throw new SyntaxError('data.set option.data must be an object');
    }

    for (name in options.data) {
        if (options.data.hasOwnProperty(name)) {
            value = options.data[name];
            $dom.data(name, value);
        }
    }
});
