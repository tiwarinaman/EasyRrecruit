CKEDITOR.replace('education');
CKEDITOR.plugins.addExternal('abbr', '/myplugins/abbr/', 'plugin.js');


CKEDITOR.replace('education', {
    extraPlugins: 'abbr'
});

CKEDITOR.replace('qualification');
CKEDITOR.plugins.addExternal('abbr', '/myplugins/abbr/', 'plugin.js');


CKEDITOR.replace('qualification', {
    extraPlugins: 'abbr'
});

CKEDITOR.replace('description');
CKEDITOR.plugins.addExternal('abbr', '/myplugins/abbr/', 'plugin.js');


CKEDITOR.replace('description', {
    extraPlugins: 'abbr'
});