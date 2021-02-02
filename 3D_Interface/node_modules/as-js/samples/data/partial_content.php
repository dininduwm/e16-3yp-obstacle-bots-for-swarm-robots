<?php
header('Cache-Control: no-cache, no-store, must-revalidate'); // HTTP 1.1.
header('Pragma: no-cache'); // HTTP 1.0.
header('Expires: 0'); // Proxies.

if ($_GET['sleep']) {
    $sleep = intval($_GET['sleep']);
    if ($sleep > 1 && $sleep < 5000) {
        usleep($sleep*1000);
    }
}
?>
<div data-id="partial_content">
    <p><?php print date('Y-m-d H:i:s'); ?></p>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum tincidunt eleifend massa, non bibendum lacus blandit vel.</p>
    <p>Nam nibh diam, scelerisque et nibh eu, dictum placerat tortor. Etiam et leo quis orci tempor congue. Aenean hendrerit mauris iaculis nibh vestibulum ultricies. Cras dapibus urna dui, in imperdiet erat consequat ut. Aliquam dictum massa enim, eu imperdiet dui tempus sed. Sed commodo vestibulum ornare. </p>
    <p>Suspendisse potenti. Sed sed ante quis augue iaculis volutpat. Donec et arcu quam. Vestibulum id nibh ultrices nibh volutpat bibendum. Morbi sed magna commodo velit ultricies aliquet quis sed enim. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla facilisis, nibh vel finibus tristique, metus eros consequat nibh, vel interdum tellus ex ut mi. </p>
</div>