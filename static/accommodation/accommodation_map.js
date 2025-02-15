window.initMap = async function() {
    try {
        // Places 라이브러리 로드 대기
        await google.maps.importLibrary("places");
        console.log("Map initialization started");

        const defaultLocation = { lat: 37.5665, lng: 126.9780 };
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 12,
            center: defaultLocation,
            mapTypeControl: true,
            fullscreenControl: true
        });

        let marker = new google.maps.Marker({
            position: defaultLocation,
            map: map,
            draggable: true,
            animation: google.maps.Animation.DROP
        });

        const geocoder = new google.maps.Geocoder();

        // 지도 클릭 이벤트
        map.addListener("click", function(event) {
            updateLocation(event.latLng, geocoder, marker);
        });

        // 마커 드래그 이벤트
        marker.addListener("dragend", function(event) {
            updateLocation(marker.getPosition(), geocoder, marker);
        });

        // 실시간 위치 및 검색 기능 초기화
        await initializeLocationFeatures(map, marker, geocoder);

    } catch (error) {
        console.error("Map initialization failed:", error);
    }
}

async function initializeLocationFeatures(map, marker, geocoder) {
    try {
        await getCurrentLocation(map, marker, geocoder);
        await enableSearchBar(map, marker, geocoder);
    } catch (error) {
        console.error("Location features initialization failed:", error);
    }
}

async function updateLocation(latLng, geocoder, marker) {
    try {
        marker.setPosition(latLng);

        const response = await new Promise((resolve, reject) => {
            geocoder.geocode({ location: latLng }, (results, status) => {
                if (status === "OK") {
                    resolve(results);
                } else {
                    reject(status);
                }
            });
        });

        const cityInput = document.getElementById("review-city");
        if (cityInput) {
            cityInput.value = response[0]?.formatted_address || "주소를 찾을 수 없음";
        }
    } catch (error) {
        console.error("Address lookup failed:", error);
        const cityInput = document.getElementById("review-city");
        if (cityInput) {
            cityInput.value = "주소 변환 오류";
        }
    }
}

function getCurrentLocation(map, marker, geocoder) {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            console.warn("Geolocation is not supported by this browser");
            resolve(false);
            return;
        }

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                try {
                    const userLocation = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };

                    map.setCenter(userLocation);
                    marker.setPosition(userLocation);
                    await updateLocation(userLocation, geocoder, marker);
                    resolve(true);
                } catch (error) {
                    console.error("Error updating location:", error);
                    resolve(false);
                }
            },
            (error) => {
                console.warn("Error getting current location:", error);
                resolve(false);
            },
            {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
            }
        );
    });
}

async function enableSearchBar(map, marker, geocoder) {
    const searchInput = document.getElementById("search-bar");
    if (!searchInput) {
        console.warn("Search bar element not found");
        return;
    }

    try {
        const autocomplete = new google.maps.places.Autocomplete(searchInput, {
            fields: ["geometry", "formatted_address"]
        });

        autocomplete.addListener("place_changed", async () => {
            const place = autocomplete.getPlace();

            if (!place.geometry || !place.geometry.location) {
                alert("선택한 장소를 찾을 수 없습니다.");
                return;
            }

            map.setCenter(place.geometry.location);
            map.setZoom(15);
            marker.setPosition(place.geometry.location);
            await updateLocation(place.geometry.location, geocoder, marker);
        });
    } catch (error) {
        console.error("Error setting up search bar:", error);
    }
}

// DOMContentLoaded 이벤트 리스너 제거 (callback으로 대체)
