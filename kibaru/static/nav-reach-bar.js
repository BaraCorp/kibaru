    $(function () {
        $('body, .navbar-collapse form[role="search"] button[type="reset"]').on('click keyup', function(event) {
            if (event.which == 27 && $('.navbar-collapse form[role="search"]').hasClass('active') ||
                $(event.currentTarget).attr('type') == 'reset') {
                closeSearch();
            }
        });
        function closeSearch() {
            var $form = $('.navbar-collapse form[role="search"].active')
            $form.find('input').val('');
            $form.removeClass('active');
        }
        $(document).on('click', '.navbar-collapse form[role="search"]:not(.active) button[type="submit"]', function(event) {
            event.preventDefault();
            var $form = $(this).closest('form'),
                $input = $form.find('input');
            $form.addClass('active');
            $input.focus();

        });
        $(document).on('click', '.navbar-collapse form[role="search"].active button[type="submit"]', function(event) {
            var $form = $(this).closest('form'),
                $input = $form.find('input');
            // Stop form from submitting normally
            event.preventDefault();
            var val_ = $input.val();
            console.log(typeof val_)
            if (val_ == ''){
                console.log("OH NO!!!");
            } else {
                console.log(val_)
                $form.submit();
            }
        });
    });