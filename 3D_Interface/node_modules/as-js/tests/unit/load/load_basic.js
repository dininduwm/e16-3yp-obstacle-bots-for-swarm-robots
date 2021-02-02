(function($) {

    QUnit.module('load:basic', {
        setup: function() {
            $.mockjaxClear();
        }
    });

    QUnit.asyncTest('puts loaded content to result of next call', function(assert) {
        assert.expect(2);

        var expectedResult = '<p>response</p>';

        $.mockjax({
            logging: false,
            url: 'data1.json',
            response: function() {
                assert.ok(true);
                this.responseText = expectedResult;
            }
        });

        AS.container.set('assertResult', function(options) {
            QUnit.start();
            assert.equal(options.result, expectedResult);
        });

        $('#btn1').click();

    });

    QUnit.asyncTest('loads different content', function(assert) {
        assert.expect(4);

        var count = 0,
            firstResponse = '<p>First</p>',
            secondResponse = '<p>Second</p>',
            $btn = $('#btn1')
            ;

        $.mockjax({
            logging: false,
            url: /.*/,
            response: function() {
                if (count == 0) {
                    assert.ok(true);
                    this.responseText = firstResponse;
                } else if (count == 1) {
                    assert.ok(true);
                    this.responseText = secondResponse;
                } else {
                    assert.ok(false);
                }
            }
        });

        AS.container.set('assertResult', function(options) {
            if (count == 0) {
                assert.equal(options.result, firstResponse);
                count++;
                setTimeout(function() {
                    $btn.click();
                }, 100);
            } else if (count == 1) {
                assert.equal(options.result, secondResponse);
                QUnit.start();
            } else {
                assert.ok(false);
            }
        });

        $btn.click();

    });

    QUnit.asyncTest('buffers multiple events into one', function(assert) {
        assert.expect(2);

        var expectedResult = '<p>response</p>';

        $.mockjax({
            logging: false,
            url: 'data2.json',
            response: function() {
                assert.ok(true);
                this.responseText = expectedResult;
            }
        });

        AS.container.set('assertResult', function(options) {
            QUnit.start();
            assert.equal(options.result, expectedResult);
        });

        $('#btn2').click();
        $('#btn2').click();
        $('#btn2').click();

    });

    QUnit.asyncTest('adds data to request', function(assert) {
        assert.expect(2);

        $.mockjax({
            url: 'data3.json',
            logging: false,
            response: function(settings) {
                assert.equal(settings.data.a, "aaa");
                assert.equal(settings.data.b, "bbb");
                this.responseText = '';
                QUnit.start();
            }
        });
        $.mockjax({
            url: /.*/,
            response: function(settings) {
                assert.ok(false, 'mismatched url: '+settings.url);
            }
        });

        $('#btn3').click();

    });

    QUnit.test('calls block on body', function(assert) {
        assert.expect(2);

        $.mockjax({
            logging: false,
            url: /.*/,
            responseText: ''
        });

        $.blockUI = function() {
            assert.ok(true);
            QUnit.start();
        };

        $.unblockUI = function() {
            assert.ok(true);
            QUnit.start();
        };

        QUnit.stop(2);

        $('#btn4').click();

    });

})(jQuery);
