
(function($) {

    QUnit.module('core:container');

    QUnit.test('set function w/out scope', function(assert) {
        assert.expect(3);

        var name = 'new.method';
        var fn = function() { var x = 1; };
        AS.container.set(name, fn);

        assert.ok(AS.container._actions[name]);
        assert.equal(AS.container._actions[name].fn, fn);
        assert.equal(AS.container._actions[name].scope, null);
    });

    QUnit.test('set function with scope', function(assert) {
        assert.expect(3);

        var name = 'new.method';
        var fn = function() { };
        var scope = {a:1};

        AS.container.set(name, fn, scope);

        assert.ok(AS.container._actions[name]);
        assert.equal(AS.container._actions[name].fn, fn);
        assert.equal(AS.container._actions[name].scope, scope);
    });

    QUnit.test('remove function', function(assert) {
        assert.expect(2);

        var name = 'new.method';
        var fn = function() { };
        AS.container.set(name, fn);

        assert.ok(AS.container._actions[name]);

        AS.container.remove(name);

        assert.equal(AS.container._actions[name], undefined);
    });

    QUnit.test('call function w/out scope', function(assert) {
        assert.expect(1);

        var expectedOptions = {
            a: 1
        };
        var name = 'new.method';
        var fn = function(actualOptions) {
            assert.equal(actualOptions, expectedOptions);
        };

        AS.container.set(name, fn);
        AS.container.call(name, expectedOptions);
    });

    QUnit.test('call function with scope', function(assert) {
        assert.expect(1);

        var expectedOptions = {
            a: 1
        };
        var obj = {
            b: 2,
            fn: function(actualOptions) {
                assert.equal(actualOptions, expectedOptions);
            }
        }
        var name = 'new.method';

        AS.container.set(name, obj.fn, obj);
        AS.container.call(name, expectedOptions);
    });

})(jQuery);
