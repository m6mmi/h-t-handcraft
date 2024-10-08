import winterImage from './winter.jpg';
import springImage from './spring.jpg';
import summerImage from './summer.jpg';
import fallImage from './fall.jpg';

async function fetchWeatherData(lat, lon) {
    const apiKey = 'WEATHER_API_KEY';
    const weatherUrl = `http://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${apiKey}`;

    try {
        const response = await fetch(weatherUrl);
        const data = await response.json();

        if (data.cod === 200) {
            document.getElementById('city').textContent = data.name;
            document.getElementById('temperature').textContent = `${data.main.temp}°C`;
            document.getElementById('feels-like-value').textContent = `${data.main.feels_like}°C`;
            document.getElementById('description').textContent = data.weather[0].description;
            setSeasonalBackground();
        } else {
            console.error('Error fetching weather data:', data.message);
        }
    } catch (error) {
        console.error('Error fetching weather data:', error);
    }
}

function geoFindMe() {
    const status = document.querySelector("#status");

    if (!navigator.geolocation) {
        status.textContent = "Geolocation is not supported by your browser";
    } else {
        status.textContent = "Locating…";
        navigator.geolocation.getCurrentPosition(success, error);
    }

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        status.textContent = "Location found.";
        fetchWeatherData(latitude, longitude);
    }

    function error() {
        status.textContent = "Unable to retrieve your location";
    }
}

function setSeasonalBackground() {
    const seasonalImage = document.getElementById('seasonal-image');
    const month = new Date().getMonth();

    if (month === 11 || month === 0 || month === 1) {
        seasonalImage.src = winterImage;
    } else if (month >= 2 && month <= 4) {
        seasonalImage.src = springImage;
    } else if (month >= 5 && month <= 7) {
        seasonalImage.src = summerImage;
    } else {
        seasonalImage.src = fallImage;
    }

    const overlay = document.querySelector('.card-img-overlay');
    overlay.style.color = (month === 11 || month === 0 || month === 1 || month >= 8) ? '#FFFFFF' : '#000000';
}

window.onload = () => {
    setSeasonalBackground();
    geoFindMe();
};

document.getElementById('refresh-btn').addEventListener('click', () => {
    const status = document.querySelector("#status");
    status.textContent = "Refreshing...";
    geoFindMe();
});