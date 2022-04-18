const orderHistory = document.getElementById("js-order-history");
const orderHistoryMsg = document.getElementById("order-history__msg");
const memberHeaderName = document.getElementById("js-member-header__name");
const memberHeaderEmail = document.getElementById("js-member-header__email");
const memberHeaderEdit = document.getElementById("js-member-header__edit-btn");
const memberHeaderTitleWrapper = document.getElementById("js-member-header__title-wrapper");
const memberHeaderInputWrapper = document.getElementById("js-member-header__input-wrapper");
const memberHeaderInput = document.getElementById("js-member-header__input");
const memberHeaderConfirm = document.getElementById("js-member-header__confirm-btn");

// View
const showOrders = (orderData) => {
    const orderHistoryWrapper = document.createElement("div");
    const orderNumber = document.createElement("span");
    const orderTime = document.createElement("span");
    const orderName = document.createElement("span");
    const orderEmail = document.createElement("span");
    const orderPhone = document.createElement("span");
    const orderPrice = document.createElement("span");
    const orderHistoryBtn = document.createElement("button");
    const orderHistoryBtnIcon = document.createElement("i");
    const orderDetail = document.createElement("div");
    const orderDetailHeader = document.createElement("div");
    const orderDetailName = document.createElement("h1");
    const orderDetailAddress = document.createElement("h1");
    const orderDetailDate = document.createElement("h1");
    const orderDetailTime = document.createElement("h1");

    orderHistory.appendChild(orderHistoryWrapper);
    orderHistoryWrapper.appendChild(orderNumber);
    orderHistoryWrapper.appendChild(orderTime);
    orderHistoryWrapper.appendChild(orderName);
    orderHistoryWrapper.appendChild(orderEmail);
    orderHistoryWrapper.appendChild(orderPhone);
    orderHistoryWrapper.appendChild(orderPrice);
    orderHistoryWrapper.appendChild(orderHistoryBtn);
    orderHistoryBtn.appendChild(orderHistoryBtnIcon);
    orderHistoryWrapper.appendChild(orderDetail);
    orderDetail.appendChild(orderDetailHeader);
    orderDetailHeader.appendChild(orderDetailName);
    orderDetailHeader.appendChild(orderDetailAddress);
    orderDetailHeader.appendChild(orderDetailDate);
    orderDetailHeader.appendChild(orderDetailTime);

    orderNumber.textContent = orderData.number;
    orderTime.textContent = orderData.time;
    orderName.textContent = orderData.contact.name;
    orderEmail.textContent = orderData.contact.email;
    orderPhone.textContent = orderData.contact.phone;
    orderPrice.textContent = orderData.price + " 元";
    orderDetailName.textContent = "景點名稱";
    orderDetailAddress.textContent = "景點地址";
    orderDetailDate.textContent = "行程日期";
    orderDetailTime.textContent = "行程時段";
    
    orderHistoryWrapper.classList.add("order-history__wrapper");
    orderNumber.classList.add("order-history__txt");
    orderTime.classList.add("order-history__txt");
    orderName.classList.add("order-history__txt");
    orderEmail.classList.add("order-history__txt");
    orderPhone.classList.add("order-history__txt");
    orderPrice.classList.add("order-history__txt");
    orderHistoryBtnIcon.classList.add("bx", "bxs-chevron-down");
    orderHistoryBtn.classList.add("order-history__btn");
    orderDetail.classList.add("order-detail", "hidden");
    orderDetailHeader.classList.add("order-detail__header");
    orderDetailName.classList.add("order-detail__sub-title");
    orderDetailAddress.classList.add("order-detail__sub-title");
    orderDetailDate.classList.add("order-detail__sub-title");
    orderDetailTime.classList.add("order-detail__sub-title");

    orderHistoryBtn.addEventListener("click", () => {
        if (orderDetail.classList.contains("hidden")) {
            showBlock(orderDetail);
            orderDetail.style.opacity ="1";
            orderDetail.style.transition = "1s";
            orderHistoryBtnIcon.classList.remove("bxs-chevron-down");
            orderHistoryBtnIcon.classList.add("bxs-chevron-up");
        }

        else {
            hideBlock(orderDetail);
            orderHistoryBtnIcon.classList.remove("bxs-chevron-up");
            orderHistoryBtnIcon.classList.add("bxs-chevron-down");
        }
    });
}

