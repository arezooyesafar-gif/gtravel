function changeDatePrice(price, opration, priceCurrency, infantPrice, baseCurrency) {
    priceCurrency = priceCurrency || 'تومان';
    baseCurrency = baseCurrency || 'تومان';
    var adj = parseInt(price) || 0;
    var infAdj = parseInt(infantPrice) || 0;

    function applyAdj(oldVal, adjVal, op) {
        if (op === 'افزایش' || op === 'طبق پکیج اصلی') return oldVal + adjVal;
        if (op === 'کاهش') return oldVal - adjVal;
        return oldVal;
    }
    function numFmt(n) {
        return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    var dollerElems = document.getElementsByClassName('doller');
    var hasDollerElems = dollerElems.length > 0;

    if (priceCurrency === 'دلار' && hasDollerElems) {
        for (var i = 0; i < dollerElems.length; i++) {
            var oldDp = parseInt(dollerElems[i].getAttribute('data-doller-price')) || 0;
            var newDp = applyAdj(oldDp, adj, opration);
            dollerElems[i].setAttribute('data-doller-price', newDp);
            dollerElems[i].innerHTML = '+ ' + numFmt(newDp) + ' دلار';
        }
    } else {
        var prices = document.getElementsByClassName('bed_price_');
        var old_prices = [], new_prices = [];
        for (var i = 0; i < prices.length; i++) {
            old_prices.push(parseInt(prices[i].getAttribute('data-price')));
        }
        for (var i = 0; i < old_prices.length; i++) {
            new_prices.push(applyAdj(old_prices[i], adj, opration));
        }
        for (var i = 0; i < prices.length; i++) {
            prices[i].innerHTML = numFmt(new_prices[i]) + ' ' + baseCurrency;
            prices[i].setAttribute('data-new-price', new_prices[i]);
        }
    }

    if (infAdj > 0) {
        var infonts = document.getElementsByClassName('infont');
        for (var i = 0; i < infonts.length; i++) {
            if (priceCurrency === 'دلار' && hasDollerElems) {
                var nextEl = infonts[i].nextElementSibling;
                while (nextEl && !nextEl.classList.contains('doller')) {
                    nextEl = nextEl.nextElementSibling;
                }
                if (nextEl) {
                    var oldDp = parseInt(nextEl.getAttribute('data-doller-price')) || 0;
                    var newDp = applyAdj(oldDp, infAdj, opration);
                    nextEl.setAttribute('data-doller-price', newDp);
                    nextEl.innerHTML = '+ ' + numFmt(newDp) + ' دلار';
                }
            } else {
                var oldInf = parseInt(infonts[i].getAttribute('data-price')) || 0;
                var newInf = applyAdj(oldInf, infAdj, opration);
                infonts[i].setAttribute('data-new-price', newInf);
                infonts[i].innerHTML = numFmt(newInf) + ' ' + baseCurrency;
            }
        }
    }
}
$(document).ready(function () {
    $('.gallery-images').click(function () {
        var imageUrl = $(this).find('img').attr('src');
        $('.gallery-active-image').attr('src', imageUrl);
    });
    $('.preloader-c').removeClass('shown')
    const elements = $('.window-shiled');
    const country_titles = $('.country-title');
    $('.window-shiled').hover(
        function () {
            $(this).find('.country-title').addClass('move-top')
        },
        function () {
            $(this).find('.country-title').removeClass('move-top')
        }
    )
    function addHover(index) {
        if (index === 0) {
            setTimeout(function () {
                $(elements[index]).removeClass('window-shiled')
                $(elements[index]).addClass('window-hover')
                $(country_titles[index]).addClass('move-top')
                addHover(index + 1)
            }, 1500)
        } else if (index === elements.length) {
            const elements2 = $('.window-hover');
            setTimeout(function () {
                elements2.removeClass('window-hover')
                country_titles.removeClass('move-top')
                elements2.addClass('window-shiled')
                addHover(0)
            }, 3000)
        } else {
            setTimeout(function () {
                $(elements[index]).removeClass('window-shiled')
                $(elements[index]).addClass('window-hover')
                $(country_titles[index]).addClass('move-top')
                addHover(index + 1)
            }, 1500)
        }
    }
    addHover(0)

    const pathname = window.location.pathname;
    const current = window.location.href;
    // هر قالبی همهٔ این متغیرها را تعریف نمی‌کند؛ مثلاً detail-tour.html
    // category_slug را ندارد. چون این خط‌ها در سطح بالای $(document).ready
    // اجرا می‌شوند، یک ReferenceError کل هندلر را متوقف می‌کرد و بقیهٔ
    // جاوااسکریپت صفحه (هایلایت منو، هندلرهای اسکرول و صفحه‌بندی) هرگز
    // اجرا نمی‌شد. با typeof خوانده می‌شوند تا نبودشان فقط یک رشتهٔ خالی بدهد.
    const v = n => n !== 'undefined' && n !== 'null' && n != null ? n : ''
    const _country = typeof country !== 'undefined' ? v(country) : ''
    const _country_id = typeof country_id !== 'undefined' ? v(country_id) : ''
    const _city = typeof city !== 'undefined' ? v(city) : ''
    const _city_id = typeof city_id !== 'undefined' ? v(city_id) : ''
    const _category_slug = typeof category_slug !== 'undefined' ? v(category_slug) : ''
    const _tour_menu = typeof tour_menu !== 'undefined' ? v(tour_menu) : ''
    const _tour_id = typeof tour_id !== 'undefined' ? v(tour_id) : ''
    const _tour_slug = typeof tour_slug !== 'undefined' ? v(tour_slug) : ''

    const country_tours_path = '/' + _country + '/' + _country_id + '/all-tour'
    const city_tours_path = '/' + _city + '/' + _city_id + '/city-tours'
    const category_tours_path = '/tours/' + _category_slug
    const menu_tour_path = '/tour/' + _tour_menu
    const country_hotels_path = '/all-country-hotel/' + _country_id + '/' + _country
    const city_hotels_path = '/all-hotel/' + _city_id + '/' + _city
    const tourpath = pathname.slice(0, 5) + '/' + _tour_id + '/' + _tour_slug
    document.querySelectorAll(".menu-item").forEach(function (elem) {
        if (elem.href.includes(current)) {
            elem.classList.add("active");
        }
    });
    if (pathname === tourpath) {
        $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            var packageBox = document.getElementById('package-content')
            var bottomHeight = packageBox.offsetHeight
            var fromTop = $('#package-content').offset().top
            if (bottomHeight > 700) {
                if (scroll >= fromTop - 200) {
                    $(".package-side").addClass("fixed_pos_side");
                    $(".package-side").removeClass("new_pos_side");
                }
                if (scroll > bottomHeight - 400) {
                    $(".package-side").removeClass("fixed_pos_side");
                    $(".package-side").addClass("new_pos_side");
                }
                if (scroll <= fromTop) {
                    $(".package-side").removeClass("fixed_pos_side");
                    $(".package-side").removeClass("new_pos_side");

                }
            }
        })
    }
    if (pathname === '/') {
        function updateTour(url, target, page) {
            const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
            const csrf = csrf_token[0].value
            data = {
                'page': page,
            }
            $.ajax({
                url: url,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                headers: {'X-CSRFToken': csrf},
                success: function (data) {
                    $(target).html(data);
                }
            });
        }


        updateTour('/toursdata', '#tous-a');
        updateTour('/postdata', '#posts-a');

        $(document).on('click', '.page-item', function () {
            const elem = $(this);
            const page = elem.data('page');
            updateTour('/toursdata', '#tous-a', page);
        });
    }
    if (pathname === '/search-result') {
        function updateTour(url, target, page) {
        const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
        const csrf = csrf_token[0].value
        data = {
            'page':page
        },
            $.ajax({
                url: url,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                headers: {'X-CSRFToken': csrf},
                success: function (data) {
                    $(target).html(data);
                }
            });
        } 

        updateTour('/postdata', '#posts-a');
        
        $(document).on('click', '.page-item', function () {
            const elem = $(this);
            const page = elem.data('page');
            updateTour('/postdata', '#post-a', page);
        });
    }
    if (pathname === '/all-tour') {
        $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            var tourBox = document.getElementById('all-tours')
            var bottomHeight = tourBox.offsetHeight
            var fromTop = $('#all-tours').offset().top
            if (bottomHeight > 700) {
                if (scroll >= fromTop) {
                    $(".sticky_menu").addClass("fixed_pos");
                }
                if (scroll > bottomHeight - 100) {
                    $(".sticky_menu").addClass("new_pos");
                    $(".sticky_menu").removeClass("fixed_pos");
                }
                if (scroll <= fromTop) {
                    $(".sticky_menu").removeClass("fixed_pos");
                    $(".sticky_menu").removeClass("new_pos");
                }
            }
        })

        
        function updateTourlist(url, target, page) {
            $.ajax({
                url: url,
                data: {
                    'page': page,
                },
                success: function (data) {
                    $(target).html(data);
                    updatePriceSliderMax();
                    if (window.currentSort) setTimeout(applyCurrentSort, 30);
                    setTimeout(checkEmptyToursAndShowState, 50);
                }
            });
        }

        
        // #all-tours همین حالا سمت سرور با همان قالب ajax/layout/tour-list.html
        // و همان صفحه‌بندی رندر شده است. درخواست اولیه فقط همان مارک‌آپ را دوباره
        // می‌گرفت و کل لیست را بازسازی می‌کرد؛ نتیجه این بود که تصویر LCP نابود و
        // دوباره ساخته می‌شد و LCP تا پایان آن درخواست عقب می‌افتاد. فقط کارهای
        // بعد از رندر را مستقیم انجام می‌دهیم.
        updatePriceSliderMax();
        if (window.currentSort) setTimeout(applyCurrentSort, 30);
        setTimeout(checkEmptyToursAndShowState, 50);

        $(document).on('click', '.page-item', function () {
            const elem = $(this);
            const page = elem.data('page');
            updateTourlist('/tourslisth', '#all-tours', page);
        });
    }
    if (pathname === country_tours_path) {
        $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            var tourBox = document.getElementById('all-tours')
            var bottomHeight = tourBox.offsetHeight
            var fromTop = $('#all-tours').offset().top
            if (bottomHeight > 700) {
                if (scroll >= fromTop - 600) {
                    $(".sticky_menu").addClass("fixed_pos");
                }
                if (scroll > bottomHeight - 100) {
                    $(".sticky_menu").addClass("new_pos");
                    $(".sticky_menu").removeClass("fixed_pos");
                }
                if (scroll <= fromTop) {
                    $(".sticky_menu").removeClass("fixed_pos");
                    $(".sticky_menu").removeClass("new_pos");
                }
            }
        })

        
        function countryTourlist(url, target, page, country) {
            const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
            const csrf = csrf_token[0].value
            const data = {
                'page': page,
                'country': country
            }
            $.ajax({
                url: url,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                headers: {'X-CSRFToken': csrf},
                success: function (data) {
                    $(target).html(data);
                    updatePriceSliderMax();
                    if (window.currentSort) setTimeout(applyCurrentSort, 30);
                    setTimeout(checkEmptyToursAndShowState, 50);
                }
            });
        }

        
        // مثل صفحهٔ /all-tour: لیست از قبل سمت سرور رندر شده. درخواست اولیه علاوه
        // بر عقب انداختن LCP، روی ?page=2 هم صفحهٔ درست را با صفحهٔ ۱ جایگزین می‌کرد.
        updatePriceSliderMax();
        if (window.currentSort) setTimeout(applyCurrentSort, 30);
        setTimeout(checkEmptyToursAndShowState, 50);

        $(document).on('click', '.page-item', function () {
            const elem = $(this);
            const page = elem.data('page');
            countryTourlist('/country_tours_ajax', '#all-tours', page, country);
        });
        $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            var tourBox = document.getElementById('all-tours')
            var bottomHeight = tourBox.offsetHeight
            var fromTop = $('#all-tours').offset().top
            if (bottomHeight > 700) {
                if (scroll >= fromTop) {
                    $(".sticky_menu").addClass("fixed_pos");
                }
                if (scroll > bottomHeight) {
                    $(".sticky_menu").addClass("new_pos");
                    $(".sticky_menu").removeClass("fixed_pos");
                }
                if (scroll <= fromTop) {
                    $(".sticky_menu").removeClass("fixed_pos");
                    $(".sticky_menu").removeClass("new_pos");
                }
            }
        })
        $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            var articleBox = document.getElementById('article')
            var articleHeight = articleBox.offsetHeight
            var fromTop = $('#article').offset().top
            if (scroll >= fromTop - 350) {
                $(".anchor-links").addClass("anchor-fixed");
                $(".anchor-links").removeClass("btm_pos")
            }
            if (scroll > articleHeight + fromTop - 400) {
                $(".anchor-links").addClass("btm_pos");
                $(".anchor-links").removeClass("anchor-fixed");
            }
            if (scroll <= fromTop) {
                $(".anchor-links").removeClass("anchor-fixed");
                $(".anchor-links").removeClass("btm_pos");
            }

        });
        
    }
    if (pathname === city_tours_path) {
        
        function cityTourlist(url, target, page, city) {
            const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
            const csrf = csrf_token[0].value
            data = {
                'page': page,
                'city': city
            }
            $.ajax({
                url: url,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                headers: {'X-CSRFToken': csrf},
                success: function (data) {
                    $(target).html(data);
                    updatePriceSliderMax();
                    if (window.currentSort) setTimeout(applyCurrentSort, 30);
                    setTimeout(checkEmptyToursAndShowState, 50);
                }
            });
        }

        
        // مثل صفحهٔ کشور: لیست از قبل سمت سرور رندر شده.
        updatePriceSliderMax();
        if (window.currentSort) setTimeout(applyCurrentSort, 30);
        setTimeout(checkEmptyToursAndShowState, 50);

        $(document).on('click', '.page-item', function () {
            const elem = $(this);
            const page = elem.data('page');
            cityTourlist('/city_tours_ajax', '#all-tours', page, city);
        });
        $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            var tourBox = document.getElementById('all-tours')
            var bottomHeight = tourBox.offsetHeight
            var fromTop = $('#all-tours').offset().top
            if (bottomHeight > 700) {
                if (scroll >= fromTop - 200) {
                    $(".sticky_menu").addClass("fixed_pos");
                }
                if (scroll > bottomHeight) {
                    $(".sticky_menu").addClass("new_pos");
                    $(".sticky_menu").removeClass("fixed_pos");
                }
                if (scroll <= fromTop) {
                    $(".sticky_menu").removeClass("fixed_pos");
                    $(".sticky_menu").removeClass("new_pos");
                }
            }
        })
    }
    if (pathname === category_tours_path) {

        function categoryTourlist(url, target, page, slug) {
    
            const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
            const csrf = csrf_token[0].value
    
            data = {
                'page': page,
                'slug': slug
            }
    
            $.ajax({
                url: url,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                headers: {'X-CSRFToken': csrf},
    
                success: function (data) {
    
                    $(target).html(data);
                    updatePriceSliderMax();
    
                }
            });
        }
    
        categoryTourlist(
            '/custom-category-tours-ajax/',
            '#all-tours',
            1,
            category_slug
        );
    
        $(document).on('click', '.page-item', function () {
    
            const elem = $(this);
    
            const page = elem.data('page');
    
            categoryTourlist(
                '/custom-category-tours-ajax/',
                '#all-tours',
                page,
                category_slug
            );
        });
    
        $(window).scroll(function () {
    
            var scroll = $(window).scrollTop();
    
            var tourBox = document.getElementById('all-tours')
    
            var bottomHeight = tourBox.offsetHeight
    
            var fromTop = $('#all-tours').offset().top
    
            if (bottomHeight > 700) {
    
                if (scroll >= fromTop - 200) {
    
                    $(".sticky_menu").addClass("fixed_pos");
                }
    
                if (scroll > bottomHeight) {
    
                    $(".sticky_menu").addClass("new_pos");
    
                    $(".sticky_menu").removeClass("fixed_pos");
                }
    
                if (scroll <= fromTop) {
    
                    $(".sticky_menu").removeClass("fixed_pos");
    
                    $(".sticky_menu").removeClass("new_pos");
                }
            }
        })
    }
    if (pathname === menu_tour_path) {
        function menuTourlist(url, target, page, menu) {
            const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
            const csrf = csrf_token[0].value
            data = {
                'page': page,
                'menu': menu
            }
            $.ajax({
                url: url,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                headers: {'X-CSRFToken': csrf},
                success: function (data) {
                    $(target).html(data);

                }
            });
        }

        
        menuTourlist('/tourslistm', '#all-tours', 1, tour_menu);
        
        $(document).on('click', '.page-item', function () {
            const elem = $(this);
            const page = elem.data('page');
            menuTourlist('/tourslistm', '#all-tours', page, tour_menu);
        });
        $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            var tourBox = document.getElementById('all-tours')
            var bottomHeight = tourBox.offsetHeight
            var fromTop = $('#all-tours').offset().top
            if (bottomHeight > 700) {
                if (scroll >= fromTop - 200) {
                    $(".sticky_menu").addClass("fixed_pos");
                }
                if (scroll > bottomHeight) {
                    $(".sticky_menu").addClass("new_pos");
                    $(".sticky_menu").removeClass("fixed_pos");
                }
                if (scroll <= fromTop) {
                    $(".sticky_menu").removeClass("fixed_pos");
                    $(".sticky_menu").removeClass("new_pos");
                }
            }
        })
    }
    if (pathname === '/all-hotel') {
        
        function hotelslist(url, target, page) {
            const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
            const csrf = csrf_token[0].value
            const data = {
                'page': page
            }
            $.ajax({
                url: url,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                headers: {'X-CSRFToken': csrf},
                success: function (data) {
                    $(target).html(data);

                }
            });
        }

        
        hotelslist('/hotel_cities_ajax', '#hotels-list');
        
        $(document).on('click', '.page-item', function () {
            const elem = $(this);
            const page = elem.data('page');
            hotelslist('/hotel_cities_ajax', '#hotels-list', page);
        });
    }
    if (pathname === country_hotels_path) {
        function countryHotelslist(url, target, page, country, fa_name, en_name, rating, service) {
            const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
            const csrf = csrf_token[0].value
            data = {
                'page': page,
                'fa_name': fa_name,
                'en_name': en_name,
                'country': country,
                'rating': rating,
                'service': service
            }
            $.ajax({
                url: url,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                headers: {'X-CSRFToken': csrf},
                success: function (data) {
                    $(target).html(data);
                }
            });
        }

        
        countryHotelslist('/country_hotels_ajax', '#hotels-list', 1, country);
        
        $(document).on('click', '.page-item', function () {
            const elem = $(this);
            const page = elem.data('page');
            countryHotelslist('/country_hotels_ajax', '#hotels-list', page, country);
        });
    }
    if (pathname === city_hotels_path) {
        function cityHotelslist(url, target, page, city, fa_name, en_name, rating, service) {
            const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
            const csrf = csrf_token[0].value
            data = {
                'page': page,
                'fa_name': fa_name,
                'en_name': en_name,
                'city': city,
                'rating': rating,
                'service': service
            }
            $.ajax({
                url: url,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                headers: {'X-CSRFToken': csrf},
                success: function (data) {
                    $(target).html(data);
                }
            });
        }
        cityHotelslist('/city_hotels_ajax', '#hotels-list', 1, city);
        $(document).on('click', '.page-item', function () {
            const elem = $(this);
            const page = elem.data('page');
            cityHotelslist('/city_hotels_ajax', '#hotels-list', page, city);
        });
    }

    // $('.spacial-tour').hover(
    //     function () {
    //         $(this).find('.price-text').stop(true, true).slideDown();
    //     },
    //     function () {
    //         $(this).find('.price-text').stop(true, true).slideUp();
    //     }
    // )
    $(document).on('mouseenter', '.spacial-tour', function () {
        $(this).find('.price-text').stop(true, true).slideDown(120);
    });
    $(document).on('mouseleave', '.spacial-tour', function () {
        $(this).find('.price-text').stop(true, true).slideUp(120);
    });
    $(window).scroll(function () {
        var scroll = $(window).scrollTop();
        // var articleBox = document.getElementById('hotel-data')
        // var articleHeight = articleBox.offsetHeight
        // var fromTop = $('#hotel-data').offset().top
        var articleBox = document.getElementById('hotel-data');
        if (!articleBox || $('.hotel-sidebar').length === 0) {
            return;
        }
        var articleHeight = articleBox.offsetHeight;
        var fromTop = $(articleBox).offset().top;
        if (scroll >= fromTop - 350) {
            $(".hotel-sidebar").addClass("anchor-fixed");
            $(".hotel-sidebar").removeClass("btm_pos")
        }
        if (scroll > articleHeight + fromTop - 400) {
            $(".hotel-sidebar").addClass("btm_pos");
            $(".hotel-sidebar").removeClass("anchor-fixed");
        }
        if (scroll <= fromTop) {
            $(".hotel-sidebar").removeClass("anchor-fixed");
            $(".hotel-sidebar").removeClass("btm_pos");
        }

    });
   
});

