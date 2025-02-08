let map;
let marker;
let placesService;
let selectedLocation = null;

async function initCreateMap() {
    console.log("Create Map initialization started");
    
    try {
        await google.maps.importLibrary("places");
        
        const defaultLocation = { lat: 37.5665, lng: 126.9780 };
        map = new google.maps.Map(document.getElementById("map"), {
            zoom: 12,
            center: defaultLocation,
            mapTypeControl: true
        });

        placesService = new google.maps.places.PlacesService(map);
        
        // 숙소 이름 입력 필드에 자동완성 추가
        const accommodationInput = document.getElementById("accommodation-name");
        const autocomplete = new google.maps.places.Autocomplete(accommodationInput);
        
        autocomplete.addListener("place_changed", () => {
            const place = autocomplete.getPlace();
            if (!place.geometry) return;
            
            // 위치 정보 저장
            selectedLocation = {
                lat: place.geometry.location.lat(),
                lng: place.geometry.location.lng(),
                place_id: place.place_id
            };
            
            // 지도 중심 이동 및 마커 표시
            map.setCenter(place.geometry.location);
            if (marker) marker.setMap(null);
            
            marker = new google.maps.Marker({
                map: map,
                position: place.geometry.location,
                title: place.name
            });
            
            // 숨겨진 입력 필드에 위치 정보 저장
            document.getElementById("latitude").value = selectedLocation.lat;
            document.getElementById("longitude").value = selectedLocation.lng;
            document.getElementById("place_id").value = selectedLocation.place_id;
            
            // 도시 정보 자동 입력
            const cityComponent = place.address_components?.find(
                component => component.types.includes('locality')
            );
            if (cityComponent) {
                document.getElementById("review-city").value = cityComponent.long_name;
            }
        });
        
        console.log("Create Map initialization completed");
    } catch (error) {
        console.error("Create Map initialization failed:", error);
    }
}