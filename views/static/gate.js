const gateBtn = document.getElementById("navbar__gate-btn");
const signOutBtn = document.getElementById("navbar__sign-out-btn");
const popup = document.getElementById("js-popup");
const gate = document.getElementById("js-gate");
const gateTitle = document.getElementById("js-gate__title");
const gateCloseBtn = document.getElementById("js-gate__close");
const signIn = document.getElementById("js-sign-in");
const signUp = document.getElementById("js-sign-up");
const signInBtn = document.getElementById("js-sign-in__btn");
const signUpBtn = document.getElementById("js-sign-up__btn");
const signInSwitchBtn = document.getElementById("js-sign-in__switch-btn");
const signUpSwitchBtn = document.getElementById("js-sign-up__switch-btn");
const signInEmail = document.getElementById("js-sign-in__email");
const signInEmailMsg = document.getElementById("js-sign-in__email-message");
const signInPwd = document.getElementById("js-sign-in__pwd");
const signInPwdMsg = document.getElementById("js-sign-in__pwd-message");
const signInMsg = document.getElementById("js-sign-in__message");
const signUpName = document.getElementById("js-sign-up__name");
const signUpNameMsg = document.getElementById("js-sign-up__name-message");
const signUpEmail = document.getElementById("js-sign-up__email");
const signUpEmailMsg = document.getElementById("js-sign-up__email-message");
const signUpPwd = document.getElementById("js-sign-up__pwd");
const signUpPwdMsg = document.getElementById("js-sign-up__pwd-message");
const signUpMsg = document.getElementById("js-sign-up__message");

// View
const validateSignUp = () => {
    const name = signUpName.value.trim();
    const email = signUpEmail.value.trim();
    const pwd = signUpPwd.value.trim();
    const pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

    if (name != true) {
        validateInput(signUpName, signUpNameMsg, "請輸入姓名");
    }

    else {
        removeMsg(signUpNameMsg);
        removeError(signUpName);
    }

    if (email) {
        if (pattern.test(email)) {
            removeError(signUpEmail);
            removeMsg(signUpEmailMsg);
        }

        else {
            setError(signUpEmail);
            setMsg(signUpEmailMsg, "電子信箱格式錯誤");
        }
    }

    else {
        setError(signUpEmail);
        setMsg(signUpEmailMsg, "請輸入電子信箱");
    }

    if (pwd != true) {
        validateInput(signUpPwd, signUpPwdMsg, "請輸入密碼");
    }

    else {
        removeMsg(signUpPwdMsg);
        removeError(signUpPwd);
    }

    if (name && email && pattern.test(email) && pwd) {
        return true;
    }

    else {
        return false;
    }
};

const validateSignIn = () => {
    const email = signInEmail.value.trim();
    const pwd = signInPwd.value.trim();
    const pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

    if (email) {
        if (pattern.test(email)) {
            removeError(signInEmail);
            removeMsg(signInEmailMsg);
        }
        
        else {
            setError(signUpEmail);
            setMsg(signUpEmailMsg, "電子信箱格式錯誤");
        }
    }

    else {
        setError(signInEmail);
        setMsg(signInEmailMsg, "請輸入電子信箱");
    }

    if (pwd) {
        removeError(signInPwd);
        removeMsg(signInPwdMsg);
    }

    else {
        setError(signInPwd);
        setMsg(signInPwdMsg, "請輸入密碼");
    }

    if (email && pattern.test(email) && pwd) {
        return true;
    }

    else {
        return false;
    }
}

const validateInput = (e, msg, txt) => {
    const value = e.value.trim();

    if (value) {
        removeError(e);
        removeMsg(e);
    }

    else {
        setError(e);
        setMsg(msg, txt);
    }
}

const setOk = (e) => {
    e.classList.add("ok");
}

const setError = (e) => {
    e.classList.add("error");
}

const removeOk = (e) => {
    e.classList.remove("ok");
}

const removeError = (e) => {
    e.classList.remove("error");
}

const setMsg = (e, txt) => {
    e.textContent = txt;
}

const removeMsg = (e) => {
    e.textContent = "";
}

const showBlock = (e) => {
    e.classList.remove("hidden");
}

const hideBlock = (e) => {
    e.classList.add("hidden");
}


gateBtn.addEventListener("click", () => {
    popup.style.pointerEvents = "all";
    popup.style.opacity = "1";
    popup.style.transition = "1s";
    gate.style.transform = "translateY(80px)";
    gate.style.transition = "0.3s";
    gateTitle.textContent = "登入會員帳號";
    showBlock(signIn);
    hideBlock(signUp);
    removeMsg(signUpNameMsg);
    removeError(signUpName);
    removeMsg(signUpEmailMsg);
    removeError(signUpEmail);
    removeMsg(signUpPwdMsg);
    removeError(signUpPwd);
    removeMsg(signInEmailMsg);
    removeError(signInEmail);
    removeMsg(signInPwdMsg);
    removeError(signInPwd);
});

