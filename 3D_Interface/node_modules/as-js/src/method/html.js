
AS.container.set('html', function(options) {
    AS.assertDefined(options, ['result']);

    var html = typeof options.result == 'object' ? options.result.body : options.result,
        $result,
        $target
    ;

    if (html.trim().indexOf('<') != 0) {
        html = '<span>' + html + '</span>';
    }
    $result = $(html);

    if (options.target) {
        $target = $(options.target);
    } else {
        $target = $('body');
        options.append = true;
    }

    if ($result.length == 0) {
        throw new SyntaxError('html not valid - must be enclosed in an html tag')
    }

    if (options.append) {
        $target.append($result);
    } else {
        $target.html($result);
    }
    AS.bind($target);

    if (options.success) {
        AS.execute($result, options.success);
    }
    if (options.complete) {
        AS.execute($result, options.complete);
    }

});