function showCountry() {
    const targetElem = $('.meniu-container')
    const subElem = $('.offcanvas-sub-menu')
    targetElem.toggle()
    subElem.css('position', 'relative')
    subElem.animate({left: '0%'}, 200)
}

function backToMain() {
    const targetElem = $('.meniu-container')
    const subElem = $('.offcanvas-sub-menu')
    subElem.animate({left: '-100%'}, 200)
    targetElem.animate({left: '0%'}, 200, function () {
        setTimeout(function () {
            targetElem.css('position', 'relative')
            targetElem.toggle()
            subElem.css('position', 'absolute')
        }, 200)
    })
}

function getCitiesOffCanvas(country_id) {
    $.ajax({
        url: "/get_country_tours_city_canvas",
        data: {
            'country_id': country_id
        },
        success: function (data) {
            const targetElem = $('.offcanvas-sub-menu')
            const subElem = $('.offcanvas-city-menu')
            subElem.html(data)
            targetElem.css('position', 'absolute')
            targetElem.toggle()
            subElem.css('position', 'relative')
            subElem.animate({right: '0%'}, 300)
        }
    });
}

function backToCountry() {
    const targetElem = $('.offcanvas-sub-menu')
    const subElem = $('.offcanvas-city-menu')
    subElem.animate({right: '100%'}, 200)
    targetElem.animate({left: '0%'}, 200, function () {
        setTimeout(function () {
            targetElem.css('position', 'relative')
            targetElem.toggle()
            subElem.css('position', 'absolute')
        }, 200)
    })
}

