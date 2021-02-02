
AS.container.set('load', function(options) {
    AS.assertTrue(options, ['url'], 'load');

    var ajaxOptions = options.ajaxOptions || {},
        blockOptions, $block,
        name, method, selector, args, $jq, m, value,
        buffer, timer, $dom
    ;

    AS.log({
        msg: 'AS - load',
        options: options
    });

    if (options.block) {
        AS.log({
            msg: 'AS - load - block',
            block: options.block
        });
        blockOptions = options.blockOptions || {};
        if (options.block == true && typeof $.blockUI == 'function') {
            $.blockUI(blockOptions);
        } else {
            $block = $(options.block);
            if ($block.length && typeof $block.block == 'function') {
                $block.block(blockOptions);
            }
        }
    }

    if (options.data) {
        ajaxOptions.data = ajaxOptions.data || {};
        for (name in options.data) {
            if (options.data.hasOwnProperty(name)) {
                selector = options.data[name][0];
                method = options.data[name][1];
                args = options.data[name][2] || [];
                $jq = $(selector);
                m = $jq[method];
                if (!m) {
                    throw new SyntaxError('jQuery of selector "' + selector + '" does not have a method "' + method + '"');
                }
                value = m.apply($jq, args);
                ajaxOptions.data[name] = value;
                AS.log({
                    msg: 'AS - load - data',
                    selector: selector,
                    method: method,
                    args: args,
                    value: value
                })
            }
        }
    }

    ajaxOptions.success = function(data) {
        AS.log({
            msg: 'AS - load - success',
            options: options,
            data: data
        });
        if (options.success) {
            AS.execute(options.dom, options.success, null, data);
        }
    };

    ajaxOptions.complete = function() {
        AS.log({
            msg: 'AS - load - complete',
            options: options
        });
        if ($block && typeof $block.unblock == 'function') {
            $block.unblock();
        }
        if (typeof $.unblockUI == 'function') {
            $.unblockUI();
        }
        if (options.complete) {
            AS.execute(options.dom, options.complete);
        }
    };

    ajaxOptions.error = function(jqXHR, textStatus, errorThrown) {
        AS.log({
            msg: 'AS - load - error',
            textStatus: textStatus,
            errorThrown: errorThrown,
            jqXHR: jqXHR,
            options: options
        });
        if (options.error) {
            AS.execute(options.dom, options.error);
        }
    };

    buffer = options.buffer || 0;
    buffer = parseInt(buffer, 10);

    if (buffer < 1) {
        $.ajax(options.url, ajaxOptions);
    } else {
        $dom = options.$dom || $('body');
        timer = $dom.data('asLoadTimer');
        clearTimeout(timer);
        timer = setTimeout(function() {
            $.ajax(options.url, ajaxOptions);
        }, buffer);
        $dom.data('asLoadTimer', timer);
    }

});
