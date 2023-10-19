const usernameField=document.querySelector('#usernameField');
const usernameSuccessOutput=document.querySelector('.usernameSuccessOutput');
const feedbackArea=document.querySelector('.invalid_feedback');
const emailField=document.querySelector('#emailField');
const emailFeedbackArea=document.querySelector('.emailFeedbackArea');
const emaiSuccessOutput=document.querySelector('.emaiSuccessOutput');
const passwordField=document.querySelector('#passwordField');
const showPasswordToggle=document.querySelector('.showPasswordToggle');
const SubmitBtn=document.querySelector('.submit-btn');
const handleToggleInput=(e)=>{
    if (showPasswordToggle.textContent === "SHOW"){
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type","text");
    }else{
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type","password");
    }
};

usernameField.addEventListener("keyup", (e) => {
    console.log("7777", 7777);
    const usernameVal=e.target.value;
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;
    usernameSuccessOutput.style.display = "block";
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = "none";
    
    if (usernameVal.length > 0){
        fetch("/authentication/validate-username",{
            body: JSON.stringify( { username: usernameVal }),
            method: "POST",
        }).then(res=>res.json()).then(data=>{
            usernameSuccessOutput.style.display="none";
            if(data.username_error){
                usernameField.classList.add("is-invalid");
                feedbackArea.style.display = "block";
                feedbackArea.innerHTML = `<p>${data.username_error}</p>`
                SubmitBtn.disabled = true;
            }else{
                SubmitBtn.removeAttribute('disabled')
            }
        });
    }
    
});

emailField.addEventListener("keyup", (e) => {
    console.log("7777", 7777);
    const emailVal=e.target.value;
    emaiSuccessOutput.textContent = `Checking ${emailVal}`;
    emaiSuccessOutput.style.display = "block";
    emailField.classList.remove("is-invalid");
    emailFeedbackArea.style.display = "none";


    if (emailVal.length > 0){
        fetch("/authentication/validate-email",{
            body: JSON.stringify( { email: emailVal }),
            method: "POST",
        }).then(res=>res.json()).then(data=>{
            console.log('data', data);
            emaiSuccessOutput.style.display="none";
            if(data.email_error){
                SubmitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedbackArea.style.display = "block";
                emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`
            }else{
                SubmitBtn.removeAttribute('disabled')
            }
        });
    }
    
});

showPasswordToggle.addEventListener("click", handleToggleInput);


