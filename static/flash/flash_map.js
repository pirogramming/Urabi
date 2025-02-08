async function initMap() {
    console.log("✅ initMap 실행됨");

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

    const service = new google.maps.places.PlacesService(map);
    const geocoder = new google.maps.Geocoder();

    // 지도 클릭 시 위치 업데이트
    map.addListener("click", async (event) => {
        try {
            updateLocation(event.latLng, geocoder, marker);
            await getNearbyPlaces(event.latLng, service);
        } catch (error) {
            console.error("🚨 지도 클릭 처리 중 오류:", error);
        }
    });

    // 마커 드래그 시 위치 업데이트
    marker.addListener("dragend", async (event) => {
        try {
            updateLocation(event.latLng, geocoder, marker);
        } catch (error) {
            console.error("🚨 마커 이동 중 오류:", error);
        }
    });

    // 기존 데이터가 있으면 해당 위치로 이동
    try {
        await loadExistingLocation(map, marker, geocoder);
    } catch (error) {
        console.warn("⚠️ 기존 데이터 로드 실패:", error);
    }

    // 현재 위치 불러오기
    await getCurrentLocation(map, marker, geocoder);

    // 검색 자동완성 활성화
    enableSearchBar(map, marker, geocoder);
}

async function updateLocation(latLng, geocoder, marker) {
    try {
        marker.setPosition(latLng);
        document.getElementById("latitude").value = latLng.lat();
        document.getElementById("longitude").value = latLng.lng();

        const results = await new Promise((resolve, reject) => {
            geocoder.geocode({ location: latLng }, (res, status) => {
                if (status === "OK" && res[0]) {
                    resolve(res[0]);
                } else {
                    reject("주소 변환 실패");
                }
            });
        });

        document.getElementById("location").value = results.formatted_address;
    } catch (error) {
        console.error("🚨 Geocoder 오류:", error);
        document.getElementById("location").value = "";
    }
}

async function getCurrentLocation(map, marker, geocoder) {
    if (!navigator.geolocation) {
        console.warn("⚠️ 이 브라우저에서는 위치 서비스를 지원하지 않습니다.");
        return;
    }

    try {
        const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
        });

        const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        console.log("📍 현재 위치:", userLocation);
        map.setCenter(userLocation);
        marker.setPosition(userLocation);
        await updateLocation(userLocation, geocoder, marker);
    } catch (error) {
        console.warn("⚠️ 현재 위치 불러오기 실패:", error);
    }
}

async function loadExistingLocation(map, marker, geocoder) {
    const existingLat = parseFloat(document.getElementById("latitude").value);
    const existingLng = parseFloat(document.getElementById("longitude").value);

    if (!isNaN(existingLat) && !isNaN(existingLng) && existingLat !== 0 && existingLng !== 0) {
        const existingLocation = { lat: existingLat, lng: existingLng };
        console.log("📌 기존 위치 불러오기:", existingLocation);
        map.setCenter(existingLocation);
        marker.setPosition(existingLocation);
        await updateLocation(existingLocation, geocoder, marker);
    }
}

function enableSearchBar(map, marker, geocoder) {
    const searchInput = document.getElementById("search-bar");
    if (!searchInput) {
        console.error("❌ 검색 바 요소를 찾을 수 없음");
        return;
    }

    const autocomplete = new google.maps.places.Autocomplete(searchInput, {
        fields: ["geometry", "formatted_address"]
    });

    autocomplete.addListener("place_changed", async () => {
        try {
            const place = autocomplete.getPlace();
            if (!place.geometry || !place.geometry.location) {
                alert("해당 장소를 찾을 수 없습니다.");
                return;
            }

            map.setCenter(place.geometry.location);
            marker.setPosition(place.geometry.location);
            await updateLocation(place.geometry.location, geocoder, marker);
        } catch (error) {
            console.error("🚨 검색 위치 설정 중 오류:", error);
        }
    });
}

async function getNearbyPlaces(location, service) {
    try {
        const request = {
            location: location,
            radius: 50,
            type: ["restaurant", "cafe", "store"]
        };

        const results = await new Promise((resolve, reject) => {
            service.nearbySearch(request, (res, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                    resolve(res);
                } else {
                    reject("장소 검색 실패");
                }
            });
        });

        if (results.length > 0) {
            await getPlaceDetails(results[0].place_id, service);
        }
    } catch (error) {
        console.error("🚨 주변 장소 검색 중 오류:", error);
    }
}

async function getPlaceDetails(placeId, service) {
    try {
        const request = { placeId: placeId };
        const place = await new Promise((resolve, reject) => {
            service.getDetails(request, (res, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                    resolve(res);
                } else {
                    reject("장소 상세 정보 불러오기 실패");
                }
            });
        });

        console.log("🏨 가게 정보:", place);

        let photoUrl = "https://via.placeholder.com/500";
        if (place.photos && place.photos.length > 0) {
            photoUrl = place.photos[0].getUrl({ maxWidth: 500, maxHeight: 500 });
        }

        document.getElementById("place-name").innerText = place.name;
        document.getElementById("place-img").src = photoUrl;
    } catch (error) {
        console.error("🚨 장소 상세 정보 조회 중 오류:", error);
    }
}
