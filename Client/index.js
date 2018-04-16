var working = false;
$('.login').on('submit', function(e) {
  e.preventDefault();
  if (working) return;
  working = true;
  var $this = $(this),
    $state = $this.find('button > .state');
  $this.addClass('loading');
  $state.html('Authenticating');
  setTimeout(function() {
    $this.addClass('ok');
    $state.html('Welcome!');
    setTimeout(function() {
      $state.html('Log in');
      $this.removeClass('ok loading');
window.location.replace('./main_chart.html');
      working = false;
    }, 500);
  }, 500);

});
