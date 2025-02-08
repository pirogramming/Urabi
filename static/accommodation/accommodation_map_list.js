window.initMap = async function() {
    console.log("Map initialization started");
    
    try {
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
        enableSearchBar(map);
        
        console.log("초기 지도 생성 성공");
    } catch (error) {
        console.error("초기 지도 생성 실패: ", error);
    }
}

async function addAccommodationMarkers(map, placesService, streetViewService, geocoder) {
    const accommodationCards = document.querySelectorAll(".accommodation-card");
    
    const markerPromises = Array.from(accommodationCards).map(card => {
        return new Promise(async (resolve) => {
            const city = card.dataset.city;
            const title = card.dataset.title;
            const reviewId = card.dataset.reviewId;
            const urlElement = card.querySelector(".view-review-btn");
            const url = urlElement ? urlElement.href : "#";
            const imgElement = document.getElementById(`place-img-${reviewId}`);
            const infoImageId = `place-img-${reviewId}`;

            if (!city) {
                console.warn("도시 주소를 찾을 수 없음:", title);
                resolve();
                return;
            }

            try {
                // Places API로 장소 검색
                const searchRequest = {
                    query: `${title} ${city}`,
                    fields: ['photos', 'place_id', 'name', 'geometry']
                };

                placesService.findPlaceFromQuery(searchRequest, async (results, status) => {
                    if (status === google.maps.places.PlacesServiceStatus.OK && results[0]) {
                        const place = results[0];
                        const location = place.geometry.location;

                        // 마커 생성
                        const marker = new google.maps.Marker({
                            position: location,
                            map: map,
                            title: title
                        });

                        // 장소 상세 정보 요청
                        placesService.getDetails({
                            placeId: place.place_id,
                            fields: ['photos']
                        }, (placeDetails, detailStatus) => {
                            if (detailStatus === google.maps.places.PlacesServiceStatus.OK && 
                                placeDetails.photos && placeDetails.photos.length > 0) {
                                
                                const photoUrl = placeDetails.photos[0].getUrl({
                                    maxWidth: 500,
                                    maxHeight: 500
                                });

                                // 이미지 업데이트
                                if (imgElement) {
                                    imgElement.src = photoUrl;
                                }

                                
                                const infoWindow = new google.maps.InfoWindow({
                                    content: `<div>
                                        <img src="${photoUrl}" 
                                            alt="${title}" 
                                            style="width:100%; max-width:150px; border-radius:10px;">
                                        <h3><a href="${url}" target="_blank">${title}</a></h3>
                                    </div>`
                                });

                                marker.addListener("click", () => {
                                    infoWindow.open(map, marker);
                                });
                            }
                            resolve();
                        });
                    } else {
                        resolve();
                    }
                });
            } catch (error) {
                console.error("장소 로딩 중 오류가 발생: ", error);
                resolve();
            }
        });
    });

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
        fields: ["place_id", "photos", "geometry"]
    };

    placesService.findPlaceFromQuery(request, async function(results, status) {
        try {
            if (status === google.maps.places.PlacesServiceStatus.OK && 
                results[0]?.photos?.length > 0) {
                const photoUrl = results[0].photos[0].getUrl({ maxWidth: 600, maxHeight: 400 });
                if (imgElement) {
                    imgElement.src = photoUrl;
                    imgElement.onerror = async () => {
                        await getStreetViewImage(city, streetViewService, infoWindow, imgElement, infoImageId, title, url);
                    };
                }
                updateInfoWindowImage(infoWindow, infoImageId, photoUrl, title, url);
            } else {
                await getStreetViewImage(city, streetViewService, infoWindow, imgElement, infoImageId, title, url);
            }
        } catch (error) {
            console.error("장소 이미지 로딩 실패: ", error);
            await getStreetViewImage(city, streetViewService, infoWindow, imgElement, infoImageId, title, url);
        }
    });
}

async function getStreetViewImage(city, streetViewService, infoWindow, imgElement, infoImageId, title, url) {
    try {
        // 위치 좌표 얻기
        const location = await new Promise((resolve, reject) => {
            const geocoder = new google.maps.Geocoder();
            geocoder.geocode({ address: city }, (results, status) => {
                if (status === "OK" && results[0]) {
                    resolve(results[0].geometry.location);
                } else {
                    reject(new Error(`Geocoding failed for ${city}`));
                }
            });
        });

        // Street View 파노라마 확인
        const panoramaData = await new Promise((resolve) => {
            streetViewService.getPanorama({
                location: location,
                radius: 50,
                source: google.maps.StreetViewSource.OUTDOOR
            }, (data, status) => {
                resolve(status === "OK" ? data : null);
            });
        });

        let imageUrl;
        if (panoramaData) {
            // Street View 이미지 URL 생성
            const panoLocation = panoramaData.location.latLng;
            const heading = panoramaData.tiles.centerHeading;
            imageUrl = `https://maps.googleapis.com/maps/api/streetview?size=600x400&location=${panoLocation.lat()},${panoLocation.lng()}&heading=${heading}&pitch=0&key=AIzaSyDZLQne-DOUQDfifh3ZP_79TmL2OmBOI7k`;
        } else {
            // Street View가 없는 경우 정적 지도 이미지 사용
            imageUrl = `https://maps.googleapis.com/maps/api/staticmap?center=${location.lat()},${location.lng()}&zoom=16&size=600x400&markers=color:red%7C${location.lat()},${location.lng()}&key=AIzaSyDZLQne-DOUQDfifh3ZP_79TmL2OmBOI7k`;
        }

        // 이미지 업데이트
        if (imgElement) {
            imgElement.src = imageUrl;
        }
        updateInfoWindowImage(infoWindow, infoImageId, imageUrl, title, url);

    } catch (error) {
        console.error("스트리트 뷰 이미지를 불러오는 데 실패: ", error);
        const defaultImage = '/static/img/room_ex1.png';
        if (imgElement) {
            imgElement.src = defaultImage;
        }
        updateInfoWindowImage(infoWindow, infoImageId, defaultImage, title, url);
    }
}

function updateImage(imgElement, newImageUrl) {
    if (imgElement) {
        imgElement.src = newImageUrl;
    } 
}

function updateInfoWindowImage(infoWindow, infoImageId, newImageUrl, title, url) {
    // 이미지를 포함하여 새로운 HTML 적용
    infoWindow.setContent(`
        <div>
            <img id="${infoImageId}" src="${newImageUrl}"
            alt="숙소 이미지" style="width:100%; max-width:150px; border-radius:10px;">
            <h3><a href="${url}" target="_blank">${title}</a></h3>
        </div>
    `);

}

function enableSearchBar(map) {
    const searchInput = document.getElementById("search-bar");
    
    
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
