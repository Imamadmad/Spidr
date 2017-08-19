function readUrl(input) {
    console.log(input.files)
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#uploaded-file')
                .attr('src', e.target.result);
            $('#uploaded-file').attr('style', "display:block;")
                .width("100%");
        };

        reader.readAsDataURL(input.files[0]);
    }
}