/**
 * Created by ricardo on 5/23/17.
 */
$(document)
    .ready(function () {
        // fix main menu to page on passing
        $('.main.menu').visibility({
            type: 'fixed'
        });

        // easter egg
        var messages = [
            '<a href="http://www.feedthechildren.org/"><i class="child icon"></i>Help the children!</a>',
            'Made with Flask, SemanticUI, <i class="coffee icon"></i> and passion'
        ];
        var s = _.sample(messages);
        $('#footer-easter-egg').html(s);

        // Init dropdowns
        $('.ui.dropdown').dropdown();
    })
;