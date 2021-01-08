const express = require('express');
const router = express.Router();
const fs = require('fs')
const ini = require('ini')
const toshow = require('./toshow')
// Get Homepage
router.get('/', ensureAuthenticated, function(req, res){
	var config = ini.parse(fs.readFileSync(__dirname+'/../../backend/hyper_parameter.ini', 'utf-8'))
	var datax = {}
	datax.test_size = config.sys.test_size
	datax.i_time = config.sys.i_time
	datax.not_ig = config.evaluation_criterion.not_ig
	datax.ig_all = config.evaluation_criterion.ig_all
	datax.ig_01 = config.evaluation_criterion.ig_01
	datax.ig_10 = config.evaluation_criterion.ig_10
	datax.ig_23 = config.evaluation_criterion.ig_23
	datax.ig_12 = config.evaluation_criterion.ig_12
	datax.ig_13 = config.evaluation_criterion.ig_13
	// console.log(data);

	res.render('setting',{
															data:toshow.alg_data,
															datax:datax,
															layout:"layout-blank"
						});

});

router.post('/', ensureAuthenticated, function(req, res){
		//console.log(req.body);
		//console.log(req.body)
		var config = ini.parse(fs.readFileSync(__dirname+'/../../backend/hyper_parameter.ini', 'utf-8'))
		console.log(req.body)
		//console.log(req.body);
		config.sys.test_size = req.body.test_size
		config.sys.i_time = req.body.i_time
		config.evaluation_criterion.not_ig = req.body.not_ig
		config.evaluation_criterion.ig_all = req.body.ig_all
		config.evaluation_criterion.ig_01 = req.body.ig_01
		config.evaluation_criterion.ig_10 = req.body.ig_10
		config.evaluation_criterion.ig_23 = req.body.ig_23
		config.evaluation_criterion.ig_12 = req.body.ig_12
		config.evaluation_criterion.ig_13 = req.body.ig_13
		fs.writeFileSync(__dirname+'/../../backend/hyper_parameter.ini', ini.stringify(config))
		req.flash('success_msg','设置成功!');
		res.redirect("/setting")
    //res.end(flight)
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
