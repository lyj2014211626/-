var Memcached = require('memcached');
var memcached = new Memcached('127.0.0.1:11211');
  memcached.get('current_time', function (err, current_time) {
            console.log(current_time)
    });