function showHotelCountry() {
    const targetElem = $('.meniu-container')
    const subElem = $('.offcanvas-hotel-sub-menu')
    targetElem.toggle()
    subElem.css('position', 'relative')
    subElem.animate({left: '0%'}, 200)
}

function backToHotelMain() {
    const targetElem = $('.meniu-container')
    const subElem = $('.offcanvas-hotel-sub-menu')
    subElem.animate({left: '-100%'}, 200)
    targetElem.animate({left: '0%'}, 200, function () {
        setTimeout(function () {
            targetElem.css('position', 'relative')
            targetElem.toggle()
            subElem.css('position', 'absolute')
        }, 200)
    })
}

function getHotelCitiesOffCanvas(country_id) {
    $.ajax({
        url: "/get_country_hotel_cities_canvas",
        data: {
            'country_id': country_id
        },
        success: function (data) {
            const targetElem = $('.offcanvas-hotel-sub-menu')
            const subElem = $('.offcanvas-hotel-city-menu')
            subElem.html(data)
            targetElem.css('position', 'absolute')
            targetElem.toggle()
            subElem.css('position', 'relative')
            subElem.animate({right: '0%'}, 300)
        }
    });
}

function backToHotelCountry() {
    const targetElem = $('.offcanvas-hotel-sub-menu')
    const subElem = $('.offcanvas-hotel-city-menu')
    subElem.animate({right: '100%'}, 200)
    targetElem.animate({left: '0%'}, 200, function () {
        setTimeout(function () {
            targetElem.css('position', 'relative')
            targetElem.toggle()
            subElem.css('position', 'absolute')
        }, 200)
    })
}


