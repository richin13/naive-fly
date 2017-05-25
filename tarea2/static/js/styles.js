/**
 * Created by ricardo on 5/24/17.
 */
$(document).ready(function () {
    $('#btn-form-submit').click(function (e) {
        var $form = document.getElementById('styles-form');

        var ca = parseInt($form.c7.value) + parseInt($form.c11.value) + parseInt($form.c15.value) + parseInt($form.c19.value) + parseInt($form.c31.value) + parseInt($form.c35.value);
        var ec = parseInt($form.c5.value) + parseInt($form.c9.value) + parseInt($form.c13.value) + parseInt($form.c17.value) + parseInt($form.c25.value) + parseInt($form.c29.value);
        var ea = parseInt($form.c4.value) + parseInt($form.c12.value) + parseInt($form.c24.value) + parseInt($form.c28.value) + parseInt($form.c32.value) + parseInt($form.c36.value);
        var or = parseInt($form.c2.value) + parseInt($form.c10.value) + parseInt($form.c22.value) + parseInt($form.c26.value) + parseInt($form.c30.value) + parseInt($form.c34.value);

        $form.ca_.value = ca;
        $form.ec_.value = ec;
        $form.ea_.value = ea;
        $form.or_.value = or;
    });
});