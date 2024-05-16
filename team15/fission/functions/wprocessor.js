module.exports = async function (context) {
    console.log(`Processed a weather data observation`);

    const observations = context.request.body.observations.data.map((observation) => {
        return {
            station_name: observation.name,
            latitude: observation.lat,
            longitude: observation.lon,
            temperature: observation.air_temp,
            apparent_temperature: observation.apparent_t,
            humidity: observation.rel_hum,
            wind_speed_kmh: observation.wind_spd_kmh,
            wind_speed_kt: observation.wind_spd_kt,
            gust_speed_kmh: observation.gust_kmh,
            gust_speed_kt: observation.gust_kt,
            pressure: observation.press,
            rainfall: observation.rain_trace,
            weather: observation.weather,
            cloud_cover: observation.cloud,
            visibility: observation.vis_km,
            timestamp: observation.local_date_time_full
        };
    });

    return {
        status: 200,
        body: JSON.stringify(observations)
    };
}