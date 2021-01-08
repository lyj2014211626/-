var express = require('express');
var router = express.Router();
const toshow = require('./toshow')
// Get Homepage
router.get('/', ensureAuthenticated, function(req, res){
	res.render('',{layout:"analysis",data_f:toshow.alg_data_f,data_z:toshow.alg_data_z,img_path1:"K2_reve_delGW.png",img_path2:"delGW.png",img_path3:"K2_reve_addGW.png",img_path4:"addGW.png"});
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
