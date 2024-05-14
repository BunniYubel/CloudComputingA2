module.exports = async function (context) {
    const accidentsData = context.request.body;
  
    const transformedAccidents = accidentsData.map((accident) => {
      return {
        state: accident.State,
        month: accident.Month,
        year: accident.Year,
        dayOfWeek: accident.Dayweek,
        time: accident.Time,
        crashType: accident.CrashType,
        fatalities: accident.NumberFatalities,
        speedLimit: accident.SpeedLimit
      };
    })}