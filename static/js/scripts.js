// HOME TABS
$(".tabs-menu a").click(function(event) {
	event.preventDefault();
	$(this).parent().addClass("current");
	$(this).parent().siblings().removeClass("current");
	var tab = $(this).attr("href");
	$(".tab-content").not(tab).css("display", "none");
	$(tab).fadeIn();
});


// BOOKING: SECONDARY NAVIGATION
$(".nav a.triggerNav").click(function(event) {
	event.preventDefault();
	$(this).parent().toggleClass("current");
	$(this).parent().siblings().removeClass("current");
	var tab = $(this).attr("href");
	$(".booking-nav-hidden").not(tab).toggleClass("display");
	$(tab).toggleClass("display");
});


// MAIN NAVIGATION
$('#triggerStMenu, #closeBtn').click(function(){
	$('.st-menu.hidden-menu').toggleClass('show');
});


// SLIDER ONE COLUMN
$('.one-col-slider').slick({
	slidesToShow: 1,
	slide: '.slider-item',
	arrows: true,
	prevArrow: '<span class="slick-prev"></span>',
	nextArrow: '<span class="slick-next"></span>',
	appendArrows: '.one-col-slider .arrow-container'
});


// SLIDER SIX COLUMNS
$('.six-col-slider').slick({
	slidesToShow: 6,
	infinite: true,
	slidesToScroll: 1,
	slide: '.slider-item',
	arrows: true,
	prevArrow: '<span class="slick-prev"></span>',
	nextArrow: '<span class="slick-next"></span>',
	appendArrows: '.six-col-slider .arrow-container',
	responsive: [
	{
		breakpoint:  1200,
		settings: {
			slidesToShow: 4
		}
	},
	{
		breakpoint: 800,
		settings: {
			slidesToShow: 3
		}
	},
	{
		breakpoint: 420,
		settings: {
		  slidesToShow: 2
		}
	},
	{
		breakpoint: 300,
		settings: {
		  slidesToShow: 1
		}
	}
	]
});


// BOOKING: ADJUST NAVIGATION WIDTH
var widthLi = $(".booking-nav .nav li").outerWidth();
var sizeLi = $(".booking-nav .nav li").length;
var totalWidthLi = widthLi * sizeLi + 100;
$(".booking-nav .nav ul").css({"width" : totalWidthLi });


// // MODALS: TRIGGER SUGGESTION LIST AT SEARCH BUTTON
// $( ".search input" ).focus(function() {
// 	$('.suggestion-list').addClass('show');
// }).blur(function() {
// 	$('.suggestion-list').removeClass('show');
// });

// POP CALENDAR
$( ".datepicker" ).datepicker({
	dateFormat: 'd MM yy'
});


// INDEX UPLOAD PHOTO: POP ADD URL BOX
$(".upload-photo").click(function(){
	$(".create-post.upload-file").addClass("show");
	$(".create-post.add-url.video-url").removeClass("show");
	$('.create-post.url-added').removeClass('show');
	$(this).siblings().css({'opacity' : '0.2'});
	$(this).css({'opacity' : '1'});
});

$(".upload-video").click(function(){
	$(".create-post.add-url.video-url").addClass("show");
	$(".create-post.upload-file").removeClass("show");
	$('.create-post.url-added').removeClass('show');
	$(this).siblings().css({'opacity' : '0.2'});
	$(this).css({'opacity' : '1'});
});

// INDEX UPLOAD PHOTO: CLICK BUTTON LINK/ UPLOAD
$(".upload-file .file-button").click(function(){
	$(".create-post.add-url.photo-url").addClass("show");
	$(this).parent().removeClass("show");
});

$('.create-post.add-url').keypress(function(e) {
	var key = e.which;
	if (key === 13) {
		$('.create-post.url-added').addClass('show');
		$(this).removeClass("show");
	}
});

// CLOSE CREATE POST WINDOW MESSAGE
$(".deny-post, .allow-post").click(function(){
	$('.create-post.url-added').removeClass('show');
	$('.create-post.choose-format').addClass('hide');
	$('.create-post.alert-message').addClass('show');
});


// TAGS
$(function() {
	$('.tags_1').tagsInput({width:'auto'});
});
