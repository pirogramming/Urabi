window.initMap = async function() {
    console.log("Map initialization started");
    
    try {
        // Places 라이브러리 로드 대기
        await google.maps.importLibrary("places");
        
        const defaultLocation = { lat: 37.5665, lng: 126.9780 };
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 12,
            center: defaultLocation,
            mapTypeControl: true,
            fullscreenControl: true
        });

        const placesService = new google.maps.places.PlacesService(map);
        const streetViewService = new google.maps.StreetViewService();
        const geocoder = new google.maps.Geocoder();

        // 마커 추가 및 검색 기능 초기화
        await addAccommodationMarkers(map, placesService, streetViewService, geocoder);
        enableSearchBar(map, geocoder);
        
        console.log("Map initialization completed");
    } catch (error) {
        console.error("Map initialization failed:", error);
    }
}

async function addAccommodationMarkers(map, placesService, streetViewService, geocoder) {
    const accommodationCards = document.querySelectorAll(".accommodation-card");
    
    const markerPromises = Array.from(accommodationCards).map(card => {
        return new Promise((resolve) => {
            const city = card.dataset.city;
            const title = card.dataset.title;
            const reviewId = card.dataset.reviewId;
            const urlElement = card.querySelector(".view-review-btn");
            const url = urlElement ? urlElement.href : "#";
            const imgElement = document.getElementById(`place-img-${reviewId}`);
            const infoImageId = `place-img-${reviewId}`;

            if (!city) {
                console.warn("Missing city address for:", title);
                resolve();
                return;
            }

            geocoder.geocode({ address: city }, (results, status) => {
                if (status !== "OK" || !results[0]) {
                    console.error("Geocoding failed for:", city);
                    resolve();
                    return;
                }

                const location = results[0].geometry.location;
                console.log("Coordinates found for:", city);

                const marker = new google.maps.Marker({
                    position: location,
                    map: map,
                    title: title,
                    animation: google.maps.Animation.DROP
                });

                const infoWindow = new google.maps.InfoWindow({
                    content: `<div>
                        <img id="${infoImageId}" src="https://via.placeholder.com/150"
                        alt="숙소 이미지" style="width:100%; max-width:150px; border-radius:10px;">
                        <h3><a href="${url}" target="_blank">${title}</a></h3>
                    </div>`
                });

                marker.addListener("click", () => {
                    infoWindow.open(map, marker);
                });

                // 이미지 로딩
                const request = {
                    query: city,
                    fields: ["place_id", "photos"]
                };

                placesService.findPlaceFromQuery(request, (results, status) => {
                    if (status === google.maps.places.PlacesServiceStatus.OK && 
                        results[0]?.photos?.length > 0) {
                        const photoUrl = results[0].photos[0].getUrl({ maxWidth: 500, maxHeight: 500 });
                        if (imgElement) imgElement.src = photoUrl;
                        updateInfoWindowImage(infoWindow, infoImageId, photoUrl, title, url);
                    }
                    resolve();
                });
            });
        });
    });

    // 모든 마커가 추가될 때까지 대기
    await Promise.all(markerPromises);
}

function getLocationCoordinates(city, geocoder, callback) {
    geocoder.geocode({ address: city }, (results, status) => {
        if (status === "OK" && results[0]) {
            const location = results[0].geometry.location;
            callback({ lat: location.lat(), lng: location.lng() });
        } else {
            console.error(`🚨 Geocoding 실패: ${city} - 상태: ${status}`);
            callback(null);
        }
    });
}

function getPlaceImage(city, placesService, streetViewService, infoWindow, imgElement, infoImageId, title, url) {
    const request = {
        query: city,
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

                updateInfoWindowImage(infoWindow, infoImageId, photoUrl, title, url)
                return;
            }
        }

        console.warn(`'${city}'의 이미지가 없음. Street View 요청`);
        getStreetViewImage(city, streetViewService, infoWindow, imgElement, infoImageId, title, url);
    });
}

function getStreetViewImage(city, streetViewService, infoWindow, imgElement, infoImageId, title, url) {
    getLocationCoordinates(city, new google.maps.Geocoder(), (location) => {
        if (!location) {
            console.error(`❌ Street View 좌표 변환 실패: ${city}`);
            return;
        }

        const streetViewUrl = `https://maps.googleapis.com/maps/api/streetview?size=500x500&location=${location.lat},${location.lng}&key=AIzaSyDZLQne-DOUQDfifh3ZP_79TmL2OmBOI7k`;

        updateImage(imgElement, streetViewUrl);
        updateInfoWindowImage(infoWindow, infoImageId, streetViewUrl, title, url)
    });
}

function updateImage(imgElement, newImageUrl) {
    if (imgElement) {
        imgElement.src = newImageUrl;
    } 
}

function updateInfoWindowImage(infoWindow, infoImageId, newImageUrl, title, url) {
    // InfoWindow 내용을 다시 렌더링 (이미지를 포함하여 새로운 HTML 적용)
    infoWindow.setContent(`
        <div>
            <img id="${infoImageId}" src="${newImageUrl}"
            alt="숙소 이미지" style="width:100%; max-width:150px; border-radius:10px;">
            <h3><a href="${url}" target="_blank">${title}</a></h3>
        </div>
    `);

}

function enableSearchBar(map, geocoder) {
    const searchInput = document.getElementById("search-bar");
    
    // Google Places Autocomplete 설정
    const autocomplete = new google.maps.places.Autocomplete(searchInput, {
        fields: ["geometry", "formatted_address"]
    });

    autocomplete.addListener("place_changed", function() {
        const place = autocomplete.getPlace();

        if (!place.geometry || !place.geometry.location) {
            alert("해당 장소를 찾을 수 없습니다.");
            return;
        }

        map.setCenter(place.geometry.location);
        map.setZoom(15);
    });
}
