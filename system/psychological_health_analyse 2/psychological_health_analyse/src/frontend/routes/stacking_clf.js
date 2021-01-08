var express = require('express');
var router = express.Router();
const toshow = require('./toshow')
// Get Homepage
router.get('/', ensureAuthenticated, function(req, res){

	res.render('stacking_clf',{layout:"algorithms-layout-blank",data_f:toshow.alg_data_f,data_z:toshow.alg_data_z,filename:"stacking.json",img_path:"stacking.jpg"});
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
