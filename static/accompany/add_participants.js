document.addEventListener("DOMContentLoaded", function () {
    const csrfToken = document.getElementById("csrf_token").value;

    // 이메일 검색 필터링
    const searchInput = document.getElementById("search-email");
    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const searchTerm = this.value.toLowerCase();
            document.querySelectorAll(".user-item").forEach(function (item) {
                const email = item.textContent.toLowerCase();
                item.style.display = email.includes(searchTerm) ? "flex" : "none";
            });
        });
    }

    // 참가 요청 버튼 클릭 이벤트
    document.body.addEventListener("click", function (event) {
        if (event.target.matches(".request-btn")) {
            handleRequest("POST", requestURL, csrfToken, "참가 신청이 완료되었습니다!");
        }
        if (event.target.matches(".request-cancel-btn")) {
            handleRequest("POST", requestCancelURL, csrfToken, "참가 신청이 취소되었습니다!");
        }
        if (event.target.matches(".add-btn")) {
            handleParticipant(event.target, addURL, csrfToken, "참여자가 추가되었습니다!");
        }
        if (event.target.matches(".part-del-btn")) {
            handleParticipant(event.target, delURL, csrfToken, "참여자가 삭제되었습니다!");
        }
    });
});

function handleRequest(method, url, csrfToken, successMessage) {
    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ travel_id: travelId }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert(successMessage);
                location.reload();
            } else {
                alert("오류 발생: " + data.message);
            }
        })
        .catch((error) => console.error("Error:", error));
}

function handleParticipant(button, url, csrfToken, successMessage) {
    const userId = button.closest("li").dataset.userId;
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ user_id: userId, travel_id: travelId }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.message) {
                alert(successMessage);
                location.reload();
            } else {
                alert("오류 발생: " + data.error);
            }
        })
        .catch((error) => console.error("Error:", error));
}
