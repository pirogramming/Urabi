{
  document.getElementById('image-upload').addEventListener('change', function() {
    const fileInput = document.getElementById('image-upload');
    const textInput = document.getElementById('image-name');
    if (fileInput.files.length > 0) {
        textInput.value = fileInput.files[0].name;
    } else {
        textInput.value = ''; // 파일이 선택되지 않았을 때
    }
  });
    document.addEventListener("DOMContentLoaded", function() {
        const addTagBtn = document.getElementById("add_tag_btn");
        const tagInput = document.getElementById("tag_input");
        const tagList = document.querySelector(".tag_list");
        const tagsHiddenInput = document.getElementById("tags_hidden");

        let tagsArray = tagsHiddenInput.value ? tagsHiddenInput.value.split(",") :[];

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
            tagsHiddenInput.value = tagsArray.join(",");
        }
        updateTagsDisplay();

    /*나이 범위 오류 경고*/
    document.querySelector('form').addEventListener('submit',function(event){
        const minAge = parseInt(document.querySelector('input[name="min_age"]').value);
        const maxAge = parseInt(document.querySelector('input[name="max_age"]').value);

        if (minAge>maxAge){
            event.preventDefault();
            alert('나이 범위를 알맞게 설정해주세요');
            
        }
    });
});

}

