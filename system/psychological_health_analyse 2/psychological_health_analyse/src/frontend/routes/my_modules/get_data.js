const line_reader = require('readline')
const fs = require('fs')
const genera_taxiway_slots = require('./genera_taxiway_slots')
const Memcached = require('memcached');



var get_SVM_data = (callback) => {
  let airlines = []
  let airlines_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/SVM.csv')
  });

  airlines_reader.on('line', function (line) {
    if(line.length !== 0)
      airlines.push(parse_airline(line))
  });

  airlines_reader.on('close',() => {

    callback(airlines)
  })
}
var get_DT_data = (callback) => {
  let airlines = []
  let airlines_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/DT.csv')
  });

  airlines_reader.on('line', function (line) {
    if(line.length !== 0)
      airlines.push(parse_airline(line))
  });

  airlines_reader.on('close',() => {

    callback(airlines)
  })
}

var get_ASD_data = (path,sick, callback) => {
  let airlines = []
  let airlines_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/'+path+'/'+sick+'_'+path+'.csv')
  });

  airlines_reader.on('line', function (line) {
    if(line.length !== 0)
      airlines.push(parse_airline(line))
  });

  airlines_reader.on('close',() => {

    callback(airlines)
  })
}
var get_gene_data = (model,sick, callback) => {
  let airlines = []
  let airlines_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/'+model+'_'+sick+'.csv')
  });

  airlines_reader.on('line', function (line) {
    if(line.length !== 0)
      airlines.push(parse_airline(line))
  });

  airlines_reader.on('close',() => {

    callback(airlines)
  })
}
var get_RF_data = (callback) => {
  let airlines = []
  let airlines_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/RF.csv')
  });

  airlines_reader.on('line', function (line) {
    if(line.length !== 0)
      airlines.push(parse_airline(line))
  });

  airlines_reader.on('close',() => {

    callback(airlines)
  })
}

var get_xgboost_data = (callback) => {
  let airlines = []
  let airlines_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/xgboost.csv')
  });

  airlines_reader.on('line', function (line) {
    if(line.length !== 0)
      airlines.push(parse_airline(line))
  });

  airlines_reader.on('close',() => {

    callback(airlines)
  })
}

var get_stacking_data = (callback) => {
  let airlines = []
  let airlines_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/stacking.csv')
  });

  airlines_reader.on('line', function (line) {
    if(line.length !== 0)
      airlines.push(parse_airline(line))
  });

  airlines_reader.on('close',() => {

    callback(airlines)
  })
}

var get_flights_data = (callback) => {
  let index = 0
  let flights = []
  console.log(__dirname);
  let flights_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/SVM.csv')
  });

  flights_reader.on('line', function (line) {
      if(line.length !== 0){
      flights.push(parse_flight(line,index))
      index++
    }
  });

  flights_reader.on('close',() => {
    callback(flights)
  })
}

var parse_flight = (flights_info,index) => {
    if(index !== 0){
      let result = []
      let temp_array = flights_info.split(/\s/)
      result[0] = temp_array[0]
      result[1] = temp_array[1]
      result[2] = temp_array[2] + " " + temp_array[3]
      result[3] = temp_array[4] + " " + temp_array[5]
      result[4] = temp_array[6]
      result[5] = temp_array[7]
      result[6] = temp_array[8]
      result[7] = temp_array[9]
      return result
    }
    else
      return flights_info.split(/\s/)
}
// callback 的参数是 data
var get_run_output_data = (filename,callback) => {
  let index = 0
  let items = []
  let items_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/'+filename)
  });

  items_reader.on('line', function (line) {
      if(line.length !== 0){
      items.push(parse_item(line,index))
      index++
    }
  });

  items_reader.on('close',() => {
    callback(items)
  })
}

var parse_item = (item) => {
    return  JSON.parse(item)
}

var get_airlines_data = (callback) => {
  let airlines = []
  let airlines_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/svm.csv')
  });

  airlines_reader.on('line', function (line) {
    if(line.length !== 0)
      airlines.push(parse_airline(line))
  });

  airlines_reader.on('close',() => {

    callback(airlines)
  })
}

var get_result_data = (filename,page,callback) => {
  let index = 0
  let items = []
  filename = filename.replace('.json','')
  real_filename = __dirname+'/../../../output_data/'+filename+'/'+filename+page+'.csv'
  let items_reader = line_reader.createInterface({
    input: fs.createReadStream(real_filename)
  });

  items_reader.on('line', function (line) {
      if(line.length !== 0){
      items.push(parse_result(line,index))
      index++
    }
  });

  items_reader.on('close',() => {
    callback(items)
  })
}

var parse_item = (item) => {
    return  JSON.parse(item)
}

var parse_result = (item) => {
    return  item.split(',')
}

/*
var get_unallocated_flight = (callback) => {
  var memcached = new Memcached('127.0.0.1:11211');
  memcached.get('unallocated_flight', function (err, datax){
    //console.log(typeof datax)
    datax = datax.split(',')
    datax.push('进港航班号')
    //console.log(datax)
    let index = 0
    let flights = []
    let flights_reader = line_reader.createInterface({
      input: fs.createReadStream(__dirname+'/../../data/flights.csv')
    });

    flights_reader.on('line', function (line) {
        if(line.length !== 0){
        parsed_flight = parse_flight(line,index)
        //console.log(parsed_flight);
        for(i of datax){
          //console.log(parsed_flight[1]+' '+i)

          if(parsed_flight[1] === i){

            flights.push(parsed_flight)
          }
        }
        index++
      }
    });

    flights_reader.on('close',() => {
      callback(flights)
    })
  })
}
*/


var parse_airline = (airline_info) => {
    return temp_array = airline_info.split("#")
}


//get_result((result)=>{console.log(result)})
module.exports.get_flights_data = get_flights_data
module.exports.get_run_output_data = get_run_output_data
module.exports.get_result_data = get_result_data
module.exports.get_airlines_data = get_airlines_data
module.exports.get_SVM_data = get_SVM_data
module.exports.get_DT_data = get_DT_data
module.exports.get_ASD_data = get_ASD_data
module.exports.get_gene_data = get_gene_data
module.exports.get_RF_data = get_RF_data
module.exports.get_xgboost_data = get_xgboost_data
module.exports.get_stacking_data = get_stacking_data