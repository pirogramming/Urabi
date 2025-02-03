let map;
let markers = []; // 마커들을 배열로 저장
let geocoder;

function initMap(){
    // 현재 위치를 가져오기 위한 기본 설정
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const userLocation ={   //현재위치치
                    lat : position.coords.latitude,
                    lng : position.coords.longitude,
                }; 

                // 구글 지도 초기화
                map = new google.maps.Map(document.getElementById("map"), {
                    center: userLocation,
                    zoom: 15
                });

                //현재 위치에 마커 추가
                addMarker(userLocation, "현재 위치", true);

                //검색 기능 추가
                searchBarLocationer();

                //기존 마커 데이터 가져오기
                // loadSeverMarkers();

                //다중 마커 기능
                google.maps.event.addListener(map, "click", function(event){
                    toggleMarker(event.latLng, "사용자 추가 마커");
                });
            },
            function(){
                alert("위치를 가져올 수 없습니다.");
            }
        );
    }else{
        alert("위치 서비스를 지원하지 않습니다.");
    }
}

//마커 추가 함수
function addMarker(position, title, isDraggable){
    const marker = new google.maps.Marker({
        position : position,
        map : map,
        title : title,
        draggable : isDraggable,   //드래그 가능여부
    });

    markers.push(marker); //새롭게 찍은 마커 배열에 추가
    const latLng = new google.maps.LatLng(position.lat, position.lng);
    updateLocation(latLng, marker); //주소업데이트

    //마커 정보창
    const infoWindow = new google.maps.InfoWindow({
        content: `<b>${title}</b>`,
    })

    marker.addListener("click",()=>{
        removeMarker(marker);  //삭제 기능 안 쓸거면 정보창 띄우면 됨
    })

    //드래그 기능
    if(isDraggable){
        marker.addListener("dragend", function(event) {
            updateLocation(event.latLng, marker);
        });
    }

    return marker
}


//마커 삭제 함수
function removeMarker(marker, addressInput){
    marker.setMap(null);
    markers = markers.filter((m) => m !== marker);
    addressInput.parentNode.remove();
}

//마커 클릭 시 추가 또는 삭제
function toggleMarker(position, title){

    //해당 좌표의 마커 존재 여부 확인
    const isExsitedMarker = markers.find(
        (marker) =>
            Math.abs(marker.getPosition().lat()-position.lat())<0.0001 &&
            Math.abs(marker.getPosition().lng()-position.lng())<0.0001
    );

    //이미 있다면 제거 없으면 추가
    if(isExsitedMarker){
        removeMarker(isExsitedMarker);
    }else{
        const newMarker = addMarker(position, title, true);
        // const latLng = new google.maps.LatLng(position.lat, position.lng);
        if(newMarker){
            updateLocation(position, newMarker);
        }else{
            console.error("새 마커 생성 실패");
        }
        
    }
}

//마커 위치 업데이트 & 좌표 저장
function updateLocation(latLng, marker) {
    if (!marker || !latLng) {
        console.error("❌ 유효하지 않은 마커 또는 위치 데이터", marker, latLng);
        return;
    }
    const lat = latLng.lat();
    const lng = latLng.lng();

    if (isNaN(lat) || isNaN(lng)) {
        console.error("❌ 위치 값이 올바르지 않습니다.", lat, lng);
        return;
    }
    marker.setPosition(latLng);
    document.getElementById("latitude").value = lat;
    document.getElementById("longitude").value = lng;

    // Geocoder를 사용하여 주소 변환
    if(!geocoder){
        geocoder = new google.maps.Geocoder();
    }

    geocoder.geocode({ location: latLng }, function(results, status) {
        if (status === "OK") {
            if (results[0]) {
                let newAddress = results[0].formatted_address; //변환 주소 생성
                let addressConatiner = document.getElementById("address_container");

                //새 주소 입력칸 생성
                let addressInput = document.createElement("input");
                addressInput.type ="text";
                addressInput.className ="address_input";
                addressInput.value =newAddress;
                addressInput.readOnly = true;
                addressInput.dataset.markerId = marker.__gm_id;

                //삭제 버튼 추가
                let deleteBtn = document.createElement("button");
                deleteBtn.textContent = "-"
                deleteBtn.className = "address_delete_btn";
                deleteBtn.onclick = function(){
                    removeMarker(marker, addressInput);
                };

                let addressWrapper = document.createElement("div");
                addressWrapper.className = "address_wrapper";
                addressWrapper.appendChild(addressInput);
                addressWrapper.appendChild(deleteBtn);

                addressConatiner.appendChild(addressWrapper);
            } else {
                document.getElementById("location").value = "주소를 찾을 수 없음";
            }
        } else {
            console.error("Geocoder 실패: " + status);
            document.getElementById("location").value = "주소 변환 오류";
        }
    });
}

//검색 바 & 위치 이동
function searchBarLocationer(){
    // 검색 바에 자동 완성 기능 추가
    const input = document.getElementById("search-bar");
    const autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.setFields(["place_id", "geometry"]);

    // 검색한 장소의 위치로 지도 이동
    autocomplete.addListener("place_changed", function() {
        const place = autocomplete.getPlace();
        if (!place.geometry) {
            alert("해당 장소를 찾을 수 없습니다.");
            return;
        }

        // 지도 중심을 검색한 장소로 이동
        map.setCenter(place.geometry.location);
        map.setZoom(15);
        addMarker(place.geometry.location, place.name, true);

        // 마커 위치 업데이트
        // if (marker) {
        // marker.setPosition(place.geometry.location);
        // } else {
        // marker = new google.maps.Marker({
        //     position: place.geometry.location,
        //     map: map,
        //     title: place.name
        // });
        // }
    });
}

//서버에서 마커 데이터 가져와서 지도에 표기
// function loadSeverMarkers(){
//     fetch("/get_locations/")
//         .then((response)=>{
//             if(!response.ok){
//                 throw new Error(`Http 오류 : ${response.status}`);
//             }
//             return response.json();
//         })
//         .then((data)=>{
//             if (data.length == 0 ){
//                 console.warn("위치 데이터가 없습니다.");
//                 return;
//             }

//             //가져온 위치에 마커 추가
//             data.forEach((location)=>{
//                 addMarker(
//                     { lat : location.latitude, lng: location.longitude },
//                     location.name,
//                     false
//                 );
//             });
//         })
//         .catch((error)=> console.error("위치 데이터 호출 실패 : ",error));
// }



window.initMap = initMap;

document.addEventListener("DOMContentLoaded", function () {
    if (typeof google !== "undefined") {
        initMap();
    } else {
        console.error("❌ Google Maps API가 로드되지 않음.");
    }
});


