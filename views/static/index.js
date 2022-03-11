const addCard = (container, imgUrl, name, mrt, category) => {
    const cardArticle = document.createElement("article");
    const cardImg = document.createElement("img");
    const cardTxtWrapper = document.createElement("div");
    const cardTitle = document.createElement("h1");
    const cardDescWrapper = document.createElement("div");
    const cardMrt = document.createElement("span");
    const cardCategory = document.createElement("span");

    container.appendChild(cardArticle);
    cardArticle.appendChild(cardImg);
    cardArticle.appendChild(cardTxtWrapper);
    cardTxtWrapper.appendChild(cardTitle);
    cardTxtWrapper.appendChild(cardDescWrapper);
    cardDescWrapper.appendChild(cardMrt);
    cardDescWrapper.appendChild(cardCategory);

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
        const imgUrl = data[i].images[0];
        const name = data[i].name;
        const mrt = data[i].mrt;
        const category = data[i].category;

        addCard(container, imgUrl, name, mrt, category);
    };
}

const initUrl = "/api/attractions?page=0";
const body = document.getElementById("js-body");
const searchBtn = document.getElementById("js-header__btn");
const main = document.getElementById("js-main");
const sentinel = document.getElementById("js-sentinel");
const searchResult = document.createElement("div");
const searchMessage = document.createElement("p");

fetch(initUrl).then((response) => {
    const promise = response.json();
    promise.then((result) => {
        let nextPage = result.nextPage
        const url = "/api/attractions?page=";
        const data = result.data;
        const shownItems = data.length;
        const callback = (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    sentinel.style.display = "none";

                    if (nextPage) {
                            fetch(url + nextPage.toString()).then((response) => {
                            const promise = response.json();
                            promise.then((result) => {
                                nextPage = result.nextPage;
                                const data = result.data;
                                const shownItems = data.length;
                    
                                loadPage(main, data, shownItems);
                                sentinel.style.display = "block";
                            });
                        });
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

        loadPage(main, data, shownItems);
        observer.observe(sentinel);
    });
});

searchBtn.addEventListener("click", () => {
    const keyword = document.getElementById("js-header__input").value;
    const searchSentinel = document.createElement("div");

    while (searchResult.lastChild) {
        searchResult.removeChild(searchResult.lastChild);
    }

    if (keyword) {
        sentinel.style.display = "none";
        main.style.display = "none";
        body.insertBefore(searchResult, sentinel);
        body.appendChild(searchSentinel);
        searchSentinel.classList.add("sentinel");
        searchResult.classList.add("main");

        fetch(initUrl + "&keyword=" + keyword).then((response) => {
            const promise = response.json();
            promise.then((result) => {
                const data = result.data;

                if (data) {
                    let nextPage = result.nextPage;
                    const shownItems = data.length;
                    const callback = (entries, observer) => {
                        entries.forEach(entry => {
                            if (entry.isIntersecting) {
                                searchSentinel.style.display = "none";
            
                                if (nextPage) {
                                        const url = "/api/attractions?page="
                                        fetch(url + nextPage.toString() + "&keyword=" + keyword).then((response) => {
                                        const promise = response.json();
                                        promise.then((result) => {
                                            nextPage = result.nextPage;
                                            const data = result.data;
                                            const shownItems = data.length;
                                
                                            loadPage(searchResult, data, shownItems);
                                            searchSentinel.style.display = "block";
                                        });
                                    });
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

                    loadPage(searchResult, data, shownItems);
                    observer.observe(searchSentinel);
                }

                else {
                    searchResult.appendChild(searchMessage);
                    searchMessage.setAttribute("class", "main__message")
                    searchMessage.textContent = "很抱歉，我們沒有找到相關的景點";
                }
            });
        });
    }

    else {
        main.style.display = "flex";
        sentinel.style.display = "block";
        body.removeChild(searchResult);
        body.removeChild(searchSentinel);
    }
});

