$(document).ready(function () {
  const pathname = window.location.pathname;
  const newpath = pathname.slice(0, 25);
  const upackgepath = pathname.slice(0, 25);
  const walletpath = pathname.slice(0, 29);
  const tripPath = pathname.slice(0, 25);
  console.log(tripPath);
  // Function to make AJAX call for updating content
  function updateContent(
    url,
    target,
    page,
    hotelName,
    hotelNameEn,
    city,
    callback
  ) {
    $.ajax({
      url: url,
      data: {
        page: page,
        hotel_name: hotelName,
        hotel_name_eng: hotelNameEn,
        city: city,
      },
      success: function (data) {
        $(target).html(data);
      },
    });
  }

  //Initial AJAX calls
  if (pathname === "/dashboard/hotels/hotel_list") {
    updateContent("/dashboard/hotels/ajax_hotel_list/", "#hotel_list");
    $("#searchBtn").on("click", function () {
      const hotelName = $("#id_hotel_name").val();
      const hotelNameEn = $("#id_hotel_name_eng").val();
      const city = $("#city_name").val();
      updateContent(
        "/dashboard/hotels/ajax_hotel_list/",
        "#hotel_list",
        1,
        hotelName,
        hotelNameEn,
        city
      );
    });
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      const hotelName = $("#id_hotel_name").val();
      const hotelNameEn = $("#id_hotel_name_eng").val();
      const city = $("#city_name").val();
      updateContent(
        "/dashboard/hotels/ajax_hotel_list/",
        "#hotel_list",
        page,
        hotelName,
        hotelNameEn,
        city,
        function () {
          elem.addClass("active");
        }
      );
    });
    // AJAX call for city names
    $.ajax({
      url: "/dashboard/hotels/hotel_cities_ajax/",
      success: function (data) {
        $("#city_name").html(data);
      },
    });
  }
  if (pathname === "/dashboard/airlines-list/") {
    updateContent("/dashboard/ajax_airline_list/", "#airline_data");
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      // Update airline data and add active class
      updateContent(
        "/dashboard/ajax_airline_list/",
        "#airline_data",
        page,
        function () {
          elem.addClass("active");
        }
      );
    });
  }
  if (pathname === "/dashboard/country_list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateCountry(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    // UPDATE PAGE WITH FUNCTION
    updateCountry("/dashboard/ajax_country_list/", "#country_list");
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateContent("/dashboard/ajax_country_list/", "#country_list", page);
    });
  }
  if (pathname === "/dashboard/city_list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateCity(url, target, page, country_name, city_name) {
      $.ajax({
        url: url,
        data: {
          page: page,
          country_name: country_name,
          city_name: city_name,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    // UPDATE PAGE WITH FUNCTION
    updateCity("/dashboard/ajax_city_list/", "#city_list");
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      const country_name = $("#country-name").val();
      const city_name = $("#city-name").val();
      updateCity(
        "/dashboard/ajax_city_list/",
        "#city_list",
        page,
        country_name,
        city_name
      );
    });
    $("#searchBtn").on("click", function () {
      const country_name = $("#country-name").val();
      const city_name = $("#city-name").val();
      updateCity(
        "/dashboard/ajax_city_list/",
        "#city_list",
        1,
        country_name,
        city_name
      );
    });
  }
  if (pathname === "/dashboard/tour-list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateTour(
      url,
      target,
      page,
      tourname,
      startdate,
      enddate,
      tour_stat
    ) {
      $.ajax({
        url: url,
        data: {
          page: page,
          tourname: tourname,
          startdate: startdate,
          enddate: enddate,
          tour_stat: tour_stat,
        },
        success: function (data) {
          $(target).html(data);
          const Toast = Swal.mixin({
            toast: true,
            position: "top-end",
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
              toast.onmouseenter = Swal.stopTimer;
              toast.onmouseleave = Swal.resumeTimer;
            },
          });
          Toast.fire({
            icon: "success",
            title: "لیست تورها بارگذاری شد.",
          });
        },
      });
    }

    // UPDATE PAGE WITH FUNCTION
    updateTour("/dashboard/ajax_tour_list/", "#tour_list");
    $("#searchBtn").on("click", function () {
      const tourname = $("#id_tour_name").val();
      const startdate = $("#hide_start_date").val();
      const enddate = $("#hide_end_date").val();
      const tour_stat = $("#tour_stat").val();
      updateTour(
        "/dashboard/ajax_tour_list/",
        "#tour_list",
        1,
        tourname,
        startdate,
        enddate,
        tour_stat
      );
    });
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      const tourname = $("#id_tour_name").val();
      const startdate = $("#hide_start_date").val();
      const enddate = $("#hide_end_date").val();
      const tour_stat = $("#tour_stat").val();
      updateTour(
        "/dashboard/ajax_tour_list/",
        "#tour_list",
        page,
        tourname,
        startdate,
        enddate,
        tour_stat
      );
    });
  }
  if (pathname === "/dashboard/blog/post-list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updatePosts(
      url,
      target,
      page,
      post_title,
      post_category,
      post_stat
    ) {
      $.ajax({
        url: url,
        data: {
          page: page,
          post_title: post_title,
          post_category: post_category,
          active: post_stat,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    // UPDATE PAGE WITH FUNCTION
    updatePosts("/dashboard/ajax_posts_list/", "#post_list");
    $("#searchBtn").on("click", function () {
      const post_title = $("#post_title").val();
      const post_category = $("#post_cat").val();
      const active = $("#post_stat").val();
      updatePosts(
        "/dashboard/ajax_posts_list/",
        "#post_list",
        1,
        post_title,
        post_category,
        active
      );
    });
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      const post_title = $("#post_title").val();
      const post_category = $("#post_cat").val();
      const active = $("#post_stat").val();
      updatePosts(
        "/dashboard/ajax_posts_list/",
        "#post_list",
        page,
        post_title,
        post_category,
        active
      );
    });
  }
  if (pathname === "/pages/file_list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateFiles(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    // UPDATE PAGE WITH FUNCTION
    updateFiles("/pages/ajax_file_list", "#file_list");
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateFiles("/pages/ajax_file_list", "#file_list", page);
    });
  }
  if (pathname === "/pages/ads_file_list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateAdsFiles(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    // UPDATE PAGE WITH FUNCTION
    updateAdsFiles("/pages/ajax_ads_files", "#file_list");
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateFiles("/pages/ajax_ads_files", "#file_list", page);
    });
  }
  if (pathname === "/dashboard/order-list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateOrderList(url, target, page, mobile, trs_code, view) {
      $.ajax({
        url: url,
        data: {
          page: page,
          mobile: mobile,
          trs_code: trs_code,
          view: view,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updateOrderList("/dashboard/ajax_order_list/", "#order_list");
    $("#searchBtn").on("click", function () {
      const mobile = $("#mobile").val();
      const trs_code = $("#trs_code").val();
      const view = $("#view").val();
      updateOrderList(
        "/dashboard/ajax_order_list/",
        "#order_list",
        1,
        mobile,
        trs_code,
        view
      );
    });
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      const mobile = $("#mobile").val();
      const trs_code = $("#trs_code").val();
      const view = $("#view").val();
      updateOrderList(
        "/dashboard/ajax_order_list/",
        "#order_list",
        page,
        mobile,
        trs_code,
        view
      );
    });
  }
  if (pathname === "/dashboard/memo-list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateMemoList(url, target, page, mobile, email, memo_stat) {
      $.ajax({
        url: url,
        data: {
          page: page,
          mobile: mobile,
          email: email,
          memo_stat: memo_stat,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updateMemoList("/dashboard/ajax_memories_list/", "#memo_list");
    $("#searchBtn").on("click", function () {
      const mobile = $("#mobile").val();
      const email = $("#email").val();
      const memo_stat = $("#memo_stat").val();
      updateMemoList(
        "/dashboard/ajax_memories_list/",
        "#memo_list",
        1,
        mobile,
        email,
        memo_stat
      );
    });
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      const mobile = $("#mobile").val();
      const email = $("#email").val();
      const memo_stat = $("#memo_stat").val();
      updateMemoList(
        "/dashboard/ajax_memories_list/",
        "#memo_list",
        page,
        mobile,
        email,
        memo_stat
      );
    });
  }
  if (pathname === "/dashboard/memo-category-list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateMemoCategoryList(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }
    updateMemoCategoryList("/dashboard/ajax_memo_categories/", "#memo_category_list");
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateMemoCategoryList(
        "/dashboard/ajax_memo_categories/",
        "#memo_category_list",
        page
      );
    });
  }
  if (pathname === "/dashboard/list-tour-category") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateListTourCategory(url, target, page) {

      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }
    updateListTourCategory("/dashboard/ajax_tour_categories/", "#list_tour_category");
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateListTourCategory(
        "/dashboard/ajax_tour_categories/",
        "#list_tour_category",
        page
      );
    });
  }
  if (pathname === "/user/user_list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateUserList(url, target, page, user, user_stat) {
      $.ajax({
        url: url,
        data: {
          page: page,
          user: user,
          user_stat: user_stat,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updateUserList("/user/ajax_user_list", "#user_list");
    $("#searchBtn").on("click", function () {
      const user = $("#username").val();
      const user_stat = $("#user_stat").val();
      updateUserList("/user/ajax_user_list", "#user_list", 1, user, user_stat);
    });
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      const user = $("#username").val();
      const user_stat = $("#user_stat").val();
      updateUserList(
        "/user/ajax_user_list",
        "#user_list",
        page,
        user,
        user_stat
      );
    });
  }
  if (pathname === "/dashboard/messages") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateMsgList(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updateMsgList("/dashboard/ajax_allmsg_list/", "#msg_list");
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateMsgList("/dashboard/ajax_allmsg_list/", "#msg_list", page);
    });
  }
  if (pathname === "/dashboard/create-airport") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateAirportList(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updateAirportList("/dashboard/ajax_airpots_list/", "#airport_list");
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateAirportList("/dashboard/ajax_airpots_list/", "#airport_list", page);
    });
  }
  if (pathname === "/dashboard/blog/post-category-list") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateCategoryList(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updateCategoryList("/dashboard/ajax_post_categories/", "#category_list");
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateCategoryList(
        "/dashboard/ajax_post_categories/",
        "#category_list",
        page
      );
    });
  }
  if (walletpath === "/dashboard/wallet/wallet_data") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateWalletwithdrawal(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updateWalletwithdrawal(
      "/dashboard/wallet/ajax_wallet_withdrawal?wallet_id=" + wallet_id,
      "#wallet_withdrawal"
    );
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateWalletwithdrawal(
        "/dashboard/wallet/ajax_wallet_withdrawal?wallet_id=" + wallet_id,
        "#wallet_withdrawal",
        page
      );
    });
  }
  if (walletpath === "/dashboard/wallet/wallet_data") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateWalletdeposit(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updateWalletdeposit(
      "/dashboard/wallet/ajax_wallet_deposite?wallet_id=" + wallet_id,
      "#wallet_deposite"
    );
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item-deposite", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateWalletdeposit(
        "/dashboard/wallet/ajax_wallet_deposite?wallet_id=" + wallet_id,
        "#wallet_deposite",
        page
      );
    });
  }
  if (pathname === "/dashboard/create-package/") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updateMpackagesList(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updateMpackagesList("/dashboard/ajax_mainPAckages_list/", "#Mpackages");
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updateMpackagesList(
        "/dashboard/ajax_mainPAckages_list/",
        "#Mpackages",
        page
      );
    });
  }
  if (newpath === "/dashboard/add-to-package") {
    $.ajax({
      url: "/dashboard/package_hotel_list/",
      data: {},
      success: function (data) {
        $("#id_HotelName").append(data);
        $("#id_Mhotel").append(data);
        $("#id_M1hotel").append(data);
        $("#id_M2hotel").append(data);
        $("#id_M3hotel").append(data);
        $(".text-input-hts").selectize();
      },
    });
    $("#id_HotelName").change(function () {
      var id = $("#id_HotelName").val();
      $("#hotelname_id").val(id);
    });
    $("#id_Mhotel").change(function () {
      var id = $("#id_Mhotel").val();
      $("#hotelname2_id").val(id);
    });
    $("#id_M1hotel").change(function () {
      var id = $("#id_M1hotel").val();
      $("#hotelname3_id").val(id);
    });
    $("#id_M2hotel").change(function () {
      var id = $("#id_M2hotel").val();
      $("#hotelname4_id").val(id);
    });
    $("#id_M3hotel").change(function () {
      var id = $("#id_M3hotel").val();
      $("#hotelname5_id").val(id);
    });
    $("#getValues").click(function () {
      var selectedValues = [];
      $(".checkbox:checked").each(function () {
        selectedValues.push($(this).val());
      });
      var jsonString = JSON.stringify(selectedValues);
      var dobel_price = document.getElementById("dubel").value;
      var single_price = document.getElementById("single").value;
      var bwb_price = document.getElementById("bwb").value;
      var bwob_price = document.getElementById("bwob").value;
      var infont_price = document.getElementById("infont").value;
      $.ajax({
        type: "GET",
        url: "/dashboard/change_price_selected_package/",
        data: {
          packages: jsonString,
          double: dobel_price,
          singel: single_price,
          bwb_price: bwb_price,
          bwob_price: bwob_price,
          infont_price: infont_price,
        },
        success: function () {
          document.getElementById("dubel").value = 0;
          document.getElementById("single").value = 0;
          document.getElementById("bwb").value = 0;
          document.getElementById("bwob").value = 0;
          document.getElementById("infont").value = 0;
          const Toast = Swal.mixin({
            toast: true,
            position: "top-end",
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
              toast.onmouseenter = Swal.stopTimer;
              toast.onmouseleave = Swal.resumeTimer;
            },
          });
          Toast.fire({
            icon: "success",
            title: "تغییرات قیمت با موفقیت ثبت شد.",
          });
          setTimeout(function () {
            window.location.reload();
          }, 5000);
        },
      });
      $(".text-input-hts").selectize();
      $('input[type="file"]').change(function (e) {
        var fileName = e.target.files[0].name;
        document.getElementById("filename").innerHTML =
          "  فایل انتخابی: " + fileName;
      });
    });
  }
  if (upackgepath === "/dashboard/update-package") {
    $.ajax({
      url: "/dashboard/package_hotel_list/",
      data: {},
      success: function (data) {
        $("#id_HotelName").append(data);
        $("#id_Mhotel").append(data);
        $("#id_M1hotel").append(data);
        $("#id_M2hotel").append(data);
        $("#id_M3hotel").append(data);
        $(".text-input-hts").selectize();
      },
    });
    $("#id_HotelName").change(function () {
      var id = $("#id_HotelName").val();
      $("#hotelname_id").val(id);
    });
    $("#id_Mhotel").change(function () {
      var id = $("#id_Mhotel").val();
      $("#hotelname2_id").val(id);
    });
    $("#id_M1hotel").change(function () {
      var id = $("#id_M1hotel").val();
      $("#hotelname3_id").val(id);
    });
    $("#id_M2hotel").change(function () {
      var id = $("#id_M2hotel").val();
      $("#hotelname4_id").val(id);
    });
    $("#id_M3hotel").change(function () {
      var id = $("#id_M3hotel").val();
      $("#hotelname5_id").val(id);
    });
    $("#getValues").click(function () {
      var selectedValues = [];
      $(".checkbox:checked").each(function () {
        selectedValues.push($(this).val());
      });
      var jsonString = JSON.stringify(selectedValues);
      var dobel_price = document.getElementById("dubel").value;
      var single_price = document.getElementById("single").value;
      var bwb_price = document.getElementById("bwb").value;
      var bwob_price = document.getElementById("bwob").value;
      var infont_price = document.getElementById("infont").value;
      $.ajax({
        type: "GET",
        url: "/dashboard/change_price_selected_package/",
        data: {
          packages: jsonString,
          double: dobel_price,
          singel: single_price,
          bwb_price: bwb_price,
          bwob_price: bwob_price,
          infont_price: infont_price,
        },
        success: function () {
          document.getElementById("dubel").value = 0;
          document.getElementById("single").value = 0;
          document.getElementById("bwb").value = 0;
          document.getElementById("bwob").value = 0;
          document.getElementById("infont").value = 0;
          location.reload();
        },
      });
      $(".text-input-hts").selectize();
      $('input[type="file"]').change(function (e) {
        var fileName = e.target.files[0].name;
        document.getElementById("filename").innerHTML =
          "  فایل انتخابی: " + fileName;
      });
    });
  }
  if (pathname === "/dashboard/online-orders/") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function paidOrdersUpdate(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    paidOrdersUpdate(
      "/dashboard/online-orders/ajax_paid_order",
      "#paid_orders"
    );
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      paidOrdersUpdate(
        "/dashboard/online-orders/ajax_paid_order",
        "#paid_orders",
        page
      );
    });
  }
  if (pathname === "/dashboard/online-orders/") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function pendingOrdersUpdate(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    pendingOrdersUpdate(
      "/dashboard/online-orders/ajax_pending_order",
      "#pending_orders"
    );
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      pendingOrdersUpdate(
        "/dashboard/online-orders/ajax_pending_order",
        "#pending_orders",
        page
      );
    });
  }
  if (pathname === "/dashboard/online-orders/") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function wallet_transactions_update(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    wallet_transactions_update(
      "/dashboard/online-orders/ajax_wallet_transaction",
      "#wallet_transaction"
    );
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item-wallet", function () {
      const elem = $(this);
      const page = elem.data("page");
      wallet_transactions_update(
        "/dashboard/online-orders/ajax_wallet_transaction",
        "#wallet_transaction",
        page
      );
    });
  }
  if (pathname === "/dashboard/online-orders/all_paid_orders") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updatePaidOrdersList(
      url,
      target,
      page,
      trs_code,
      paid_date,
      submit_date
    ) {
      $.ajax({
        url: url,
        data: {
          page: page,
          trs_code: trs_code,
          paid_date: paid_date,
          submit_date: submit_date,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updatePaidOrdersList(
      "/dashboard/online-orders/all_ajax_paid_order",
      "#paid_orders"
    );
    $("#searchBtn").on("click", function () {
      const trs_code = $("#trs_code").val();
      const paid_date = $("#id_paid_date").val();
      const submit_date = $("#id_submit_date").val();
      updatePaidOrdersList(
        "/dashboard/online-orders/all_ajax_paid_order",
        "#paid_orders",
        1,
        trs_code,
        paid_date,
        submit_date
      );
    });
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      const trs_code = $("#trs_code").val();
      const paid_date = $("#id_paid_date").val();
      const submit_date = $("#id_submit_date").val();
      updatePaidOrdersList(
        "/dashboard/online-orders/all_ajax_paid_order",
        "#paid_orders",
        page,
        trs_code,
        paid_date,
        submit_date
      );
    });
  }
  if (pathname === "/dashboard/online-orders/all_pending_orders") {
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updatePendingOrdersList(
      url,
      target,
      page,
      trs_code,
      paid_date,
      submit_date
    ) {
      $.ajax({
        url: url,
        data: {
          page: page,
          trs_code: trs_code,
          paid_date: paid_date,
          submit_date: submit_date,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updatePendingOrdersList(
      "/dashboard/online-orders/all_ajax_pending_order",
      "#paid_orders"
    );
    $("#searchBtn").on("click", function () {
      const trs_code = $("#trs_code").val();
      const paid_date = $("#id_paid_date").val();
      const submit_date = $("#id_submit_date").val();
      updatePendingOrdersList(
        "/dashboard/online-orders/all_ajax_pending_order",
        "#paid_orders",
        1,
        trs_code,
        paid_date,
        submit_date
      );
    });
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      const trs_code = $("#trs_code").val();
      const paid_date = $("#id_paid_date").val();
      const submit_date = $("#id_submit_date").val();
      updatePendingOrdersList(
        "/dashboard/online-orders/all_ajax_pending_order",
        "#paid_orders",
        page,
        trs_code,
        paid_date,
        submit_date
      );
    });
  }
  if (tripPath === "/dashboard/add_trip_plan/") {
    console.log("tripPath");
    // AJAX CALL FUNCTION FOR COUNTRY LIST
    function updatePtripplansList(url, target, page) {
      $.ajax({
        url: url,
        data: {
          page: page,
        },
        success: function (data) {
          $(target).html(data);
        },
      });
    }

    updatePtripplansList(
      "/dashboard/ajax_trip_plans/?tour_id=" + tour_id,
      "#plans_data",
      1
    );
    // PAGINATION WITHOUT SEARCH TERM
    $(document).on("click", ".page-item", function () {
      const elem = $(this);
      const page = elem.data("page");
      updatePtripplansList(
        "/dashboard/ajax_trip_plans/?tour_id=" + tour_id,
        "#plans_data",
        page
      );
    });
  }
});

function isNumberKey(evt) {
  var charCode = evt.which ? evt.which : evt.keyCode;
  if (charCode === 44) {
    return true;
  } else if (charCode > 31 && (charCode < 48 || charCode > 57)) {
    // Allow only numeric digits and commas
    return false;
  }
}

function separateDigits() {
  let inputElement = document.getElementById("wallet_balance");
  let number = inputElement.value;
  number = number.replace(/,/g, "");
  number = parseInt(number);
  if (isNaN(number)) {
    inputElement.value = "0";
  } else {
    inputElement.value = number.toLocaleString("en-US");
  }
}

function wallet_charging() {
  let inputElement = document.getElementById("wallet_balance");
  let number = inputElement.value;
  number = number.replace(/,/g, "");
  number = parseInt(number);
  let charg_link = document.getElementById("charge_link");
  charg_link.href =
    "/dashboard/wallet/start_wallet_charge?wallet_id=" +
    wallet_id +
    "&amount=" +
    number;
}

function packageChangeSingle(package_id) {
  var hotel1 = document.getElementById("hotel1-" + package_id).value;
  var hotel2 = document.getElementById("hotel2-" + package_id).value;
  var hotel3 = document.getElementById("hotel3-" + package_id).value;
  var hotel4 = document.getElementById("hotel4-" + package_id).value;
  var hotel5 = document.getElementById("hotel5-" + package_id).value;
  var hotel1_view = document.getElementById("hotel1-view-" + package_id).value;
  var hotel2_view = document.getElementById("hotel2-view-" + package_id).value;
  var hotel3_view = document.getElementById("hotel3-view-" + package_id).value;
  var hotel4_view = document.getElementById("hotel4-view-" + package_id).value;
  var hotel5_view = document.getElementById("hotel5-view-" + package_id).value;
  var hotel1_service = document.getElementById(
    "hotel1-service-" + package_id
  ).value;
  var hotel2_service = document.getElementById(
    "hotel2-service-" + package_id
  ).value;
  var hotel3_service = document.getElementById(
    "hotel3-service-" + package_id
  ).value;
  var hotel4_service = document.getElementById(
    "hotel4-service-" + package_id
  ).value;
  var hotel5_service = document.getElementById(
    "hotel5-service-" + package_id
  ).value;
  var mainpackages = document.getElementById(
    "mainpackages-" + package_id
  ).value;
  var prcy = document.getElementById("prcy-" + package_id).value;
  var fr_Pcry = document.getElementById("fr_Pcry-" + package_id).value;
  var main_view = document.getElementById("main-view-" + package_id).value;
  var d_price = document.getElementById("doubel-price-" + package_id).value;
  var s_price = document.getElementById("single-price-" + package_id).value;
  var bwb_price = document.getElementById("bwb-" + package_id).value;
  var bwob_price = document.getElementById("bwob-" + package_id).value;
  var infont_price = document.getElementById("infont-" + package_id).value;
  var d_price_d = document.getElementById(
    "doller-doubel-price-" + package_id
  ).value;
  var s_price_d = document.getElementById(
    "doller-single-price-" + package_id
  ).value;
  var bwb_price_d = document.getElementById("doller-bwb-" + package_id).value;
  var bwob_price_d = document.getElementById("doller-bwob-" + package_id).value;
  var infont_price_d = document.getElementById(
    "doller-infont-" + package_id
  ).value;
  var static_price_d = document.getElementById(
    "static_DollerPrice-" + package_id
  ).value;
  var soldoutEl = document.getElementById("soldout-" + package_id);
  var soldout = soldoutEl ? soldoutEl.checked : false;
  $.ajax({
    url: "/dashboard/change_package_price_single/",
    data: {
      package_id: package_id,
      soldout: soldout,
      d_price: d_price,
      s_price: s_price,
      bwb_price: bwb_price,
      bwob_price: bwob_price,
      infont_price: infont_price,
      d_price_d: d_price_d,
      s_price_d: s_price_d,
      bwb_price_d: bwb_price_d,
      bwob_price_d: bwob_price_d,
      infont_price_d: infont_price_d,
      static_price_d: static_price_d,
      hotel1: hotel1,
      hotel2: hotel2,
      hotel3: hotel3,
      hotel4: hotel4,
      hotel5: hotel5,
      hotel1_view: hotel1_view,
      hotel2_view: hotel2_view,
      hotel3_view: hotel3_view,
      hotel4_view: hotel4_view,
      hotel5_view: hotel5_view,
      hotel1_service: hotel1_service,
      hotel2_service: hotel2_service,
      hotel3_service: hotel3_service,
      hotel4_service: hotel4_service,
      hotel5_service: hotel5_service,
      mainpackages: mainpackages,
      prcy: prcy,
      fr_Pcry: fr_Pcry,
      main_view: main_view,
    },
    success: function (data) {
      const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.onmouseenter = Swal.stopTimer;
          toast.onmouseleave = Swal.resumeTimer;
        },
      });
      Toast.fire({
        icon: "success",
        title: "تغییر قیمت ثبت شد.",
      });
    },
  });
  console.log(
    package_id,
    d_price,
    s_price,
    bwb_price,
    bwob_price,
    infont_price,
    d_price_d,
    s_price_d,
    bwb_price_d,
    bwob_price_d,
    infont_price_d
  );
}

function getCityList() {
  country = document.getElementById("id_country").value;
  $.ajax({
    url: "/dashboard/related_city_ajax/",
    data: {
      country: country,
    },
    success: function (data) {
      $("#id_city").html(data);
    },
  });
}

function getTourList() {
  city = document.getElementById("id_city").value;
  $.ajax({
    url: "/dashboard/related_tour_ajax/",
    data: {
      city: city,
    },
    success: function (data) {
      $("#id_related_tour").html(data);
    },
  });
}

function getPstList() {
  category = document.getElementById("category").value;
  $.ajax({
    url: "/dashboard/blog/ajax_related_pst",
    data: {
      category: category,
    },
    success: function (data) {
      $("#id_related_post").html(data);
    },
  });
}

function getHotelsList(packageId, elemTag) {
  var tagId = "#" + elemTag;
  $.ajax({
    url: "/dashboard/package_hotel_list/",
    data: {},
    success: function (data) {
      $(tagId).append(data).select2();
    },
  });
}