
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



let gamepadConnected = false;

let lastX = null;
let lastY = null;

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

	$(window).on("gamepadconnected", function (e) {
		const gamepad = e.originalEvent.gamepad
		Toast.fire({
			icon: 'success',
			title: "Gamepad connected: " + e.originalEvent.gamepad.id
		});
		gamepadConnected = true;
		checkInputs(); 
		vibrateController(gamepad);
	});

	$(window).on("gamepaddisconnected", function (e) {
		Toast.fire({
			icon: 'error',
			title: "Gamepad disconnected: " + e.originalEvent.gamepad.id
		});
		gamepadConnected = false;
	});


	$("#startBtn").click(function(){
		$.ajax({
			url: '/start_recording/',
			method: 'GET',
			success: function(data) {
				console.log(data.status);
				Toast.fire({
					icon: 'success',
					title: "Recording Started"
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
					title: "Recording Stopped"
				});
			}
		});
	});

	$("#snapBtn").click(function(){
		$.ajax({
			url: '/take_screenshot/',
			method: 'GET',
			success: function(data) {
				Toast.fire({
					icon: 'success',
					title: "Snapshot taken: " + data.status
				});
			}
		});
	});
});
