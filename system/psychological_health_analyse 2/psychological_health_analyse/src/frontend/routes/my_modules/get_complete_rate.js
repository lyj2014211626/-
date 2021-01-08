const line_reader = require('readline')
const fs = require('fs')


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





//get_result((result)=>{console.log(result)})
module.exports.get_run_output_data = get_run_output_data
module.exports.get_result_data = get_result_data
