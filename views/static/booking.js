let prime = null;
let totalPrice = 0
const bookingHeadline = document.getElementById("js-booking-main__headline");
const memberName = document.getElementById("js-booking-main__name");
const bookedSchedule = document.getElementById("js-booked-schedule");
const emptySchedule = document.getElementById("js-empty-schedule");
const scheduleList = document.getElementById("js-schedule-list");
const summaryPrice = document.getElementById("js-summary__price");
const contactInputs = document.querySelectorAll(".contact__input");
const contactName = document.getElementById("js-contact__name");
const contactEmail = document.getElementById("js-contact__email");
const contactPhone = document.getElementById("js-contact__phone");
const summaryBtn = document.getElementById("js-summary__btn");
const confirmPopup = document.getElementById("js-booking-confirm");
const confirmPopupSuccess = document.getElementById("js-booking-confirm__success");
const confirmPopupFailure = document.getElementById("js-booking-confirm__failure");
const confirmPopupResult = document.getElementById("js-booking-confirm__result");
const confirmPopupMsg = document.getElementById("js-booking-confirm__msg");
const confirmPopupIcon = document.getElementById("js-booking-confirm__icon");
const confirmPopupBtn = document.getElementById("js-booking-confirm__btn");
const phonePattern = /^09\d{8}$/;

// model
const getData = async (url) => {
    const response = await fetch(url);
    const promise = await response.json();
    const result = await promise;
    return result;
}

const onSubmit = async () => {
    const tappayStatus = await TPDirect.card.getTappayFieldsStatus();

    if (tappayStatus.canGetPrime === false) {
        prime = null;
    }

    await new Promise((resolve, reject) => {
        TPDirect.card.getPrime((result) => {
            if (result.status !== 0) {
                prime = null;
                resolve();
            }
    
            else {
                prime = result.card.prime;
                resolve();
            }
        });
    });
}