function getCityList(country_id, target) {
    $.ajax({
        url: "/country_tour_cities",
        data: {
            'country_id': country_id
        },
        success: function (data) {
            targetClass = '.col-menu-' + target
            subMwnuClass = '.sub-menu-' + target
            const targetElem = $(targetClass)
            const subElem = $(subMwnuClass)
            subElem.html(data)
            targetElem.css('position', 'absolute')
            targetElem.toggle()
            subElem.css('position', 'relative')
            subElem.animate({left: '0%'}, 200)
        }
    });
}

function backToList(target) {
    targetClass = '.col-menu-' + target
    subMwnuClass = '.sub-menu-' + target
    const targetElem = $(targetClass)
    const subElem = $(subMwnuClass)
    subElem.animate({left: '-105%'}, 100)
    targetElem.animate({left: '0%'}, 200, function () {
        setTimeout(function () {
            targetElem.css('position', 'relative')
            targetElem.toggle()
            subElem.css('position', 'absolute')
        }, 200)
    })
}

function getHotelCityList(country_id, target) {
    $.ajax({
        url: "/country_hotel_cities",
        data: {
            'country_id': country_id
        },
        success: function (data) {
            targetClass = '.hotel-col-menu-' + target
            subMwnuClass = '.hotel-sub-menu-' + target
            const targetElem = $(targetClass)
            const subElem = $(subMwnuClass)
            subElem.html(data)
            targetElem.css('position', 'absolute')
            targetElem.toggle()
            subElem.css('position', 'relative')
            subElem.animate({left: '0%'}, 200)
        }
    });
}

function backToHotelList(target) {
    targetClass = '.hotel-col-menu-' + target
    subMwnuClass = '.hotel-sub-menu-' + target
    const targetElem = $(targetClass)
    const subElem = $(subMwnuClass)
    subElem.animate({left: '-105%'}, 100)
    targetElem.animate({left: '0%'}, 200, function () {
        setTimeout(function () {
            targetElem.css('position', 'relative')
            targetElem.toggle()
            subElem.css('position', 'absolute')
        }, 200)
    })
}

function SidebarFilter() {
    fromPrice = document.getElementById('fromSlider').value
    toPrice = document.getElementById('toSlider').value
    dayCount = document.getElementById('day-Count').value
    selectedCountry = []
    selectedCity = []
    hotelRate = []
    airlines = []
    allCheckBox = document.getElementsByName('country-checkbox')
    allCityCheckBox = document.getElementsByName('city-checkbox')
    allRateCheckBox = document.getElementsByName('hotel-rate')
    allAirlineCheckBox = document.getElementsByName('airline-checkbox')
    for (var i = 0; i < allCheckBox.length; i++) {
        if (allCheckBox[i].checked) {
            selectedCountry.push(allCheckBox[i].getAttribute('data-ctry-id'));
        }
    }
    for (var i = 0; i < allCityCheckBox.length; i++) {
        if (allCityCheckBox[i].checked) {
            selectedCity.push(allCityCheckBox[i].getAttribute('data-city-id'));
        }
    }
    for (var i = 0; i < allRateCheckBox.length; i++) {
        if (allRateCheckBox[i].checked) {
            hotelRate.push(allRateCheckBox[i].getAttribute('data-rate'));
        }
    }
    for (var i = 0; i < allAirlineCheckBox.length; i++) {

        if (allAirlineCheckBox[i].checked) {
            airlines.push(allAirlineCheckBox[i].getAttribute('data-airline'));
        }
    }
    if (country_id === '' && city_id === '') {
        $.ajax({
            url: "/sidebar_filter",
            data: {
                'fromPrice': fromPrice,
                'toPrice': toPrice,
                'selectedCountry': JSON.stringify(selectedCountry),
                'selectedCity': JSON.stringify(selectedCity),
                'hotelRate': JSON.stringify(hotelRate),
                'airlines': JSON.stringify(airlines),
                'dayCount': dayCount,
            },
            success: function (data) {
                $("#all-tours").html(data);

                function topFunction() {
                    document.getElementById('sidebar').classList.remove('fixed_pos')
                    if (country === '' && city === '') {
                        document.body.scrollTop = 500; 
                        document.documentElement.scrollTop = 500; 
                    } else if (country !== '') {
                        document.body.scrollTop = 300; 
                        document.documentElement.scrollTop = 300; 
                    }
                }

                topFunction()
            }
        });
    } else if (country_id !== '' && city_id !== '') {
        selectedCountry.push(country_id)
        selectedCity.push(city_id)
        $.ajax({
            url: "/sidebar_filter",
            data: {
                'fromPrice': fromPrice,
                'toPrice': toPrice,
                'selectedCountry': JSON.stringify(selectedCountry),
                'selectedCity': JSON.stringify(selectedCity),
                'hotelRate': JSON.stringify(hotelRate),
                'airlines': JSON.stringify(airlines),
                'dayCount': dayCount,
            },
            success: function (data) {
                $("#all-tours").html(data);

                function topFunction() {
                    document.getElementById('sidebar').classList.remove('fixed_pos')
                    if (country === '' && city === '') {
                        document.body.scrollTop = 500; 
                        document.documentElement.scrollTop = 500; 
                    } else if (country !== '') {
                        document.body.scrollTop = 300; 
                        document.documentElement.scrollTop = 300; 
                    }
                }

                topFunction()
            }
        });
    } else if (country_id !== '') {
        selectedCountry.push(country_id)
        $.ajax({
            url: "/sidebar_filter",
            data: {
                'fromPrice': fromPrice,
                'toPrice': toPrice,
                'selectedCountry': JSON.stringify(selectedCountry),
                'selectedCity': JSON.stringify(selectedCity),
                'hotelRate': JSON.stringify(hotelRate),
                'airlines': JSON.stringify(airlines),
                'dayCount': dayCount,
            },
            success: function (data) {
                $("#all-tours").html(data);

                function topFunction() {
                    document.getElementById('sidebar').classList.remove('fixed_pos')
                    if (country === '' && city === '') {
                        document.body.scrollTop = 500; 
                        document.documentElement.scrollTop = 500; 
                    } else if (country !== '') {
                        document.body.scrollTop = 300; 
                        document.documentElement.scrollTop = 300; 
                    }
                }

                topFunction()
            }
        });
    } else if (city_id !== '') {
        selectedCity.push(city_id)
        $.ajax({
            url: "/sidebar_filter",
            data: {
                'fromPrice': fromPrice,
                'toPrice': toPrice,
                'selectedCountry': JSON.stringify(country_id),
                'selectedCity': JSON.stringify(city_id),
                'hotelRate': JSON.stringify(hotelRate),
                'airlines': JSON.stringify(airlines),
                'dayCount': dayCount,
            },
            success: function (data) {
                $("#all-tours").html(data);

                function topFunction() {
                    document.getElementById('sidebar').classList.remove('fixed_pos')
                    if (country === '' && city === '') {
                        document.body.scrollTop = 500; 
                        document.documentElement.scrollTop = 500; 
                    } else if (country !== '') {
                        document.body.scrollTop = 300; 
                        document.documentElement.scrollTop = 300; 
                    }
                }

                topFunction()
            }
        });
    }


}

