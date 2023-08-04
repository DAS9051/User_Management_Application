
function handleSubmit(event) {
    event.preventDefault(); 
 
    var userName = document.getElementById("user_name").value;
    var firstName = document.getElementById("first_name").value;
    var lastName = document.getElementById("last_name").value;
    var department = document.getElementById("department").value;
    var company = document.getElementById("company").value;
    var companyEmail = document.getElementById("company_email").value;

    domain = "http://127.0.0.1:5000/create-user";
    url = domain.concat("/", userName, "/", firstName, "/", lastName, "/", department,"/", company, "/", companyEmail)  
    console.log(url)
    fetch(url,{
        headers: {
            'Accept': 'application/json'
        }
    })
        .then(response => response.text())
        .then(text => console.log(text))
}

var form = document.querySelector("form");
form.addEventListener("submit", handleSubmit);
