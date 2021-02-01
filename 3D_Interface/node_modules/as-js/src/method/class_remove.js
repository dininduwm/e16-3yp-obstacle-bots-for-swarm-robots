
AS.container.set('class.remove', function(options) {

    AS.assertTrue(options, ['class', 'target'], 'class.add');

    var $target = AS.assertSelector(options.target, 'class.add empty target');

    $target.removeClass(options.class);

    if (options.success) {
        AS.execute(options.dom, options.success);
    }

    return $target.length;
});
