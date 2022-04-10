let data = null;
let images = null;
let lastImg = null;
let sliderDotList = null;
let currentImg = 1;
let offset = 540;
let loaded = true;
const sliderShowcase = document.getElementById("js-slider__showcase");
const sliderLastImg = document.getElementById("js-slider__last-img");
const sliderFirstImg = document.getElementById("js-slider__first-img");
const sliderContainer = document.getElementById("js-slider__container");
const sliderIndicator = document.getElementById("js-slider__indicator");
const sliderPreviousBtn = document.getElementById("js-slider__previous-btn");
const sliderNextBtn = document.getElementById("js-slider__next-btn");
const profileTitle = document.getElementById("js-profile__title");
const profileDesc = document.getElementById("js-profile__desc");
const order = document.getElementById("js-order");
const orderDate = document.getElementById("js-order__date");
const orderMorning = document.getElementById("js-order__morning");
const orderAfternoon = document.getElementById("js-order__afternoon");
const orderPrice = document.getElementById("js-order__price");
const info = document.getElementById("js-info");
const infoDesc = document.getElementById("js-info__desc");
const infoAddress = document.getElementById("js-info__address");
const infoTransport = document.getElementById("js-info__transport");
const orderBtn = document.getElementById("js-order__btn");
const confirmPopup = document.getElementById("js-attraction-confirm");
const confirmPopupSuccess = document.getElementById("js-attraction-confirm__success");
const confirmPopupFailure = document.getElementById("js-attraction-confirm__failure");
const confirmPopupBtn = document.getElementById("js-attraction-confirm__btn");

// Model
const url = () => {
    const path = location.pathname;
    return "/api" + path;
}

const getData = async (url) => {
    const response = await fetch(url);
    const promise = await response.json();
    const result = await promise;
    data = result.data;
    images = data.images;
    lastImg = data.images.length;
}

// View
const setPrice = (price) => {
    orderPrice.textContent = price;
}

const removeSkeleton = () => {
    sliderShowcase.classList.remove("skeleton");
    profileTitle.classList.remove("skeleton");
    profileDesc.classList.remove("skeleton");
    order.classList.remove("skeleton");
    infoDesc.classList.remove("skeleton");
    infoAddress.classList.remove("skeleton");
    infoTransport.classList.remove("skeleton");
    info.querySelectorAll(".info__sub-title")[0].classList.remove("skeleton");
    info.querySelectorAll(".info__sub-title")[1].classList.remove("skeleton");
}

// Controller
const validateDate = (date) => {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const currentDay = currentDate.getDate();
    const selectedYear = parseInt(date.split("-")[0]);
    const selectedMonth = parseInt(date.split("-")[1]);
    const selectedDay = parseInt(date.split("-")[2]);

    if (selectedYear >= currentYear) {
        if (selectedMonth >= currentMonth) {
            if (selectedDay >= currentDay) {
                return true;
            }

            else {
                return false;
            }
        }

        else {
            return false;
        }
    }

    else {
        return false;
    }
}

const init = async () => {
    const signInResponse = await fetch("/api/user");
    const signInPromise = await signInResponse.json();
    const signInResult = await signInPromise;
    
    if (signInResult.data) {
        showBlock(signOutBtn);
        hideBlock(gateBtn);
    }

    else{
        showBlock(gateBtn);
        hideBlock(signOutBtn);
    }

    await getData(url());
    const name = data.name;
    const category = data.category;
    const mrt = data.mrt;
    const description = data.description;
    const address = data.address;
    const transport = data.transport;

    sliderLastImg.setAttribute("src", images[lastImg - 1]);
    
    await images.forEach((image) => {
        const sliderImg = document.createElement("img");
        const sliderDot = document.createElement("div");

        sliderContainer.appendChild(sliderImg);
        sliderImg.setAttribute("class", "slider__img");
        sliderImg.setAttribute("src", image);
        sliderIndicator.appendChild(sliderDot);
        sliderDot.classList.add("slider__dot");
    });
    
    sliderFirstImg.setAttribute("src", images[0]);

    sliderDotList = sliderIndicator.childNodes;
    sliderDotList[0].classList.add("current");
    profileTitle.textContent = name;
    profileDesc.textContent = category + " at " + mrt;
    infoDesc.textContent = description;
    infoAddress.textContent = address;
    infoTransport.textContent = transport;

    setTimeout(() => {
        removeSkeleton();
    }, 1500);
}

