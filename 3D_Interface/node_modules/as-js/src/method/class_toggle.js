
AS.container.set('class.toggle', function(options) {

    AS.assertTrue(options, ['target'], 'class.toggle');
    AS.assertDefined(options, ['class'], 'class.toggle');

    var $target = AS.assertSelector(options.target, 'class.toggle empty target'),
        $parent, $children, result
        ;

    if (options.parent) {
        $parent = options.parent === true ? $target.parent() : $(options.parent);
        $children = options.children ? $parent.find(options.children) : $parent.children();
        $children.removeClass(options.class);
        $target.addClass(options.class);
    } else {
        $target.toggleClass(options.class);
    }

    return $target;
});
