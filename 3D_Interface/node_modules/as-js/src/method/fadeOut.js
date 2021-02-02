AS.container.set('fadeOut', function(options) {

    options.type = 'out';
    AS.execute(options.dom, {
        fade: options
    }, options.domEvent);

});
