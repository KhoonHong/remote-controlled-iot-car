
/*!

=========================================================
* Argon Dashboard - v1.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard
* Copyright 2020 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard/blob/master/LICENSE.md)

* Coded by www.creative-tim.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/



//
// Layout
//

'use strict';

var Layout = (function () {

	function pinSidenav() {
		$('.sidenav-toggler').addClass('active');
		$('.sidenav-toggler').data('action', 'sidenav-unpin');
		$('body').removeClass('g-sidenav-hidden').addClass('g-sidenav-show g-sidenav-pinned');
		$('body').append('<div class="backdrop d-xl-none" data-action="sidenav-unpin" data-target=' + $('#sidenav-main').data('target') + ' />');

		// Store the sidenav state in a cookie session
		Cookies.set('sidenav-state', 'pinned');
	}

	function unpinSidenav() {
		$('.sidenav-toggler').removeClass('active');
		$('.sidenav-toggler').data('action', 'sidenav-pin');
		$('body').removeClass('g-sidenav-pinned').addClass('g-sidenav-hidden');
		$('body').find('.backdrop').remove();

		// Store the sidenav state in a cookie session
		Cookies.set('sidenav-state', 'unpinned');
	}

	// Set sidenav state from cookie

	var $sidenavState = Cookies.get('sidenav-state') ? Cookies.get('sidenav-state') : 'pinned';

	if ($(window).width() > 1200) {
		if ($sidenavState == 'pinned') {
			pinSidenav()
		}

		if (Cookies.get('sidenav-state') == 'unpinned') {
			unpinSidenav()
		}

		$(window).resize(function () {
			if ($('body').hasClass('g-sidenav-show') && !$('body').hasClass('g-sidenav-pinned')) {
				$('body').removeClass('g-sidenav-show').addClass('g-sidenav-hidden');
			}
		})
	}

	if ($(window).width() < 1200) {
		$('body').removeClass('g-sidenav-hide').addClass('g-sidenav-hidden');
		$('body').removeClass('g-sidenav-show');
		$(window).resize(function () {
			if ($('body').hasClass('g-sidenav-show') && !$('body').hasClass('g-sidenav-pinned')) {
				$('body').removeClass('g-sidenav-show').addClass('g-sidenav-hidden');
			}
		})
	}



	$("body").on("click", "[data-action]", function (e) {

		e.preventDefault();

		var $this = $(this);
		var action = $this.data('action');
		var target = $this.data('target');


		// Manage actions

		switch (action) {
			case 'sidenav-pin':
				pinSidenav();
				break;

			case 'sidenav-unpin':
				unpinSidenav();
				break;

			case 'search-show':
				target = $this.data('target');
				$('body').removeClass('g-navbar-search-show').addClass('g-navbar-search-showing');

				setTimeout(function () {
					$('body').removeClass('g-navbar-search-showing').addClass('g-navbar-search-show');
				}, 150);

				setTimeout(function () {
					$('body').addClass('g-navbar-search-shown');
				}, 300)
				break;

			case 'search-close':
				target = $this.data('target');
				$('body').removeClass('g-navbar-search-shown');

				setTimeout(function () {
					$('body').removeClass('g-navbar-search-show').addClass('g-navbar-search-hiding');
				}, 150);

				setTimeout(function () {
					$('body').removeClass('g-navbar-search-hiding').addClass('g-navbar-search-hidden');
				}, 300);

				setTimeout(function () {
					$('body').removeClass('g-navbar-search-hidden');
				}, 500);
				break;
		}
	})


	// Add sidenav modifier classes on mouse events

	$('.sidenav').on('mouseenter', function () {
		if (!$('body').hasClass('g-sidenav-pinned')) {
			$('body').removeClass('g-sidenav-hide').removeClass('g-sidenav-hidden').addClass('g-sidenav-show');
		}
	})

	$('.sidenav').on('mouseleave', function () {
		if (!$('body').hasClass('g-sidenav-pinned')) {
			$('body').removeClass('g-sidenav-show').addClass('g-sidenav-hide');

			setTimeout(function () {
				$('body').removeClass('g-sidenav-hide').addClass('g-sidenav-hidden');
			}, 300);
		}
	})


	// Make the body full screen size if it has not enough content inside
	$(window).on('load resize', function () {
		if ($('body').height() < 800) {
			$('body').css('min-height', '100vh');
			$('#footer-main').addClass('footer-auto-bottom')
		}
	})

})();

//
// Charts
//

'use strict';

var Charts = (function () {

	// Variable

	var $toggle = $('[data-toggle="chart"]');
	var mode = 'light';//(themeMode) ? themeMode : 'light';
	var fonts = {
		base: 'Open Sans'
	}

	// Colors
	var colors = {
		gray: {
			100: '#f6f9fc',
			200: '#e9ecef',
			300: '#dee2e6',
			400: '#ced4da',
			500: '#adb5bd',
			600: '#8898aa',
			700: '#525f7f',
			800: '#32325d',
			900: '#212529'
		},
		theme: {
			'default': '#172b4d',
			'primary': '#5e72e4',
			'secondary': '#f4f5f7',
			'info': '#11cdef',
			'success': '#2dce89',
			'danger': '#f5365c',
			'warning': '#fb6340'
		},
		black: '#12263F',
		white: '#FFFFFF',
		transparent: 'transparent',
	};


	// Methods

	// Chart.js global options
	function chartOptions() {

		// Options
		var options = {
			defaults: {
				global: {
					responsive: true,
					maintainAspectRatio: false,
					defaultColor: (mode == 'dark') ? colors.gray[700] : colors.gray[600],
					defaultFontColor: (mode == 'dark') ? colors.gray[700] : colors.gray[600],
					defaultFontFamily: fonts.base,
					defaultFontSize: 13,
					layout: {
						padding: 0
					},
					legend: {
						display: false,
						position: 'bottom',
						labels: {
							usePointStyle: true,
							padding: 16
						}
					},
					elements: {
						point: {
							radius: 0,
							backgroundColor: colors.theme['primary']
						},
						line: {
							tension: .4,
							borderWidth: 4,
							borderColor: colors.theme['primary'],
							backgroundColor: colors.transparent,
							borderCapStyle: 'rounded'
						},
						rectangle: {
							backgroundColor: colors.theme['warning']
						},
						arc: {
							backgroundColor: colors.theme['primary'],
							borderColor: (mode == 'dark') ? colors.gray[800] : colors.white,
							borderWidth: 4
						}
					},
					tooltips: {
						enabled: true,
						mode: 'index',
						intersect: false,
					}
				},
				doughnut: {
					cutoutPercentage: 83,
					legendCallback: function (chart) {
						var data = chart.data;
						var content = '';

						data.labels.forEach(function (label, index) {
							var bgColor = data.datasets[0].backgroundColor[index];

							content += '<span class="chart-legend-item">';
							content += '<i class="chart-legend-indicator" style="background-color: ' + bgColor + '"></i>';
							content += label;
							content += '</span>';
						});

						return content;
					}
				}
			}
		}

		// yAxes
		Chart.scaleService.updateScaleDefaults('linear', {
			gridLines: {
				borderDash: [2],
				borderDashOffset: [2],
				color: (mode == 'dark') ? colors.gray[900] : colors.gray[300],
				drawBorder: false,
				drawTicks: false,
				drawOnChartArea: true,
				zeroLineWidth: 0,
				zeroLineColor: 'rgba(0,0,0,0)',
				zeroLineBorderDash: [2],
				zeroLineBorderDashOffset: [2]
			},
			ticks: {
				beginAtZero: true,
				padding: 10,
				callback: function (value) {
					if (!(value % 10)) {
						return value
					}
				}
			}
		});

		// xAxes
		Chart.scaleService.updateScaleDefaults('category', {
			gridLines: {
				drawBorder: false,
				drawOnChartArea: false,
				drawTicks: false
			},
			ticks: {
				padding: 20
			},
			maxBarThickness: 10
		});

		return options;

	}

	// Parse global options
	function parseOptions(parent, options) {
		for (var item in options) {
			if (typeof options[item] !== 'object') {
				parent[item] = options[item];
			} else {
				parseOptions(parent[item], options[item]);
			}
		}
	}

	// Push options
	function pushOptions(parent, options) {
		for (var item in options) {
			if (Array.isArray(options[item])) {
				options[item].forEach(function (data) {
					parent[item].push(data);
				});
			} else {
				pushOptions(parent[item], options[item]);
			}
		}
	}

	// Pop options
	function popOptions(parent, options) {
		for (var item in options) {
			if (Array.isArray(options[item])) {
				options[item].forEach(function (data) {
					parent[item].pop();
				});
			} else {
				popOptions(parent[item], options[item]);
			}
		}
	}

	// Toggle options
	function toggleOptions(elem) {
		var options = elem.data('add');
		var $target = $(elem.data('target'));
		var $chart = $target.data('chart');

		if (elem.is(':checked')) {

			// Add options
			pushOptions($chart, options);

			// Update chart
			$chart.update();
		} else {

			// Remove options
			popOptions($chart, options);

			// Update chart
			$chart.update();
		}
	}

	// Update options
	function updateOptions(elem) {
		var options = elem.data('update');
		var $target = $(elem.data('target'));
		var $chart = $target.data('chart');

		// Parse options
		parseOptions($chart, options);

		// Toggle ticks
		toggleTicks(elem, $chart);

		// Update chart
		$chart.update();
	}

	// Toggle ticks
	function toggleTicks(elem, $chart) {

		if (elem.data('prefix') !== undefined || elem.data('prefix') !== undefined) {
			var prefix = elem.data('prefix') ? elem.data('prefix') : '';
			var suffix = elem.data('suffix') ? elem.data('suffix') : '';

			// Update ticks
			$chart.options.scales.yAxes[0].ticks.callback = function (value) {
				if (!(value % 10)) {
					return prefix + value + suffix;
				}
			}

			// Update tooltips
			$chart.options.tooltips.callbacks.label = function (item, data) {
				var label = data.datasets[item.datasetIndex].label || '';
				var yLabel = item.yLabel;
				var content = '';

				if (data.datasets.length > 1) {
					content += '<span class="popover-body-label mr-auto">' + label + '</span>';
				}

				content += '<span class="popover-body-value">' + prefix + yLabel + suffix + '</span>';
				return content;
			}

		}
	}


	// Events

	// Parse global options
	if (window.Chart) {
		parseOptions(Chart, chartOptions());
	}

	// Toggle options
	$toggle.on({
		'change': function () {
			var $this = $(this);

			if ($this.is('[data-add]')) {
				toggleOptions($this);
			}
		},
		'click': function () {
			var $this = $(this);

			if ($this.is('[data-update]')) {
				updateOptions($this);
			}
		}
	});


	// Return

	return {
		colors: colors,
		fonts: fonts,
		mode: mode
	};

})();

//
// Icon code copy/paste
//

'use strict';

var CopyIcon = (function () {

	// Variables

	var $element = '.btn-icon-clipboard',
		$btn = $($element);


	// Methods

	function init($this) {
		$this.tooltip().on('mouseleave', function () {
			// Explicitly hide tooltip, since after clicking it remains
			// focused (as it's a button), so tooltip would otherwise
			// remain visible until focus is moved away
			$this.tooltip('hide');
		});

		var clipboard = new ClipboardJS($element);

		clipboard.on('success', function (e) {
			$(e.trigger)
				.attr('title', 'Copied!')
				.tooltip('_fixTitle')
				.tooltip('show')
				.attr('title', 'Copy to clipboard')
				.tooltip('_fixTitle')

			e.clearSelection()
		});
	}


	// Events
	if ($btn.length) {
		init($btn);
	}

})();

//
// Navbar
//

'use strict';

var Navbar = (function () {

	// Variables

	var $nav = $('.navbar-nav, .navbar-nav .nav');
	var $collapse = $('.navbar .collapse');
	var $dropdown = $('.navbar .dropdown');

	// Methods

	function accordion($this) {
		$this.closest($nav).find($collapse).not($this).collapse('hide');
	}

	function closeDropdown($this) {
		var $dropdownMenu = $this.find('.dropdown-menu');

		$dropdownMenu.addClass('close');

		setTimeout(function () {
			$dropdownMenu.removeClass('close');
		}, 200);
	}


	// Events

	$collapse.on({
		'show.bs.collapse': function () {
			accordion($(this));
		}
	})

	$dropdown.on({
		'hide.bs.dropdown': function () {
			closeDropdown($(this));
		}
	})

})();


//
// Navbar collapse
//


var NavbarCollapse = (function () {

	// Variables

	var $nav = $('.navbar-nav'),
		$collapse = $('.navbar .navbar-custom-collapse');


	// Methods

	function hideNavbarCollapse($this) {
		$this.addClass('collapsing-out');
	}

	function hiddenNavbarCollapse($this) {
		$this.removeClass('collapsing-out');
	}


	// Events

	if ($collapse.length) {
		$collapse.on({
			'hide.bs.collapse': function () {
				hideNavbarCollapse($collapse);
			}
		})

		$collapse.on({
			'hidden.bs.collapse': function () {
				hiddenNavbarCollapse($collapse);
			}
		})
	}

	var navbar_menu_visible = 0;

	$(".sidenav-toggler").click(function () {
		if (navbar_menu_visible == 1) {
			$('body').removeClass('nav-open');
			navbar_menu_visible = 0;
			$('.bodyClick').remove();

		} else {

			var div = '<div class="bodyClick"></div>';
			$(div).appendTo('body').click(function () {
				$('body').removeClass('nav-open');
				navbar_menu_visible = 0;
				$('.bodyClick').remove();

			});

			$('body').addClass('nav-open');
			navbar_menu_visible = 1;

		}

	});

})();

//
// Popover
//

'use strict';

var Popover = (function () {

	// Variables

	var $popover = $('[data-toggle="popover"]'),
		$popoverClass = '';


	// Methods

	function init($this) {
		if ($this.data('color')) {
			$popoverClass = 'popover-' + $this.data('color');
		}

		var options = {
			trigger: 'focus',
			template: '<div class="popover ' + $popoverClass + '" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'
		};

		$this.popover(options);
	}


	// Events

	if ($popover.length) {
		$popover.each(function () {
			init($(this));
		});
	}

})();

//
// Scroll to (anchor links)
//

'use strict';

var ScrollTo = (function () {

	//
	// Variables
	//

	var $scrollTo = $('.scroll-me, [data-scroll-to], .toc-entry a');


	//
	// Methods
	//

	function scrollTo($this) {
		var $el = $this.attr('href');
		var offset = $this.data('scroll-to-offset') ? $this.data('scroll-to-offset') : 0;
		var options = {
			scrollTop: $($el).offset().top - offset
		};

		// Animate scroll to the selected section
		$('html, body').stop(true, true).animate(options, 600);

		event.preventDefault();
	}


	//
	// Events
	//

	if ($scrollTo.length) {
		$scrollTo.on('click', function (event) {
			scrollTo($(this));
		});
	}

})();

//
// Tooltip
//

'use strict';

var Tooltip = (function () {

	// Variables

	var $tooltip = $('[data-toggle="tooltip"]');


	// Methods

	function init() {
		$tooltip.tooltip();
	}


	// Events

	if ($tooltip.length) {
		init();
	}

})();

//
// Form control
//

'use strict';

var FormControl = (function () {

	// Variables

	var $input = $('.form-control');


	// Methods

	function init($this) {
		$this.on('focus blur', function (e) {
			$(this).parents('.form-group').toggleClass('focused', (e.type === 'focus'));
		}).trigger('blur');
	}


	// Events

	if ($input.length) {
		init($input);
	}

})();

//
// Bars chart
//

var BarsChart = (function () {

	// Variables
	var $chart = $('#chart-bars');
	var ordersChart;

	// Init chart
	function initChart($chart, data, labels) {
		ordersChart = new Chart($chart, {
			type: 'bar',
			data: {
				labels: labels,
				datasets: [{
					label: 'Humidity',
					data: data
				}]
			},
			options: {
				scales: {
					yAxes: [{
						ticks: {
							callback: function (value) {
								return value + ' g/kg';
							}
						}
					}],
					xAxes: [{
						type: 'time',
						time: {
							unit: 'hour', // Change the unit to 'hour'
							displayFormats: {
								hour: 'MM/DD, h A' // Will display like '10/04, 6 PM'
							}
						},
						gridLines: {
							lineWidth: 1,
							color: 'gray',
							zeroLineColor: 'gray'
						}
					}]
				},
				tooltips: {
					callbacks: {
						label: function (item, data) {
							var label = data.datasets[item.datasetIndex].label || '';
							var yLabel = item.yLabel;
							return label + ': ' + yLabel + ' g/kg';
						}
					}
				}
			}
		});
		$chart.data('chart', ordersChart);
	}


	// Update chart
	function updateChart(newData, newLabels) {
		ordersChart.data.labels = newLabels;
		ordersChart.data.datasets[0].data = newData;
		ordersChart.update();
	}


	// Initialize the chart with empty data
	if ($chart.length) {
		initChart($chart, [], []);
		console.log("Chart initialized.");

		// AJAX request to populate data
		$.ajax({
			url: "/get_sensor_data/",
			method: "GET",
			success: function (response) {
				console.log("Response received:", response);
				if (response.status === "success") {
					let newData = [];
					let newLabels = [];
					if (Array.isArray(response.data)) {
						console.log("Data is an array.");
						response.data.forEach((item) => {
							newData.push(item.humidity);
							newLabels.push(new Date(item.timestamp).toISOString());
						});
						console.log("New Data:", newData);
						console.log("New Labels:", newLabels);
						updateChart(newData, newLabels);
					} else {
						console.log("Data is not an array.");
					}
				}
			},
			error: function (error) {
				console.log("Error:", error);
			}
		});
	}


})();


'use strict';
var init;
var envDataChart;
var EnvironmentalDataChart = (function () {
	// Variables
	var $chart = $('#chart-environmental-data');

	// Methods to initialize the chart
	init = function ($chart, data, labels) {
		envDataChart = new Chart($chart, {
			type: 'line',
			options: {
				scales: {
					xAxes: [{
						type: 'time',
						time: {
							unit: 'hour', // Change the unit to 'hour'
							displayFormats: {
								hour: 'MM/DD, h A' // Will display like '10/04, 6 PM'
							}
						},
						gridLines: {
							lineWidth: 1,
							color: 'gray',
							zeroLineColor: 'gray'
						}
					}],

					yAxes: [{
						gridLines: {
							lineWidth: 1,
							color: 'gray',
							zeroLineColor: 'gray'
						},
						ticks: {
							callback: function (value) {
								return value + '°C';
							}
						}
					}]
				},
				tooltips: {
					callbacks: {
						label: function (item, data) {
							var label = data.datasets[item.datasetIndex].label || '';
							var yLabel = item.yLabel;
							return label + ': ' + yLabel + '°C';
						}
					}
				}
			},
			data: {
				labels: labels,
				datasets: [{
					label: 'Temperature',
					data: data,
				}]
			}
		});
		$chart.data('chart', envDataChart);
	};

	// Method to update the chart
	function updateChart(newData, newLabels) {
		envDataChart.data.labels = newLabels;
		envDataChart.data.datasets[0].data = newData;
		envDataChart.update();
	}

	// AJAX call to fetch data
	if ($chart.length) {
		$.ajax({
			url: "/get_sensor_data/",
			method: "GET",
			success: function (response) {
				if (response.status === "success") {
					let newData = [];
					let newLabels = [];
					if (Array.isArray(response.data)) {
						response.data.forEach((item) => {
							newData.push(item.temperature);
							newLabels.push(new Date(item.timestamp).toISOString());
						});
						if (!envDataChart) {
							init($chart, newData, newLabels);  // Initialize chart if it's not already initialized
						} else {
							updateChart(newData, newLabels);  // Update the chart if it's already initialized
						}
					} else {
						console.log("Data is not an array.");
					}
				}
				console.log("Response received:", response);
			},
			error: function (error) {
				console.log("Error:", error);
			}
		});
	}
})();



function formatDateTime(dateTimeStr) {
	const date = new Date(dateTimeStr);
	const year = date.getFullYear();
	const month = date.getMonth() + 1;
	const day = date.getDate();
	const hours = date.getHours();
	const minutes = date.getMinutes();
	return `${year}-${month}-${day} ${hours}:${minutes}`;
}

//
// Bootstrap Datepicker
//

'use strict';

var Datepicker = (function () {

	// Variables

	var $datepicker = $('.datepicker');


	// Methods

	function init($this) {
		var options = {
			disableTouchKeyboard: true,
			autoclose: false
		};

		$this.datepicker(options);
	}


	// Events

	if ($datepicker.length) {
		$datepicker.each(function () {
			init($(this));
		});
	}

})();

//
// Form control
//

'use strict';

var noUiSlider = (function () {

	// Variables

	// var $sliderContainer = $('.input-slider-container'),
	// 		$slider = $('.input-slider'),
	// 		$sliderId = $slider.attr('id'),
	// 		$sliderMinValue = $slider.data('range-value-min');
	// 		$sliderMaxValue = $slider.data('range-value-max');;


	// // Methods
	//
	// function init($this) {
	// 	$this.on('focus blur', function(e) {
	//       $this.parents('.form-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
	//   }).trigger('blur');
	// }
	//
	//
	// // Events
	//
	// if ($input.length) {
	// 	init($input);
	// }



	if ($(".input-slider-container")[0]) {
		$('.input-slider-container').each(function () {

			var slider = $(this).find('.input-slider');
			var sliderId = slider.attr('id');
			var minValue = slider.data('range-value-min');
			var maxValue = slider.data('range-value-max');

			var sliderValue = $(this).find('.range-slider-value');
			var sliderValueId = sliderValue.attr('id');
			var startValue = sliderValue.data('range-value-low');

			var c = document.getElementById(sliderId),
				d = document.getElementById(sliderValueId);

			noUiSlider.create(c, {
				start: [parseInt(startValue)],
				connect: [true, false],
				//step: 1000,
				range: {
					'min': [parseInt(minValue)],
					'max': [parseInt(maxValue)]
				}
			});

			c.noUiSlider.on('update', function (a, b) {
				d.textContent = a[b];
			});
		})
	}

	if ($("#input-slider-range")[0]) {
		var c = document.getElementById("input-slider-range"),
			d = document.getElementById("input-slider-range-value-low"),
			e = document.getElementById("input-slider-range-value-high"),
			f = [d, e];

		noUiSlider.create(c, {
			start: [parseInt(d.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
			connect: !0,
			range: {
				min: parseInt(c.getAttribute('data-range-value-min')),
				max: parseInt(c.getAttribute('data-range-value-max'))
			}
		}), c.noUiSlider.on("update", function (a, b) {
			f[b].textContent = a[b]
		})
	}

})();

//
// Scrollbar
//

'use strict';

var Scrollbar = (function () {

	// Variables

	var $scrollbar = $('.scrollbar-inner');


	// Methods

	function init() {
		$scrollbar.scrollbar().scrollLock()
	}


	// Events

	if ($scrollbar.length) {
		init();
	}

})();


const Toast = Swal.mixin({
	toast: true,
	position: 'top-end',
	showConfirmButton: false,
	timer: 3000,
	timerProgressBar: true,
	iconColor: 'white',
	customClass: {
		popup: 'colored-toast'
	},
	didOpen: (toast) => {
		toast.addEventListener('mouseenter', Swal.stopTimer)
		toast.addEventListener('mouseleave', Swal.resumeTimer)
	}
})
// Function to make the controller vibrate
function vibrateController(gamepad) {
	gamepad.vibrationActuator.playEffect('dual-rumble', {
		startDelay: 0, // Add a delay in milliseconds
		duration: 500, // Total duration in milliseconds
		weakMagnitude: 0.5, // intensity (0-1) of the small ERM 
		strongMagnitude: 1 // intesity (0-1) of the bigger ERM
	}).then(() => {
		console.log('Vibration played successfully');
	})
		.catch(err => {
			console.error('Error playing vibration:', err);
		});
}


function updateSensorData() {
	$.ajax({
		url: "/get_sensor_data/",
		method: "GET",
		success: function (response) {
			if (response.status === "success") {
				let newData = [];
				let newLabels = [];
				response.data.forEach((item) => {
					newData.push(item.temperature);
					newLabels.push(item.timestamp);
				});

				return newData, newLabels;
			}
		}
	});
}

let gamepadConnected = false;
let lastX = null;
let lastY = null;
let gamepad;
let aButtonPressed = false; // flag to keep track of A button state
let bButtonPressed = false;

function checkInputs() {
	if (!gamepadConnected) {
		console.log('Gamepad polling stopped due to disconnection.');
		return;  // Exit the function if the gamepad is not connected
	}

	let gamepads = navigator.getGamepads();

	// Check if a gamepad is present
	if (!gamepads || !gamepads[0]) {
		console.log('No gamepad connected');
		return;
	}

	let x = gamepads[0].axes[0];
	let y = gamepads[0].axes[1];

	// Check if the current x and y values are the same as the last recorded values
	if (x !== lastX || y !== lastY) {
		console.log(x, y);
		sendDataToBackend(x, y);

		// Update the last known x and y values
		lastX = x;
		lastY = y;
	}

	if (gamepadConnected) {
		requestAnimationFrame(checkInputs);
	}
}


function sendDataToBackend(x, y) {
	// Human reaction delay (in milliseconds)
	const HUMAN_REACTION_DELAY = 200; // for 200ms delay, adjust as needed

	setTimeout(() => {
		fetch("/control_car_view/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ x: x, y: y }),
		});
	}, HUMAN_REACTION_DELAY);
}

$(document).ready(function () {
	// CSRF Token needed for Django POST requests
	var csrfToken = $("[name=csrfmiddlewaretoken]").val();
	// var newData = [];
	// var newLabels = [];
	// newData, newLabels = updateSensorData();
	// // Initialize your chart
	// init($('#chart-environmental-data'), newData, newLabels);

	$(window).on("gamepadconnected", function (e) {
		const gamepad = e.originalEvent.gamepad
		Toast.fire({
			icon: 'success',
			text: "Gamepad connected: " + e.originalEvent.gamepad.id
		});
		gamepadConnected = true;
		checkInputs();
		vibrateController(gamepad);
	});

	$(window).on("gamepaddisconnected", function (e) {
		Toast.fire({
			icon: 'error',
			text: "Gamepad disconnected: " + e.originalEvent.gamepad.id
		});
		gamepadConnected = false;
	});

	function updateGamepad() {
		let gamepad = navigator.getGamepads()[0];

		// Check if the "A" button is pressed (button index 0)
		if (gamepad.buttons[0].pressed && !aButtonPressed) {
			aButtonPressed = true;
			// Trigger LED on
			triggerAction('on', 'light_led');
		} else if (!gamepad.buttons[0].pressed && aButtonPressed) {
			aButtonPressed = false;
			// Trigger LED off
			triggerAction('off', 'light_led');
		}

		// Check if the "B" button is pressed (button index 1)
		if (gamepad.buttons[1].pressed && !bButtonPressed) {
			bButtonPressed = true;
			// Trigger Buzzer on
			triggerAction('on', 'activate_buzzer');
		} else if (!gamepad.buttons[1].pressed && bButtonPressed) {
			bButtonPressed = false;
			// Trigger Buzzer off
			triggerAction('off', 'activate_buzzer');
		}
	}

	function triggerAction(status, endpoint) {
		$.ajax({
			url: `/${endpoint}/`,
			method: 'POST',
			headers: { "X-CSRFToken": csrfToken },
			data: { 'status': status },
			success: function (data) {
				console.log(data.status);
			}
		});
	}

	// Update the gamepad state at a regular interval
	setInterval(function () {
		if (gamepadConnected) {
			updateGamepad();
		}
	}, 100);

	async function checkMotionDetected() {
		try {
			const response = await fetch('/check_motion_detected/');
			const data = await response.json();

			if (data.motion_detected) {
				// Code to vibrate the Xbox controller
				const gamepads = navigator.getGamepads();
				if (gamepads[0]) {
					// gamepads[0].vibrationActuator.playEffect("dual-rumble", {
					// 	duration: 1000,
					// 	strongMagnitude: 1.0,
					// 	weakMagnitude: 1.0
					// });
				}
			}
		} catch (error) {
			console.error('Error:', error);
		} finally {
			// Restart long polling
			checkMotionDetected();
		}
	}

	// Start the long polling
	checkMotionDetected();


	$("#startBtn").click(function () {
		$.ajax({
			url: '/start_recording/',
			method: 'GET',
			success: function (data) {
				console.log(data.status);
				Toast.fire({
					icon: 'success',
					title: "Recording Started"
				});
			}
		});
	});

	$("#stopBtn").click(function () {
		$.ajax({
			url: '/stop_recording/',
			method: 'GET',
			success: function (data) {
				Toast.fire({
					icon: 'success',
					title: "Recording Stopped"
				});
			}
		});
	});

	$("#snapBtn").click(function () {
		$.ajax({
			url: '/take_screenshot/',
			method: 'GET',
			success: function (data) {
				Toast.fire({
					icon: 'success',
					title: "Snapshot taken"
				});
			}
		});
	});
});

