function shareOnFacebook(obj){
  var title = $(obj).data('title');
  window.open("https://www.facebook.com/sharer/sharer.php?u="+escape(window.location.href)+"&t="+title, '',
  'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=300,width=600');
}

function shareOnTwitter(obj){
  var title = $(obj).data('title');
  window.open("https://twitter.com/share?url="+escape(window.location.href)+"&text="+title, '',
  'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=300,width=600');
}

$(document).ready(function(){
  $(this).find('.social-btn-tw').click(function(){
    shareOnTwitter(this);
  });
  $(this).find('.social-btn-fb').click(function(){
    shareOnFacebook(this);
  });
});
