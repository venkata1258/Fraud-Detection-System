document.addEventListener("DOMContentLoaded", function () {
    
    // Fraud Report Submission
    let fraudReportForm = document.getElementById("fraudReportForm");
    if (fraudReportForm) {
        fraudReportForm.addEventListener("submit", function (event) {
            event.preventDefault();

            let fraudType = document.getElementById("fraudType").value;
            let details = document.getElementById("details").value.trim();

            if (!details) {
                alert("Please enter fraud details.");
                return;
            }

            let alertBox = document.createElement("div");
            alertBox.classList.add("alert-item");
            alertBox.innerHTML = `<strong>${fraudType.toUpperCase()}:</strong> ${details}`;
            document.getElementById("fraudAlerts").prepend(alertBox);
            fraudReportForm.reset();
        });
    }

    // Signup Function
    let signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            event.preventDefault();

            let name = document.getElementById("name").value;
            let email = document.getElementById("email").value;
            let password = document.getElementById("password").value;

            let users = JSON.parse(localStorage.getItem("users")) || [];

            if (users.some(user => user.email === email)) {
                alert("Email is already registered!");
                return;
            }

            users.push({ name, email, password });
            localStorage.setItem("users", JSON.stringify(users));

            alert("Signup successful! Please login.");
            window.location.href = "login.html";
        });
    }

    // Login Function
    let loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();

            let email = document.getElementById("loginEmail").value;
            let password = document.getElementById("loginPassword").value;

            let users = JSON.parse(localStorage.getItem("users")) || [];
            let validUser = users.find(user => user.email === email && user.password === password);

            if (validUser) {
                localStorage.setItem("loggedInUser", JSON.stringify(validUser));
                alert("Login successful!");
                window.location.href = "index.html";
            } else {
                alert("Invalid email or password!");
            }
        });
    }

    // Logout Function
    let logoutButton = document.getElementById("logoutButton");
    if (logoutButton) {
        logoutButton.addEventListener("click", function () {
            localStorage.removeItem("loggedInUser");
            alert("Logged out!");
            window.location.href = "login.html";
        });
    }

    // Load Fraud Reports
    let fraudReportsTable = document.getElementById("fraudReports");
    if (fraudReportsTable) {
        fetch("/fraud-reports")
            .then(response => response.json())
            .then(data => {
                fraudReportsTable.innerHTML = data.map(report => `
                    <tr>
                        <td>${report.id}</td>
                        <td>${report.fraudType}</td>
                        <td>${report.description}</td>
                        <td>${report.evidence}</td>
                        <td>${report.status}</td>
                    </tr>
                `).join('');
            });
    }

    // Fetch Call/SMS/Email Logs
    let logsTable = document.getElementById("logs");
    if (logsTable) {
        fetch("/logs")
            .then(response => response.json())
            .then(data => {
                logsTable.innerHTML = data.map(log => `
                    <tr>
                        <td>${log.number}</td>
                        <td>${log.type}</td>
                        <td>${log.content}</td>
                        <td>${log.time}</td>
                    </tr>
                `).join('');
            });
    }

    // Fetch and Track Scammer Location
    let mapElement = document.getElementById("map");
    if (mapElement) {
        fetch("/location")
            .then(response => response.json())
            .then(data => {
                let map = new google.maps.Map(mapElement, {
                    zoom: 10,
                    center: { lat: data.lat, lng: data.lng }
                });
                new google.maps.Marker({
                    position: { lat: data.lat, lng: data.lng },
                    map: map,
                    title: "Scammer's Last Location"
                });
            });
    }
});