// View
const loadSchedule = (scheduleId, img, name, date, time, price, address) => {
    const schedule = document.createElement("article");
    const scheduleImg = document.createElement("img");
    const scheduleWrapper = document.createElement("div");
    const scheduleTitle = document.createElement("h1");
    const scheduleBtn = document.createElement("button");
    const scheduleBtnIcon = document.createElement("img");

    scheduleList.appendChild(schedule);
    schedule.appendChild(scheduleImg);
    schedule.appendChild(scheduleWrapper);
    scheduleWrapper.appendChild(scheduleTitle);

    for (let i = 0; i < 4; i++) {
        const scheduleTxtWrapper = document.createElement("div");
        const scheduleSubTitle = document.createElement("h1");
        const scheduleDesc = document.createElement("span");
        scheduleWrapper.append(scheduleTxtWrapper);
        scheduleTxtWrapper.appendChild(scheduleSubTitle);
        scheduleTxtWrapper.appendChild(scheduleDesc);

        scheduleTxtWrapper.classList.add("schedule__txt-wrapper", "va");
        scheduleSubTitle.setAttribute("class", "schedule__sub-title");
        scheduleDesc.setAttribute("class", "schedule__desc");
    }

    scheduleWrapper.appendChild(scheduleBtn);
    scheduleBtn.appendChild(scheduleBtnIcon);
    scheduleBtn.addEventListener("click", async () => {
        const data = {
            "scheduleId": scheduleId
        }
        const option = {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        const result = await fetch("/api/booking", option)

        if (result.ok) {
            if (scheduleList.childNodes.length == 1) {
                window.location.reload();
            }

            else {
                schedule.remove();
                summaryPrice.textContent = totalPrice -= price;
                showSchedules();
            }
        }
    });

    schedule.setAttribute("class", "schedule");
    scheduleImg.setAttribute("class", "schedule__img");
    scheduleImg.setAttribute("src", img);
    scheduleWrapper.setAttribute("class", "schedule__wrapper");
    scheduleTitle.setAttribute("class", "schedule__title");
    scheduleTitle.textContent = "台北一日遊：" + name;
    scheduleBtn.setAttribute("class", "schedule__btn");
    scheduleBtnIcon.setAttribute("src", "../static/img/icon_delete.png");
    scheduleWrapper.children[1].children[0].textContent = "日期：";
    scheduleWrapper.children[1].children[1].textContent = date;
    scheduleWrapper.children[2].children[0].textContent = "時間：";

    if (time == "morning") {
        scheduleWrapper.children[2].children[1].textContent = "早上 9 點到下午 4 點";
    }

    else {
        scheduleWrapper.children[2].children[1].textContent = "下午 1 點到晚上 8 點";
    }
    
    scheduleWrapper.children[3].children[0].textContent = "費用：";
    scheduleWrapper.children[3].children[1].textContent = "新台幣 " + price + " 元";
    scheduleWrapper.children[4].children[0].textContent = "地點：";
    scheduleWrapper.children[4].children[1].textContent = address;
}

const validateInputs = () => {
    const name = contactName.value.trim();
    const email = contactEmail.value.trim();
    const phone = contactPhone.value.trim();

    if (name) {
        removeError(contactName);
        removeErrorIcon(contactName);
    }

    else {
        setError(contactName);
        setErrorIcon(contactName);
    }

    if (emailPattern.test(email)) {
        removeError(contactEmail);
        removeErrorIcon(contactEmail);
    }

    else {
        setError(contactEmail);
        setErrorIcon(contactEmail);
    }

    if (phonePattern.test(phone)) {
        removeError(contactPhone);
        removeErrorIcon(contactPhone);
    }

    else {
        setError(contactPhone);
        setErrorIcon(contactPhone);
    }

    if (name && emailPattern.test(email) && phonePattern.test(phone)) {
        return true;
    }

    else {
        return false;
    }
}

// Controller
const init = async () => {
    const signInResponse = await fetch("/api/user");
    const signInPromise = await signInResponse.json();
    const signInResult = await signInPromise;

    if (signInResult.data) {
        const signInName = signInResult.data.name;
        
        showBlock(signOutBtn);
        hideBlock(gateBtn);
        bookingHeadline.style.opacity = "1";
        bookingHeadline.style.transform = "translateY(0)";
        memberName.textContent = signInName;

        const result = await getData("/api/booking");
        const scheduleList = result.data;
        
        if (scheduleList) {
            bookedSchedule.style.opacity = "1";
            bookedSchedule.style.transform = "translateY(0)";
            emptySchedule.style.opacity = "0";
            emptySchedule.style.transform = "translateY(-5px)";
            
            for (i = 0; i < scheduleList.length; i++) {
                const scheduleId = scheduleList[i].scheduleId;
                const img = scheduleList[i].attraction.image;
                const name = scheduleList[i].attraction.name;
                const address = scheduleList[i].attraction.address;
                const date = scheduleList[i].date;
                const time = scheduleList[i].time;
                const price = scheduleList[i].price;
                totalPrice += price
    
                loadSchedule(scheduleId, img, name, date, time, price, address);
            }
    
            summaryPrice.textContent = totalPrice;
        }
    
        else {
            bookedSchedule.style.opacity = "0";
            bookedSchedule.style.transform = "translateY(-20px)";
            emptySchedule.style.opacity = "1";
            emptySchedule.style.transform = "translateY(0)";
        }
    }

    else{
        window.location.href = "/";
    }
}

//
init();

contactInputs.forEach((input) => {
    input.addEventListener("focus", () => {
        removeError(input);
        removeErrorIcon(input);
    });
});

contactName.addEventListener("blur", () => {
    const value = contactName.value.trim();
    
    if (value) {
        removeError(contactName);
        removeErrorIcon(contactName);
    }

    else {
        setError(contactName);
        setErrorIcon(contactName);
    }
});

contactEmail.addEventListener("blur", () => {
    const value = contactEmail.value.trim();

    if (emailPattern.test(value)) {
        removeError(contactEmail);
        removeErrorIcon(contactEmail);
    }

    else {
        setError(contactEmail);
        setErrorIcon(contactEmail);
    }
});

contactPhone.addEventListener("blur", () => {
    const value = contactPhone.value.trim();

    if (value && value.startsWith("09") && value.length == 10) {
        removeError(contactPhone);
        removeErrorIcon(contactPhone);
    }

    else {
        setError(contactPhone);
        setErrorIcon(contactPhone);
    }
});

summaryBtn.addEventListener("click", async () => {
    await onSubmit();
    confirmPopupResult.textContent = "處理付款流程中";
    confirmPopupMsg.textContent = "請稍後片刻";
    
    if (validateInputs() && prime) {
        confirmPopup.style.transform = "scale(1)";
        showBlock(confirmPopupSuccess);
        showBlock(confirmPopupIcon);
        hideBlock(confirmPopupFailure);
        hideBlock(confirmPopupBtn);

        const scheduleResult = await getData("/api/booking");
        const scheduleList = scheduleResult.data;
        const trip = [];
        const name = contactName.value.trim();
        const email = contactEmail.value.trim();
        const phone = contactPhone.value.trim();
        const price = parseInt(summaryPrice.textContent);
        
        for (i = 0; i < scheduleList.length; i++) {
            const scheduleId = scheduleList[i].scheduleId;
            const attraction = scheduleList[i].attraction;
            const date = scheduleList[i].date;
            const time = scheduleList[i].time;
            const schedule = {
                "scheduleId": scheduleId,
                "attraction": attraction,
                "date": date,
                "time": time
            }

            trip.push(schedule);
        }

        const data = {
            "prime": prime,
            "order": {
                "price": price,
                "trip": trip,
                "contact": {
                    "name": name,
                    "email": email,
                    "phone": phone
                }
            }
        };
        const option = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        };

        const response = await fetch("/api/orders", option);
        const promise = await response.json();
        const result = await promise;
        const status = result.data.payment.status;
        const orderNumber = result.data.number;
        
        if (status == 0) {
            window.location.href = "/thankyou?number=" + orderNumber;
        }

        else {
            confirmPopupResult.textContent = "付款失敗";
            confirmPopupMsg.textContent = "請嘗試重新提交訂單";
            showBlock(confirmPopupBtn);
            hideBlock(confirmPopupIcon);
        }
    }

    else {
        confirmPopup.style.transform = "scale(1)";
        showBlock(confirmPopupFailure);
        showBlock(confirmPopupBtn);
        hideBlock(confirmPopupSuccess);
        hideBlock(confirmPopupIcon);
    }
});

