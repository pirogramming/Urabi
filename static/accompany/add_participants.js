document.addEventListener('click', function(event) {
  if (event.target.matches('#add-participant')) {
      const searchInput = document.getElementById('search-email');
      const userItems = document.querySelectorAll('.user-item');

      if (searchInput && userItems.length > 0) {
          // 이메일 검색 필터링 이벤트 추가
          searchInput.addEventListener('input', function() {
              const searchTerm = this.value.toLowerCase();

              userItems.forEach(function(item) {
                  const email = item.textContent.toLowerCase();
                  if (email.includes(searchTerm)) {
                      item.style.display = 'flex';
                  } else {
                      item.style.display = 'none';
                  }
              });
          });
      }
  }
});

document.addEventListener('click', function(event) {
  if (event.target.matches('.add-btn')) {
      const userId = event.target.closest('li').dataset.userId;  // 유저 ID
      const csrfToken = document.getElementById('csrf_token').value;

      fetch(addURL, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({
              user_id: userId,
              travel_id: travelId,
          }),
      })
      .then(response => response.json())
      .then(data => {
          if (data.message) {
              alert(data.message);  // 성공 메시지 출력
              location.reload();  // 새로고침하여 참가자 목록 반영
          } else {
              alert(data.error);  // 오류 메시지 출력
          }
      })
      .catch(error => console.error('Error:', error));
  }

  if (event.target.matches('.part-del-btn')) {
      const userId = event.target.closest('li').dataset.userId;  // 유저 ID
      const csrfToken = document.getElementById('csrf_token').value;

      fetch(delURL, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({
              user_id: userId,
              travel_id: travelId,
          }),
      })
      .then(response => response.json())
      .then(data => {
          if (data.message) {
              alert(data.message);  // 성공 메시지 출력
              location.reload();  // 새로고침하여 참가자 목록 반영
          } else {
              alert(data.error);  // 오류 메시지 출력
          }
      })
      .catch(error => console.error('Error:', error));
  }
});