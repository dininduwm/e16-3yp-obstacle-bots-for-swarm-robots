(function($) {

    QUnit.module('core:prepareOptions');

    QUnit.test('does nothing if property set to null', function(assert) {
        assert.expect(1);
        var options = {
            result: null
        };
        AS.prepareOptions(options, {
            target: ['result', '$dom', 'dom']
        });
        assert.equal(options.result, null);
    });

    QUnit.test('does nothing if property set', function(assert) {
        assert.expect(1);
        var options = {
            result: 123
        };
        AS.prepareOptions(options, {
            target: ['result', '$dom', 'dom']
        });
        assert.equal(options.result, 123);
    });

    QUnit.test('sets first property', function(assert) {
        assert.expect(1);
        var options = {
            $dom: 111,
            dom: 222
        };
        AS.prepareOptions(options, {
            target: ['result', '$dom', 'dom']
        });
        assert.equal(options.target, 111);
    });

    QUnit.test('sets second property', function(assert) {
        assert.expect(1);
        var options = {
            dom: 222
        };
        AS.prepareOptions(options, {
            target: ['result', '$dom', 'dom']
        });
        assert.equal(options.target, 222);
    });

})(jQuery);
