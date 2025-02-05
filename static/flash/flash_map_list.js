function initMap() {
    console.log("initMap 실행됨");

    const defaultLocation = { lat: 37.5665, lng: 126.9780 }; // 기본 위치: 서울
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: defaultLocation
    });

    // Geocoder 인스턴스 생성 (위도/경도를 주소로 변환)
    const geocoder = new google.maps.Geocoder();


    // 실시간 위치 불러오기
    getCurrentLocation(map, geocoder);

    // 🔹 번개 모임 리스트에서 위치 가져와 지도에 마커 추가
    addFlashMeetingMarkers(map);

    // 🔹 검색 바 자동완성 기능 추가
    enableSearchBar(map, geocoder);
}

function addFlashMeetingMarkers(map) {
    const flashCards = document.querySelectorAll(".flash_card");
    const placesService = new google.maps.places.PlacesService(map);
    const streetViewService = new google.maps.StreetViewService();

    flashCards.forEach((card) => {
        const lat = parseFloat(card.dataset.lat);
        const lng = parseFloat(card.dataset.lng);
        const title = card.querySelector("h3 a").innerText;
        const url = card.querySelector("h3 a").href;
        const date = card.dataset.date || "날짜 없음";
        const placeAddress = card.dataset.placeAddress; 
        const imgElement = card.querySelector("img");
        const meetingId = imgElement.id.replace("place-img-", ""); // 🔹 flash.meeting_id 가져오기
        const infoImageId = `place-img-${meetingId}`;
    

        if (!isNaN(lat) && !isNaN(lng)) {
            const marker = new google.maps.Marker({
                position: { lat, lng },
                map: map,
                title: title
            });

            const infoWindow = new google.maps.InfoWindow({
                content: `<div>
                            <img id="${infoImageId}" src="https://via.placeholder.com/150"
                            alt="장소 이미지" style="width:100%; max-width:150px; border-radius:10px; margin-top:5px;">
                            <h3><a href="${url}" target="_blank">${title}</a></h3>
                            <p>📅 ${date}</p>
                          </div>`,
            });

            marker.addListener("click", function () {
                infoWindow.open(map, marker);

                setTimeout(() => {
                    getPlaceImage(placesService, streetViewService, placeAddress, lat, lng, imgElement, infoImageId, infoWindow, title, url, date);
                }, 500);
            });

            getPlaceImage(placesService, streetViewService, placeAddress, lat, lng, imgElement, infoImageId, infoWindow, title, url, date);
        }
    });
}



function getPlaceImage(placesService, streetViewService, placeAddress, lat, lng, imgElement, infoImageId, infoWindow, title, url, date) {
    if (!placeAddress) {
        console.warn("장소 주소가 제공되지 않음");
        return;
    }

    const request = {
        query: placeAddress,
        fields: ["place_id", "photos"]
    };

    placesService.findPlaceFromQuery(request, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK && results.length > 0) {
            const place = results[0];

            if (place.photos && place.photos.length > 0) {
                const photoUrl = place.photos[0].getUrl({ maxWidth: 500, maxHeight: 500 });

                if (imgElement) {
                    imgElement.src = photoUrl;
                }

                updateInfoWindowImage(infoWindow, infoImageId, photoUrl, title, url, date);
                return; 
            }
        }

        // 가게 이미지가 없으면 Street View로 대체
        console.warn(`'${placeAddress}'의 이미지가 없음. Street View 요청`);
        getStreetViewImage(streetViewService, lat, lng, imgElement, infoImageId, infoWindow, title, url, date);
    });
}

function getStreetViewImage(streetViewService, lat, lng, imgElement, infoImageId, infoWindow, title, url, date) {
    const streetViewUrl = `https://maps.googleapis.com/maps/api/streetview?size=500x500&location=${lat},${lng}&key=AIzaSyDZLQne-DOUQDfifh3ZP_79TmL2OmBOI7k`;

    updateImage(imgElement, infoImageId, streetViewUrl);
    updateInfoWindowImage(infoWindow, infoImageId, streetViewUrl, title, url, date);
}

function updateImage(imgElement, infoImageId, newImageUrl) {
    console.log(`🔄 이미지 업데이트 시도: ${newImageUrl}`);

    if (imgElement) {
        imgElement.src = newImageUrl;
    } 
}

function updateInfoWindowImage(infoWindow, infoImageId, newImageUrl, title, url, date) {
    console.log(`🔄 InfoWindow 업데이트 시도: ${infoImageId}, 새로운 이미지: ${newImageUrl}`);

    // InfoWindow 내용을 다시 렌더링 (이미지를 포함하여 새로운 HTML 적용)
    infoWindow.setContent(`
        <div>
            <img id="${infoImageId}" src="${newImageUrl}"
                alt="장소 이미지" style="width:100%; max-width:150px; border-radius:10px; margin-top:5px;">
            <h3><a href="${url}" target="_blank">${title}</a></h3>
            <p>📅 ${date}</p>
        </div>
    `);

}

function updateLocation(latLng, geocoder) {
    document.getElementById("latitude").value = latLng.lat;
    document.getElementById("longitude").value = latLng.lng;

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

function getCurrentLocation(map, geocoder) {
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
                updateLocation(userLocation, geocoder);
            },
            function() {
                console.warn("위치를 가져올 수 없습니다.");
            }
        );
    } else {
        console.warn("이 브라우저에서는 위치 서비스를 지원하지 않습니다.");
    }
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

        // 지도 중심 이동 & 마커 이동
        map.setCenter(place.geometry.location);
        map.setZoom(15);

    });
}