//
init();

orderMorning.addEventListener("click", () => {
    setPrice("2000");
});

orderAfternoon.addEventListener("click", () => {
    setPrice("2500");
});

sliderNextBtn.addEventListener("click", async () => {
    sliderContainer.style.transition = "0.5s";
    sliderFirstImg.style.transition = "0.5s";


    if (loaded) {
        if (currentImg == lastImg) {
            sliderFirstImg.style.transform = "translateX(-540px)";
            sliderContainer.style.transform = "translateX(" + - currentImg * offset + "px)";
            sliderDotList[currentImg - 1].classList.remove("current");
            sliderDotList[0].classList.add("current");
            currentImg = 1;
            loaded = false;
        }

        else {
            sliderContainer.style.transform = "translateX(" + - currentImg * offset + "px)";
            sliderDotList[currentImg - 1].classList.remove("current");
            sliderDotList[currentImg].classList.add("current");
            currentImg += 1;
            loaded = false;
        }
    }
});

sliderPreviousBtn.addEventListener("click", ()  => {
    sliderContainer.style.transition = "0.5s";
    sliderLastImg.style.transition = "0.5s";

    if (loaded) {
        if (currentImg == 1) {
            sliderLastImg.style.transform = "translateX(540px)";
            sliderContainer.style.transform = "translateX(" + currentImg * offset + "px)";
            sliderDotList[currentImg - 1].classList.remove("current");
            sliderDotList[lastImg - 1].classList.add("current");
            currentImg = lastImg;
            loaded = false;
        }

        else {
            currentImg -= 1;
            sliderDotList[currentImg].classList.remove("current");
            sliderDotList[currentImg - 1].classList.add("current");
            sliderContainer.style.transform = "translateX(" + (- currentImg + 1) * offset + "px)";
            loaded = false;
        }
    }
});

sliderContainer.addEventListener("transitionend", () => {
    loaded = true;

    if (currentImg == 1) {
        sliderContainer.style.transition = "none";
        sliderContainer.style.transform = "translateX(0)";
    }

    else if (currentImg == lastImg) {
        sliderContainer.style.transition = "none";
        sliderContainer.style.transform = "translateX(" + - (currentImg - 1) * offset + "px)";
    };
});

sliderFirstImg.addEventListener("transitionend", () => {
    loaded = true;
    sliderFirstImg.style.transition = "none";
    sliderFirstImg.style.transform = "translateX(0)";
});

sliderLastImg.addEventListener("transitionend", () => {
    loaded = true;
    sliderLastImg.style.transition = "none";
    sliderLastImg.style.transform = "translateX(0)";
});

orderBtn.addEventListener("click", async () => {
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
        const attractionId = location.pathname.split("/attraction/")[1];
        const date = orderDate.value;
        const time = document.querySelector("input[name='order__time']:checked").value;
        const price = parseInt(orderPrice.textContent);
        const data = {
            "attractionId": attractionId,
            "date": date,
            "time": time,
            "price": price
        };
        const option = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        };
        
        if (attractionId && validateDate(date) && time && price) {
            await fetch("/api/booking", option);
            confirmPopup.style.transform = "scale(1)";
            showBlock(confirmPopupSuccess);
            hideBlock(confirmPopupFailure);
            showSchedules();
            confirmPopupBtn.textContent = "繼續瀏覽"
        }
    
        else {
            confirmPopup.style.transform = "scale(1)";
            showBlock(confirmPopupFailure);
            hideBlock(confirmPopupSuccess);
            confirmPopupBtn.textContent = "確認"
        }
    }

    else{
        popup.style.pointerEvents = "all";
        popup.style.opacity = "1";
        popup.style.transition = "1s";
        gate.style.transform = "translateY(80px)";
        gate.style.transition = "0.3s";
        gateTitle.textContent = "登入會員帳號";
        showBlock(signIn);
        hideBlock(signUp);
        resetGateInput();
    }
});

confirmPopupBtn.addEventListener("click", () =>{
    confirmPopup.style.transform = "scale(0)";
});