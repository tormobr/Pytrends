function getTimes(stopID, stopName, methods) {

        
    const id = "NSR:StopPlace:59648"
    const query = `{
        stopPlace(id: "${stopID}") {
        name, 
        id
            estimatedCalls(numberOfDepartures: 30) {
          expectedDepartureTime
          aimedDepartureTime
          destinationDisplay {
            frontText
          }
          serviceJourney {
            line {
              publicCode
              transportMode
            }
          }
        }
      }
    }`
    console.log(query)
    var values = {}
    fetch('https://api.entur.io/journey-planner/v2/graphql', {
        method: 'POST',
        headers: {
            // Replace this with your own client name:
            'ET-Client-Name': 'Brandyberry',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query }),
    })
        .then(res => res.json())
        .then(stopPlaceData => {
        console.log(stopPlaceData);

        const data = stopPlaceData.data.stopPlace.estimatedCalls;
        data.forEach(item => {
            const name = item.destinationDisplay.frontText;
            if (values[name] === undefined){
                values[name] = [{"time": item.expectedDepartureTime, "method":item.serviceJourney.line.transportMode}]
            }
            else{
                values[name].push({"time": item.expectedDepartureTime, "method":item.serviceJourney.line.transportMode})
            }
            //if (values[name] == undefined){
                //values.push({ key: name, value: item.aimedDepartureTime })
            //}

        })

        for (var key in values){
            var tableBody = document.getElementById(values[key][0].method);
            const elem = document.createElement("tr");
            const k = document.createElement("td");
            const method = values[key][0].method
            k.innerHTML = key + "(" + method + ")";
            elem.appendChild(k);
            for (var i = 0; i < 4; i++){
                time = document.createElement("td");
                const val = values[key][i]
                console.log(key)
                if (val){
                    const minutes = (new Date(val.time).getTime() - Date.now()) / (1000 * 60)
                    time.innerHTML = minutes.toFixed(1)
                }
                else {
                    time.innerHTML = ""
                }
                elem.appendChild(time);
                tableBody.appendChild(elem)
            }

        }
    })
}
