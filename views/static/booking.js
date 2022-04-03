const memberName = document.getElementById("js-booking-main__name");
const bookedSchedule = document.getElementById("js-booked-schedule");
const emptySchedule = document.getElementById("js-empty-schedule");
const scheduleList = document.getElementById("js-schedule-list");
const summaryPrice = document.getElementById("js-summary__price");
const contactInputs = document.querySelectorAll(".contact__input");
const paymentInputs = document.querySelectorAll(".payment__input");
const contactName = document.getElementById("js-contact__name");
const contactEmail = document.getElementById("js-contact__email");
const contactPhone = document.getElementById("js-contact__phone");
const paymentNumber = document.getElementById("js-payment__number");
const paymentExpiration = document.getElementById("js-payment__expiration");
const paymentVerification = document.getElementById("js-payment__verification");

// model
const getData = async (url) => {
    const response = await fetch(url);
    const promise = await response.json();
    const result = await promise;
    return result;
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
            window.location.reload();
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


// Controller
const init = async () => {
    const signInOption = {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    };
    const signInResponse = await fetch("/api/user", signInOption);
    const signInPromise = await signInResponse.json();
    const signInResult = await signInPromise;

    if (signInResult.data) {
        const signInName = signInResult.data.name;
        showBlock(signOutBtn);
        hideBlock(gateBtn);
        memberName.textContent = signInName;
    }

    else{
        window.location.href = "/";
    }

    const result = await getData("/api/booking");
    const scheduleList = result.data;
    
    if (scheduleList) {
        showBlock(bookedSchedule);
        hideBlock(emptySchedule);
        let totalPrice = 0

        for (let i = 0; i < scheduleList.length; i++) {
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
        showBlock(emptySchedule);
        hideBlock(bookedSchedule);
    }
}

init();

contactInputs.forEach((input) => {
    input.addEventListener("focus", () => {
        removeError(input);
        removeErrorIcon(input);
    });
});

paymentInputs.forEach((input) => {
    input.addEventListener("focus", () => {
        removeError(input);
        removeErrorIcon(input);
    });
});

contactName.addEventListener("blur", () => {
    if (contactName.value) {
        removeError(contactName);
        removeErrorIcon(contactName);
    }

    else {
        setError(contactName);
        setErrorIcon(contactName);
    }
});

contactEmail.addEventListener("blur", () => {
    if (contactEmail.value) {
        removeError(contactEmail);
        removeErrorIcon(contactEmail);
    }

    else {
        setError(contactEmail);
        setErrorIcon(contactEmail);
    }
});

contactPhone.addEventListener("blur", () => {
    if (contactPhone.value) {
        removeError(contactPhone);
        removeErrorIcon(contactPhone);
    }

    else {
        setError(contactPhone);
        setErrorIcon(contactPhone);
    }
});

paymentNumber.addEventListener("blur", () => {
    if (paymentNumber.value) {
        removeError(paymentNumber);
        removeErrorIcon(paymentNumber);
    }

    else {
        setError(paymentNumber);
        setErrorIcon(paymentNumber);
    }
});

paymentExpiration.addEventListener("blur", () => {
    if (paymentExpiration.value) {
        removeError(paymentExpiration);
        removeErrorIcon(paymentExpiration);
    }

    else {
        setError(paymentExpiration);
        setErrorIcon(paymentExpiration);
    }
});

paymentVerification.addEventListener("blur", () => {
    if (paymentVerification.value) {
        removeError(paymentVerification);
        removeErrorIcon(paymentVerification);
    }

    else {
        setError(paymentVerification);
        setErrorIcon(paymentVerification);
    }
});