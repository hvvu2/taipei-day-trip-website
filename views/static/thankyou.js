const thankyouIcon = document.getElementById("js-thankyou-main__icon");
const thankyouWrapper = document.getElementById("js-thankyou-main__txt-wrapper");
const thankyouOrderNumber = document.getElementById("js-thankyou-main__order-number");

const init = async () => {
    const signInResponse = await fetch("/api/user");
    const signInPromise = await signInResponse.json();
    const signInResult = await signInPromise;

    if (signInResult.data) {
        showBlock(signOutBtn);
        hideBlock(gateBtn);
    }

    else{
        window.location.href = "/";
    }

    const orderNumber = window.location.search.split("?number=")[1];

    thankyouIcon.style.opacity = "1";
    thankyouIcon.style.transform = "translateY(0)";
    thankyouOrderNumber.textContent = orderNumber;
    thankyouWrapper.style.opacity = "1";
    thankyouWrapper.style.transform = "translateY(0)";
}

init();