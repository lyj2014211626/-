var express = require('express');
var router = express.Router();
const toshow = require('./toshow')
// Get Homepage
router.get('/', ensureAuthenticated, function(req, res){
	res.render('classfy',{layout:"layout-blank",data_f:toshow.alg_data_f, data_z:toshow.alg_data_z,filename:"knn.json",img_path1:"SPG.png",img_path2:"SPGPG.png",img_path3:"SPGCG.png",img_path4:"SPGMGCG.png"});
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
