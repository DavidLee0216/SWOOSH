const request = require('request'); // ���Jrequest�Ҳ�

request({
    url: 'http://104.196.179.255:5000/timeline/',
    json: true
}, (error, response, body) => {
    var result = JSON.stringify(body, undefined, 2);
    console.log("123" + result); // body�O�^�Ǫ�json����A�ϥ�JSON.stringify()�ରjson�r��
    //result.
    });