// ===============================
// LOGIN
// ===============================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function(event) {

        event.preventDefault();

        window.location.href = "dashboard.html";

    });

}


// ===============================
// LOGOUT
// ===============================

function logout() {

    window.location.href = "index.html";

}


// ===============================
// OPEN PROJECTS
// ===============================

function openProjects() {

    window.location.href = "projects.html";

}


// ===============================
// CREATE PROJECT
// ===============================

const projectForm = document.getElementById("projectForm");

if (projectForm) {

    projectForm.addEventListener("submit", async function(event) {

        event.preventDefault();


        const projectName =
            document.getElementById("projectName").value;

        const repository =
            document.getElementById("repository").value;

        const branch =
            document.getElementById("branch").value;

        const appType =
            document.getElementById("appType").value;


        try {

            const response = await fetch(
                "http://127.0.0.1:5001/api/projects",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        name: projectName,

                        repository: repository,

                        branch: branch,

                        app_type: appType

                    })
                }
            );


            const data = await response.json();


            if (response.ok) {

                alert("Project saved successfully!");

                projectForm.reset();

                loadProjects();

            } else {

                alert(
                    "Error: " +
                    (data.error || "Could not create project")
                );

            }

        } catch (error) {

            console.error(error);

            alert(
                "Cannot connect to Flask backend.\n" +
                "Make sure Flask is running on port 5001."
            );

        }

    });

}


// ===============================
// LOAD PROJECTS
// ===============================

async function loadProjects() {

    const table =
        document.getElementById("projectTable");

    if (!table) {

        return;

    }


    try {

        const response = await fetch(
            "http://127.0.0.1:5001/api/projects"
        );


        const projects =
            await response.json();


        table.innerHTML = "";


        projects.forEach(function(project) {

            const row =
                document.createElement("tr");


            row.innerHTML = `

                <td>
                    ${project.name}
                </td>

                <td>
                    ${project.repository}
                </td>

                <td>
                    ${project.branch}
                </td>

                <td>
                    ${project.app_type}
                </td>

                <td>

                    <span class="status success">
                        READY
                    </span>

                </td>

            `;


            table.appendChild(row);

        });


    } catch (error) {

        console.error(
            "Could not load projects:",
            error
        );

    }

}


// ===============================
// LOAD PROJECTS WHEN PAGE OPENS
// ===============================

if (
    document.getElementById("projectTable")
) {

    loadProjects();

}