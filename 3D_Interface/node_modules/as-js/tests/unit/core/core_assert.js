(function($) {

    QUnit.module('core:assert');

    QUnit.test('assertTrue does nothing if true', function(assert) {
        assert.expect(1);
        var options = {
            a: 123
        };
        AS.assertTrue(options, ['a']);
        assert.equal(options.a, 123);
    });

    QUnit.test('assertTrue throws on null', function(assert) {
        assert.expect(2);
        var options = {
            a: null
        };
        assert.throws(function() {
            AS.assertTrue(options, ['a']);
        })
        assert.equal(options.a, null);
    });

    QUnit.test('assertDefined does nothing if null', function(assert) {
        assert.expect(1);
        var options = {
            a: null
        };
        AS.assertDefined(options, ['a']);
        assert.equal(options.a, null);
    });

    QUnit.test('assertDefined throws when missing', function(assert) {
        assert.expect(2);
        var options = {};
        assert.throws(function() {
            AS.assertDefined(options, ['a']);
        });
        assert.ok(typeof options.a == "undefined");
    });

})(jQuery);
