document.addEventListener('DOMContentLoaded', function() {
    const webcamElement = document.getElementById('webcam');
    const canvasElement = document.getElementById('snapshot_image');
    const snapshotButton = document.getElementById('snapshot');
    const submitButton = document.getElementById('submit');
    const constraints = { video: true }; // Start with the most basic constraint
    let snapshotTaken = false;

    // Access the webcam with specific constraints
    if (navigator.mediaDevices.getUserMedia) {
        const constraints = {
            video: {
                width: { ideal: 1280 },  // Define ideal width
                height: { ideal: 720 },  // Define ideal height
                aspectRatio: { ideal: 16 / 9 }  // Define ideal aspect ratio
            }
        };

        navigator.mediaDevices.getUserMedia(constraints)
            .then(function(stream) {
                webcamElement.srcObject = stream;
                webcamElement.play().catch(function(error) {
                    console.log("Error auto-playing the video: ", error);
                });
            })
            .catch(function(error) {
                console.log("Something went wrong accessing the webcam: ", error);
            });
    }

    // Resize canvas to match webcam video size
    webcamElement.addEventListener('loadedmetadata', function() {
        canvasElement.width = webcamElement.videoWidth;
        canvasElement.height = webcamElement.videoHeight;
    });

    // Take a snapshot
    snapshotButton.addEventListener('click', function() {
        console.log('Snapshot button clicked');
        const context = canvasElement.getContext('2d');
        context.drawImage(webcamElement, 0, 0, webcamElement.videoWidth, webcamElement.videoHeight);
        canvasElement.style.display = 'block';
        snapshotTaken = true;
        submitButton.disabled = false; // Enable the submit button
    });

    // Submit form button event listener
    document.getElementById('myform').addEventListener('submit', function(e) {
        e.preventDefault();

        // Extract form data
        var canvas = document.getElementById('snapshot_image');
        var nid = document.querySelector('input[name="NID"]').value;

        // Check if NID is filled and a snapshot is taken
        if (!nid) {
            alert('Please enter your NID.');
            return;
        }
        if (!snapshotTaken) {
            alert('Please take a snapshot before submitting.');
            return;
        }

        // Sending the screenshot in binary
        canvas.toBlob(function(blob) {
            var formData = new FormData();
            var filename = nid + ".png";

            // Embed the post request with our variables
            formData.append('NID', nid);
            formData.append('SnapShot', blob, filename);

            // Do the submission in "multipart/form-data"
            fetch('/Submit-RollCall', {
                method: 'POST',
                body: formData  // Send the formData with the image blob and NID
            })
            .then(response => response.text())
            .then(data => {
                console.log('Success:', data);
                
                // Force redirect
                window.location.href = `/Success?NID=${encodeURIComponent(nid)}`;
            });
        }, 'image/png');
    });
});
