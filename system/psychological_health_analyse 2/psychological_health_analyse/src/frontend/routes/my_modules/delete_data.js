const line_reader = require('readline')
const fs = require('fs')

/*
 * 可以使用偏函数来进行优化
*/

// callback 的参数是 data
var delete_flight = (item,callback) => {
  item = item.replace(/\n/g,"").replace(/\s/g,"")
  //console.log(item);
  let flights = ""
  let flag = false
  let flights_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/flights.csv')
  });

  flights_reader.on('line', function (line) {
      let temp = line.replace(/\n/g,"").replace(/\s/g,"")
      if(temp != item){
          //console.log(temp)
          flights += line
          flights += "\n"
      }
      else{
          flag = true
          //console.log("11111111111111111111111111")
      }
  });

  flights_reader.on('close',() => {
      if(flag === true){
          fs.writeFile(__dirname+'/../../data/flights.csv',flights,(err) => {
              if(err)
                  console.log(err)
              callback(flag)
          })
      }
      else
        callback(flag)
  })
}

// callback 的参数是 data
var delete_slot = (item,callback) => {
  item = item.replace(/\n/g,"").replace(/\s/g,"")
  //console.log(item);
  let slots = ""
  let flag = false
  let slots_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/slots.csv')
  });

  slots_reader.on('line', function (line) {
      let temp = line.replace(/\n/g,"").replace(/\s/g,"")
      if(temp != item){
          //console.log(temp)
          slots += line
          slots += "\n"
      }
      else{
          flag = true
          //console.log("11111111111111111111111111")
      }
  });

  slots_reader.on('close',() => {
      if(flag === true){
          fs.writeFile(__dirname+'/../../data/slots.csv',slots,(err) => {
              if(err)
                  console.log(err)
              callback(flag)
          })
      }
      else
        callback(flag)
  })
}



// callback 的参数是 data
var delete_airline = (item,callback) => {
  item = item.replace(/\n/g,"").replace(/\s/g,"")
  //console.log(item);
  let airlines = ""
  let flag = false
  let airlines_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/airlines.csv')
  });

  airlines_reader.on('line', function (line) {
      let temp = line.replace(/\n/g,"").replace(/\s/g,"")
      if(temp != item){
          //console.log(temp)
          airlines += line
          airlines += "\n"
      }
      else{
          flag = true
          //console.log("11111111111111111111111111")
      }
  });

  airlines_reader.on('close',() => {
      if(flag === true){
          fs.writeFile(__dirname+'/../../data/airlines.csv',airlines,(err) => {
              if(err)
                  console.log(err)
              callback(flag)
          })
      }
      else
        callback(flag)
  })
}

var delete_track = (item,callback) => {
  item = item.replace(/\n/g,"").replace(/\s/g,"")
  //console.log(item);
  let tracks = ""
  let flag = false
  let tracks_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/tracks.csv')
  });

  tracks_reader.on('line', function (line) {
      let temp = line.replace(/\n/g,"").replace(/\s/g,"")
      if(temp != item){
          //console.log(temp)
          tracks += line
          tracks += "\n"
      }
      else{
          flag = true
          //console.log("11111111111111111111111111")
      }
  });

  tracks_reader.on('close',() => {
      if(flag === true){
          fs.writeFile(__dirname+'/../../data/tracks.csv',tracks,(err) => {
              if(err)
                  console.log(err)
              callback(flag)
          })
      }
      else
        callback(flag)
  })
}

var delete_task_type = (item,callback) => {
  item = item.replace(/\n/g,"").replace(/\s/g,"")
  //console.log(item);
  let task_types = ""
  let flag = false
  let task_types_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/task_types.csv')
  });

  task_types_reader.on('line', function (line) {
      let temp = line.replace(/\n/g,"").replace(/\s/g,"")
      if(temp != item){
          //console.log(temp)
          task_types += line
          task_types += "\n"
      }
      else{
          flag = true
          //console.log("11111111111111111111111111")
      }
  });

  task_types_reader.on('close',() => {
      if(flag === true){
          fs.writeFile(__dirname+'/../../data/task_types.csv',task_types,(err) => {
              if(err)
                  console.log(err)
              callback(flag)
          })
      }
      else
        callback(flag)
  })
}


var delete_aircraft_type = (item,callback) => {
  item = item.replace(/\n/g,"").replace(/\s/g,"")
  //console.log(item);
  let aircraft_types = ""
  let flag = false
  let aircraft_types_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/aircraft_types.csv')
  });

  aircraft_types_reader.on('line', function (line) {
      let temp = line.replace(/\n/g,"").replace(/\s/g,"")
      if(temp != item){
          //console.log(temp)
          aircraft_types += line
          aircraft_types += "\n"
      }
      else{
          flag = true
          //console.log("11111111111111111111111111")
      }
  });

  aircraft_types_reader.on('close',() => {
      if(flag === true){
          fs.writeFile(__dirname+'/../../data/aircraft_types.csv',aircraft_types,(err) => {
              if(err)
                  console.log(err)
              callback(flag)
          })
      }
      else
        callback(flag)
  })
}

module.exports.delete_flight = delete_flight
module.exports.delete_slot = delete_slot
module.exports.delete_airline = delete_airline
module.exports.delete_track = delete_track
module.exports.delete_task_type = delete_task_type
module.exports.delete_aircraft_type = delete_aircraft_type
