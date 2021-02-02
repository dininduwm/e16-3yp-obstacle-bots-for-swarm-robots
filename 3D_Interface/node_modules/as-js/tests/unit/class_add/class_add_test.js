(function($) {

    QUnit.module('class.add');

    QUnit.asyncTest('adds class', function(assert) {
        assert.expect(1);

        AS.container.set('assertResult', function(options) {
            assert.ok($('#target').hasClass('selected'));
            QUnit.start();
        });

        $('#btn1').click();

    });

    QUnit.test('throws on empty target', function(assert) {
        assert.expect(1);
        assert.throws(function() {
            $('#btn2').click();
        }, 'class.add empty target');

    });

})(jQuery);
