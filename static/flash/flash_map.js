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

    //// 장소 검색 서비스 활성화
    service = new google.maps.places.PlacesService(map)
    
    google.maps.event.addListener(map, "click", function(event) {
        const request = {
            location: event.latLng,
            radius: 50, // 클릭한 위치 반경 50m 이내의 장소 검색
            type: ["restaurant", "cafe", "store"] // 원하는 타입 설정
        };

        service.nearbySearch(request, function(results, status) {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                const place = results[0]; // 가장 가까운 가게 선택
                getPlaceDetails(place.place_id);
            }
        });
    });


    // Geocoder 인스턴스 생성 (위도/경도를 주소로 변환)
    const geocoder = new google.maps.Geocoder();

    // 사용자가 지도 클릭하면 마커 이동 + 위도/경도 업데이트 + 주소 가져오기
    google.maps.event.addListener(map, "click", function(event) {
        updateLocation(event.latLng, geocoder, marker);
    });

    // 마커를 드래그해서 위치 변경할 때
    google.maps.event.addListener(marker, "dragend", function(event) {
        updateLocation(event.latLng, geocoder, marker);
    });

    // 기존 데이터가 있으면 해당 위치로 이동
    const existingLat = parseFloat(document.getElementById("latitude").value);
    const existingLng = parseFloat(document.getElementById("longitude").value);
    if (!isNaN(existingLat) && !isNaN(existingLng) && existingLat !== 0 && existingLng !== 0) {
        const existingLocation = { lat: existingLat, lng: existingLng };
        map.setCenter(existingLocation);
        marker.setPosition(existingLocation);
        updateLocation(existingLocation, geocoder, marker);
    }

    // 실시간 위치 불러오기
    getCurrentLocation(map, marker, geocoder);

    // 🔹 검색 바 자동완성 기능 추가
    enableSearchBar(map, marker, geocoder);
}

function updateLocation(latLng, geocoder, marker) {
    marker.setPosition(latLng);
    document.getElementById("latitude").value = latLng.lat();
    document.getElementById("longitude").value = latLng.lng();

    // Geocoder를 사용하여 주소 변환
    geocoder.geocode({ location: latLng }, function(results, status) {
        if (status === "OK") {
            if (results[0]) {
                document.getElementById("location").value = results[0].formatted_address;
            } else {
                document.getElementById("location").value = "주소를 찾을 수 없음";
            }
        } else {
            console.error("Geocoder 실패: " + status);
            document.getElementById("location").value = "주소 변환 오류";
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

//  특정 가게의 상세 정보 가져오기
function getPlaceDetails(placeId) {
    const request = { placeId: placeId };

    service.getDetails(request, function(place, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            console.log("가게 정보:", place);

            // 가게 대표 이미지 가져오기
            let photoUrl = "";
            if (place.photos && place.photos.length > 0) {
                photoUrl = place.photos[0].getUrl({ maxWidth: 500, maxHeight: 500 });
            } else {
                photoUrl = "https://via.placeholder.com/500"; // 이미지 없을 경우 기본 이미지
            }

            // 결과 출력
            document.getElementById("place-name").innerText = place.name;
            document.getElementById("place-img").src = photoUrl;
        }
    });
}