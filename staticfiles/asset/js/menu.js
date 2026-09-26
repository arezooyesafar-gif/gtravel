(function ($) {
    "use strict";

    $(function () {
        const $tourButton = $("#nav #submenuactive");
        const $hotelButton = $("#nav #hotelmenuactive");

        const $tourMenu = $("#submenu");
        const $hotelMenu = $("#hotel-submenu");

        $tourButton.on("click.menu", function (event) {
            event.preventDefault();
            event.stopPropagation();

            $hotelMenu.stop(true, true).slideUp(500);
            $tourMenu.stop(true, true).slideToggle(500);
        });

        $hotelButton.on("click.menu", function (event) {
            event.preventDefault();
            event.stopPropagation();

            $tourMenu.stop(true, true).slideUp(500);
            $hotelMenu.stop(true, true).slideToggle(500);
        });

        $tourMenu.add($hotelMenu).on("click.menu", function (event) {
            event.stopPropagation();
        });

        $(document).on("click.menu", function () {
            $tourMenu
                .add($hotelMenu)
                .stop(true, true)
                .slideUp(500);
        });
    });

})(jQuery);