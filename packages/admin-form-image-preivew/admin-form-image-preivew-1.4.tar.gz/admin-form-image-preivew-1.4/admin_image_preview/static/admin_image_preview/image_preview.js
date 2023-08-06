(function(){
    function set_previews() {
        let image_fields = document.querySelectorAll('form .form-row input[accept="image/*"]');
        if(!image_fields.length) {
            console.log('No image fields found in form => form .form-row input[accept="image/*"]');
            return;
        }
        //localStorage.setItem('test_image_preivew', 1);
        if(localStorage.getItem('test_image_preivew')){
            test_usability();
        }
        //localStorage.removeItem('test_image_preivew');

        function test_usability(){
            let cnt = image_fields.length;
            if(!cnt){
                console.log('No file inputs with accept="image/*" were found in form.');
                return;
            }

            let subject = ' Image Preview => ';
            let message = 'You should see an image preview after changing any of '+cnt+' file input having accept="image/*"';
            let image_links = document.querySelector('a.deletelink');
            if(image_links){
                let upload_field_conrtainers = document.querySelector('p.file-upload');
                let cnt1 = upload_field_conrtainers.length;
                let cnt2 = upload_field_conrtainers.querySelector('a').length;
                if(cnt2 == cnt){
                    console.log('Success:' + subject, 'edit mode');
                }
                else{
                    let message1 = 'Preview only available for ';
                    let message2 = '  file inputs having accept="image/*" enclosed by <p class="file-upload"> ';
                    if(cnt1 == cnt){
                        message2 += ' and containing link (a) to image';
                        message = message1 + cnt2 + message;
                    }
                    else{
                        message = message1 + cnt1 + message;
                    }
                    console.log('Failure:' + subject, 'edit mode');
                }
            }
            else{
                console.log('Success:' + subject, 'create mode');
            }
            console.log(message);
        }

        function readFileShowImage(preview_container, input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (ev1) {
                    let image_url = ev1.target.result;
                    preview_container.innerHTML = (`<img src="${image_url}" style="max-height:20vh;" />`);
                };
                reader.readAsDataURL(input.files[0]);
            } else {
                preview_container.innerHTML = ('');
            }
        }
        for (let file_el of image_fields) {
            if (file_el.name.indexOf('__prefix__') > -1) { return; }
            let parent_obj = file_el.parentNode;
            let preview_container = parent_obj.querySelector('.image-preview');
            if(!preview_container){
                preview_container = document.createElement('div');
                preview_container.setAttribute('class', 'image-preview');
                preview_container.setAttribute('style', 'padding-top:10px');
                parent_obj.appendChild(preview_container);
                preview_container = parent_obj.querySelector('.image-preview');
            }
            let link_el = parent_obj.querySelector('a');
            if(link_el){
                let link_href = link_el.getAttribute('href');
                preview_container.innerHTML = (`<a href="${link_href}" target="_blank"><img src="${link_href}" style="max-height:20vh;" /></a>`);
            }
            else{
                preview_container.innerHTML = ('');
            }
            file_el.addEventListener("change", function(ev){
                readFileShowImage(preview_container, file_el);
            }, true);
        }
    }
    set_previews();
})();