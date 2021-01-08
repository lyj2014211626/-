const express = require('express');
const router = express.Router();
const get_data = require("./my_modules/get_data")
const toshow = require('./toshow')

// Get Homepage
router.get('/', ensureAuthenticated, function(req, res){
	console.log(req.query['sick']+'_'+req.query['path'])
	path=req.query['path']
	sick=req.query['sick']
	get_data.get_ASD_data(path,sick,function(airlines_data){
		let head = airlines_data.shift()
		res.render('asd',{
																head:head,
																airlines_data:airlines_data,
																
																layout:"layout-blank",
																data_f:toshow.alg_data_f,
																data_z:toshow.alg_data_z,

															});
	})
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