confirmPopupBtn.addEventListener("click", () => {
    confirmPopup.style.transform = "scale(0)";
});

// Tappay
const fields = {
    number: {
        element: document.getElementById("card-number"),
        placeholder: "**** **** **** ****"
    },
    expirationDate: {
        element: document.getElementById("card-expiration-date"),
        placeholder: "MM / YY"
    },
    ccv: {
        element: document.getElementById("card-ccv"),
        placeholder: "CCV"
    }
};

TPDirect.card.setup({
    fields: fields,
    styles: {
        "input": {
            "color": "black"
        },
        "input.ccv": {
        },
        "input.expiration-date": {
        },
        "input.card-number": {
        },
        ":focus": {
        },
        ".valid": {
            "color": "#00CD28"
        },
        ".invalid": {
            "color": "#FF1B1B"
        }
    }
})

TPDirect.card.onUpdate(function (update) {
    // update.canGetPrime === true
    // --> you can call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        // submitButton.removeAttribute("disabled")
    } else {
        // Disable submit Button to get prime.
        // submitButton.setAttribute("disabled", true)
    }

    // cardTypes = ["mastercard", "visa", "jcb", "amex", "unionpay","unknown"]
    if (update.cardType === "visa") {
        // Handle card type visa.
    }

    // number 欄位是錯誤的
    if (update.status.number === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.number === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }

    if (update.status.expiry === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.expiry === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }

    if (update.status.ccv === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.ccv === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }
})
