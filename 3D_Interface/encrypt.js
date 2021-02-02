var aesjs = require('aes-js');
const utf8 = require('utf8');
var key = [139, 190, 60, 202, 65, 17, 46, 241, 173, 243, 170, 221, 190, 150, 115, 6];

export function decrypt(data) {

    try {
        var iv = data.slice(0, 16)
        var cipher = data.slice(16, data.length)
        var aesofb = new aesjs.ModeOfOperation.ofb(key, iv);
        var decryptedBytes = aesofb.decrypt(cipher);
    } catch {
        console.log('decryption error')
    }
    return decryptedBytes
}

export function encryptString(data) {
    
    try{
        var iv = new Uint8Array([ 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,35, 36 ]);
        var aesofb = new aesjs.ModeOfOperation.ofb(key, iv);
        var Bytes = aesjs.utils.utf8.toBytes(data);
        var encryptedBytes = aesofb.encrypt(Bytes);
    }catch(e){
        console.log('encryption error', e)
    }

    var concat = new Uint8Array(iv.length + encryptedBytes.length)
    concat.set(iv)
    concat.set(encryptedBytes, iv.length)
    return concat
}

export function decryptString(data){
    return new TextDecoder().decode(decrypt(data))
}