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
                values[name] = [{"time": item.expectedDepartureTime, "method":item.serviceJourney.line.transportMode, "num":item.serviceJourney.line.publicCode}]
            }
            else{
                values[name].push({"time": item.expectedDepartureTime, "method":item.serviceJourney.line.transportMode, "num":item.serviceJourney.line.publicCode})
            }
            //if (values[name] == undefined){
                //values.push({ key: name, value: item.aimedDepartureTime })
            //}

        })

        const header = document.createElement("h1")
        header.innerHTML = stopName
        document.body.appendChild(header)

        for (var key in values){
            const method = values[key][0].method
            var tableBody = document.getElementById(method);
            if (tableBody === null){
                tableBody = createTable(method)
            }
            console.log("ETF")
            const elem = document.createElement("tr");
            const k = document.createElement("td");
            const number = values[key][0].num
            const span = document.createElement("td")
            span.innerHTML = number
            k.innerHTML = key
            elem.appendChild(span);
            elem.appendChild(k);

            for (var i = 0; i < 4; i++){
                time = document.createElement("td");
                const val = values[key][i]
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

    function createTable(id){
        console.log("creating table hree")
        var table = document.createElement("table")
        const body = document.body.appendChild(table)
        table.setAttribute("id", "times")
        var tableBody = document.createElement("tbody");
        tableBody.setAttribute("id", id)
        table.appendChild(tableBody)
        const row = document.createElement("tr")
        const rute = document.createElement("th")
        rute.innerHTML = "Rute"
        rute.setAttribute("colspan", 2)
        const time = document.createElement("th")
        time.setAttribute("colspan", 4)
        time.innerHTML = "Minutter til Ankomst"
        tableBody.appendChild(rute)
        tableBody.appendChild(time)
        return tableBody
    }
}
