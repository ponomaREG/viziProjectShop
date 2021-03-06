/*  ---------------------------------------------------
    Template Name: Ogani
    Description:  Ogani eCommerce  HTML Template
    Author: Colorlib
    Author URI: https://colorlib.com
    Version: 1.0
    Created: Colorlib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Gallery filter
        --------------------*/
        $('.featured__controls li').on('click', function () {
            $('.featured__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.featured__filter').length > 0) {
            var containerEl = document.querySelector('.featured__filter');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Humberger Menu
    $(".humberger__open").on('click', function () {
        $(".humberger__menu__wrapper").addClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").addClass("active");
        $("body").addClass("over_hid");
    });

    $(".humberger__menu__overlay").on('click', function () {
        $(".humberger__menu__wrapper").removeClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").removeClass("active");
        $("body").removeClass("over_hid");
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*-----------------------
        Categories Slider
    ------------------------*/
    // $(".categories__slider").owlCarousel({
    //     loop: true,
    //     margin: 0,
    //     items: 4,
    //     dots: false,
    //     nav: true,
    //     navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
    //     animateOut: 'fadeOut',
    //     animateIn: 'fadeIn',
    //     smartSpeed: 1200,
    //     autoHeight: false,
    //     autoplay: true,
    //     responsive: {

    //         0: {
    //             items: 1,
    //         },

    //         480: {
    //             items: 2,
    //         },

    //         768: {
    //             items: 3,
    //         },

    //         992: {
    //             items: 4,
    //         }
    //     }
    // });


    $('.hero__categories__all').on('click', function(){
        $('.hero__categories ul').slideToggle(400);
    });

    /*--------------------------
        Latest Product Slider
    ----------------------------*/
    // $(".latest-product__slider").owlCarousel({
    //     loop: true,
    //     margin: 0,
    //     items: 1,
    //     dots: false,
    //     nav: true,
    //     navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
    //     smartSpeed: 1200,
    //     autoHeight: false,
    //     autoplay: true
    // });

    /*-----------------------------
        Product Discount Slider
    -------------------------------*/
    // $(".product__discount__slider").owlCarousel({
    //     loop: true,
    //     margin: 0,
    //     items: 3,
    //     dots: true,
    //     smartSpeed: 1200,
    //     autoHeight: false,
    //     autoplay: true,
    //     responsive: {

    //         320: {
    //             items: 1,
    //         },

    //         480: {
    //             items: 2,
    //         },

    //         768: {
    //             items: 2,
    //         },

    //         992: {
    //             items: 3,
    //         }
    //     }
    // });

    /*---------------------------------
        Product Details Pic Slider
    ----------------------------------*/
    // $(".product__details__pic__slider").owlCarousel({
    //     loop: true,
    //     margin: 20,
    //     items: 4,
    //     dots: true,
    //     smartSpeed: 1200,
    //     autoHeight: false,
    //     autoplay: true
    // });

    /*-----------------------
		Price Range Slider
	------------------------ */
    var rangeSlider = $(".price-range"),
        minamount = $("#minamount"),
        maxamount = $("#maxamount"),
        minPrice = rangeSlider.data('min'),
        maxPrice = rangeSlider.data('max');
    rangeSlider.slider({
        range: true,
        min: minPrice,
        max: maxPrice,
        values: [minPrice, maxPrice],
        slide: function (event, ui) {
            minamount.val('$' + ui.values[0]);
            maxamount.val('$' + ui.values[1]);
        }
    });
    minamount.val('$' + rangeSlider.slider("values", 0));
    maxamount.val('$' + rangeSlider.slider("values", 1));

    /*--------------------------
        Select
    ----------------------------*/
    $("select").niceSelect();

    /*------------------
		Single Product
	--------------------*/
    $('.product__details__pic__slider img').on('click', function () {

        var imgurl = $(this).data('imgbigurl');
        var bigImg = $('.product__details__pic__item--large').attr('src');
        if (imgurl != bigImg) {
            $('.product__details__pic__item--large').attr({
                src: imgurl
            });
        }
    });

    /*-------------------
		Quantity change
	--------------------- */
    var proQty = $('.pro-qty');
    var productID = parseInt(proQty.attr('value'))
    var cost = parseFloat($('.product__details__price').text()).toFixed(1)
    // proQty.prepend('<span class="dec qtybtn">-</span>');
    // proQty.append('<span class="inc qtybtn">+</span>');
    proQty.on('click', '.qtybtn', function () {
        var $button = $(this);
        var oldValue = $button.parent().find('input').val();
        if ($button.hasClass('inc')) {
            $.getJSON('/api/cart/add','product='+productID,function(data){
            if(data.status == 120){
                window.location.replace('/login')
            }else if(data.status == 0){
                var newVal = parseFloat(oldValue) + 1;
                $button.parent().find('input').val(newVal);
                updateIndicators(1,cost)
            }else{
                alert(data.message)
            }
            })
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 0) {
                $.getJSON('/api/cart/remove','product='+productID,function(data){
            if(data.status == 120){
                window.location.replace('/login')
            }else if(data.status == 0){
                var newVal = parseFloat(oldValue) - 1;
                $button.parent().find('input').val(newVal);
                updateIndicators(-1,-cost)
                if(oldValue == 1){
                    proQty.css('display','none')
                    var buttonAddInCart = $('#primary__btn__add__to__cart')
                    buttonAddInCart.css('display','inline-block')
                }
            }else{
                alert(data.message)
            }
            })
            } else {
                proQty.css('display','none')
                var buttonAddInCart = $('#primary__btn__add__to__cart')
                buttonAddInCart.css('display','inline-block')
            }
        
        }
    });


    var prBtn = $('#primary__btn__add__to__cart')
    prBtn.on('click',function(){
        $.getJSON('/api/cart/add','product='+productID,function(data){
            if(data.status == 120){
                window.location.replace('/login')
            }else if(data.status == 0){
                proQty.find('input').val('1')
                updateIndicators(1,cost)
                proQty.css('display','inline-block')
                prBtn.css('display','none')
            }else{
                alert(data.message)
            }
            })
    });
    

    var shoppingCart = $('.shopping__cart')
    shoppingCart.on('click', function(){
        var productID = $(this).attr('id')
        var cost = parseFloat($(this).attr('value'))
        $.getJSON('/api/cart/add','product='+productID,function(data){
            console.log(data)
            if(data.status == 120){
                window.location.replace('/login')
            }
            else if(data.status == 0){
                var delay = 2000;
                document.getElementById('msg_pop').style.className -= ' fadeOut'
                document.getElementById('msg_pop').className += ' fadeIn';
                document.getElementById('msg_pop').style.display='block';
                setTimeout("document.getElementById('msg_pop').className -= ' fadeIn';$('#msg_pop').fadeOut('slow');", delay);
                updateIndicators(1,cost)

            }
            else{
                alert(data.message)
            }

        })
    })

    function updateIndicators(val,cost){
                var indicator = $('#fa__fa-shopping-bag__indicator__quantity')
                indicator.text(parseInt(indicator.text()) + val)
                var indicator_humberg = $('#humberg__fa__fa-shopping-bag__indicator__quantity')
                indicator_humberg.text(parseInt(indicator_humberg.text()) + val)
                var indicatorTotalCost = $('#header__cart__price__totalCost')
                indicatorTotalCost.text((parseFloat(indicatorTotalCost.text()) + parseFloat(cost)).toFixed(1) + "P");
                var indicatorTotalCostHumberg = $('#humberg__header__cart__price__totalCost')
                indicatorTotalCostHumberg.text((parseFloat(indicatorTotalCostHumberg.text()) + parseFloat(cost)).toFixed(1)+"P");
    }


    var qtyCart = $('.pro-qty-cart')

    qtyCart.on('click','.qtybtn',function(){
        
        var $button = $(this)
        var productID = parseInt($button.parent().attr('value'))
        var oldValue = parseInt($button.parent().find('input').val())
        var cost = parseFloat($button.parent().attr('id'))
        if($button.hasClass('inc')){
            $.getJSON('/api/cart/add','product='+productID,function(data){
                if(data.status == 120){
                    window.location.replace('/login')
                }else if(data.status == 0){
                    var newVal = parseFloat(oldValue) + 1;
                    $button.parent().find('input').val(newVal);
                    var $total = $('tr#'+productID).find('.shoping__cart__total')
                    $total.text((parseFloat($total.text())+cost).toFixed(1) + 'P')
                    var $totalCost = $('.shoping__checkout')
                    var oldCost = parseFloat($totalCost.find('span').text())
                    $totalCost.find('span').text(parseFloat((oldCost+cost)).toFixed(1)+'P')
                    updateIndicators(1,cost)
            }else{
                alert(data.message)
            }
            })
        }else{
            if (oldValue > 0) {
                $.getJSON('/api/cart/remove','product='+productID,function(data){
            if(data.status == 120){
                window.location.replace('/login')
            }else if(data.status == 0){
                var newVal = oldValue - 1;
                $button.parent().find('input').val(newVal);
                var $total = $('tr#'+productID).find('.shoping__cart__total')
                $total.text((parseFloat($total.text())-cost).toFixed(1) + 'P')
                var $totalCost = $('.shoping__checkout')
                $totalCost.find('span').text((parseFloat($totalCost.find('span').text()).toFixed(1)-cost).toFixed(1)+'P')
                updateIndicators(-1,-cost);
                if(oldValue == 1){
                    var container = $('tr#'+productID+' ');
                    container.css('display','none'); //TODO:CHECK EMPTY CART
                    if(parseFloat($('#header__cart__price__totalCost').text()) == 0){
                        $('#primary-btn-checkout').css('display','none')
                    }
                }
            }else{
                alert(data.message);
            }
            })
            } else {
                var container = $('td#'+productID);
                container.css('display','none');
            }
        }

        })



    var ratingBar = $('#rating-bar');
    var ratingBarButton = $('#rating-bar-submit')
    var ratingBarStatus = $('#rating-bar-status')
    ratingBarButton.on('click',function(){
        console.log(parseInt(ratingBar.attr('value')));
        console.log(parseInt(ratingBar.val()));
        console.log(ratingBar.val())
        $.getJSON('/api/rate',
        {
            'productID':parseInt(ratingBar.attr('value')),
            'mark':parseInt(ratingBar.val())
        },function(data){
            console.log(data.status)
            if(data.status == 120){
                window.location.replace('/login')
            }else if(data.status == 0){
                ratingBarStatus.text('Вы поставили свою оценку')
            } else if(data.status == 9){
                ratingBarStatus.text('Вы уже поставили свою оценку')
            }
        })
    })
    
    


})(jQuery);