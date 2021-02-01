
AS.container.set('stopPropagation', function(options) {
    if (options.domEvent && typeof option.domEvent.stopPropagation == 'function') {
        option.domEvent.stopPropagation();
    }
});
