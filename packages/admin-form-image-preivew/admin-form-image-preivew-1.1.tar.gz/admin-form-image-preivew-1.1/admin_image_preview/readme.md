Installation
----------------------------------------------------------------

1. pip install admin_from_image_preview
2. in settings.py append following line

INSTALLED_APPS = INSTALLED_APPS + ['admin_from_image_preview']
----------------------------------------------------------------
Usability:
----------------------------------------------------------------

Only works only for image fields like
<input type="file" accept="image/*">
additional attributes do not matter but it must have type="file" and accept="image/*

because this plugin reads only
let image_fields = $('form .form-row input[accept="image/*"]'); => line 2 in image_preview.js

----------------------------------------------------------------

Also after saving the form, when we open same form record by default django updates

<input type="file" accept="image/*">

to

<p class="file-upload">
    Currently: <a href="/someimageurl">something</a> <br>
    Change: <input type="file" accept="image/*">
</p>

tested for Django-admin 2, expected to be same for django 3 and 4
If its same case for you then the plugin should work for you
----------------------------------------------------------------
Test manually:
----------------------------------------------------------------

1. Write follwing statement in console (Guide to console => https://developer.chrome.com/docs/devtools/console/javascript/)
localStorage.setItem('test_image_preivew', 1);
2. press enter
3. open/refresh any django admin form

If module successfully loaded then whenever you open any django admin form (in create/edit mode)

You must be able see in colnsole
1. Success: Image Preview
or
2. Failure: Image Preview

After testing
write follwing statement in console
localStorage.removeItem('test_image_preivew');



