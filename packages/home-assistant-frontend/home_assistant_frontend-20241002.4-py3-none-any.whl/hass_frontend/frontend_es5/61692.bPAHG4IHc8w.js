(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[61692],{58975:function(t,e,n){"use strict";var r;n(39790),n(7760),n(29152),(r="undefined"!=typeof process&&"[object process]"==={}.toString.call(process)||"undefined"!=typeof navigator&&"ReactNative"===navigator.product?global:self).Proxy||(r.Proxy=n(67899)(),r.Proxy.revocable=r.Proxy.revocable)},67899:function(t,e,n){var r=n(22711).default;n(71499),n(18193),n(54774),n(25734),n(62635),n(53940),n(60682),n(39790),n(253),n(54846),n(66555),t.exports=function(){var t,e=null;function n(t){return!!t&&("object"===r(t)||"function"==typeof t)}function o(t){if(null!==t&&!n(t))throw new TypeError("Object prototype may only be an Object or null: "+t)}var u=Object,i=Boolean(u.create)||!({__proto__:null}instanceof u),c=u.create||(i?function(t){return o(t),{__proto__:t}}:function(t){if(o(t),null===t)throw new SyntaxError("Native Object.create is required to create objects with null prototype");var e=function(){};return e.prototype=t,new e}),a=function(){return null},f=u.getPrototypeOf||([].__proto__===Array.prototype?function(t){var e=t.__proto__;return n(e)?e:null}:a);return t=function(r,l){if(void 0===(this&&this instanceof t?this.constructor:void 0))throw new TypeError("Constructor Proxy requires 'new'");if(!n(r)||!n(l))throw new TypeError("Cannot create proxy with a non-object as target or handler");var s=function(){};e=function(){r=null,s=function(t){throw new TypeError("Cannot perform '".concat(t,"' on a proxy that has been revoked"))}},setTimeout((function(){e=null}),0);var p=l;for(var y in l={get:null,set:null,apply:null,construct:null},p){if(!(y in l))throw new TypeError("Proxy polyfill does not support trap '".concat(y,"'"));l[y]=p[y]}"function"==typeof p&&(l.apply=p.apply.bind(p));var b,d=f(r),v=!1,h=!1;"function"==typeof r?(b=function(){var t=this&&this.constructor===b,e=Array.prototype.slice.call(arguments);return s(t?"construct":"apply"),t&&l.construct?l.construct.call(this,r,e):!t&&l.apply?l.apply(r,this,e):t?(e.unshift(r),new(r.bind.apply(r,e))):r.apply(this,e)},v=!0):r instanceof Array?(b=[],h=!0):b=i||null!==d?c(d):{};var _=l.get?function(t){return s("get"),l.get(this,t,b)}:function(t){return s("get"),this[t]},g=l.set?function(t,e){s("set");l.set(this,t,e,b)}:function(t,e){s("set"),this[t]=e},w=u.getOwnPropertyNames(r),m={};w.forEach((function(t){if(!v&&!h||!(t in b)){var e=u.getOwnPropertyDescriptor(r,t),n={enumerable:Boolean(e.enumerable),get:_.bind(r,t),set:g.bind(r,t)};u.defineProperty(b,t,n),m[t]=!0}}));var x=!0;if(v||h){var P=u.setPrototypeOf||([].__proto__===Array.prototype?function(t,e){return o(e),t.__proto__=e,t}:a);d&&P(b,d)||(x=!1)}if(l.get||!x)for(var j in r)m[j]||u.defineProperty(b,j,{get:_.bind(r,j)});return u.seal(r),u.seal(b),b},t.revocable=function(n,r){return{proxy:new t(n,r),revoke:e}},t}},22711:function(t,e,n){function r(e){return t.exports=r="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},t.exports.__esModule=!0,t.exports.default=t.exports,r(e)}n(42942),n(48062),n(67336),n(95737),n(39790),n(99019),n(96858),t.exports=r,t.exports.__esModule=!0,t.exports.default=t.exports},60682:function(t,e,n){"use strict";var r=n(41765),o=n(26887),u=n(18414).onFreeze,i=n(41927),c=n(26906),a=Object.seal;r({target:"Object",stat:!0,forced:c((function(){a(1)})),sham:!i},{seal:function(t){return a&&o(t)?a(u(t)):t}})},29152:function(t,e,n){"use strict";var r=n(41765),o=n(21621),u=n(14349),i=n(70501),c=TypeError,a=Object.defineProperty,f=o.self!==o;try{if(i){var l=Object.getOwnPropertyDescriptor(o,"self");!f&&l&&l.get&&l.enumerable||u(o,"self",{get:function(){return o},set:function(t){if(this!==o)throw new c("Illegal invocation");a(o,"self",{value:t,writable:!0,configurable:!0,enumerable:!0})},configurable:!0,enumerable:!0})}else r({global:!0,simple:!0,forced:f},{self:o})}catch(s){}},75702:function(t,e,n){"use strict";n.d(e,{IU:function(){return f},Jt:function(){return c},Yd:function(){return o},hZ:function(){return a},y$:function(){return u}});var r;n(658),n(95737),n(97741),n(89655),n(39790),n(66457),n(99019),n(253),n(54846),n(16891),n(66555),n(96858);function o(t){return new Promise((function(e,n){t.oncomplete=t.onsuccess=function(){return e(t.result)},t.onabort=t.onerror=function(){return n(t.error)}}))}function u(t,e){var n=indexedDB.open(t);n.onupgradeneeded=function(){return n.result.createObjectStore(e)};var r=o(n);return function(t,n){return r.then((function(r){return n(r.transaction(e,t).objectStore(e))}))}}function i(){return r||(r=u("keyval-store","keyval")),r}function c(t){return(arguments.length>1&&void 0!==arguments[1]?arguments[1]:i())("readonly",(function(e){return o(e.get(t))}))}function a(t,e){return(arguments.length>2&&void 0!==arguments[2]?arguments[2]:i())("readwrite",(function(n){return n.put(e,t),o(n.transaction)}))}function f(){return(arguments.length>0&&void 0!==arguments[0]?arguments[0]:i())("readwrite",(function(t){return t.clear(),o(t.transaction)}))}}}]);
//# sourceMappingURL=61692.bPAHG4IHc8w.js.map