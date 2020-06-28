

function WSocket(url, notifier) {
    (this.__ws = new WebSocket("ws://"+ url)).holder = this;
    this.__ws.onmessage = (notifier || {}).onmessage;
    this.__ws.onerror = (notifier || {}).onerror;

    if("undefined" != typeof WSocket.__init__) return;

    WSocket.prototype.post = function(msg) {
        if(1 != this.__ws.readyState) return;
        this.__ws.send(msg);
        return this.__ws.bufferedAmount;
    }

    WSocket.prototype.keepAlive = function() {
        this.__ws.onclose = function() { WSocket.call(this.holder, url, notifier); this.holder.keepAlive(); }
    }

    WSocket.__init__ = true;
}