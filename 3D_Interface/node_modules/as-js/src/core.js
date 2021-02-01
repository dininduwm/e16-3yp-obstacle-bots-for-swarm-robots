(function(window, $) {

    var AS = window.AS = {};

    AS.debug = false;

    AS.container = {
        _actions: {},
        _listeners: {},
        _bindListeners: []
    };

    AS.container.set = function(name, fn, scope) {
        AS.log({
            msg: 'AS - container - set',
            name: name,
            fn: fn,
            scope: scope
        });
        AS.container._actions[name] = {
            fn: fn,
            scope: scope ? scope : null
        };
    };

    AS.container.remove = function(name) {
        AS.log({
            msg: 'AS - container - remove',
            name: name
        });
        delete AS.container._actions[name];
    };

    AS.container.call = function(name, options) {
        var scope, result;

        AS.log({
            msg: 'AS - container - call',
            name: name,
            options: options
        });

        if (AS.container._actions[name] &&
            typeof AS.container._actions[name].fn &&
            typeof AS.container._actions[name].fn.apply == 'function'
        ) {
            scope = AS.container._actions[name].scope ? AS.container._actions[name].scope : null;

            if (scope) {
                result = AS.container._actions[name].fn.apply(scope, [options]);
            } else {
                result = AS.container._actions[name].fn(options);
            }

            AS.log({
                msg: 'AS - container - call - result',
                name: name,
                result: result,
                options: options
            });

            return result;
        }
    };

    AS.container.getEventListeners = function(eventName) {
        return typeof AS.container._listeners[eventName] != 'undefined'
            ? AS.container._listeners[eventName]
            : [];
    };

    AS.container.addBindListener = function(callback) {
        AS.container._bindListeners.push(callback);
    };

    AS.container.callBindListeners = function(root) {
        var r = root;
        $.each(AS.container._bindListeners, function() {
            this(r);
        })
    };

    AS.log = function() {
        if (AS.debug) {
            console.log(arguments);
        }
    };

    AS.execute = function(dom, cmd, domEvent, result) {
        var $dom = $(dom).first(),
            fn, options, tmp;
        if (cmd == null || typeof cmd == 'undefined') {
            cmd = {};
        }
        if (typeof cmd == 'string') {
            tmp = {};
            tmp[cmd] = null;
            cmd = tmp;
        }
        AS.log({
            msg: 'AS - execute - start',
            dom: dom,
            cmd: cmd
        });
        for (fn in cmd) {
            if (cmd.hasOwnProperty(fn)) {
                options = $.extend(true, {}, cmd[fn]);
                options = options ? options : {};
                options.dom = $dom.get(0);
                options.$dom = $dom;
                options.domEvent = domEvent;
                options.result = options.result ? options.result : result;
                result = AS.container.call(fn, options);
            }
        }

        return result;
    };

    AS.bind = function(root, reset) {
        var $root = root ? $(root) : $('body');
        AS.container.callBindListeners($root);
        $root.find('[data-as]').each(function() {
            var $dom = $(this),
                index = $dom.data('asIndex'),
                stopPropagation = $dom.data('asStopPropagation'),
                preventDefault = $dom.data('asPreventDefault'),
                data = $dom.data('as'),
                eventName, cmd, listenerAdded
            ;

            if (typeof data != 'object') {
                throw new SyntaxError('data-as must be an object');
            }

            index = index ? index : {};
            stopPropagation = typeof stopPropagation == 'undefined' ? true : stopPropagation;
            preventDefault = typeof preventDefault == 'undefined' ? true : preventDefault;

            for (eventName in data) {
                if (data.hasOwnProperty(eventName)) {
                    if (typeof AS.container._listeners[eventName] == 'undefined') {
                        AS.container._listeners[eventName] = [];
                    }
                    listenerAdded = false;
                    $(AS.container._listeners[eventName]).each(function() {
                        if (this == $dom.get(0)) {
                            listenerAdded = true;
                            return false;
                        }
                    });
                    if (!listenerAdded) {
                        AS.container._listeners[eventName].push($dom.get(0));
                    }

                    cmd = data[eventName];

                    if (reset) {
                        $dom.off(eventName);
                    } else {
                        if (index[eventName]) {
                            return;
                        }
                    }

                    index[eventName] = 1;
                    $dom.data('asIndex', index);

                    $dom.on(eventName, (function(c) {
                        return function(e) {
                            if (stopPropagation) {
                                e.stopPropagation();
                            }
                            if (preventDefault) {
                                e.preventDefault();
                            }
                            AS.execute($dom, c, e);
                        }
                    })(cmd));

                }
            }
        });
    };

    AS.prepareOptions = function(options, spec) {
        var name, value, i = 0, altName;
        for (name in spec) {
            if (spec.hasOwnProperty(name)) {
                value = options[name];

                while (typeof value == 'undefined') {
                    altName = spec[name][i++];
                    value = options[altName];
                }

                if (typeof value != 'undefined') {
                    options[name] = value;
                }
            }
        }
    };

    AS.assertTrue = function(options, names, origin) {
        var i, name;
        for (i in names) {
            if (names.hasOwnProperty(i)) {
                name = names[i];
                if (!options[name]) {
                    throw new SyntaxError(origin + ' not allowed null option "' + name + '"');
                }
            }
        }
    };

    AS.assertDefined = function(options, names, origin) {
        var i, name;
        for (i in names) {
            if (names.hasOwnProperty(i)) {
                name = names[i];
                if (typeof options[name] == 'undefined') {
                    throw new SyntaxError(origin + ' not allowed undefined option ' + name);
                }
            }
        }
    };

    AS.assertSelector = function(selector, msg) {
        var jq = $(selector);

        if (jq.length == 0) {
            throw new SyntaxError(msg);
        }

        return jq;
    };

})(window, jQuery);
