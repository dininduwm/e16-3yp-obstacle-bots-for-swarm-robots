AS.container.set('fadeIn', function(options) {

    options.type = 'in';
    AS.execute(options.dom, {
        fade: options
    }, options.domEvent);

});
