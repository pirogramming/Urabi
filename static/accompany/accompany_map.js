console.log("✅ accompany_map.js 파일이 정상적으로 로드됨.");

function initMap() {
    console.log("initMap 실행됨");

    const defaultLocation = { lat: 37.5665, lng: 126.9780 }; // 기본 위치: 서울
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: defaultLocation
    });


    // 기본 마커 생성
    let marker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        draggable: true
    });

    fetch("/get_locations/")
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP 오류! 상태 코드: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("🔹 서버에서 받은 위치 데이터:", data);
        
        if (data.length === 0) {
            console.warn("⚠️ 위치 데이터가 없습니다. `get_locations/` API 응답을 확인하세요.");
            return; // 데이터가 없으면 더 이상 실행하지 않음
        }

        data.forEach(location => {
            console.log("📍 마커 추가: ", location.name, location.latitude, location.longitude);

            let newMarker = new google.maps.Marker({
                position: { lat: location.latitude, lng: location.longitude },
                map: map,
                draggable: true
            });

            let infoWindow = new google.maps.InfoWindow({
                content: `<b>${location.name}</b>`
            });

            newMarker.addListener("click", () => {
                infoWindow.open(map, newMarker);
            });

            // ✅ 드래그 이벤트 추가
            newMarker.addListener("dragend", function(event) {
                updateLocation(event.latLng, new google.maps.Geocoder(), newMarker);
            });
        });
    })
    .catch(error => console.error("❌ 위치 데이터 불러오기 실패:", error));



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
}
//내가 추가
window.initMap = initMap;

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


document.getElementById('image-upload').addEventListener('change', function() {
    const fileInput = document.getElementById('image-upload');
    const textInput = document.getElementById('image-name');
    if (fileInput.files.length > 0) {
        textInput.value = fileInput.files[0].name;
    } else {
        textInput.value = ''; // 파일이 선택되지 않았을 때
    }
});

document.addEventListener("DOMContentLoaded", function () {
    if (typeof google !== "undefined") {
        initMap();
    } else {
        console.error("❌ Google Maps API가 로드되지 않음.");
    }
});
