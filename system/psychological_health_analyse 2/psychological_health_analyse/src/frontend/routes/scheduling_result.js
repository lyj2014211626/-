const express = require('express');
const router = express.Router();
const get_data = require("./my_modules/get_data")


// Get Homepage
router.get('/', ensureAuthenticated, function(req, res){
	get_data.get_slots_data(function(slots_data){
		let head = slots_data.shift()
		res.render('scheduling_result',{
																layout:"layout-blank"
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
