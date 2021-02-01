
AS.container.set('eval', function(options) {

    AS.assertTrue(options.exp);

    return eval(options.exp);

});
