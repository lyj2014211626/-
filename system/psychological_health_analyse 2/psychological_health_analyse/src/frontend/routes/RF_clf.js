var express = require('express');
var router = express.Router();
const toshow = require('./toshow')
// Get Homepage
router.get('/', ensureAuthenticated, function(req, res){

	res.render('RF_clf',{layout:"algorithms-layout-blank",data_f:toshow.alg_data_f,data_z:toshow.alg_data_z,filename:"RF.json",img_path:"RF.jpg"});
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
