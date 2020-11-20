function getTimes(stopID, stopName, parentdiv) {
    console.log("gettim times for: ", stopName)
    const id = "NSR:StopPlace:59648"
    const query = `{
        stopPlace(id: "${stopID}") {
        name, 
        id
            estimatedCalls(numberOfDepartures: 200) {
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
         
        const data = stopPlaceData.data.stopPlace.estimatedCalls;
        console.log(data)
        data.forEach(item => {
            const name = item.destinationDisplay.frontText;
            if (values[name] === undefined){
                values[name] = [{"time": item.expectedDepartureTime, "method":item.serviceJourney.line.transportMode, "num":item.serviceJourney.line.publicCode}]
            }
            else{
                values[name].push({"time": item.expectedDepartureTime, "method":item.serviceJourney.line.transportMode, "num":item.serviceJourney.line.publicCode})
            }

        })
        


        for (var key in values){
            var method = values[key][0].method
            if (values[key][0].num.toString().length > 2 && method == "bus"){
                method = "longbus"
            }

            div = null
            var children = parentdiv.getElementsByTagName("div")
            for (var i = 0; i < children.length; i++){
                if (children[i].getAttribute("id") == stopName + " " + method){
                    div = children[i]
                }
            }
            if (div == null){
                console.log("creating div here")
                div = document.createElement("div")
                div.setAttribute("id", stopName + " " + method)
                parentdiv.appendChild(div)
                const header = document.createElement("h1")
                header.innerHTML = stopName + " " + method
                div.appendChild(header)
            }

            var tableBody = null

            children = div.getElementsByTagName("tbody")
            for (var i = 0; i < children.length; i++){
                if (children[i].getAttribute("id") == method){
                    tableBody = children[i]
                }
            }
            if (tableBody === null){
                tableBody = createTable(method, div)
            }
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

}
function createTable(id, div){
    var table = document.createElement("table")
    div.appendChild(table)
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

function getStop(stopName, parentdiv){
    const url = "https://api.entur.io/geocoder/v1/autocomplete?text="+stopName+"&lang=en"
    var ret = null
    fetch(url)
    .then(res => res.json())
    .then(data => data.features[0].properties)
    .then(data => {
        console.log(data)
        const headers = document.getElementsByTagName("h1")
        for (var i = 0; i < headers.length; i++){
            if (headers[i].innerText == data.name){
                return
            }
        }
        console.log(data.id, data.name, parentdiv)
        getTimes(data.id, data.name, parentdiv)
    })
}
