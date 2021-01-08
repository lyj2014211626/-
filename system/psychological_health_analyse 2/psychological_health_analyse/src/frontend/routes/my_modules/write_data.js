const fs = require('fs')

// callback 的参数是 data
var insert_flight = (flight) => {
      fs.appendFile(__dirname+'/../../data/flights.csv',flight,'utf-8',(err)=>{
          if(err)
              console.log(err)
      })
}

var insert_slot = (slot) => {
      fs.appendFile(__dirname+'/../../data/slots.csv',slot,'utf-8',(err)=>{
          if(err)
              console.log(err)
      })
}

var insert_airline = (airline) => {
      fs.appendFile(__dirname+'/../../data/airlines.csv',airline,'utf-8',(err)=>{
          if(err)
              console.log(err)
      })
}

var insert_track = (track) => {
      fs.appendFile(__dirname+'/../../data/tracks.csv',track,'utf-8',(err)=>{
          if(err)
              console.log(err)
      })
}

var insert_task_type = (task_type) => {
      fs.appendFile(__dirname+'/../../data/task_types.csv',task_type,'utf-8',(err)=>{
          if(err)
              console.log(err)
      })
}

var insert_aircraft_type = (aircraft_type) => {
      fs.appendFile(__dirname+'/../../data/aircraft_types.csv',aircraft_type,'utf-8',(err)=>{
          if(err)
              console.log(err)
      })
}
module.exports.insert_flight = insert_flight
module.exports.insert_slot = insert_slot
module.exports.insert_airline = insert_airline
module.exports.insert_track = insert_track
module.exports.insert_task_type = insert_task_type
module.exports.insert_aircraft_type = insert_aircraft_type
