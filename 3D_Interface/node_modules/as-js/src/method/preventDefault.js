
AS.container.set('preventDefault', function(options) {
    if (options.domEvent && typeof option.domEvent.preventDefault == 'function') {
        option.domEvent.preventDefault();
    }
});
