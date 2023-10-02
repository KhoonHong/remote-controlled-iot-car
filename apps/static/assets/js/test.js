




$(document).ready(function () {
	$("#startBtn").click(function(){
		$.ajax({
			url: '/start_recording/',
			method: 'GET',
			success: function(data) {
				console.log(data.status);
				Toast.fire({
					icon: 'success',
					title: "Recording Started: " + data.status
				});
			}
		});
	});

	$("#stopBtn").click(function(){
		$.ajax({
			url: '/stop_recording/',
			method: 'GET',
			success: function(data) {
				Toast.fire({
					icon: 'success',
					title: "Recording Stopped: " + data.status
				});
			}
		});
	});
});


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