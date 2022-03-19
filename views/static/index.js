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
const addCard = (container, url, imgUrl, name, mrt, category) => {
    const attractionLink = document.createElement("a");
    const cardArticle = document.createElement("article");
    const cardImg = document.createElement("img");
    const cardTxtWrapper = document.createElement("div");
    const cardTitle = document.createElement("h1");
    const cardDescWrapper = document.createElement("div");
    const cardMrt = document.createElement("span");
    const cardCategory = document.createElement("span");

    container.appendChild(attractionLink);
    attractionLink.appendChild(cardArticle);
    cardArticle.appendChild(cardImg);
    cardArticle.appendChild(cardTxtWrapper);
    cardTxtWrapper.appendChild(cardTitle);
    cardTxtWrapper.appendChild(cardDescWrapper);
    cardDescWrapper.appendChild(cardMrt);
    cardDescWrapper.appendChild(cardCategory);

    attractionLink.setAttribute("href", url);
    cardArticle.setAttribute("class", "card");
    cardImg.setAttribute("class", "card__img");
    cardImg.setAttribute("src", imgUrl);
    cardTxtWrapper.setAttribute("class", "card__txt-wrapper");
    cardTitle.setAttribute("class", "card__title");
    cardDescWrapper.setAttribute("class", "card__desc-wrapper");
    cardMrt.setAttribute("class", "card__desc");
    cardCategory.setAttribute("class", "card__desc");

    cardTitle.textContent = name;
    cardMrt.textContent = mrt;
    cardCategory.textContent = category;
}

const loadPage = (container, data, shownItems) => {
    for (i = 0; i < shownItems; i++) {
        const id = data[i].id.toString();
        const url = "/attraction/" + id;
        const imgUrl = data[i].images[0];
        const name = data[i].name;
        const mrt = data[i].mrt;
        const category = data[i].category;

        addCard(container, url, imgUrl, name, mrt, category);
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

const show = (e) => {
    e.classList.remove("hidden");
}

const hide = (e) => {
    e.classList.add("hidden");
}

// Controller
const infiniteScrolling = (result, container, target, keyword) => {
    let loaded = true;
    let nextPage = result.nextPage;
    const callback = (entries, observer) => {
        entries.forEach(async (entry) => {
            if (entry.isIntersecting && loaded) {
                loaded = false;

                if (nextPage) {
                    const result = await getData(url(nextPage, keyword));
                    nextPage = result.nextPage;
                    const data = result.data;
                    const shownItems = data.length;
        
                    loadPage(container, data, shownItems);
                    loaded = true;
                }

                else {
                    loaded = true;
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
    const result = await getData(url(0, ""));
    const sentinel = document.createElement("div");
    const data = result.data;
    const shownItems = data.length;

    loadPage(main, data, shownItems);
    addSentinel(main, sentinel);
    infiniteScrolling(result, main, sentinel, "");
}

const search = async () => {
    const keyword = document.getElementById("js-header__input").value;

    while (searchResult.lastChild) {
        searchResult.removeChild(searchResult.lastChild);
    }

    if (keyword) {
        show(searchResult);
        hide(main);

        const result = await getData(url(0, keyword));
        const data = result.data;
        
        if (data) {
            const sentinel = document.createElement("div");
            const shownItems = data.length;

            loadPage(searchResult, data, shownItems);
            addSentinel(searchResult, sentinel);
            infiniteScrolling(result, searchResult, sentinel, keyword);
        }

        else {
            const searchMessage = document.createElement("p");
            addMessage(searchResult, searchMessage, "main__message", "很抱歉，我們沒有找到相關的景點");
        }
    }

    else {
        show(main);
        hide(searchResult);
    }
}

//
init();

searchBtn.addEventListener("click", search);