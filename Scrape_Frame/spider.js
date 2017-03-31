var page = require('webpage').create(), system = require('system');
page.open(system.args[1], function(status) {
  if(status === "success") {
    var fs = require('fs');
    var path = system.args[1].split("=")[1]+ '.html';
    // var timestamp = new Date().getTime();
    // var path = system.args[1].split("=")[1] + '-' + timestamp + '.html';
    var content = page.content;
    fs.write(path, content, 'w');
    phantom.exit(0);
    } else {
        phantom.exit(1);
    }
});