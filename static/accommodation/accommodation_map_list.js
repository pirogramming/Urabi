function initMap() {
    console.log("🗺️ initMap 실행됨");

    const defaultLocation = { lat: 37.5665, lng: 126.9780 }; // 기본 위치: 서울
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: defaultLocation
    });

    const placesService = new google.maps.places.PlacesService(map);
    const streetViewService = new google.maps.StreetViewService();

    // 숙소 리스트에서 위치 가져와 지도에 마커 추가
    addAccommodationMarkers(map, placesService, streetViewService);
}

function addAccommodationMarkers(map, placesService, streetViewService) {
    const accommodationCards = document.querySelectorAll(".accommodation-card");

    accommodationCards.forEach((card) => {
        const lat = parseFloat(card.dataset.lat);
        const lng = parseFloat(card.dataset.lng);
        const title = card.dataset.title;
        const reviewId = card.dataset.reviewId;
        const imgElement = document.getElementById(`place-img-${reviewId}`);

        if (!isNaN(lat) && !isNaN(lng)) {
            const marker = new google.maps.Marker({
                position: { lat, lng },
                map: map,
                title: title
            });

            const infoWindow = new google.maps.InfoWindow({
                content: `<div>
                            <img id="info-img-${reviewId}" src="https://via.placeholder.com/150"
                            alt="숙소 이미지" style="width:100%; max-width:150px; border-radius:10px;">
                            <h3>${title}</h3>
                          </div>`,
            });

            marker.addListener("click", function () {
                infoWindow.open(map, marker);
            });

            getPlaceImage(placesService, streetViewService, lat, lng, imgElement, `info-img-${reviewId}`);
        }
    });
}

function getPlaceImage(placesService, streetViewService, lat, lng, imgElement, infoImageId) {
    const request = {
        location: { lat, lng },
        radius: 50,
        fields: ["place_id", "photos"]
    };

    placesService.nearbySearch(request, function (results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK && results.length > 0) {
            const place = results[0];

            if (place.photos && place.photos.length > 0) {
                const photoUrl = place.photos[0].getUrl({ maxWidth: 500, maxHeight: 500 });
                updateImage(imgElement, infoImageId, photoUrl);
                return;
            }
        }

        // Street View 이미지로 대체
        getStreetViewImage(streetViewService, lat, lng, imgElement, infoImageId);
    });
}

function getStreetViewImage(streetViewService, lat, lng, imgElement, infoImageId) {
    const streetViewUrl = `https://maps.googleapis.com/maps/api/streetview?size=500x500&location=${lat},${lng}&key=YOUR_GOOGLE_MAPS_API_KEY`;

    updateImage(imgElement, infoImageId, streetViewUrl);
}

function updateImage(imgElement, infoImageId, newImageUrl) {
    if (imgElement) {
        imgElement.src = newImageUrl;
    }

    setTimeout(() => {
        const infoImage = document.getElementById(infoImageId);
        if (infoImage) {
            infoImage.src = newImageUrl;
        }
    }, 500);
}
