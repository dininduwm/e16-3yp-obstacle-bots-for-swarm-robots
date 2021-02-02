Html function
=============

Options
-------

 * result - required, string or object. The html to set to dom. If object, html string must be in the ```body``` property.
 * target - optional, string or jQuery. Target where to set the html result to. If empty, the content will be added at the end of document body.
 * append - optional, bool, default false. If true content will be added as last child of ```target```, if true ```target``` will be emptied first.

**Note** - content must be wrapped in an html tag, so plain text is not valid.

HTML Example
------------

``` html
<button type="button" data-as='
    "click": {
        "html": {
            "result": "<p>Some html</p>",
            "target": "#div"
        }
    }
'>Click me</button>
```
