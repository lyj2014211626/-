const express = require('express');
const router = express.Router();
const eventproxy = require('eventproxy');
const get_data = require('../my_modules/get_data')

var ep = new eventproxy();
// Get Homepage
router.post('/', ensureAuthenticated, function(req, res){
    //console.log(req.body)
    get_data.get_run_output_data(req.body.filename,(items)=>{
			res.json(items)
		})
});


ep.all('tpl', 'data', function (tpl, data) { // or ep.all(['tpl', 'data'], function (tpl, data) {})
  // 在所有指定的事件触发后，将会被调用执行
  // 参数对应各自的事件名
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
