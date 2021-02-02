(function($) {

    QUnit.module('core:bind');

    QUnit.test('binds to all', function(assert) {
        assert.expect(2*4);

        var expectedNumber;

        AS.container.set('dummy', function(options) {
            assert.equal(options.dom.id, 'b'+expectedNumber);
            assert.equal(options.a, expectedNumber);
            QUnit.start();
        });

        AS.bind();

        for (expectedNumber=1; expectedNumber<=4; expectedNumber++) {
            QUnit.stop();
            $('#b'+expectedNumber).click();
        }

    });


    QUnit.test('does not delete existing event listeners', function(assert) {

        assert.expect(2);

        AS.container.set('dummy', function(options) {
            assert.ok(true);
            QUnit.start();
        });

        $('#b1').click(function() {
            QUnit.ok(true);
            QUnit.start();
        })

        QUnit.stop();
        QUnit.stop();

        AS.bind();

        $('#b1').click();
    });

    QUnit.test('does delete existing event listeners', function(assert) {

        assert.expect(1);

        AS.container.set('dummy', function(options) {
            assert.ok(true);
            QUnit.start();
        });

        $('#b1').click(function() {
            QUnit.ok(false);
            QUnit.start();
        })

        QUnit.stop();

        AS.bind(null, true);

        $('#b1').click();
    });

})(jQuery);
