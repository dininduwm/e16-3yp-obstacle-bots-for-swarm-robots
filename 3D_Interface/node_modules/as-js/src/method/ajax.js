
$(function() {
    function xReload(xhr) {
        var value = xhr.getResponseHeader('X-AS-Reload');
        if (value) {
            value = parseInt(value, 10);
            if (value && value > 0) {
                if (typeof $.blockUI == 'function') {
                    $.blockUI();
                }
                setTimeout(function() {
                    window.location.reload()
                }, value);
            }
        }
    }

    function xExecute(xhr) {
        var header = xhr.getResponseHeader('X-AS-Execute'),
            json = header ? JSON.parse(header) : null
            ;
        json = typeof json == 'string' ? [json] : json;
        $(json).each(function(index, value) {
            if (typeof value.dom != 'undefined' && value.cmd != 'undefined') {
                AS.execute(value.dom, value.cmd, $.Event('click'));
            }
        });
    }

    function xTrigger(xhr) {
        var header = xhr.getResponseHeader('X-AS-Trigger'),
            json = header ? JSON.parse(header) : null
            ;
        json = typeof json == 'string' ? [json] : json;
        $(json).each(function(index, value) {
            if (typeof value.event != 'undefined') {
                AS.execute('body', {
                    trigger: {
                        event: value.event,
                        selector: value.selector
                    }
                }, $.Event('click'));
            }
        });
    }

    $(document).ajaxComplete(function(event, xhr, options) {
        xReload(xhr);
        xExecute(xhr);
        xTrigger(xhr);
    });

});
