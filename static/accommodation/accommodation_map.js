function initMap() {
    console.log("initMap 실행됨");

    const defaultLocation = { lat: 37.5665, lng: 126.9780 }; // 기본 위치: 서울
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: defaultLocation
    });

    // Geocoder 인스턴스 생성 (위도/경도를 주소로 변환)
    const geocoder = new google.maps.Geocoder();
    
    // 검색 바 자동완성 기능 추가
    enableSearchBar(map, geocoder);
    
    // 클릭한 위치에 마커 추가 및 주소 업데이트
    addMarkerOnClick(map, geocoder);
}

function enableSearchBar(map, geocoder) {
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

        // 지도 중심 이동 및 마커 업데이트
        updateMarkerLocation(map, place.geometry.location, geocoder);
    });
}

function addMarkerOnClick(map, geocoder) {
    let marker = new google.maps.Marker({
        map: map,
        draggable: true
    });

    google.maps.event.addListener(map, "click", function(event) {
        updateMarkerLocation(map, event.latLng, geocoder);
    });

    google.maps.event.addListener(marker, "dragend", function(event) {
        updateMarkerLocation(map, event.latLng, geocoder);
    });
}

function updateMarkerLocation(map, latLng, geocoder) {
    if (!latLng) return;
    
    const marker = new google.maps.Marker({
        position: latLng,
        map: map,
        draggable: true
    });
    
    map.setCenter(latLng);
    
    geocoder.geocode({ location: latLng }, function(results, status) {
        if (status === "OK" && results[0]) {
            document.getElementById("review-city").value = results[0].formatted_address;
        } else {
            document.getElementById("review-city").value = "주소를 찾을 수 없음";
        }
    });
}

// Google Maps API 로드 시 initMap 실행
window.onload = function() {
    if (typeof google !== "undefined") {
        initMap();
    }
};
