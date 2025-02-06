function initMap() {
    console.log("initMap 실행됨");

    const defaultLocation = { lat: 37.5665, lng: 126.9780 }; // 기본 위치: 서울
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: defaultLocation
    });

    let marker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        draggable: true
    });

    // Geocoder 인스턴스 생성
    const geocoder = new google.maps.Geocoder();

    // 사용자가 지도 클릭하면 마커 이동 + 주소 업데이트
    google.maps.event.addListener(map, "click", function(event) {
        updateLocation(event.latLng, geocoder, marker);
    });

    // 마커를 드래그해서 위치 변경할 때
    google.maps.event.addListener(marker, "dragend", function(event) {
        updateLocation(event.latLng, geocoder, marker);
    });

    // 실시간 위치 불러오기
    getCurrentLocation(map, marker, geocoder);

    // 🔹 검색 바 자동완성 기능 추가
    enableSearchBar(map, marker, geocoder);
}

function updateLocation(latLng, geocoder, marker) {
    marker.setPosition(latLng);

    // Geocoder를 사용하여 주소 변환
    geocoder.geocode({ location: latLng }, function(results, status) {
        if (status === "OK") {
            if (results[0]) {
                document.getElementById("review-city").value = results[0].formatted_address;
            } else {
                document.getElementById("review-city").value = "주소를 찾을 수 없음";
            }
        } else {
            console.error("Geocoder 실패: " + status);
            document.getElementById("review-city").value = "주소 변환 오류";
        }
    });
}

function getCurrentLocation(map, marker, geocoder) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                console.log("현재 위치:", userLocation);

                // 지도 및 마커 업데이트
                map.setCenter(userLocation);
                marker.setPosition(userLocation);
                updateLocation(userLocation, geocoder, marker);
            },
            function() {
                console.warn("위치를 가져올 수 없습니다.");
            }
        );
    } else {
        console.warn("이 브라우저에서는 위치 서비스를 지원하지 않습니다.");
    }
}

function enableSearchBar(map, marker, geocoder) {
    const searchInput = document.getElementById("search-bar");
    if (!searchInput) {
        console.error("❌ 검색 바 요소를 찾을 수 없음");
        return;
    }

    // Google Places Autocomplete 설정
    const autocomplete = new google.maps.places.Autocomplete(searchInput, {
        fields: ["geometry", "formatted_address"]
    });

    // 검색한 장소 선택 시 실행
    autocomplete.addListener("place_changed", function() {
        const place = autocomplete.getPlace();
        console.log("검색한 장소 정보:", place);

        if (!place.geometry || !place.geometry.location) {
            alert("해당 장소를 찾을 수 없습니다.");
            return;
        }

        // 지도 중심 이동 & 마커 이동
        map.setCenter(place.geometry.location);
        marker.setPosition(place.geometry.location);

        // 위치 업데이트
        updateLocation(place.geometry.location, geocoder, marker);
    });
}

// 초기화
document.addEventListener("DOMContentLoaded", function() {
    initMap();
});