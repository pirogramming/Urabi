document.addEventListener("DOMContentLoaded", function() {
    const addTagBtn = document.getElementById("add_tag_btn");
    const tagInput = document.getElementById("tag_input");
    const tagList = document.querySelector(".tag_list");
    const tagsHiddenInput = document.getElementById("tags_hidden");

    let tagsArray = tagsHiddenInput.value ? tagsHiddenInput.value.split(",") : [];

    addTagBtn.addEventListener("click", function() {
        let tagValue = tagInput.value.trim();
        if (tagValue !== "" && !tagsArray.includes(tagValue)) {
            tagsArray.push(tagValue);
            updateTagsDisplay();
            tagInput.value = "";
        }
    });

    function updateTagsDisplay() {
        tagList.innerHTML = "";
        tagsArray.forEach(tag => {
            const tagItem = document.createElement("span");
            tagItem.classList.add("tag_item");
            tagItem.textContent = "#" + tag;

            const removeBtn = document.createElement("button");
            removeBtn.classList.add("tag_remove_btn");
            removeBtn.textContent = "x";
            removeBtn.addEventListener("click", function() {
                tagsArray = tagsArray.filter(t => t !== tag);
                updateTagsDisplay();
            });

            tagItem.appendChild(removeBtn);
            tagList.appendChild(tagItem);
        });

        // 태그들을 쉼표로 연결하여 hidden input에 저장
        tagsHiddenInput.value = tagsArray.join(",");
    }

    // 페이지 로드 시 기존 태그 렌더링
    updateTagsDisplay();
});