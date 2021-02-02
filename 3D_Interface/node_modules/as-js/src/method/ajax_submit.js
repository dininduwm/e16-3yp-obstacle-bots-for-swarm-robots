
AS.container.addBindListener(function(root) {
    $(root).find('form[data-ajax-form]').each(function() {
        var _this = this,
            $form = $(_this),
            options = $form.data('dataAjaxForm'),
            $parent = $form.parent(),
            beforeSubmit, success
        ;
        if (!options) {
            options = {
                target: $form,
                replaceTarget: true
            };
        }

        beforeSubmit = options.beforeSubmit;
        success = options.success;

        options.beforeSubmit = function() {
            if (typeof $.blockUI == 'function') {
                $.blockUI();
            }
            if (beforeSubmit) {
                beforeSubmit.apply(this, arguments);
            }
        };

        options.success = function(responseText, statusText, xhr, jqForm) {
            AS.bind($parent);
            if (typeof $.unblockUI == 'function') {
                $.unblockUI();
            }
            if (typeof success == 'function') {
                success.apply(this, arguments);
            } else if (typeof success == 'object') {
                AS.execute(jqForm, success);
            }
        };

        setTimeout(function() {
            $form.ajaxForm(options);
        }, 100);
    });
});

AS.container.set('ajax.submit', function(options) {

    var $form, opt, $target, $block, blockOptions, $parent;

    AS.ajaxSubmit = {
        setDefaultButton: function(frm, btn) {
            var $frm = $(frm).first(),
                $btn = $(btn).first();

            $frm.on('submit', function(e) {
                var $frm = $(this);
                if (!$frm.data('asSubmit')) {
                    e.preventDefault();
                    e.stopPropagation();
                    setTimeout(function() {
                        $btn.click();
                    }, 20);
                    return false;
                }
            })
        }
    };

    if (options.form) {
        $form = $(options.form);
    } else {
        $form = options.$dom.closest('form');
    }

    if (!$form || !$form.length) {
        throw new SyntaxError('No form for ajax.submit');
    }

    $form = $form.first();

    $form.data('asSubmit', true);

    opt = typeof 'options.options' == 'object' ? options.options : {
        target: $form,
        replaceTarget: true
    };

    if (options.block) {
        if (options.block === true && typeof $.blockUI == 'function') {
            $.blockUI(options.blockOptions);
        } else if (options.block == '$target') {
            $block = $target;
        } else {
            $block = $(options.block);
        }
        if ($block && typeof $block.block == 'function') {
            $block.block(options.blockOptions)
        }
    }

    $target = $(opt.target);
    $parent = $target.parent();

    opt.success = function(response, statusText, jqXHR, jqForm) {
        AS.bind($parent);
        if (typeof $form.unblock == 'function') {
            $form.unblock();
        }
        if (options.block && typeof $.unblockUI == 'function') {
            $.unblockUI();
        }
        if ($block && typeof $block.unblock == 'function') {
            $block.unblock();
        }

        if (options.success) {
            AS.execute(options.dom, options.success, null, jqForm);
        }
    };

    $form.ajaxSubmit(opt);
});
