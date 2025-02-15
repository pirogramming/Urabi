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
    map = new google.maps.Map(document.getElementById("map"), {
        center: center,
        zoom: 15
    });

    polyline = new google.maps.Polyline({
        path: [],
        geodesic: true,
        strokeColor: "#EF4141",
        strokeWeight: 2,
        map: map,
    });

    if (window.mapData) {
        const mapData = window.mapData;
        
        // 기존 마커 추가할 때 customName 포함하여 전달
        mapData.markers.forEach(markerData => {
            const position = { lat: markerData.lat, lng: markerData.lng };
            const marker = addMarker(
                position,
                markerData.customName || markerData.title,
                false
            );
            
            // 마커에 customName 저장
            marker.customName = markerData.customName;
            
            // 주소와 customName으로 input 생성
            createMarkerInputs(marker, markerData.address || '위치 정보 없음', markerData.customName);
        });

        const polylinePath = mapData.polyline.map(point => ({ lat: point.lat, lng: point.lng }));
        polyline.setPath(polylinePath);
    }

    searchBarLocationer();

    google.maps.event.addListener(map, "click", function(event) {
        toggleMarker(event.latLng, "사용자 추가 마커");
    });

    document.querySelector('form').addEventListener('submit', saveMapData);
}

// 마커 추가 함수
function addMarker(position, title, isDraggable) {
    const marker = new google.maps.Marker({
        position: position,
        map: map,
        title: title,
        draggable: isDraggable,
        id: markerIdCounter++
    });
    
    markers.push(marker);
    updatePolyline();
    const latLng = new google.maps.LatLng(position.lat, position.lng);
    updateLocation(latLng, marker);

    // 마커 클릭 이벤트 수정
    marker.addListener("click", () => {
        removeMarker(marker);  // 마커 객체만 전달
    });

    if (isDraggable) {
        marker.addListener("dragend", function(event) {
            updateLocation(event.latLng, marker);
        });
    }

    return marker;
}
function createMarkerInputs(marker, address, customName) {
  const addressContainer = document.getElementById("address_container");
  if (!addressContainer) return;
  const wrapper = document.createElement("div");
  wrapper.className = "address_wrapper";
  wrapper.dataset.markerId = marker.id;
  
  const addressDisplay = document.createElement("span");
  addressDisplay.className = "address_display";
  addressDisplay.textContent = address || "주소 정보 없음";
  
  const nameInput = document.createElement("input");
  nameInput.type = "text";
  nameInput.className = "marker_name_input";
  nameInput.placeholder = "장소 이름을 입력하세요";
  nameInput.dataset.markerId = marker.id;
  nameInput.value = customName || "";
  nameInput.addEventListener("change", function() {
    marker.customName = this.value;
    marker.setTitle(this.value);
    updateMarkersField();
    updateMarkerTimeline();
  });
  
  // 삭제 버튼
  const deleteBtn = document.createElement("button");
  deleteBtn.textContent = "-";
  deleteBtn.className = "address_delete_btn";
  deleteBtn.onclick = function(e) {
    e.preventDefault();
    removeMarker(marker, wrapper);
  };

  // 세로로 정렬: 각 요소 사이에 <br> 태그 추가
  wrapper.appendChild(addressDisplay);
  wrapper.appendChild(document.createElement("br"));
  wrapper.appendChild(nameInput);
  wrapper.appendChild(deleteBtn);
  
  addressContainer.appendChild(wrapper);
}

  
function removeMarker(marker, wrapper) {
    marker.setMap(null);
    markers = markers.filter((m) => m !== marker);
    updatePolyline(); // 선 업데이트
    if (wrapper) {
        wrapper.remove();
    } else {
        // 마커 클릭으로 삭제할 경우
        const wrapper = document.querySelector(`.address_wrapper[data-marker-id="${marker.id}"]`);
        if (wrapper) {
            wrapper.remove();
        }
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

    if (!geocoder) {
        geocoder = new google.maps.Geocoder();
    }

    geocoder.geocode({ location: latLng }, function(results, status) {
        if (status === "OK" && results[0]) {
            const address = results[0].formatted_address;
            marker.address = address;
        
            const existingWrapper = document.querySelector(`.address_wrapper[data-marker-id="${marker.id}"]`);
            if (existingWrapper) {
            const addressDisplay = existingWrapper.querySelector('.address_display');
            if (addressDisplay) addressDisplay.textContent = address;
            } else {
            createMarkerInputs(marker, address, marker.customName);
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
    const formInputs = document.querySelectorAll('form input:not([type="hidden"])');
    
    formInputs.forEach(input => {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                if (input.type !== 'textarea' && input.type !== 'submit') {
                    e.preventDefault();
                }
            }
        });
    });

    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        if (event.submitter === null || event.submitter.type !== 'submit') {
            event.preventDefault();
        }
    });
});

function saveMapData(event) {
    if (event.submitter && event.submitter.type === 'submit') {
        const markersData = markers.map(marker => ({
            lat: marker.getPosition().lat(),
            lng: marker.getPosition().lng(),
            title: marker.getTitle(),
            customName: marker.customName || '',
            address: marker.address || ''
        }));

        const polylineData = polyline.getPath().getArray().map(latLng => ({
            lat: latLng.lat(),
            lng: latLng.lng()
        }));

        document.getElementById('markers').value = JSON.stringify(markersData);
        document.getElementById('polyline').value = JSON.stringify(polylineData);
    }
}

function updateMarkerTimeline() {
    const markerListEl = document.getElementById("marker-list");
    if (!markerListEl) return;
    
    markerListEl.innerHTML = "";
    
    if (markers.length === 0) {
      const li = document.createElement("li");
      li.textContent = "등록된 장소가 없습니다.";
      markerListEl.appendChild(li);
    } else {
      markers.forEach((marker) => {
        const li = document.createElement("li");
        li.textContent = marker.customName || marker.title || "장소 없음";
        markerListEl.appendChild(li);
      });
    }
  }
  