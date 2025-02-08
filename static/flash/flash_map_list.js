window.initMap = async function () {
    console.log("⚡ 번개 지도 initMap 실행됨");

    try {
        await google.maps.importLibrary("places");

        const defaultLocation = { lat: 37.5665, lng: 126.9780 }; // 기본 위치: 서울
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 12,
            center: defaultLocation,
            mapTypeControl: true,
            fullscreenControl: true
        });

        const placesService = new google.maps.places.PlacesService(map);
        const streetViewService = new google.maps.StreetViewService();
        const geocoder = new google.maps.Geocoder();

        await addFlashMeetingMarkers(map, placesService, streetViewService, geocoder);
        getCurrentLocation(map, geocoder);
        enableSearchBar(map);

        console.log("✅ 번개 지도 로드 완료");
    } catch (error) {
        console.error("🚨 번개 지도 로드 실패:", error);
    }
};

async function addFlashMeetingMarkers(map, placesService, streetViewService, geocoder) {
    try {
        const flashCards = document.querySelectorAll(".flash_card");

        const markerPromises = Array.from(flashCards).map(card => {
            return new Promise(async (resolve) => {
                try {
                    const lat = parseFloat(card.dataset.lat);
                    const lng = parseFloat(card.dataset.lng);
                    const title = card.querySelector("h3 a").innerText;
                    const url = card.querySelector("h3 a").href;
                    const date = card.dataset.date || "날짜 없음";
                    const placeAddress = card.dataset.placeAddress;
                    const imgElement = card.querySelector("img");
                    const meetingId = imgElement.id.replace("place-img-", "");
                    const infoImageId = `place-img-${meetingId}`;

                    if (isNaN(lat) || isNaN(lng)) {
                        console.warn(`❌ 유효하지 않은 좌표: ${placeAddress}`);
                        resolve();
                        return;
                    }

                    // 마커 추가
                    const marker = new google.maps.Marker({
                        position: { lat, lng },
                        map: map,
                        title: title
                    });

                    // InfoWindow 생성
                    const infoWindow = new google.maps.InfoWindow({
                        content: `<div>
                                    <img id="${infoImageId}" src="https://via.placeholder.com/150"
                                    alt="장소 이미지" style="width:100%; max-width:150px; border-radius:10px;">
                                    <h3><a href="${url}" target="_blank">${title}</a></h3>
                                    <p>📅 ${date}</p>
                                  </div>`
                    });

                    marker.addListener("click", () => {
                        infoWindow.open(map, marker);
                    });

                    await getPlaceImage(placesService, streetViewService, placeAddress, imgElement, infoImageId, infoWindow, title, url, date);
                    
                    resolve(); // ✅ 마커 추가 완료 후 resolve 호출
                } catch (markerError) {
                    console.error("🚨 마커 추가 중 오류 발생:", markerError);
                    resolve();
                }
            });
        });

        await Promise.all(markerPromises);
        console.log("✅ 모든 번개 모임 마커 추가 완료");
    } catch (error) {
        console.error("🚨 번개 모임 마커 로드 실패:", error);
    }
}

async function getPlaceImage(placesService, streetViewService, placeAddress, imgElement, infoImageId, infoWindow, title, url, date) {
    if (!placeAddress) {
        console.warn("장소 주소가 제공되지 않음");
        return;
    }

    try {
        const request = { query: placeAddress, fields: ["place_id", "photos"] };

        const results = await new Promise((resolve, reject) => {
            placesService.findPlaceFromQuery(request, (res, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK && res.length > 0) {
                    resolve(res);
                } else {
                    reject(`Google Places API 실패 - 상태: ${status}`);
                }
            });
        });

        const place = results[0];
        if (place.photos && place.photos.length > 0) {
            const photoUrl = place.photos[0].getUrl({ maxWidth: 500, maxHeight: 500 });

            if (imgElement) {
                imgElement.src = photoUrl;
            }

            await updateInfoWindowImage(infoWindow, infoImageId, photoUrl, title, url, date);
            return;
        }

        console.warn(`'${placeAddress}'의 이미지가 없음. Street View 요청`);
        await getStreetViewImage(streetViewService, placeAddress, imgElement, infoImageId, infoWindow, title, url, date);
    } catch (error) {
        console.error(`🚨 장소 이미지 로드 중 오류 발생: ${placeAddress}`, error);
    }
}

async function getStreetViewImage(streetViewService, placeAddress, imgElement, infoImageId, infoWindow, title, url, date) {
    try {
        const streetViewUrl = `https://maps.googleapis.com/maps/api/streetview?size=500x500&location=${placeAddress}&key=AIzaSyDZLQne-DOUQDfifh3ZP_79TmL2OmBOI7k`;

        updateImage(imgElement, streetViewUrl);
        await updateInfoWindowImage(infoWindow, infoImageId, streetViewUrl, title, url, date);
    } catch (error) {
        console.error("🚨 Street View 이미지 로드 실패:", error);
    }
}

function updateImage(imgElement, newImageUrl) {
    if (imgElement) {
        imgElement.src = newImageUrl;
    }
}

async function updateInfoWindowImage(infoWindow, infoImageId, newImageUrl, title, url, date) {
    try {
        infoWindow.setContent(`
            <div>
                <img id="${infoImageId}" src="${newImageUrl}"
                alt="장소 이미지" style="width:100%; max-width:150px; border-radius:10px;">
                <h3><a href="${url}" target="_blank">${title}</a></h3>
                <p>📅 ${date}</p>
            </div>
        `);
    } catch (error) {
        console.error("🚨 InfoWindow 업데이트 중 오류 발생:", error);
    }
}


function enableSearchBar(map) {
    const searchInput = document.getElementById("search-bar");

    const autocomplete = new google.maps.places.Autocomplete(searchInput, {
        fields: ["geometry", "formatted_address"]
    });

    autocomplete.addListener("place_changed", function () {
        const place = autocomplete.getPlace();

        if (!place.geometry || !place.geometry.location) {
            alert("해당 장소를 찾을 수 없습니다.");
            return;
        }

        map.setCenter(place.geometry.location);
        map.setZoom(15);
    });
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

