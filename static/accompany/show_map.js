function initMap() {
    const mapData = window.mapData;
  
    let center = { lat: 37.5665, lng: 126.9780 }; // 기본 위치 (서울)
  
    if (mapData.markers.length > 0) {
        center = { lat: mapData.markers[0].lat, lng: mapData.markers[0].lng }; // 첫 번째 마커 위치
    }
  
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: center
    });
  
    // 마커 추가
    mapData.markers.forEach(markerData => {
        const marker = new google.maps.Marker({
            position: { lat: markerData.lat, lng: markerData.lng },
            map: map,
            title: markerData.customName,
            icon: markerData.customName ? 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
        });
  
        // 인포윈도우 추가
        const infowindow = new google.maps.InfoWindow({
            content: markerData.customName || '이름 없음'
        });
  
        // 마커 클릭 시 인포윈도우 표시
        marker.addListener('click', () => {
            infowindow.open(map, marker);
        });
    });
  
    // 폴리라인 추가
    const polylinePath = mapData.polyline.map(point => ({ lat: point.lat, lng: point.lng }));
    new google.maps.Polyline({
        path: polylinePath,
        geodesic: true,
        strokeColor: '#EF4141',
        strokeWeight: 2,
        map: map
    });
  }
  
  window.initMap = initMap;