function get_cities() {
    allCheckBox = document.getElementsByName('country-checkbox')
    selectedCountry = []
    for (var i = 0; i < allCheckBox.length; i++) {
        if (allCheckBox[i].checked) {
            selectedCountry.push(allCheckBox[i].getAttribute('data-ctry-id'));
        }
    }
    $.ajax({
        url: "/sidebar_filter_city",
        data: {
            'selectedCountry': JSON.stringify(selectedCountry),
        },
        success: function (data) {
            $("#filter-city").html(data);
        }
    });
}
// function search_hotel() {
//     var hotelInput = document.getElementById('id_hotel_name');
//     var searchLink = document.getElementById('search_link');

//     if (!hotelInput || !searchLink) {
//         console.error('Hotel name input or search link element is missing.');
//         return;
//     }

//     var hotelName = hotelInput.value.trim();
//     var selectedOption = document.querySelector('input[name="filter"]:checked');
//     var filterValue = selectedOption ? selectedOption.value : '';

//     if (!hotelName) {
//         alert('Please enter a hotel name.');
//         return;
//     }

//     searchLink.href = `/hotel_search?hotel_name=${encodeURIComponent(hotelName)}&hotel_rate=${encodeURIComponent(filterValue)}`;
// }


// function search_hotel() {
//     var x = document.getElementById('id_hotel_name').value;
//     var selectedOption = document.querySelector('input[name="filter"]:checked');
//     var selectedValue = selectedOption ? selectedOption.value : '';
//     var y = document.getElementById('search_link');
//     y.href = `/hotel_search?hotel_name=${encodeURIComponent(x)}&hotel_rate=${encodeURIComponent(selectedValue)}`;
// }

function getCountryId() {
    ctry_id = document.getElementById('country-select').value
    $.ajax({
        url: "/get_country_city",
        data: {
            'country_id': ctry_id
        },
        success: function (data) {
            $("#city").html(data);
        }
    });
}

jQuery(document).ready(function ($) {
    $(document).on('initialized.owl.carousel', function(e) {
        $(e.target).find('.owl-dot').each(function(i) {
            $(this).attr('aria-label', 'برو به اسلاید ' + (i + 1));
        });
    });
    $('#calc_btn').click(function () {
        $('#calc_sec').animate({
            height: $('#calc_sec').height() === 0 ? '475px' : '0'
        }, 500); 
    });
    $('#colse_pane').click(function () {
        $('#calc_sec').animate({
            height: $('#calc_sec').height() === 0 ? '475px' : '0'
        }, 500); 
    });
    $('.owl-two').owlCarousel({
        rtl: true, margin: 10, nav: true, loop: true, autoplay: true, responsive: {
            0: {
                items: 1, loop: true, dots: false,
            }, 600: {
                items: 2, loop: true, dots: false,nav: true,
            }, 1000: {
                items: 4, loop: true, dots: false, nav: true,
            }
        }
    });
    $('.owl-dest-city').owlCarousel({
        rtl: true, margin: 10, nav: false, loop: false, autoplay: true, dots: true, responsive: {
            0: {
                items: 2, loop: false, dots: true, smartSpeed: 1500,
            }, 600: {
                items: 2, loop: false, dots: true, smartSpeed: 1500,
            }, 1000: {
                items: 4, loop: false, dots: true, smartSpeed: 1500,
            }
        }
    });
    $('.owl-dest').owlCarousel({
        rtl: true, margin: 10, nav: false, loop: true, autoplay: true, dots: true, responsive: {
            0: {
                items: 2.5, loop: true, dots: true,
            }, 600: {
                items: 2.5, loop: true, dots: true,
            }, 1000: {
                items: 6, loop: true, dots: true,
            }
        }
    });
    $('.owl-dest-city').owlCarousel({
        rtl: true, margin: 10, nav: false, loop: true, autoplay: true, dots: true, responsive: {
            0: {
                items: 2, loop: true, dots: true, smartSpeed: 1500,
            }, 600: {
                items: 2, loop: true, dots: true, smartSpeed: 1500,
            }, 1000: {
                items: 4, loop: true, dots: true, smartSpeed: 1500,
            }
        }
    });
    $('.owl-one').owlCarousel({
        rtl: true, margin: 10, nav: false, loop: false, autoplay: false, responsive: {
            0: {
                items: 1.5, loop: false, dots: true,
            }, 600: {
                items: 1.5, loop: false, dots: true
            }, 1000: {
                items: 4, loop: false, dots: true,
            }
        }
    });
    $('.owl-tree').owlCarousel({
        rtl: true, margin: 10, nav: true, loop: false, autoplay: false, responsive: {
            0: {
                items: 1, loop: false, dots: true,
            }, 600: {
                items: 2, loop: false, dots: true,
            }, 1000: {
                items: 4, loop: false, dots: true,
            }
        }
    });
    $('.owl-about-us').owlCarousel({
        rtl: true, margin: 10, nav: true, loop: false, autoplay: false, responsive: {
            0: {
                items: 1, loop: false, dots: true, nav: false,
            }, 600: {
                items: 2, loop: false, dots: true, nav: false,
            }, 1000: {
                items: 4, loop: false, dots: true, nav: false,
            }
        }
    });
    $('.office-gallery').click(function () {
        var $mainImg = $('.office-img').children('img')
        var $thumbImg = $(this).find('img')
        var mainSrc = $mainImg.attr('src')
        var mainSrcset = $mainImg.attr('srcset')
        $mainImg.attr('src', $thumbImg.attr('src'))
        $mainImg.attr('srcset', $thumbImg.attr('srcset'))
        $thumbImg.attr('src', mainSrc)
        $thumbImg.attr('srcset', mainSrcset)
    })
    $('.about-image').click(function () {
        imageUrl = $(this).find('img').attr('src')
        activeImage = $('.about-gallery').find('img').attr('src', imageUrl)
    })

})

function calculateprice(pack_id) {
    all_price = document.getElementsByClassName('price-' + pack_id)
    all_doller_price = document.getElementsByClassName('d_price-' + pack_id)
    all_count = document.getElementsByClassName('count-' + pack_id)
    prices = [];
    doller_prices = [];
    counts = [];
    total_price = 0;
    total_doller_price = 0;
    for (i = 0; i < all_price.length; i++) {
        prices.push(parseInt(all_price[i].getAttribute('data-new-price')))
    }
    for (i = 0; i < all_doller_price.length; i++) {
        doller_prices.push(parseInt(all_doller_price[i].getAttribute('data-doller-price')))
    }
    for (i = 0; i < all_count.length; i++) {
        counts.push(parseInt(all_count[i].value))
        total_price += prices[i] * parseInt(all_count[i].value)
        total_doller_price += doller_prices[i] * parseInt(all_count[i].value)
    }
    if (prices[0] === total_price && doller_prices[0] === total_doller_price) {
        document.getElementById('price-' + pack_id).innerText = prices[0].toLocaleString() + ' ' + 'تومان' + ' + ' + doller_prices[0].toLocaleString() + ' ' + 'دلار'
    } else if (total_price > 0 && total_doller_price > 0) {
        document.getElementById('price-' + pack_id).innerText = total_price.toLocaleString() + ' ' + 'تومان' + ' + ' + total_doller_price.toLocaleString() + ' ' + 'دلار'
    } else {
        document.getElementById('price-' + pack_id).innerText = total_price.toLocaleString() + ' ' + 'تومان'
    }
}

