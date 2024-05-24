module.exports = async function (context) {
    console.log(`Processed a weather data observation`);

    // Log the entire request body to debug the structure
    console.log('Request values01:', Object.values(context.request.body).length);
    // console.log('Request data:', context.request.data);
    console.log("observatuibs: ", Object.values(context.request.body)[0].name)

    if (!context.request.body) {
        console.log('Invalid request format');
        return {
            status: 400,
            body: 'Invalid request format'
        };
    }
    

    const observations = Object.values(context.request.body).map((observation) => {
        return {
            station_name: observation.name,
            history_product: observation.history_product,
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
    console.log("observations:", observations.station_name )
    

    return {
        status: 200,
        body: JSON.stringify(observations)
    };
}