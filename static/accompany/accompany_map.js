let map;
let markers = []; // 마커들을 배열로 저장
let geocoder;
let polyline;
let markerIdCounter = 0; // 고유 마커 ID를 위한 카운터

window.initMap = async function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                initializeMap(userLocation);
            },
            function() {
                alert("위치를 가져올 수 없습니다.");
                const defaultLocation = { lat: 37.5665, lng: 126.9780 }; // 기본 위치 (서울)
                initializeMap(defaultLocation);
            }
        );
    } else {
        alert("위치 서비스를 지원하지 않습니다.");
        const defaultLocation = { lat: 37.5665, lng: 126.9780 }; // 기본 위치 (서울)
        initializeMap(defaultLocation);
    }
}

function initializeMap(center) {
    // 구글 지도 초기화
    map = new google.maps.Map(document.getElementById("map"), {
        center: center,
        zoom: 15
    });

    // polyline 초기화
    polyline = new google.maps.Polyline({
        path: [],
        geodesic: true, // 지구 곡률 반영한 직선거리
        strokeColor: "#EF4141",
        strokeWeight: 2,
        map: map,
    });

    if (window.mapData) {
        const mapData = window.mapData;

        // 기존 마커 추가
        mapData.markers.forEach(markerData => {
            addMarker({ lat: markerData.lat, lng: markerData.lng }, markerData.title, false);
        });

        // 기존 폴리라인 추가
        const polylinePath = mapData.polyline.map(point => ({ lat: point.lat, lng: point.lng }));
        polyline.setPath(polylinePath);
    }

    // 검색 기능 추가
    searchBarLocationer();

    // 다중 마커 기능
    google.maps.event.addListener(map, "click", function(event) {
        toggleMarker(event.latLng, "사용자 추가 마커");
    });

    // 폼 제출 시 마커와 폴리라인 데이터를 저장
    document.querySelector('form').addEventListener('submit', saveMapData);
}

// 마커 추가 함수
function addMarker(position, title, isDraggable) {
    const marker = new google.maps.Marker({
        position: position,
        map: map,
        title: title,
        draggable: isDraggable,   // 드래그 가능 여부
        id: markerIdCounter++ // 고유 ID 할당
    });
    
    markers.push(marker); // 새롭게 찍은 마커 배열에 추가
    updatePolyline(); // 선 업데이트
    const latLng = new google.maps.LatLng(position.lat, position.lng);
    updateLocation(latLng, marker); // 주소 업데이트

    // 마커 정보창
    const infoWindow = new google.maps.InfoWindow({
        content: `<b>${title}</b>`,
    });

    marker.addListener("click", () => {
        removeMarker(marker);  // 삭제 기능 안 쓸거면 정보창 띄우면 됨
    });

    // 드래그 기능
    if (isDraggable) {
        marker.addListener("dragend", function(event) {
            updateLocation(event.latLng, marker);
        });
    }

    return marker;
}

// 마커 삭제 함수
function removeMarker(marker, addressInput) {
    marker.setMap(null);
    markers = markers.filter((m) => m !== marker);
    updatePolyline(); // 선 업데이트
    if (addressInput) {
        addressInput.parentNode.remove();
    } else {
        // 주소 입력칸도 함께 삭제
        const addressInputs = document.querySelectorAll('.address_input');
        addressInputs.forEach(input => {
            if (input.dataset.markerId == marker.id) {
                input.parentNode.remove();
            }
        });
    }
}

// 마커 클릭 시 추가 또는 삭제
function toggleMarker(position, title) {
    // 해당 좌표의 마커 존재 여부 확인
    const isExistedMarker = markers.find(
        (marker) =>
            Math.abs(marker.getPosition().lat() - position.lat()) < 0.0001 &&
            Math.abs(marker.getPosition().lng() - position.lng()) < 0.0001
    );

    // 이미 있다면 제거 없으면 추가
    if (isExistedMarker) {
        removeMarker(isExistedMarker);
    } else {
        const newMarker = addMarker(position, title, true);
        if (newMarker) {
            updateLocation(position, newMarker);
        } else {
            console.error("새 마커 생성 실패");
        }
    }
}