// function search_hotel() {
//     var x = document.getElementById('id_hotel_name').value;
//     var selectedOption = document.querySelector('input[name="filter"]:checked');
//     var selectedValue = selectedOption ? selectedOption.value : '';
//     var y = document.getElementById('search_link');
//     y.href = `/hotel_search?hotel_name=${encodeURIComponent(x)}&hotel_rate=${encodeURIComponent(selectedValue)}`;
// }

jQuery(document).ready(function ($) {
    $('.minus').click(function () {
        var $input = $(this).parent().find('input');
        const input_value = $input.val()
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function () {
        var $input = $(this).parent().find('input');
        const input_value = $input.val()
        if (input_value === '') {
            $input.val(0)
            var count = parseInt($input.val()) + 1;
            $input.val(count);
            $input.change();
            return false;
        } else {
            var count = parseInt($input.val()) + 1;
            $input.val(count);
            $input.change();
            return false;
        }
    });
    $('.inst_minus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 3 ? 3 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.inst_plus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) + 1;
        count = count > 6 ? 6 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.cheq_minus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.cheq_plus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) + 1;
        count = count > 6 ? 6 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('#more_show').click(function () {
        $('#tour_cities_container').animate({height: '100%'}, 10000);
        $('#more_show').css('display', 'none');
    });
    $('#calc_btn').click(function () {
        $('#calc_sec').animate({
            height: $('#calc_sec').height() === 0 ? '480px' : '0'
        }, 500); 
    });
    $('#colse_pane').click(function () {
        $('#calc_sec').animate({
            height: $('#calc_sec').height() === 0 ? '480px' : '0'
        }, 500); 
    });
    $('.owl-one').owlCarousel({
        rtl: true, margin: 10, nav: true, loop: false, autoplay: false, responsive: {
            0: {
                items: 1, loop: true, dots: true,
            }, 600: {
                items: 2, loop: true, dots: true,
            }, 1000: {
                items: 4, loop: true, dots: true,
            }
        }
    });
    $('.owl-two').owlCarousel({
        rtl: true, margin: 10, nav: true, loop: false, autoplay: false, responsive: {
            0: {
                items: 1, loop: true, dots: true,
            }, 600: {
                items: 2, loop: true, dots: true,
            }, 1000: {
                items: 3, loop: true, dots: true,
            }
        }
    });
    $('.owl-tree').owlCarousel({
        rtl: true, margin: 10, nav: true, loop: false, autoplay: false, responsive: {
            0: {
                items: 1, loop: true, dots: true,
            }, 600: {
                items: 2, loop: true, dots: true,
            }, 1000: {
                items: 4, loop: true, dots: true,
            }
        }
    });
    $('#adult_c').on('input', function () {
        var input = $(this).val();
        var total_price = 0
        var pre_paid = 0
        if (parseInt(input) === 1) {
            var total_price = SingleBedPrice * parseInt(input)
            var baby_wb_count = document.getElementById('baby_wb_c').value
            var baby_wb_price = BabyWithBedPrice * parseInt(baby_wb_count)
            var baby_wob_count = document.getElementById('baby_wob_c').value
            var baby_wob_price = BabyWithoutBedPrice * parseInt(baby_wob_count)
            var infont_count = document.getElementById('infont_c').value
            var infont_price = InfontPrice * parseInt(infont_count)
            var total = total_price + baby_wb_price + baby_wob_price + infont_price
            $('#total_price').text(total.toLocaleString('en-us'))
            $('#adult_price').text(total_price.toLocaleString('en-us'))
            $('#baby_wb_c').prop('disabled', false);
            $('#baby_wob_c').prop('disabled', false);
            $('#infont_c').prop('disabled', false);
        } else {
            var total_price = DoubleBedPrice * parseInt(input)
            var baby_wb_count = document.getElementById('baby_wb_c').value
            var baby_wb_price = BabyWithBedPrice * parseInt(baby_wb_count)
            var baby_wob_count = document.getElementById('baby_wob_c').value
            var baby_wob_price = BabyWithoutBedPrice * parseInt(baby_wob_count)
            var infont_count = document.getElementById('infont_c').value
            var infont_price = InfontPrice * parseInt(infont_count)
            var total = total_price + baby_wb_price + baby_wob_price + infont_price
            $('#baby_wb_c').prop('disabled', false);
            $('#baby_wob_c').prop('disabled', false);
            $('#infont_c').prop('disabled', false);
            $('#total_price').text(total.toLocaleString('en-us'))
            $('#adult_price').text(total_price.toLocaleString('en-us'))
        }
        if (parseInt(input) === 3) {
            $('#baby_wb_c').prop('disabled', true);
            $('#baby_wob_c').prop('disabled', true);
            $('#infont_c').prop('disabled', true);
        }
        $('#adult_count').text(input);
    });
    $('#baby_wb_c').on('input', function () {
        var input = $(this).val();
        var total_price = BabyWithBedPrice * parseInt(input)
        var adult_count = document.getElementById('adult_c').value
        var adult_price = DoubleBedPrice * parseInt(adult_count)
        var baby_wob_count = document.getElementById('baby_wob_c').value
        var baby_wob_price = BabyWithoutBedPrice * parseInt(baby_wob_count)
        var infont_count = document.getElementById('infont_c').value
        var infont_price = InfontPrice * parseInt(infont_count)
        var total = total_price + adult_price + baby_wob_price + infont_price
        $('#total_price').text(total.toLocaleString('en-us'))
        $('#Baby_wb_count').text(input);
        $('#Baby_wb_price').text(total_price.toLocaleString('en-us'))
    });
    $('#baby_wob_c').on('input', function () {
        var input = $(this).val();
        var total_price = BabyWithoutBedPrice * parseInt(input)
        var adult_count = document.getElementById('adult_c').value
        var adult_price = DoubleBedPrice * parseInt(adult_count)
        var baby_wb_count = document.getElementById('baby_wb_c').value
        var baby_wb_price = BabyWithBedPrice * parseInt(baby_wb_count)
        var infont_count = document.getElementById('infont_c').value
        var infont_price = InfontPrice * parseInt(infont_count)
        var total = total_price + adult_price + baby_wb_price + infont_price
        $('#total_price').text(total.toLocaleString('en-us'))
        $('#baby_wob_count').text(input);
        $('#Baby_wob_price').text(total_price.toLocaleString('en-us'))
    });
    $('#infont_c').on('input', function () {
        var input = $(this).val();
        var total_price = InfontPrice * parseInt(input)
        var adult_count = document.getElementById('adult_c').value
        var adult_price = DoubleBedPrice * parseInt(adult_count)
        var baby_wb_count = document.getElementById('baby_wb_c').value
        var baby_wb_price = BabyWithBedPrice * parseInt(baby_wb_count)
        var baby_wob_count = document.getElementById('baby_wob_c').value
        var baby_wob_price = BabyWithoutBedPrice * parseInt(baby_wob_count)
        var total = total_price + adult_price + baby_wb_price + baby_wob_price
        $('#total_price').text(total.toLocaleString('en-us'))
        $('#infont_count').text(input);
        $('#infont_price').text(total_price.toLocaleString('en-us'))
    });
    $('#room').on('click', function () {
        var adult_count = document.getElementById('adult_c').value
        var baby_wb_count = document.getElementById('baby_wb_c').value
        var baby_wob_count = document.getElementById('baby_wob_c').value
        var infont_count = document.getElementById('infont_c').value
        link = '/add_order_item?tour_id=' + tour_id + "&package_id=" + pacjage_id + '&adult_count=' + adult_count + '&baby_wb_count=' + baby_wb_count + '&baby_wob_count=' + baby_wob_count + '&infont_count=' + infont_count
        $(this).attr('href', link)
    });
})


$(document).ready(function () {

});

function topFunction() {
    document.body.scrollTop = 0; 
    document.documentElement.scrollTop = 0; 
}

function menuSearch() {
    const searchTerm = $('.menu-search').val()
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
    const csrf = csrf_token[0].value
    data = {
        'search': searchTerm,
    }
    $.ajax({
        url: "/menuSearch",
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        headers: {
            'X-CSRFToken': csrf
        },
        success: function (data) {
            const subElem = $('.menu_list')
            subElem.html(data)
        }
    });

}

function resetCalculator() {
    let tourElement = document.getElementById('tour_price');
    let paidElement = document.getElementById('pre_paid');
    let paidvalueElement = document.getElementById('pre_paid_value');
    let instPeriodElement = document.getElementById('inst_period');
    let instElement = document.getElementById('inst_num');
    let tourTotalElement = document.getElementById('tour_total_price');
    $('.resualt-box').slideUp(300)
    tourElement.value = ''
    paidElement.value = ''
    paidvalueElement.value = ''
    instPeriodElement.value = ''
    instElement.value = 2
    tourTotalElement.value = ''
}

function sendReply(taget_id) {
    targetElem = '.cm-' + taget_id
    $(targetElem).toggle(300)
}

function sendReplyData(cm_id) {
    nameElem = 'nameData-' + cm_id
    emailElem = 'emailData-' + cm_id
    messageElem = 'desc-' + cm_id
    errorElem = 'invalid-cm-' + cm_id
    const name = document.getElementById(nameElem).value
    const email = document.getElementById(emailElem).value
    const message = document.getElementById(messageElem).value
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
    const csrf = csrf_token[0].value
    if (name === '' || email === '' || message === '') {
        const success_message = document.getElementById(errorElem)
        errorMessage = document.getElementById(errorElem)
        errorMessage.style.display = 'block'
        success_message.innerHTML = 'اطلاعات ناقص وارد شده است.'
    } else {
        data = {
            'comment': cm_id,
            'name': name,
            'email': email,
            'message': message
        }
        $.ajax({
            url: "/add-reply",
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=utf-8',
            headers: {
                'X-CSRFToken': csrf
            },
            success: function (data) {
                scssElem = 'success-msg-' + cm_id
                errorElem = 'invalid-cm-' + cm_id
                errorMessage = document.getElementById(errorElem)
                errorMessage.style.display = 'none'
                const success_message = document.getElementById(scssElem)
                success_message.innerHTML = 'پاسخ شما با موفقیت ارسال شد'
                success_message.style.display = 'block'
                document.getElementById(nameElem).value = ''
                document.getElementById(emailElem).value = ''
                document.getElementById(messageElem).value = ''
            }
        })
    }

}

function toggleService(target_id) {
    targetElem = '.item-' + target_id
    subElem = '.sub-' + target_id
    $(subElem).slideToggle("100");
    $(targetElem).find('img').toggleClass('arrow-up')
}

function submitComment(post_id) {
    const name = document.getElementById('id_full_name')
    const email = document.getElementById('id_email')
    const desc = document.getElementById('id_desc')
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
    const csrf = csrf_token[0].value
    if (name.value === '' || email.value === '' || desc === '') {
        const success_message = document.getElementById('invalid-cm')
        message = document.getElementById('invalid-cm')
        message.style.display = 'block'
        success_message.innerHTML = 'اطلاعات ناقص وارد شده است.'
    } else {
        data = {
            'name': name.value,
            'email': email.value,
            'desc': desc.value,
            'postId': post_id
        }
        $.ajax({
            url: "/submit-cm",
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=utf-8',
            headers: {
                'X-CSRFToken': csrf
            },
            success: function (data) {
                message = document.getElementById('invalid-cm')
                message.style.display = 'none'
                const success_message = document.getElementById('success-cm')
                success_message.innerHTML = 'دیدگاه شما با موفقیت ارسال شد'
                success_message.style.display = 'block'
                document.getElementById('id_full_name').value = ''
                document.getElementById('id_email').value = ''
                document.getElementById('id_desc').value = ''
            }
        })
    }
}

function sendHotelCm(hotel_id) {
    const name = document.getElementById('id_full_name')
    const email = document.getElementById('id_email')
    const desc = document.getElementById('id_desc')
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')
    const csrf = csrf_token[0].value
    const all_rate = document.getElementsByClassName('cmt_rate_filed')
    star_rate = ''
    for (i = 0; i < all_rate.length; i++) {
        if (all_rate[i].checked) {
            star_rate = all_rate[i].value
        }
    }
    if (name.value === "" || email.value === '' || desc.value === '') {
        const success_message = document.getElementById('invalid-cm')
        message = document.getElementById('invalid-cm')
        message.style.display = 'block'
        success_message.innerHTML = 'اطلاعات ناقص وارد شده است.'
    } else {
        data = {
            'name': name.value,
            'email': email.value,
            'desc': desc.value,
            'hotelId': hotel_id,
            'rate': star_rate
        }
        $.ajax({
            url: "/submit-hotel-cm",
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=utf-8',
            headers: {
                'X-CSRFToken': csrf
            },
            success: function (data) {
                message = document.getElementById('invalid-cm')
                message.style.display = 'none'
                const success_message = document.getElementById('success-cm')
                success_message.innerHTML = 'دیدگاه شما با موفقیت ارسال شد'
                success_message.style.display = 'block'
                document.getElementById('id_full_name').value = ''
                document.getElementById('id_email').value = ''
                document.getElementById('id_desc').value = ''
            }
        })
    }

}
/* ===== sort bar ===== */
window.currentSort = null;
window.currentSortDir = 1;
function applyCurrentSort() {
    if (!window.currentSort) return;
    var allTours = document.getElementById('all-tours');
    if (!allTours) return;
    // Keep sorted cards inside their visual wrapper. Appending directly to
    // #all-tours removes .tour-box's gap and makes cards stick together.
    var container = allTours.querySelector(':scope > .tour-box') || allTours.querySelector('.tour-box') || allTours;
    var cards = Array.from(container.querySelectorAll(':scope > .tour_grid'));
    if (!cards.length && container === allTours) {
        cards = Array.from(allTours.querySelectorAll('.tour_grid'));
    }
    if (cards.length < 2) return;
    var sort = window.currentSort;
    var dir = window.currentSortDir;
    cards.sort(function(a, b) {
        if (sort === 'price') {
            var rate = (window.DOLLAR_RATE || 170000);
            var aVal = (function(el) {
                var priceEl = el.querySelector('.irprice');
                if (!priceEl) return 0;
                var nums = (priceEl.textContent || '').match(/[\d,]+/g) || [];
                nums = nums.map(function(m){ return parseInt(m.replace(/,/g,''),10); }).filter(function(n){ return n>0; });
                if (!nums.length) return 0;
                if (nums[0] >= 1000000) return nums[0] + (nums[1]||0) * rate;
                return nums[0] * rate;
            })(a);
            var bVal = (function(el) {
                var priceEl = el.querySelector('.irprice');
                if (!priceEl) return 0;
                var nums = (priceEl.textContent || '').match(/[\d,]+/g) || [];
                nums = nums.map(function(m){ return parseInt(m.replace(/,/g,''),10); }).filter(function(n){ return n>0; });
                if (!nums.length) return 0;
                if (nums[0] >= 1000000) return nums[0] + (nums[1]||0) * rate;
                return nums[0] * rate;
            })(b);
            return (aVal - bVal) * dir;
        } else if (sort === 'duration') {
            return (parseInt(a.getAttribute('data-duration') || 0) - parseInt(b.getAttribute('data-duration') || 0)) * dir;
        } else if (sort === 'date') {
            var aDate = a.getAttribute('data-date') || '';
            var bDate = b.getAttribute('data-date') || '';
            return (aDate > bDate ? 1 : aDate < bDate ? -1 : 0) * dir;
        }
        return 0;
    });
    var frag = document.createDocumentFragment();
    cards.forEach(function(c){ frag.appendChild(c); });
    container.appendChild(frag);
}
function setSort(btn) {
    var sort = btn.getAttribute('data-sort');
    if (sort === window.currentSort) {
        window.currentSortDir = window.currentSortDir * -1;
        var dirIcon = btn.querySelector('.sort-dir-icon');
        if (dirIcon) {
            if (window.currentSortDir === -1) dirIcon.classList.add('flip');
            else dirIcon.classList.remove('flip');
        }
    } else {
        document.querySelectorAll('.sort-btn').forEach(function(b){
            b.classList.remove('active');
            var di = b.querySelector('.sort-dir-icon');
            if (di) di.classList.remove('flip');
        });
        btn.classList.add('active');
        window.currentSort = sort;
        window.currentSortDir = 1;
    }
    applyCurrentSort();
}
$(document).ajaxComplete(function(e, xhr, settings) {
    if (settings.url && settings.url.indexOf('sidebar_filter') !== -1) {
        setTimeout(applyCurrentSort, 30);
    }
});

/* ===== dynamic price slider max ===== */
function updatePriceSliderMax() {
    if (window._priceSliderInitialized) return;
    var rate = window.DOLLAR_RATE || 170000;
    var priceEls = document.querySelectorAll('#all-tours .irprice');
    if (!priceEls.length) return;
    var maxVal = 0;
    priceEls.forEach(function(priceEl) {
        var nums = (priceEl.textContent || '').match(/[\d,]+/g) || [];
        nums = nums.map(function(m){ return parseInt(m.replace(/,/g,''),10); }).filter(function(n){ return n > 0; });
        if (!nums.length) return;
        var val = nums[0] >= 1000000 ? nums[0] + (nums[1] || 0) * rate : nums[0] * rate;
        if (val > maxVal) maxVal = val;
    });
    if (maxVal <= 0) return;
    maxVal = Math.ceil(maxVal / 5000000) * 5000000;
    var toSlider = document.getElementById('toSlider');
    var fromSlider = document.getElementById('fromSlider');
    var toInput = document.getElementById('toInput');
    if (!toSlider || !fromSlider || !toInput) return;
    toSlider.max = maxVal;
    toSlider.value = maxVal;
    fromSlider.max = maxVal;
    toInput.value = maxVal.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    toSlider.dispatchEvent(new Event('input'));
    var ri = document.querySelector('.range-input');
    if (ri) ri.style.visibility = 'visible';
    window._priceSliderInitialized = true;
}

function _getTourPageInfo() {
    var type = '', slug = '';
    if (typeof category_slug !== 'undefined' && category_slug) { type = 'category'; slug = category_slug; }
    else if (typeof city !== 'undefined' && city && city !== 'undefined') { type = 'city'; slug = city; }
    else if (typeof country !== 'undefined' && country && country !== 'undefined') { type = 'country'; slug = country; }
    return { type: type, slug: slug };
}

function checkEmptyToursAndShowState() {
    var container = document.getElementById('all-tours');
    if (!container) return;
    if (container.querySelectorAll('.tour_grid').length > 0) {
        var es = document.getElementById('_tourEmptyState');
        if (es) es.style.display = 'none';
        container.style.display = '';
        var sc = document.querySelector('.sidebar-container');
        if (sc) sc.style.display = '';
        var sortBar = document.querySelector('.sort-bar');
        if (sortBar) sortBar.style.display = '';
        return;
    }
    container.style.display = 'none';
    var sc = document.querySelector('.sidebar-container');
    if (sc) sc.style.display = 'none';
    var sortBar = document.querySelector('.sort-bar');
    if (sortBar) sortBar.style.display = 'none';
    if (document.getElementById('_tourEmptyState')) return;
    var info = _getTourPageInfo();
    var html = '<div id="_tourEmptyState" style="padding:0 1rem 1rem; display:flex; justify-content:center;">' +
        '<div style="background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:2rem; width:100%; display:flex; align-items:center; gap:2rem; flex-wrap:wrap; overflow:hidden;">' +
        '<div style="flex:1 1 250px; min-width:0; overflow:hidden;">' +
        '<span style="display:inline-block; background:#ffc107; color:#633806; font-size:12px; padding:3px 14px; border-radius:6px; margin-bottom:0.75rem;">به زودی</span>' +
        '<h2 style="margin:0 0 0.5rem; font-size:18px; word-break:break-word;">تور فعال موجود نیست</h2>' +
        '<p style="color:#6b7280; font-size:14px; line-height:1.8; margin:0 0 1rem; word-break:break-word;">تاریخ‌های جدید این تور به‌زودی اعلام می‌شود. شماره موبایل خود را بگذارید تا به محض فعال شدن، اولین نفری باشید که خبردار می‌شوید.</p>' +
        '<div style="display:flex; flex-direction:column; gap:8px;">' +
        '<div style="display:flex; gap:8px; flex-wrap:wrap;">' +
        '<input id="_ti_name" type="text" placeholder="نام" style="flex:1 1 100px; min-width:0; padding:8px 12px; border:1px solid #d1d5db; border-radius:6px; text-align:right; direction:rtl; font-size:14px;" />' +
        '<input id="_ti_family" type="text" placeholder="نام خانوادگی" style="flex:1 1 100px; min-width:0; padding:8px 12px; border:1px solid #d1d5db; border-radius:6px; text-align:right; direction:rtl; font-size:14px;" />' +
        '</div>' +
        '<div style="display:flex; gap:8px; flex-wrap:wrap;">' +
        '<input id="_ti_phone" type="tel" placeholder="شماره موبایل" style="flex:1 1 100px; min-width:0; padding:8px 12px; border:1px solid #d1d5db; border-radius:6px; text-align:right; direction:rtl; font-size:14px;" />' +
        '<button onclick="submitTourInterest()" style="background:#185FA5; color:#fff; border:none; border-radius:6px; padding:0 20px; font-size:14px; cursor:pointer; white-space:nowrap;">ثبت شماره</button>' +
        '</div>' +
        '<div id="_ti_msg" style="font-size:13px; color:green; display:none; text-align:right;"></div>' +
        '</div></div>' +
        '<div id="_es_icon_div" style="flex:0 0 150px; width:150px; height:150px; background:#E6F1FB; border-radius:12px; display:flex; align-items:center; justify-content:center;">' +
        '<span style="font-size:60px;">✈️</span>' +
        '</div>' +
        '</div></div>';
    container.insertAdjacentHTML('afterend', html);
}

function submitTourInterest() {
    var name = (document.getElementById('_ti_name') || {}).value || '';
    var family = (document.getElementById('_ti_family') || {}).value || '';
    var phone = (document.getElementById('_ti_phone') || {}).value || '';
    var msg = document.getElementById('_ti_msg');
    if (!phone) { if (msg) { msg.style.color = 'red'; msg.textContent = 'لطفاً شماره موبایل را وارد کنید'; msg.style.display = 'block'; } return; }
    var info = _getTourPageInfo();
    var csrf = (document.getElementsByName('csrfmiddlewaretoken')[0] || {}).value || '';
    fetch('/save-tour-interest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
        body: JSON.stringify({ name: name, family: family, phone: phone, page_type: info.type, page_slug: info.slug })
    }).then(function(r) { return r.json(); }).then(function(d) {
        if (msg) {
            if (d.status === 'ok') { msg.style.color = 'green'; msg.textContent = 'با موفقیت ثبت شد. به محض فعال شدن تور خبرتان می‌کنیم.'; }
            else { msg.style.color = 'red'; msg.textContent = d.msg || 'خطا در ثبت'; }
            msg.style.display = 'block';
        }
    }).catch(function() { if (msg) { msg.style.color = 'red'; msg.textContent = 'خطا در ارتباط با سرور'; msg.style.display = 'block'; } });
}