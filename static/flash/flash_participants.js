document.addEventListener("DOMContentLoaded", function () {
    const csrfToken = document.getElementById("csrf_token")?.value;
    const flashIdElement = document.querySelector("#flash-data");
    const flashId = flashIdElement ? flashIdElement.dataset.flashId : null;
    
    const applyURL = "/flash/apply_participant/";
    const cancelURL = "/flash/cancel_participant/";
    const addURL = "/flash/add_participant/";
    const delURL = "/flash/remove_participant/";

    /** 참가자 리스트 토글 기능 */
    document.getElementById('toggleMembers')?.addEventListener('click', function() {
        var memberList = document.getElementById('memberList');
        if (memberList.style.display === 'none') {
            memberList.style.display = 'block';
            this.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-down-fill" viewBox="0 0 16 16"><path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/></svg>';
        } else {
            memberList.style.display = 'none';
            this.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-right-fill" viewBox="0 0 16 16"><path d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"/></svg>';
        }
    });

    /** 참가 요청 및 삭제 이벤트 핸들러 */
    document.body.addEventListener("click", function (event) {
        if (event.target.matches(".flash_apply_btn")) {
            const button = event.target;
            const flashId = flashIdElement.dataset.flashId; 
            if (button.classList.contains("request-btn")) {
                handleRequest("POST", applyURL, csrfToken, flashId, "참가 신청이 완료되었습니다!", button);
            } else if (button.classList.contains("request-cancel-btn")) {
                handleRequest("POST", cancelURL, csrfToken, flashId, "참가 신청이 취소되었습니다!", button);
            }
        }
        if (event.target.matches(".add-btn")) {
            handleParticipant(event.target, addURL, csrfToken, "참여자가 추가되었습니다!");
        }
        if (event.target.matches(".part-del-btn")) {
            handleParticipant(event.target, delURL, csrfToken, "참여자가 삭제되었습니다!");
        }
    });
    
    tippy("#add-participant", {
        content: "이메일 입력",
        placement: "bottom-end",
        arrow: false,
        theme: "light",
        trigger: "click",
        interactive: true,
        allowHTML: true,
        onShow(instance) {
            fetch(`/flash/${flashId}/requests/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let listHTML = data.requests.map(user => 
                        `<li data-user-id="${user.id}">
                            ${user.email} <button class="add-btn">+</button>
                        </li>`).join("");
                    instance.setContent(`<ul>${listHTML}</ul>`);
                } else {
                    instance.setContent("참가 요청이 없습니다.");
                }
            })
            .catch(error => {
                console.error("Error fetching request list:", error);
                instance.setContent("오류 발생");
            });
        }
    });
    
});


/**
 * 요청 관리
 */
function handleRequest(method, url, csrfToken, flashId, successMessage, button) {
    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ flash_id: flashId }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            alert(successMessage);
            // 버튼 상태 업데이트
            if (button.classList.contains("request-btn")) {
                button.classList.remove("request-btn");
                button.classList.add("request-cancel-btn");
                button.textContent = "요청 취소";
            } else {
                button.classList.remove("request-cancel-btn");
                button.classList.add("request-btn");
                button.textContent = "참여 요청";
            }
        } else {
            alert("오류 발생: " + data.message);
        }
    })
    .catch((error) => console.error("Error:", error));
}

/**
 * 참가 관리
 */
function handleParticipant(button, url, csrfToken, successMessage) {
    const userId = button.closest("li").dataset.userId;
    const flashIdElement = document.querySelector("#flash-data");
    const flashId = flashIdElement ? flashIdElement.dataset.flashId : null;

    console.log(JSON.stringify({ user_id: userId, flash_id: flashId }));
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ user_id: userId, flash_id: flashId }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.message) {
            alert(successMessage);

            if (data.participant_ids) {
                updateParticipantList(data.participant_ids);
            }
            location.reload();  // 페이지 새로고침
        } else {
            alert("오류 발생: " + data.error);
        }
    })
    .catch((error) => console.error("Error:", error));
}

function updateParticipantList(participantIds) {
    document.querySelectorAll(".ing").forEach((elem) => {
        const userId = parseInt(elem.dataset.userId, 10);
        if (!participantIds.includes(userId)) {
            elem.remove();
        }
    });
}
