// 功能：根据slots.csv和flights.csv文件产生 taxiway和 slots之间的关系
const line_reader = require('readline')
const fs = require('fs')


var genera_taxiway_slots_inter = (callback) => {
  let taxiway = []
  let slots = []
  let slots_info = []
  let slots_reader = line_reader.createInterface({
    input: fs.createReadStream(__dirname+'/../../data/slots.csv')
  });

  slots_reader.on('line', function (line) {
    //console.log('32211111111111111111');
    if(line.length !== 0){
        let temp_array = parse_slot(line)
        if(temp_array[0] !== "停机位"){
            slots.push(temp_array[0])
            slots_info[temp_array[0]] = temp_array
        }
        if(temp_array[3] !== "无限制" && temp_array[3] !== "滑行道"){
            if(taxiway.indexOf(temp_array[3]) === -1)
                taxiway[temp_array[3]] = []
        }
    }
  });

  slots_reader.on('close',() => {
    callback(taxiway,slots,slots_info)
  })
}



var parse_slot = (slot_info) => {
    return temp_array = slot_info.split(/\s/)
}


var callback = (taxiway,slots,slots_info) => {
    console.log('fffffffffffffffff')
    for(let i of slots){
        //console.log("$$$ "+i)
        if(slots_info[i][3] !== "无限制"){
            taxiway[slots_info[i][3]].push(i)
        }
        else {
            for(let j of taxiway){
                j.push(i)
            }
        }
    }
    let data = "滑行道 停机位\n"
    for(let i in taxiway){
        data += i
        data += " "
        for(let j of taxiway[i]){
            data += j
            data += ","
        }
        data = data.replace(/,$/g,'\n')
    }
    //console.log(data)
    fs.writeFileSync(__dirname+'/../../data/taxiways.csv',data)
    //console.log('11111111111111111');
}

var genera_taxiway_slots = (f)=>{
      genera_taxiway_slots_inter(callback)
      //console.log('///////////////');
      f()
}
genera_taxiway_slots_inter(callback)

module.exports.genera_taxiway_slots = genera_taxiway_slots
