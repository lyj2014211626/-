const express = require('express');
const router = express.Router();
const eventproxy = require('eventproxy');
const fs = require('fs')

var ep = new eventproxy();
// Get Homepage
router.post('/', ensureAuthenticated, function(req, res){

  fs.readFile(__dirname+"/../../../complete_file.txt",'utf-8', function (err, data) {
    if (err) {
      return console.error(err);
   }
      //console.log(data);
      //console.log(typeof data);
      data = data.split(',')
      result_data = {}
      result_data.complete_rate = data[0]/data[1]
      res.json(result_data)
    });
});


function ensureAuthenticated(req, res, next){
	if(req.isAuthenticated()){
		return next();
	} else {
		req.flash('error_msg','You are not logged in');
		res.redirect('/users/login');
	}
}

module.exports = router;
