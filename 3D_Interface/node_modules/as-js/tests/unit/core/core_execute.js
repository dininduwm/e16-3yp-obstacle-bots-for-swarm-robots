(function($) {

    QUnit.module('core:execute');

    QUnit.test('calls all functions with specified options', function(assert) {
        assert.expect(6);

        var rank = 1;

        var option1 = {
            a: 1
        };
        var option2 = {
            b: 2
        };
        AS.container.set('first', function(options) {
            assert.equal(rank++, 1);
            assert.ok(options);
            assert.equal(options.a, option1.a);
        });
        AS.container.set('second', function(options) {
            assert.equal(rank++, 2);
            assert.ok(options);
            assert.equal(options.b, option2.b);
        });

        AS.execute(null, {
            'first': option1,
            'second': option2
        });
    });

    var expectedResult = { a: 1 };

    QUnit.test('calls next function with previous result', function(assert) {
        assert.expect(1);

        AS.container.set('first', function(options) {
            return expectedResult;
        });
        AS.container.set('second', function(options) {
            assert.equal(options.result, expectedResult);
        });

        AS.execute(null, {
            'first': null,
            'second': null
        });
    });


})(jQuery);
