$(document).ready(function () {
	$(window).scroll(function () {
		var scrollPosition = $(this).scrollTop();

		// Anpassbare Werte für Effekt-Stärke:
		var opacity = 1 - scrollPosition * 0.002;  // 0.002 = Geschwindigkeit des Opacity-Verlusts
		var translateY = scrollPosition * 0.1;     // 0.1 = Geschwindigkeit der Bewegung

		// Grenzen setzen (optional):
		opacity = Math.max(0.1, opacity);          // Mindest-Opacity 10%
		translateY = Math.min(100, translateY);     // Maximale Verschiebung 100px

		// Effekt anwenden:
		$('.hero .scroll-parallax').css({
			'opacity': opacity,
			'transform': 'translateY(' + translateY + 'px)'
		});
	});
});