gateCloseBtn.addEventListener("click", () => {
    popup.style.pointerEvents = "none";
    popup.style.opacity = "0";
    popup.style.transition = "none";
    gate.style.transform = "translateY(-400px)";
    gate.style.transition = "none";
});

signInSwitchBtn.addEventListener("click", () => {
    gateTitle.textContent = "註冊會員帳號";
    showBlock(signUp);
    hideBlock(signIn);
});

signUpSwitchBtn.addEventListener("click", () => {
    gateTitle.textContent = "登入會員帳號";
    showBlock(signIn);
    hideBlock(signUp);
});

signInBtn.addEventListener("click", async () => {
    const email = signInEmail.value.trim();
    const pwd = signInPwd.value.trim();
    const data = {
        "email": email,
        "password": pwd
    }
    const option = {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    };

    if (validateSignIn()) {
        const response = await fetch("/api/user", option);
        const promise = await response.json();
        const result = await promise;

        if (result.ok) {
            popup.style.pointerEvents = "none";
            popup.style.opacity = "0";
            popup.style.transition = "1s";
            gate.style.transform = "translateY(-400px)";
            gate.style.transition = "0.3s";
            hideBlock(gateBtn);
            showBlock(signOutBtn);
        }

        else if (result.error) {
            setError(signInEmail);
            setError(signInPwd);
            setMsg(signInMsg, "電子信箱或密碼錯誤，請重新輸入");
        }
    }
});

signOutBtn.addEventListener("click", async () => {
    const option = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        }
    };

    const response = await fetch("/api/user", option);
    const promise = await response.json();
    const result = await promise;

    if (result.ok) {
        window.location.reload();
        showBlock(gateBtn);
        hideBlock(signOutBtn);
    }
})

signUpBtn.addEventListener("click", async () => {
    const name = signUpName.value.trim();
    const email = signUpEmail.value.trim();
    const pwd = signUpPwd.value.trim();
    const data = {
        "name": name,
        "email": email,
        "password": pwd
    };
    const option = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    };

    if (validateSignUp()) {
        const response = await fetch("/api/user", option);
        const promise = await response.json();
        const result = await promise;

        if (result.ok) {
            removeError(signUpMsg)
            removeError(signUpEmail)
            setOk(signUpMsg)
            setMsg(signUpMsg, "註冊成功！");
        }

        else if (result.error) {
            if (result.message == "The email has already been registered.") {
                setError(signUpEmail);
                setError(signUpMsg);
                removeOk(signUpMsg);
                setMsg(signUpMsg, "此電子信箱已被其他使用者註冊");
            }

            else {
                setError(signUpMsg);
                removeOk(signUpMsg);
                setMsg(signUpMsg, "註冊失敗，請重新輸入");
            }
        }
    }
});

signUpName.addEventListener("focus", () =>{
    removeMsg(signUpNameMsg);
    removeError(signUpName);
});

signUpEmail.addEventListener("focus", () => {
    removeMsg(signUpEmailMsg);
    removeError(signUpEmail);
});

signUpPwd.addEventListener("focus", () => {
    removeMsg(signUpPwdMsg);
    removeError(signUpPwd);
});

signUpName.addEventListener("blur", () =>{
    validateInput(signUpName, signUpNameMsg, "請輸入姓名");
});

signUpEmail.addEventListener("blur", () => {
    const email = signUpEmail.value.trim();
    const pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

    if (email) {
        if (pattern.test(email)) {
            removeError(signUpEmail);
            removeMsg(signUpEmailMsg);
        }

        else {
            setError(signUpEmail);
            setMsg(signUpEmailMsg, "電子信箱格式錯誤");
        }
    }

    else {
        setError(signUpEmail);
        setMsg(signUpEmailMsg, "請輸入電子信箱");
    }
});

signUpPwd.addEventListener("blur", () => {
    validateInput(signUpPwd, signUpPwdMsg, "請輸入密碼");
});

signInEmail.addEventListener("focus", () => {
    removeMsg(signInEmailMsg);
    removeError(signInEmail);
});

signInPwd.addEventListener("focus", () => {
    removeMsg(signInPwdMsg);
    removeError(signInPwd);
});

signInEmail.addEventListener("blur", () => {
    const email = signInEmail.value.trim();
    const pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

    if (email) {
        if (pattern.test(email)) {
            removeError(signInEmail);
            removeMsg(signInEmailMsg);
        }

        else {
            setError(signInEmail);
            setMsg(signInEmailMsg, "電子信箱格式錯誤");
        }
    }

    else {
        setError(signInEmail);
        setMsg(signInEmailMsg, "請輸入電子信箱");
    }
});

signInPwd.addEventListener("blur", () => {
    validateInput(signInPwd, signInPwdMsg, "請輸入密碼");
});

