"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[16204],{77226:function(e,t,r){r.d(t,{A:function(){return i}});r(71499),r(28552),r(36016),r(55228),r(43037);var a=function(e){var t=parseFloat(e);if(isNaN(t))throw new Error("".concat(e," is not a number"));return t};function i(e){if(!e)return null;try{if(e.endsWith("%"))return{w:100,h:a(e.substr(0,e.length-1))};var t=e.replace(":","x").split("x");return 0===t.length?null:1===t.length?{w:a(t[0]),h:1}:{w:a(t[0]),h:a(t[1])}}catch(r){}return null}},65619:function(e,t,r){var a,i,n,s,o,d,l,c=r(33994),h=r(22858),u=r(64599),v=r(35806),f=r(71008),k=r(62193),p=r(2816),y=r(27927),m=r(35890),_=(r(81027),r(15112)),g=r(29818),b=r(33922),A=r(19244),w=r(42496),E=r(88800),I=(r(62745),r(39790),r(66457),r(253),r(54846),r(66555),r(34897)),x=function(){var e=(0,h.A)((0,c.A)().mark((function e(t){return(0,c.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",t.callWS({type:"rtsp_to_webrtc/get_settings"}));case 1:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}();r(13292),(0,y.A)([(0,g.EM)("ha-web-rtc-player")],(function(e,t){var r,s,o=function(t){function r(){var t;(0,f.A)(this,r);for(var a=arguments.length,i=new Array(a),n=0;n<a;n++)i[n]=arguments[n];return t=(0,k.A)(this,r,[].concat(i)),e(t),t}return(0,p.A)(r,t),(0,v.A)(r)}(t);return{F:o,d:[{kind:"field",decorators:[(0,g.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,g.MZ)()],key:"entityid",value:void 0},{kind:"field",decorators:[(0,g.MZ)({type:Boolean,attribute:"controls"})],key:"controls",value:function(){return!1}},{kind:"field",decorators:[(0,g.MZ)({type:Boolean,attribute:"muted"})],key:"muted",value:function(){return!1}},{kind:"field",decorators:[(0,g.MZ)({type:Boolean,attribute:"autoplay"})],key:"autoPlay",value:function(){return!1}},{kind:"field",decorators:[(0,g.MZ)({type:Boolean,attribute:"playsinline"})],key:"playsInline",value:function(){return!1}},{kind:"field",decorators:[(0,g.MZ)()],key:"posterUrl",value:void 0},{kind:"field",decorators:[(0,g.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,g.P)("#remote-stream")],key:"_videoEl",value:void 0},{kind:"field",key:"_peerConnection",value:void 0},{kind:"field",key:"_remoteStream",value:void 0},{kind:"method",key:"render",value:function(){return this._error?(0,_.qy)(a||(a=(0,u.A)(['<ha-alert alert-type="error">',"</ha-alert>"])),this._error):(0,_.qy)(i||(i=(0,u.A)([' <video id="remote-stream" ?autoplay="','" .muted="','" ?playsinline="','" ?controls="','" .poster="','" @loadeddata="','"></video> '])),this.autoPlay,this.muted,this.playsInline,this.controls,this.posterUrl,this._loadedData)}},{kind:"method",key:"connectedCallback",value:function(){(0,m.A)(o,"connectedCallback",this,3)([]),this.hasUpdated&&this._startWebRtc()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,m.A)(o,"disconnectedCallback",this,3)([]),this._cleanUp()}},{kind:"method",key:"updated",value:function(e){e.has("entityid")&&this._videoEl&&this._startWebRtc()}},{kind:"method",key:"_startWebRtc",value:(s=(0,h.A)((0,c.A)().mark((function e(){var t,r,a,i,n,s,o,d,l,u,v=this;return(0,c.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._error=void 0,e.next=3,this._fetchPeerConfiguration();case 3:return t=e.sent,(r=new RTCPeerConnection(t)).createDataChannel("dataSendChannel"),r.addTransceiver("audio",{direction:"recvonly"}),r.addTransceiver("video",{direction:"recvonly"}),a={offerToReceiveAudio:!0,offerToReceiveVideo:!0},e.next=11,r.createOffer(a);case 11:return i=e.sent,e.next=14,r.setLocalDescription(i);case 14:return n="",s=new Promise((function(e){r.addEventListener("icecandidate",function(){var t=(0,h.A)((0,c.A)().mark((function t(r){var a;return(0,c.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(null!==(a=r.candidate)&&void 0!==a&&a.candidate){t.next=3;break}return e(),t.abrupt("return");case 3:n+="a=".concat(r.candidate.candidate,"\r\n");case 4:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}())})),e.next=18,s;case 18:return o=i.sdp+n,e.prev=19,e.next=22,(0,E.ey)(this.hass,this.entityid,o);case 22:d=e.sent,e.next=30;break;case 25:return e.prev=25,e.t0=e.catch(19),this._error="Failed to start WebRTC stream: "+e.t0.message,r.close(),e.abrupt("return");case 30:return l=new MediaStream,r.addEventListener("track",(function(e){l.addTrack(e.track),v._videoEl.srcObject=l})),this._remoteStream=l,u=new RTCSessionDescription({type:"answer",sdp:d.answer}),e.prev=34,e.next=37,r.setRemoteDescription(u);case 37:e.next=44;break;case 39:return e.prev=39,e.t1=e.catch(34),this._error="Failed to connect WebRTC stream: "+e.t1.message,r.close(),e.abrupt("return");case 44:this._peerConnection=r;case 45:case"end":return e.stop()}}),e,this,[[19,25],[34,39]])}))),function(){return s.apply(this,arguments)})},{kind:"method",key:"_fetchPeerConfiguration",value:(r=(0,h.A)((0,c.A)().mark((function e(){var t;return(0,c.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if((0,b.x)(this.hass,"rtsp_to_webrtc")){e.next=2;break}return e.abrupt("return",{});case 2:return e.next=4,x(this.hass);case 4:if((t=e.sent)&&t.stun_server){e.next=7;break}return e.abrupt("return",{});case 7:return e.abrupt("return",{iceServers:[{urls:["stun:".concat(t.stun_server)]}]});case 8:case"end":return e.stop()}}),e,this)}))),function(){return r.apply(this,arguments)})},{kind:"method",key:"_cleanUp",value:function(){this._remoteStream&&(this._remoteStream.getTracks().forEach((function(e){e.stop()})),this._remoteStream=void 0),this._videoEl&&(this._videoEl.removeAttribute("src"),this._videoEl.load()),this._peerConnection&&(this._peerConnection.close(),this._peerConnection=void 0)}},{kind:"method",key:"_loadedData",value:function(){(0,I.r)(this,"load")}},{kind:"get",static:!0,key:"styles",value:function(){return(0,_.AH)(n||(n=(0,u.A)([":host,video{display:block}video{width:100%;max-height:var(--video-max-height,calc(100vh - 97px))}"])))}}]}}),_.WF),(0,y.A)([(0,g.EM)("ha-camera-stream")],(function(e,t){var r,a,i=function(t){function r(){var t;(0,f.A)(this,r);for(var a=arguments.length,i=new Array(a),n=0;n<a;n++)i[n]=arguments[n];return t=(0,k.A)(this,r,[].concat(i)),e(t),t}return(0,p.A)(r,t),(0,v.A)(r)}(t);return{F:i,d:[{kind:"field",decorators:[(0,g.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,g.MZ)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,g.MZ)({type:Boolean,attribute:"controls"})],key:"controls",value:function(){return!1}},{kind:"field",decorators:[(0,g.MZ)({type:Boolean,attribute:"muted"})],key:"muted",value:function(){return!1}},{kind:"field",decorators:[(0,g.MZ)({type:Boolean,attribute:"allow-exoplayer"})],key:"allowExoPlayer",value:function(){return!1}},{kind:"field",decorators:[(0,g.wk)()],key:"_posterUrl",value:void 0},{kind:"field",decorators:[(0,g.wk)()],key:"_forceMJPEG",value:void 0},{kind:"field",decorators:[(0,g.wk)()],key:"_url",value:void 0},{kind:"field",decorators:[(0,g.wk)()],key:"_connected",value:function(){return!1}},{kind:"method",key:"willUpdate",value:function(e){var t;e.has("stateObj")&&!this._shouldRenderMJPEG&&this.stateObj&&(null===(t=e.get("stateObj"))||void 0===t?void 0:t.entity_id)!==this.stateObj.entity_id&&(this._getPosterUrl(),this.stateObj.attributes.frontend_stream_type===E.Ub&&(this._forceMJPEG=void 0,this._url=void 0,this._getStreamUrl()))}},{kind:"method",key:"connectedCallback",value:function(){(0,m.A)(i,"connectedCallback",this,3)([]),this._connected=!0}},{kind:"method",key:"disconnectedCallback",value:function(){(0,m.A)(i,"disconnectedCallback",this,3)([]),this._connected=!1}},{kind:"method",key:"render",value:function(){return this.stateObj?this._shouldRenderMJPEG?(0,_.qy)(s||(s=(0,u.A)(['<img .src="','" .alt="','">'])),this._connected?(0,E.CK)(this.stateObj):"","Preview of the ".concat((0,A.u)(this.stateObj)," camera.")):this.stateObj.attributes.frontend_stream_type===E.Ub?this._url?(0,_.qy)(o||(o=(0,u.A)(['<ha-hls-player autoplay playsinline .allowExoPlayer="','" .muted="','" .controls="','" .hass="','" .url="','" .posterUrl="','"></ha-hls-player>'])),this.allowExoPlayer,this.muted,this.controls,this.hass,this._url,this._posterUrl):_.s6:this.stateObj.attributes.frontend_stream_type===E.zS?(0,_.qy)(d||(d=(0,u.A)(['<ha-web-rtc-player autoplay playsinline .muted="','" .controls="','" .hass="','" .entityid="','" .posterUrl="','"></ha-web-rtc-player>'])),this.muted,this.controls,this.hass,this.stateObj.entity_id,this._posterUrl):_.s6:_.s6}},{kind:"get",key:"_shouldRenderMJPEG",value:function(){return this._forceMJPEG===this.stateObj.entity_id||(!(0,w.$)(this.stateObj,E.JT)||(this.stateObj.attributes.frontend_stream_type===E.zS?"undefined"==typeof RTCPeerConnection:!(0,b.x)(this.hass,"stream")))}},{kind:"method",key:"_getPosterUrl",value:(a=(0,h.A)((0,c.A)().mark((function e(){return(0,c.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,(0,E.C4)(this.hass,this.stateObj.entity_id,this.clientWidth,this.clientHeight);case 3:this._posterUrl=e.sent,e.next=9;break;case 6:e.prev=6,e.t0=e.catch(0),this._posterUrl=void 0;case 9:case"end":return e.stop()}}),e,this,[[0,6]])}))),function(){return a.apply(this,arguments)})},{kind:"method",key:"_getStreamUrl",value:(r=(0,h.A)((0,c.A)().mark((function e(){var t,r;return(0,c.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,(0,E.wv)(this.hass,this.stateObj.entity_id);case 3:t=e.sent,r=t.url,this._url=r,e.next=12;break;case 8:e.prev=8,e.t0=e.catch(0),console.error(e.t0),this._forceMJPEG=this.stateObj.entity_id;case 12:case"end":return e.stop()}}),e,this,[[0,8]])}))),function(){return r.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return(0,_.AH)(l||(l=(0,u.A)([":host,img{display:block}img{width:100%}"])))}}]}}),_.WF)},62745:function(e,t,r){var a,i,n,s,o=r(33994),d=r(22858),l=r(64599),c=r(35806),h=r(71008),u=r(62193),v=r(2816),f=r(27927),k=r(35890),p=(r(88871),r(81027),r(95737),r(39790),r(66457),r(36016),r(7760),r(99019),r(96858),r(84341),r(49365),r(38389),r(74860),r(71011),r(71174),r(15112)),y=r(29818),m=r(34897),_=r(61441);r(13292),(0,f.A)([(0,y.EM)("ha-hls-player")],(function(e,t){var f,g,b,A,w=function(t){function r(){var t;(0,h.A)(this,r);for(var a=arguments.length,i=new Array(a),n=0;n<a;n++)i[n]=arguments[n];return t=(0,u.A)(this,r,[].concat(i)),e(t),t}return(0,v.A)(r,t),(0,c.A)(r)}(t);return{F:w,d:[{kind:"field",decorators:[(0,y.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,y.MZ)()],key:"url",value:void 0},{kind:"field",decorators:[(0,y.MZ)()],key:"posterUrl",value:void 0},{kind:"field",decorators:[(0,y.MZ)({type:Boolean,attribute:"controls"})],key:"controls",value:function(){return!1}},{kind:"field",decorators:[(0,y.MZ)({type:Boolean,attribute:"muted"})],key:"muted",value:function(){return!1}},{kind:"field",decorators:[(0,y.MZ)({type:Boolean,attribute:"autoplay"})],key:"autoPlay",value:function(){return!1}},{kind:"field",decorators:[(0,y.MZ)({type:Boolean,attribute:"playsinline"})],key:"playsInline",value:function(){return!1}},{kind:"field",decorators:[(0,y.MZ)({type:Boolean,attribute:"allow-exoplayer"})],key:"allowExoPlayer",value:function(){return!1}},{kind:"field",decorators:[(0,y.P)("video")],key:"_videoEl",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"_errorIsFatal",value:function(){return!1}},{kind:"field",key:"_hlsPolyfillInstance",value:void 0},{kind:"field",key:"_exoPlayer",value:function(){return!1}},{kind:"field",static:!0,key:"streamCount",value:function(){return 0}},{kind:"method",key:"connectedCallback",value:function(){(0,k.A)(w,"connectedCallback",this,3)([]),w.streamCount+=1,this.hasUpdated&&(this._resetError(),this._startHls())}},{kind:"method",key:"disconnectedCallback",value:function(){(0,k.A)(w,"disconnectedCallback",this,3)([]),w.streamCount-=1,this._cleanUp()}},{kind:"method",key:"render",value:function(){return(0,p.qy)(a||(a=(0,l.A)([" "," "," "])),this._error?(0,p.qy)(i||(i=(0,l.A)(['<ha-alert alert-type="error" class="','"> '," </ha-alert>"])),this._errorIsFatal?"fatal":"retry",this._error):"",this._errorIsFatal?"":(0,p.qy)(n||(n=(0,l.A)(['<video .poster="','" ?autoplay="','" .muted="','" ?playsinline="','" ?controls="','" @loadeddata="','"></video>'])),this.posterUrl,this.autoPlay,this.muted,this.playsInline,this.controls,this._loadedData))}},{kind:"method",key:"updated",value:function(e){(0,k.A)(w,"updated",this,3)([e]),e.has("url")&&(this._cleanUp(),this._resetError(),this._startHls())}},{kind:"method",key:"_startHls",value:(A=(0,d.A)((0,o.A)().mark((function e(){var t,a,i,n,s,d,l,c,h,u;return(0,o.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a=fetch(this.url),e.next=3,Promise.all([r.e(72915),r.e(96860)]).then(r.bind(r,96860));case 3:if(i=e.sent.default,this.isConnected){e.next=6;break}return e.abrupt("return");case 6:if((n=i.isSupported())||(n=""!==this._videoEl.canPlayType("application/vnd.apple.mpegurl")),n){e.next=11;break}return this._setFatalError(this.hass.localize("ui.components.media-browser.video_not_supported")),e.abrupt("return");case 11:return s=this.allowExoPlayer&&(null===(t=this.hass.auth.external)||void 0===t?void 0:t.config.hasExoPlayer),e.next=14,a;case 14:return e.next=16,e.sent.text();case 16:if(d=e.sent,this.isConnected){e.next=19;break}return e.abrupt("return");case 19:c=(l=/#EXT-X-STREAM-INF:.*?(?:CODECS=".*?(hev1|hvc1)?\..*?".*?)?(?:\n|\r\n)(.+)/g).exec(d),h=l.exec(d),u=null!==c&&null===h?new URL(c[2],this.url).href:this.url,s&&null!==c&&void 0!==c[1]?this._renderHLSExoPlayer(u):i.isSupported()?this._renderHLSPolyfill(this._videoEl,i,u):this._renderHLSNative(this._videoEl,u);case 24:case"end":return e.stop()}}),e,this)}))),function(){return A.apply(this,arguments)})},{kind:"method",key:"_renderHLSExoPlayer",value:(b=(0,d.A)((0,o.A)().mark((function e(t){return(0,o.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._exoPlayer=!0,window.addEventListener("resize",this._resizeExoPlayer),this.updateComplete.then((function(){return(0,_.E)()})).then(this._resizeExoPlayer),this._videoEl.style.visibility="hidden",e.next=6,this.hass.auth.external.fireMessage({type:"exoplayer/play_hls",payload:{url:new URL(t,window.location.href).toString(),muted:this.muted}});case 6:case"end":return e.stop()}}),e,this)}))),function(e){return b.apply(this,arguments)})},{kind:"field",key:"_resizeExoPlayer",value:function(){var e=this;return function(){if(e._videoEl){var t=e._videoEl.getBoundingClientRect();e.hass.auth.external.fireMessage({type:"exoplayer/resize",payload:{left:t.left,top:t.top,right:t.right,bottom:t.bottom}})}}}},{kind:"method",key:"_isLLHLSSupported",value:function(){if(w.streamCount<=2)return!0;if(!("performance"in window)||0===performance.getEntriesByType("resource").length)return!1;var e=performance.getEntriesByType("resource")[0];return"nextHopProtocol"in e&&"h2"===e.nextHopProtocol}},{kind:"method",key:"_renderHLSPolyfill",value:(g=(0,d.A)((0,o.A)().mark((function e(t,r,a){var i,n=this;return(0,o.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:i=new r({backBufferLength:60,fragLoadingTimeOut:3e4,manifestLoadingTimeOut:3e4,levelLoadingTimeOut:3e4,maxLiveSyncPlaybackRate:2,lowLatencyMode:this._isLLHLSSupported()}),this._hlsPolyfillInstance=i,i.attachMedia(t),i.on(r.Events.MEDIA_ATTACHED,(function(){n._resetError(),i.loadSource(a)})),i.on(r.Events.FRAG_LOADED,(function(e,t){n._resetError()})),i.on(r.Events.ERROR,(function(e,t){if(t.fatal)if(t.type===r.ErrorTypes.NETWORK_ERROR){switch(t.details){case r.ErrorDetails.MANIFEST_LOAD_ERROR:var a="Error starting stream, see logs for details";void 0!==t.response&&void 0!==t.response.code&&(t.response.code>=500?a+=" (Server failure)":t.response.code>=400?a+=" (Stream never started)":a+=" ("+t.response.code+")"),n._setRetryableError(a);break;case r.ErrorDetails.MANIFEST_LOAD_TIMEOUT:n._setRetryableError("Timeout while starting stream");break;default:n._setRetryableError("Stream network error")}i.startLoad()}else t.type===r.ErrorTypes.MEDIA_ERROR?(n._setRetryableError("Error with media stream contents"),i.recoverMediaError()):n._setFatalError("Error playing stream")}));case 6:case"end":return e.stop()}}),e,this)}))),function(e,t,r){return g.apply(this,arguments)})},{kind:"method",key:"_renderHLSNative",value:(f=(0,d.A)((0,o.A)().mark((function e(t,r){return(0,o.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:t.src=r,t.addEventListener("loadedmetadata",(function(){t.play()}));case 2:case"end":return e.stop()}}),e)}))),function(e,t){return f.apply(this,arguments)})},{kind:"method",key:"_cleanUp",value:function(){this._hlsPolyfillInstance&&(this._hlsPolyfillInstance.destroy(),this._hlsPolyfillInstance=void 0),this._exoPlayer&&(window.removeEventListener("resize",this._resizeExoPlayer),this.hass.auth.external.fireMessage({type:"exoplayer/stop"}),this._exoPlayer=!1),this._videoEl&&(this._videoEl.removeAttribute("src"),this._videoEl.load())}},{kind:"method",key:"_resetError",value:function(){this._error=void 0,this._errorIsFatal=!1}},{kind:"method",key:"_setFatalError",value:function(e){this._error=e,this._errorIsFatal=!0}},{kind:"method",key:"_setRetryableError",value:function(e){this._error=e,this._errorIsFatal=!1}},{kind:"method",key:"_loadedData",value:function(){(0,m.r)(this,"load")}},{kind:"get",static:!0,key:"styles",value:function(){return(0,p.AH)(s||(s=(0,l.A)([":host,video{display:block}video{width:100%;max-height:var(--video-max-height,calc(100vh - 97px))}.fatal{display:block;padding:100px 16px}.retry{display:block}"])))}}]}}),p.WF)},9755:function(e,t,r){r.d(t,{e:function(){return a}});r(81027);var a=function(e){return"/api/image_proxy/".concat(e.entity_id,"?token=").concat(e.attributes.access_token,"&state=").concat(e.state)}},16204:function(e,t,r){var a,i,n,s,o,d,l=r(33994),c=r(22858),h=r(64599),u=r(35806),v=r(71008),f=r(62193),k=r(2816),p=r(27927),y=r(35890),m=(r(81027),r(13025),r(82386),r(82115),r(39790),r(36604),r(253),r(2075),r(15112)),_=r(29818),g=r(85323),b=r(63073),A=r(94872),w=r(213),E=r(77226),I=(r(65619),r(37629),r(88800)),x=r(9883),M=r(9755),C=function(e){return e[e.Loading=1]="Loading",e[e.Loaded=2]="Loaded",e[e.Error=3]="Error",e}(C||{});(0,p.A)([(0,_.EM)("hui-image")],(function(e,t){var r,p,S,O,P=function(t){function r(){var t;(0,v.A)(this,r);for(var a=arguments.length,i=new Array(a),n=0;n<a;n++)i[n]=arguments[n];return t=(0,f.A)(this,r,[].concat(i)),e(t),t}return(0,k.A)(r,t),(0,u.A)(r)}(t);return{F:P,d:[{kind:"field",decorators:[(0,_.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,_.MZ)()],key:"entity",value:void 0},{kind:"field",decorators:[(0,_.MZ)()],key:"image",value:void 0},{kind:"field",decorators:[(0,_.MZ)({attribute:!1})],key:"stateImage",value:void 0},{kind:"field",decorators:[(0,_.MZ)()],key:"cameraImage",value:void 0},{kind:"field",decorators:[(0,_.MZ)()],key:"cameraView",value:void 0},{kind:"field",decorators:[(0,_.MZ)()],key:"aspectRatio",value:void 0},{kind:"field",decorators:[(0,_.MZ)()],key:"filter",value:void 0},{kind:"field",decorators:[(0,_.MZ)({attribute:!1})],key:"stateFilter",value:void 0},{kind:"field",decorators:[(0,_.MZ)()],key:"darkModeImage",value:void 0},{kind:"field",decorators:[(0,_.MZ)()],key:"darkModeFilter",value:void 0},{kind:"field",decorators:[(0,_.MZ)()],key:"fitMode",value:void 0},{kind:"field",decorators:[(0,_.wk)()],key:"_imageVisible",value:function(){return!1}},{kind:"field",decorators:[(0,_.wk)()],key:"_loadState",value:void 0},{kind:"field",decorators:[(0,_.wk)()],key:"_cameraImageSrc",value:void 0},{kind:"field",decorators:[(0,_.wk)()],key:"_loadedImageSrc",value:void 0},{kind:"field",decorators:[(0,_.wk)()],key:"_lastImageHeight",value:void 0},{kind:"field",key:"_intersectionObserver",value:void 0},{kind:"field",key:"_cameraUpdater",value:void 0},{kind:"field",key:"_ratio",value:function(){return null}},{kind:"method",key:"connectedCallback",value:function(){(0,y.A)(P,"connectedCallback",this,3)([]),void 0===this._loadState&&(this._loadState=C.Loading),this.cameraImage&&"live"!==this.cameraView&&this._startIntersectionObserverOrUpdates()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,y.A)(P,"disconnectedCallback",this,3)([]),this._stopUpdateCameraInterval(),this._stopIntersectionObserver(),this._imageVisible=void 0}},{kind:"method",key:"handleIntersectionCallback",value:function(e){this._imageVisible=e[0].isIntersecting}},{kind:"method",key:"willUpdate",value:function(e){if(e.has("hass")){var t=e.get("hass");this._shouldStartCameraUpdates(t)?this._startIntersectionObserverOrUpdates():this.hass.connected||(this._stopUpdateCameraInterval(),this._stopIntersectionObserver(),this._loadState=C.Loading,this._cameraImageSrc=void 0,this._loadedImageSrc=void 0)}e.has("_imageVisible")&&(this._imageVisible?this._shouldStartCameraUpdates()&&this._startUpdateCameraInterval():this._stopUpdateCameraInterval()),e.has("aspectRatio")&&(this._ratio=this.aspectRatio?(0,E.A)(this.aspectRatio):null),this._loadState!==C.Loading||this.cameraImage||(this._loadState=C.Loaded)}},{kind:"method",key:"render",value:function(){if(!this.hass)return m.s6;var e,t,r=Boolean(this._ratio&&this._ratio.w>0&&this._ratio.h>0),d=this.entity?this.hass.states[this.entity]:void 0,l=d?d.state:x.Hh,c=!this.stateImage;if(this.cameraImage)"live"===this.cameraView?t=this.hass.states[this.cameraImage]:e=this._cameraImageSrc;else if(this.stateImage){var u=this.stateImage[l];u?e=u:(e=this.image,c=!0)}else e=this.darkModeImage&&this.hass.themes.darkMode?this.darkModeImage:d&&"image"===(0,w.m)(d.entity_id)?(0,M.e)(d):this.image;e&&(e=this.hass.hassUrl(e));var v=this.filter||"";(this.hass.themes.darkMode&&this.darkModeFilter&&(v+=this.darkModeFilter),this.stateFilter&&this.stateFilter[l]&&(v+=this.stateFilter[l]),!v&&this.entity)&&(v=(!d||A.jj.includes(l))&&c?"grayscale(100%)":"");return(0,m.qy)(a||(a=(0,h.A)([' <div style="','" class="container ','"> '," "," </div> "])),(0,b.W)({paddingBottom:r?"".concat((100*this._ratio.h/this._ratio.w).toFixed(2),"%"):void 0===this._lastImageHeight?"56.25%":void 0,backgroundImage:r&&this._loadedImageSrc?'url("'.concat(this._loadedImageSrc,'")'):void 0,filter:this._loadState===C.Loaded||"live"===this.cameraView?v:void 0}),(0,g.H)({ratio:r||void 0===this._lastImageHeight,contain:"contain"===this.fitMode,fill:"fill"===this.fitMode}),this.cameraImage&&"live"===this.cameraView?(0,m.qy)(i||(i=(0,h.A)([' <ha-camera-stream muted .hass="','" .stateObj="','" @load="','"></ha-camera-stream> '])),this.hass,t,this._onVideoLoad):void 0===e?m.s6:(0,m.qy)(n||(n=(0,h.A)([' <img id="image" src="','" @error="','" @load="','" style="','"> '])),e,this._onImageError,this._onImageLoad,(0,b.W)({display:r||this._loadState===C.Loaded?"block":"none"})),this._loadState===C.Error?(0,m.qy)(s||(s=(0,h.A)(['<div id="brokenImage" style="','"></div>'])),(0,b.W)({height:r?void 0:"".concat(this._lastImageHeight,"px")||0})):"live"===this.cameraView||void 0!==e&&this._loadState!==C.Loading?"":(0,m.qy)(o||(o=(0,h.A)(['<div class="progress-container" style="','"> <ha-circular-progress class="render-spinner" indeterminate size="small"></ha-circular-progress> </div>'])),(0,b.W)({height:r?void 0:"".concat(this._lastImageHeight,"px")||0})))}},{kind:"method",key:"_shouldStartCameraUpdates",value:function(e){return!(e&&e.connected===this.hass.connected||!this.hass.connected||"live"===this.cameraView)}},{kind:"method",key:"_startIntersectionObserverOrUpdates",value:function(){"IntersectionObserver"in window?(this._intersectionObserver||(this._intersectionObserver=new IntersectionObserver(this.handleIntersectionCallback.bind(this))),this._intersectionObserver.observe(this)):(this._imageVisible=!0,this._startUpdateCameraInterval())}},{kind:"method",key:"_stopIntersectionObserver",value:function(){this._intersectionObserver&&this._intersectionObserver.disconnect()}},{kind:"method",key:"_startUpdateCameraInterval",value:function(){var e=this;this._stopUpdateCameraInterval(),this._updateCameraImageSrc(),this.cameraImage&&this.isConnected&&(this._cameraUpdater=window.setInterval((function(){return e._updateCameraImageSrcAtInterval()}),1e4))}},{kind:"method",key:"_stopUpdateCameraInterval",value:function(){this._cameraUpdater&&(clearInterval(this._cameraUpdater),this._cameraUpdater=void 0)}},{kind:"method",key:"_onImageError",value:function(){this._loadState=C.Error}},{kind:"method",key:"_onImageLoad",value:(O=(0,c.A)((0,l.A)().mark((function e(t){var r;return(0,l.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._loadState=C.Loaded,r=t.target,this._ratio&&this._ratio.w>0&&this._ratio.h>0&&(this._loadedImageSrc=r.src),e.next=5,this.updateComplete;case 5:this._lastImageHeight=r.offsetHeight;case 6:case"end":return e.stop()}}),e,this)}))),function(e){return O.apply(this,arguments)})},{kind:"method",key:"_onVideoLoad",value:(S=(0,c.A)((0,l.A)().mark((function e(t){var r;return(0,l.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._loadState=C.Loaded,r=t.currentTarget,e.next=4,this.updateComplete;case 4:this._lastImageHeight=r.offsetHeight;case 5:case"end":return e.stop()}}),e,this)}))),function(e){return S.apply(this,arguments)})},{kind:"method",key:"_updateCameraImageSrcAtInterval",value:(p=(0,c.A)((0,l.A)().mark((function e(){return(0,l.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._loadState===C.Loading&&this._onImageError(),e.abrupt("return",this._updateCameraImageSrc());case 2:case"end":return e.stop()}}),e,this)}))),function(){return p.apply(this,arguments)})},{kind:"method",key:"_updateCameraImageSrc",value:(r=(0,c.A)((0,l.A)().mark((function e(){var t,r,a;return(0,l.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this.hass&&this.cameraImage){e.next=2;break}return e.abrupt("return");case 2:if(this.hass.states[this.cameraImage]){e.next=6;break}return this._onImageError(),e.abrupt("return");case 6:return t=this.clientWidth||640,r=Math.ceil(t*devicePixelRatio),this._lastImageHeight?a=Math.ceil(this._lastImageHeight*devicePixelRatio):this._ratio&&this._ratio.w>0&&this._ratio.h>0?a=Math.ceil(r*(this._ratio.h/this._ratio.w)):(r*=2,a=Math.ceil(.5625*r)),e.next=11,(0,I.C4)(this.hass,this.cameraImage,r,a);case 11:this._cameraImageSrc=e.sent,void 0===this._cameraImageSrc&&this._onImageError();case 13:case"end":return e.stop()}}),e,this)}))),function(){return r.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return(0,m.AH)(d||(d=(0,h.A)([':host{display:block}.container{transition:filter .2s linear;height:100%}img{display:block;height:100%;width:100%;object-fit:cover}.progress-container{display:flex;justify-content:center;align-items:center}.ratio{position:relative;width:100%;height:0;background-position:center;background-size:cover}.ratio.fill{background-size:100% 100%}.ratio.contain{background-size:contain;background-repeat:no-repeat}.fill img{object-fit:fill}.contain img{object-fit:contain}.ratio div,.ratio img{position:absolute;top:0;left:0;width:100%;height:100%}.ratio img{visibility:hidden}#brokenImage{background:grey url("/static/images/image-broken.svg") center/36px no-repeat}'])))}}]}}),m.WF)}}]);
//# sourceMappingURL=16204.Z-95eMbAQ4c.js.map