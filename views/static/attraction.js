let data = null;
let images = null;
let lastImg = null;
let sliderDotList = null;
const sliderLastImg = document.getElementById("slider__last-img");
const sliderFirstImg = document.getElementById("slider__first-img");
const sliderContainer = document.getElementById("js-slider__container");
const sliderIndicator = document.getElementById("js-slider__indicator");
const sliderPreviousBtn = document.getElementById("js-slider__previous-btn");
const sliderNextBtn = document.getElementById("js-slider__next-btn");
const profileTitle = document.getElementById("js-profile__title");
const profileDesc = document.getElementById("js-profile__desc");
const orderMorning = document.getElementById("js-order__morning");
const orderAfternoon = document.getElementById("js-order__afternoon");
const orderPrice = document.getElementById("js-order__price");
const infoDesc = document.getElementById("js-info__desc");
const infoAddress = document.getElementById("js-info__address");
const infoTransport = document.getElementById("js-info__transport");

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
    orderPrice.textContent = "新台幣 " + price + " 元";
}

// Controller
const init = async () => {
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
}

//
init();

orderMorning.addEventListener("click", () => {
    setPrice("2000");
});

orderAfternoon.addEventListener("click", () => {
    setPrice("2500");
});

let currentImg = 1;
let offset = 540;
let loaded = true;

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