const showOrderDetails = (container, tripData) => {
    for (j = 0; j < tripData.length; j++) {
        const orderDetailWrapper = document.createElement("div");
        const attractionName = document.createElement("span");
        const attractionAddress = document.createElement("span");
        const scheduleDate = document.createElement("span");
        const scheduleTime = document.createElement("span");

        container.appendChild(orderDetailWrapper);
        orderDetailWrapper.appendChild(attractionName);
        orderDetailWrapper.appendChild(attractionAddress);
        orderDetailWrapper.appendChild(scheduleDate);
        orderDetailWrapper.appendChild(scheduleTime);

        attractionName.textContent = tripData[j].attraction.name;
        attractionAddress.textContent = tripData[j].attraction.address;
        scheduleDate.textContent = tripData[j].date;
        if (tripData[j].time == "morning") {
            scheduleTime.textContent = "早上 9 點到下午 4 點";
        }

        else {
            scheduleTime.textContent = "下午 1 點到晚上 8 點";
        }

        orderDetailWrapper.classList.add("order-detail__wrapper");
        attractionName.classList.add("order-detail__txt");
        attractionAddress.classList.add("order-detail__txt");
        scheduleDate.classList.add("order-detail__txt");
        scheduleTime.classList.add("order-detail__txt");
    };
}

// Controller
const init = async () => {
    const signInResponse = await fetch("/api/user");
    const signInPromise = await signInResponse.json();
    const signInResult = await signInPromise;

    if (signInResult.data) {
        showBlock(memberBtn);
        hideBlock(gateBtn);
        showBlock(memberHeaderEdit);

        memberHeaderName.textContent = signInResult.data.name;
        memberHeaderEmail.textContent = signInResult.data.email;
    }

    else{
        window.location.href = "/";
    }

    const orderResponse = await fetch("/api/orders");
    const orderPromise = await orderResponse.json();
    const orderResult = await orderPromise;
    const orderData = orderResult.data;

    if (orderData) {
        hideBlock(orderHistoryMsg);
        orderHistory.style.opacity = "1";
        orderHistory.style.transform = "translateY(0)";

        for (i = 0; i < orderData.length; i++) {
            showOrders(orderData[i]);
        }

        for (i = 0; i < orderData.length; i++) {
            const orderNumber = orderData[i].number;
            const tripResponse = await fetch("/api/order/" + orderNumber);
            const tripPromise = await tripResponse.json();
            const tripResult = await tripPromise;
            const tripData = tripResult.data;
            const orderDetail = orderHistory.querySelectorAll(".order-detail")[i];

            showOrderDetails(orderDetail, tripData);
        }
    }

    else {
        hideBlock(orderHistory);
        orderHistoryMsg.style.opacity = "1";
        orderHistoryMsg.style.transform = "translateY(0)";
    }
}

init();

memberHeaderEdit.addEventListener("click", () => {
    showBlock(memberHeaderInputWrapper);
    hideBlock(memberHeaderTitleWrapper);
    memberHeaderInput.value = "";
});

memberHeaderConfirm.addEventListener("click", async () => {
    const newName = memberHeaderInput.value.trim();
    
    if (namePattern.test(newName)) {
        const data = {
            "new_name": newName,
        };
        const option = {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        };
        const response = await fetch("api/user", option);
        const promise = await response.json();
        const result = await promise;

        if (result.ok) {
            memberHeaderName.textContent = result.new_name;
            showBlock(memberHeaderTitleWrapper);
            hideBlock(memberHeaderInputWrapper);
        }

        else {
            setError(memberHeaderInput);
        }
    }

    else {
        setError(memberHeaderInput);
    }
});

memberHeaderInput.addEventListener("focus", () => {
    removeError(memberHeaderInput);
})

document.addEventListener("click", (e) => {
    if (e.target == memberHeaderInput || e.target == memberHeaderConfirm) {
        showBlock(memberHeaderInputWrapper);
        hideBlock(memberHeaderTitleWrapper);
    }

    else {
        showBlock(memberHeaderTitleWrapper);
        hideBlock(memberHeaderInputWrapper);
    }
}, true);