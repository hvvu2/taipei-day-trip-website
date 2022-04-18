const searchBtn = document.getElementById("js-header__btn");
const main = document.getElementById("js-main");
const searchResult = document.getElementById("js-search-result");

// Model
const url = (page, keyword) => {
    return "/api/attractions?page=" + page.toString() + "&keyword=" + keyword;
}

const getData = async (url) => {
    const response = await fetch(url);
    const promise = await response.json();
    const result = await promise;
    return result;
}

// View
const addCard = (container) => {
    const attractionLink = document.createElement("a");
    const card = document.createElement("article");
    const cardImg = document.createElement("div");
    const cardWrapper = document.createElement("div");
    const cardName = document.createElement("h1");
    const cardDescWrapper = document.createElement("div");
    const cardMrt = document.createElement("span");
    const cardCategory = document.createElement("span");

    container.appendChild(attractionLink);
    attractionLink.appendChild(card);
    card.appendChild(cardImg);
    card.appendChild(cardWrapper);
    cardWrapper.appendChild(cardName);
    cardWrapper.appendChild(cardDescWrapper);
    cardDescWrapper.appendChild(cardMrt);
    cardDescWrapper.appendChild(cardCategory);

    attractionLink.classList.add("main__link");
    card.classList.add("card");
    cardImg.classList.add("card__img", "skeleton");
    cardWrapper.classList.add("card__wrapper");
    cardName.classList.add("card__title", "skeleton");
    cardDescWrapper.classList.add("card__desc-wrapper");
    cardMrt.classList.add("card__desc", "skeleton");
    cardCategory.classList.add("card__desc", "skeleton");
}

const setCardInfo = (data, currentPage, shownItems) => {
    for (i = 0; i < shownItems; i++) {
        const mainLink = currentPage.querySelectorAll(".main__link")[i];
        const cardImg = mainLink.querySelector(".card__img");
        const cardName = mainLink.querySelector(".card__title");
        const cardMrt = mainLink.querySelectorAll(".card__desc")[0];
        const cardCategory = mainLink.querySelectorAll(".card__desc")[1];

        const id = data[i].id.toString();
        const url = "/attraction/" + id;
        const imgUrl = data[i].images[0];
        const name = data[i].name;
        const mrt = data[i].mrt;
        const category = data[i].category;

        mainLink.setAttribute("href", url);
        cardImg.style.backgroundImage = "url(" + imgUrl +")";
        cardName.textContent = name;
        cardMrt.textContent = mrt;
        cardCategory.textContent = category;
    }
}

const removeSkeleton = (currentPage, shownItems) => {
    for (i = 0; i < shownItems; i++) {
        const mainLink = currentPage.querySelectorAll(".main__link")[i];
        const cardImg = mainLink.querySelector(".card__img");
        const cardName = mainLink.querySelector(".card__title");
        const cardMrt = mainLink.querySelectorAll(".card__desc")[0];
        const cardCategory = mainLink.querySelectorAll(".card__desc")[1];

        cardImg.classList.remove("skeleton");
        cardName.classList.remove("skeleton");
        cardMrt.classList.remove("skeleton");
        cardCategory.classList.remove("skeleton");
    }
}

const removeRemainder = (currentPage, lastItems, shownItems) => {
    if (lastItems < shownItems) {
        for (i = 0; i < shownItems - lastItems; i++) {
            currentPage.lastChild.remove();
        }
    }
}

const loadPage = (container, shownItems) => {
    const page = document.createElement("div");
    container.appendChild(page);
    page.classList.add("main__wrapper");

    for (i = 0; i < shownItems; i++) {
        addCard(page);
    };
}

const addSentinel = (container, sentinel) => {
    sentinel.classList.add("main__sentinel");
    container.appendChild(sentinel);
}

const addMessage = (container, message, classname, text) => {
    container.appendChild(message);
    message.setAttribute("class", classname);
    message.textContent = text;
}

// Controller
const infiniteScrolling = (result, page, container, target, keyword) => {
    let loaded = true;
    let nextPage = result.nextPage;
    const callback = (entries) => {
        entries.forEach(async (entry) => {
            if (entry.isIntersecting && loaded) {
                loaded = false;
                target.classList.add("hidden");

                if (nextPage) {
                    loadPage(container, 12);
                    page += 1;

                    const currentPage = container.querySelectorAll(".main__wrapper")[page];
                    const result = await getData(url(nextPage, keyword));
                    nextPage = result.nextPage;
                    const data = result.data;
                    const shownItems = data.length;

                    setCardInfo(data, currentPage, shownItems);

                    setTimeout(() => {
                        removeSkeleton(currentPage, shownItems);
                        removeRemainder(currentPage, shownItems, 12);
                        target.classList.remove("hidden");
                    }, 1500);
        
                    loaded = true;
                }

                else {
                    loaded = true;
                    target.classList.remove("hidden");
                }
            }
        });
    };
    const options = {
        root: null,
        rootMargin: "0px 0px 30px 0px",
        threshold: 1
    };
    const observer = new IntersectionObserver(callback, options);
    observer.observe(target);
}

const init = async () => {
    let page = 0;
    const signInResponse = await fetch("/api/user");
    const signInPromise = await signInResponse.json();
    const signInResult = await signInPromise;
    
    if (signInResult.data) {
        hideBlock(gateBtn);
        showBlock(memberBtn);
    }

    else{
        showBlock(gateBtn);
        hideBlock(memberBtn);
    }

    const result = await getData(url(0, ""));
    const sentinel = document.createElement("div");
    const data = result.data;
    const shownItems = data.length;
    const currentPage = main.querySelectorAll(".main__wrapper")[page];

    setCardInfo(data, currentPage, shownItems);

    setTimeout(() => {
        removeSkeleton(currentPage, shownItems);
        addSentinel(main, sentinel);
    }, 1500);

    infiniteScrolling(result, page, main, sentinel, "");
}

const search = async () => {
    let page = 0
    const keyword = document.getElementById("js-header__input").value;

    while (searchResult.lastChild) {
        searchResult.removeChild(searchResult.lastChild);
    }

    if (keyword) {
        showBlock(searchResult);
        hideBlock(main);
        loadPage(searchResult, 12);

        const result = await getData(url(0, keyword));
        const data = result.data;
        
        if (data) {
            const sentinel = document.createElement("div");
            const shownItems = data.length;
            const currentPage = searchResult.querySelectorAll(".main__wrapper")[page];

            setTimeout(() => {
                removeSkeleton(currentPage, shownItems);
                removeRemainder(currentPage, shownItems, 12);
                addSentinel(searchResult, sentinel);
            }, 2000)
            setCardInfo(data, currentPage, shownItems);
            infiniteScrolling(result, page, searchResult, sentinel, keyword);
        }

        else {
            const searchMessage = document.createElement("p");
            addMessage(searchResult, searchMessage, "main__txt", "很抱歉，我們沒有找到相關的景點");
        }
    }

    else {
        showBlock(main);
        hideBlock(searchResult);
    }
}

//
init();

searchBtn.addEventListener("click", search);