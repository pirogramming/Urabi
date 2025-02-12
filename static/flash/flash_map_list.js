const DEFAULT_IMAGE_URL = "/static/img/default_map_image.jpg";

function isGoogleMapsLoaded() {
    return typeof google !== "undefined" && typeof google.maps !== "undefined";
}

window.initMap = function () {
    if (!isGoogleMapsLoaded()) {
        console.error("🚨 Google Maps API가 아직 로드되지 않음!");
        return;
    }
    window.actualInitMap?.();
};

window.actualInitMap = async function () {
    try {
        await google.maps.importLibrary("places");
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 12,
            center: { lat: 37.5665, lng: 126.9780 },
            mapTypeControl: true,
            fullscreenControl: true
        });

        const placesService = new google.maps.places.PlacesService(map);
        const streetViewService = new google.maps.StreetViewService();
        const geocoder = new google.maps.Geocoder();

        await addFlashMeetingMarkers(map, placesService, streetViewService);
        enableSearchBar(map);
        getCurrentLocation(map);
    } catch (error) {
        console.error("🚨 번개 지도 로드 실패:", error);
    }
};

async function addFlashMeetingMarkers(map, placesService, streetViewService) {
    const flashCards = document.querySelectorAll(".flash_card");
    
    await Promise.all(Array.from(flashCards).map(async (card) => {
        const lat = parseFloat(card.dataset.lat);
        const lng = parseFloat(card.dataset.lng);
        if (isNaN(lat) || isNaN(lng)) return;

        const title = card.querySelector("h3 a").innerText;
        const url = card.querySelector("h3 a").href;
        const date = card.dataset.date || "날짜 없음";
        const placeAddress = card.dataset.placeAddress;
        const imgElement = card.querySelector("img");
        const infoImageId = `place-img-${imgElement.id.replace("place-img-", "")}`;

        const marker = new google.maps.Marker({ position: { lat, lng }, map, title });
        const infoWindow = new google.maps.InfoWindow({ content: createInfoWindowContent(DEFAULT_IMAGE_URL, title, url, date, infoImageId) });
        marker.addListener("click", () => infoWindow.open(map, marker));

        await loadPlaceImage(placesService, streetViewService, placeAddress, imgElement, infoWindow, infoImageId, title, url, date);
    }));
}

async function loadPlaceImage(placesService, streetViewService, placeAddress, imgElement, infoWindow, infoImageId, title, url, date) {
    if (!placeAddress) return setImage(imgElement, DEFAULT_IMAGE_URL);
    
    try {
        const results = await findPlaceFromQuery(placesService, placeAddress);
        const photoUrl = results[0]?.photos?.[0]?.getUrl({ maxWidth: 500, maxHeight: 500 }) || null;

        if (photoUrl) {
            return setImage(imgElement, photoUrl, infoWindow, infoImageId, title, url, date);
        }
        
        console.warn(`'${placeAddress}'의 장소 이미지 없음. Street View 시도`);
        await loadStreetViewImage(streetViewService, placeAddress, imgElement, infoWindow, infoImageId, title, url, date);
    } catch (error) {
        console.error(`🚨 이미지 로드 실패: ${placeAddress}`, error);
        setImage(imgElement, DEFAULT_IMAGE_URL);
    }
}

async function loadStreetViewImage(streetViewService, placeAddress, imgElement, infoWindow, infoImageId, title, url, date) {
    try {
        const streetViewUrl = `https://maps.googleapis.com/maps/api/streetview?size=500x500&location=${placeAddress}&key=AIzaSyDZLQne-DOUQDfifh3ZP_79TmL2OmBOI7k`;
        setImage(imgElement, streetViewUrl, infoWindow, infoImageId, title, url, date);
    } catch (error) {
        console.error("🚨 Street View 이미지 로드 실패:", error);
        setImage(imgElement, DEFAULT_IMAGE_URL);
    }
}

async function findPlaceFromQuery(placesService, query) {
    return new Promise((resolve, reject) => {
        placesService.findPlaceFromQuery({ query, fields: ["place_id", "photos"] }, (res, status) => {
            status === google.maps.places.PlacesServiceStatus.OK ? resolve(res) : reject(`Google Places API 실패 - 상태: ${status}`);
        });
    });
}

function setImage(imgElement, imageUrl, infoWindow, infoImageId, title, url, date) {
    imgElement.src = imageUrl;
    if (infoWindow) infoWindow.setContent(createInfoWindowContent(imageUrl, title, url, date, infoImageId));
}

function createInfoWindowContent(imageUrl, title, url, date, infoImageId) {
    return `<div>
        <img id="${infoImageId}" src="${imageUrl}" alt="장소 이미지" style="width:100%; max-width:150px; border-radius:10px;">
        <h3><a href="${url}" target="_blank">${title}</a></h3>
        <p>📅 ${date}</p>
    </div>`;
}

function enableSearchBar(map) {
    const searchInput = document.getElementById("search-bar");
    const autocomplete = new google.maps.places.Autocomplete(searchInput, { fields: ["geometry"] });
    
    autocomplete.addListener("place_changed", () => {
        const place = autocomplete.getPlace();
        if (!place.geometry) return alert("해당 장소를 찾을 수 없습니다.");
        map.setCenter(place.geometry.location);
        map.setZoom(15);
    });
}

function getCurrentLocation(map) {
    if (!navigator.geolocation) {
        console.warn("이 브라우저에서는 위치 서비스를 지원하지 않습니다.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function (position) {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            console.log("✅ 현재 위치:", userLocation);

            // 지도 중심을 사용자 위치로 변경
            map.setCenter(userLocation);
        },
        function (error) {
            console.warn("🚨 위치 정보를 가져올 수 없음:", error);
        }
    );
}

