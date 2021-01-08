const express = require('express');
const router = express.Router();
const fs = require('fs')

// Get Homepage
router.post('/', ensureAuthenticated, function(req, res){
    var pid = fs.readFileSync(__dirname+'/../../../backend/pid.txt','utf-8')
    try{
      if(process.kill(pid,'SIGPIPE') == true){
        res.json({status:'run'})
      }
    }catch(err){
      //console.log(err);
      console.log('the python process not start');
      res.json({status:'stop'})
    }
});

router.post('/update', ensureAuthenticated, function(req, res){
    console.log(req.body)

    if(req.body.status === 'run'){
      var exec = require('child_process').exec;
      var cmdStr = 'python '+__dirname+'/../../../backend/run.py';
      console.log(cmdStr);
      exec(cmdStr, function(err,stdout,stderr){
        if(err) {
            console.log('execute application error:'+stderr);
            res.end('failed')
        }
        else {
          res.end('ok')
        }
      });
    }

    if(req.body.status === 'stop'){
      var exec = require('child_process').exec;
      var pid = fs.readFileSync(__dirname+'/../../../backend/pid.txt','utf-8')
      process.kill(pid)
      //console.log(cmdStr);
      res.end('ok')

    }
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
