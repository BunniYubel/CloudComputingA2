module.exports = async function (context) {
    console.log(`Processed a traffic accident observation`);
    return {
        status: 200,
        body: JSON.stringify(context.request.body.map((accident) => {
        return {
            // Change the field names to the ones you want
            accident_id: accident.id, // Assuming there's an 'id' field
            location: [accident.longitude, accident.latitude], // Assuming 'longitude' and 'latitude' fields
            timestamp: accident.timestamp, // Assuming a 'timestamp' field
            severity: accident.severity, // Assuming a 'severity' field
            description: accident.description // Assuming a 'description' field
        };
        }))
    };
    }