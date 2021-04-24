var Base = {
    init:function(){
        Base.mmenu();
        Base.headerScroll();
    },
    mmenu:function(){
        $('#my-menu').mmenu({
            "slidingSubmenus": false,
            "extensions": [
               "theme-dark"
            ]
         });
    },
    headerScroll:function(){
        var header = $('.header');
        /// ON LOAD
        if($(window).scrollTop() >= 100){
            header.toggleClass('active')
        }
        // WHEN SCROLL
        $(window).scroll(function(){
            if($(window).scrollTop() >= 100){
                header.addClass('active')
            } else{
                header.removeClass('active')
            }
        })
    }
}
$(function(){
    Base.init()
})