// 선 업데이트 
function updatePolyline() {
    const path = markers.map((marker) => marker.getPosition());
    polyline.setPath(path);
}

// 마커 위치 업데이트 & 좌표 저장
function updateLocation(latLng, marker) {
    if (!marker || !latLng) {
        console.error("❌ 유효하지 않은 마커 또는 위치 데이터", marker, latLng);
        return;
    }
    const lat = latLng.lat();
    const lng = latLng.lng();

    if (isNaN(lat) || isNaN(lng)) {
        return;
    }
    marker.setPosition(latLng);

    // Geocoder를 사용하여 주소 변환
    if (!geocoder) {
        geocoder = new google.maps.Geocoder();
    }

    geocoder.geocode({ location: latLng }, function(results, status) {
        if (status === "OK") {
            if (results[0]) {
                let newAddress = results[0].formatted_address; // 변환 주소 생성
                let addressContainer = document.getElementById("address_container");
                
                // 새 주소 입력칸 생성
                let addressInput = document.createElement("input");
                addressInput.type = "text";
                addressInput.className = "address_input";
                addressInput.value = newAddress;
                addressInput.dataset.markerId = marker.id;

                // 삭제 버튼 추가
                let deleteBtn = document.createElement("button");
                deleteBtn.textContent = "-"
                deleteBtn.className = "address_delete_btn";
                deleteBtn.onclick = function() {
                    removeMarker(marker, addressInput);
                };

                let addressWrapper = document.createElement("div");
                addressWrapper.className = "address_wrapper";
                addressWrapper.appendChild(addressInput);
                addressWrapper.appendChild(deleteBtn);

                addressContainer.appendChild(addressWrapper);
            } else {
                console.error("주소를 찾을 수 없음");
            }
        } else {
            console.error("Geocoder 실패: " + status);
        }
    });
}

// 검색 바 & 위치 이동
function searchBarLocationer() {
    const input = document.getElementById("search-bar");
    const autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.setFields(["place_id", "geometry", "name"]);

    autocomplete.addListener("place_changed", function() {
        const place = autocomplete.getPlace();
        if (!place.geometry) {
            alert("해당 장소를 찾을 수 없습니다.");
            return;
        }

        const position = place.geometry.location;

        // 지도 중심을 검색한 장소로 이동
        map.setCenter(position);
        map.setZoom(15);

        // 검색된 위치에 마커 추가
        const newMarker = addMarker(position, place.name || "검색 위치", true);

        // 주소 업데이트 (마커 위치에 따른 주소 자동 입력)
        if (newMarker) {
            updateLocation(position, newMarker);
        }
    });
}
document.addEventListener('DOMContentLoaded', function() {
    // form 내의 모든 input 요소를 찾습니다
    const formInputs = document.querySelectorAll('form input:not([type="hidden"])');
    
    formInputs.forEach(input => {
        input.addEventListener('keydown', function(e) {
            // 엔터 키가 눌렸을 때
            if (e.key === 'Enter') {
                // textarea나 submit 버튼이 아닌 경우 기본 동작 방지
                if (input.type !== 'textarea' && input.type !== 'submit') {
                    e.preventDefault();
                }
            }
        });
    });

    // form 제출은 submit 버튼을 통해서만 가능하도록 설정
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        // submit 버튼을 통한 제출이 아닌 경우 기본 동작 방지
        if (event.submitter === null || event.submitter.type !== 'submit') {
            event.preventDefault();
        }
    });
});
// 폼 제출 시 마커와 폴리라인 데이터를 저장
function saveMapData(event) {
    // submit 버튼을 통한 제출인 경우에만 처리
    if (event.submitter && event.submitter.type === 'submit') {
        const markersData = markers.map(marker => ({
            lat: marker.getPosition().lat(),
            lng: marker.getPosition().lng(),
            title: marker.getTitle()
        }));

        const polylineData = polyline.getPath().getArray().map(latLng => ({
            lat: latLng.lat(),
            lng: latLng.lng()
        }));

        document.getElementById('markers').value = JSON.stringify(markersData);
        document.getElementById('polyline').value = JSON.stringify(polylineData);
    }
}