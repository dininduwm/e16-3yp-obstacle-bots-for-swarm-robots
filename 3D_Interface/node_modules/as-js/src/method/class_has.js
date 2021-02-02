
AS.container.set('class.has', function(options) {

    AS.assertTrue(options, ['class', 'target'], 'class.add');

    var $target = AS.assertSelector(options.target, 'class.add empty target');

    return $target.hasClass(options.class);
});
