/*! For license information please see 20288.SZMZHuFotcY.js.LICENSE.txt */
export const id=20288;export const ids=[20288];export const modules={5884:(t,e,n)=>{n.d(e,{Q1:()=>F});n(16891);function o(t){return t+.5|0}const r=(t,e,n)=>Math.max(Math.min(t,n),e);function i(t){return r(o(2.55*t),0,255)}function a(t){return r(o(255*t),0,255)}function s(t){return r(o(t/2.55)/100,0,1)}function c(t){return r(o(100*t),0,100)}const l={0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,A:10,B:11,C:12,D:13,E:14,F:15,a:10,b:11,c:12,d:13,e:14,f:15},f=[..."0123456789ABCDEF"],u=t=>f[15&t],h=t=>f[(240&t)>>4]+f[15&t],d=t=>(240&t)>>4==(15&t);function g(t){var e=(t=>d(t.r)&&d(t.g)&&d(t.b)&&d(t.a))(t)?u:h;return t?"#"+e(t.r)+e(t.g)+e(t.b)+((t,e)=>t<255?e(t):"")(t.a,e):void 0}const p=/^(hsla?|hwb|hsv)\(\s*([-+.e\d]+)(?:deg)?[\s,]+([-+.e\d]+)%[\s,]+([-+.e\d]+)%(?:[\s,]+([-+.e\d]+)(%)?)?\s*\)$/;function b(t,e,n){const o=e*Math.min(n,1-n),r=(e,r=(e+t/30)%12)=>n-o*Math.max(Math.min(r-3,9-r,1),-1);return[r(0),r(8),r(4)]}function y(t,e,n){const o=(o,r=(o+t/60)%6)=>n-n*e*Math.max(Math.min(r,4-r,1),0);return[o(5),o(3),o(1)]}function x(t,e,n){const o=b(t,1,.5);let r;for(e+n>1&&(r=1/(e+n),e*=r,n*=r),r=0;r<3;r++)o[r]*=1-e-n,o[r]+=e;return o}function m(t){const e=t.r/255,n=t.g/255,o=t.b/255,r=Math.max(e,n,o),i=Math.min(e,n,o),a=(r+i)/2;let s,c,l;return r!==i&&(l=r-i,c=a>.5?l/(2-r-i):l/(r+i),s=function(t,e,n,o,r){return t===r?(e-n)/o+(e<n?6:0):e===r?(n-t)/o+2:(t-e)/o+4}(e,n,o,l,r),s=60*s+.5),[0|s,c||0,a]}function v(t,e,n,o){return(Array.isArray(e)?t(e[0],e[1],e[2]):t(e,n,o)).map(a)}function w(t,e,n){return v(b,t,e,n)}function M(t){return(t%360+360)%360}function k(t){const e=p.exec(t);let n,o=255;if(!e)return;e[5]!==n&&(o=e[6]?i(+e[5]):a(+e[5]));const r=M(+e[2]),s=+e[3]/100,c=+e[4]/100;return n="hwb"===e[1]?function(t,e,n){return v(x,t,e,n)}(r,s,c):"hsv"===e[1]?function(t,e,n){return v(y,t,e,n)}(r,s,c):w(r,s,c),{r:n[0],g:n[1],b:n[2],a:o}}const _={x:"dark",Z:"light",Y:"re",X:"blu",W:"gr",V:"medium",U:"slate",A:"ee",T:"ol",S:"or",B:"ra",C:"lateg",D:"ights",R:"in",Q:"turquois",E:"hi",P:"ro",O:"al",N:"le",M:"de",L:"yello",F:"en",K:"ch",G:"arks",H:"ea",I:"ightg",J:"wh"},O={OiceXe:"f0f8ff",antiquewEte:"faebd7",aqua:"ffff",aquamarRe:"7fffd4",azuY:"f0ffff",beige:"f5f5dc",bisque:"ffe4c4",black:"0",blanKedOmond:"ffebcd",Xe:"ff",XeviTet:"8a2be2",bPwn:"a52a2a",burlywood:"deb887",caMtXe:"5f9ea0",KartYuse:"7fff00",KocTate:"d2691e",cSO:"ff7f50",cSnflowerXe:"6495ed",cSnsilk:"fff8dc",crimson:"dc143c",cyan:"ffff",xXe:"8b",xcyan:"8b8b",xgTMnPd:"b8860b",xWay:"a9a9a9",xgYF:"6400",xgYy:"a9a9a9",xkhaki:"bdb76b",xmagFta:"8b008b",xTivegYF:"556b2f",xSange:"ff8c00",xScEd:"9932cc",xYd:"8b0000",xsOmon:"e9967a",xsHgYF:"8fbc8f",xUXe:"483d8b",xUWay:"2f4f4f",xUgYy:"2f4f4f",xQe:"ced1",xviTet:"9400d3",dAppRk:"ff1493",dApskyXe:"bfff",dimWay:"696969",dimgYy:"696969",dodgerXe:"1e90ff",fiYbrick:"b22222",flSOwEte:"fffaf0",foYstWAn:"228b22",fuKsia:"ff00ff",gaRsbSo:"dcdcdc",ghostwEte:"f8f8ff",gTd:"ffd700",gTMnPd:"daa520",Way:"808080",gYF:"8000",gYFLw:"adff2f",gYy:"808080",honeyMw:"f0fff0",hotpRk:"ff69b4",RdianYd:"cd5c5c",Rdigo:"4b0082",ivSy:"fffff0",khaki:"f0e68c",lavFMr:"e6e6fa",lavFMrXsh:"fff0f5",lawngYF:"7cfc00",NmoncEffon:"fffacd",ZXe:"add8e6",ZcSO:"f08080",Zcyan:"e0ffff",ZgTMnPdLw:"fafad2",ZWay:"d3d3d3",ZgYF:"90ee90",ZgYy:"d3d3d3",ZpRk:"ffb6c1",ZsOmon:"ffa07a",ZsHgYF:"20b2aa",ZskyXe:"87cefa",ZUWay:"778899",ZUgYy:"778899",ZstAlXe:"b0c4de",ZLw:"ffffe0",lime:"ff00",limegYF:"32cd32",lRF:"faf0e6",magFta:"ff00ff",maPon:"800000",VaquamarRe:"66cdaa",VXe:"cd",VScEd:"ba55d3",VpurpN:"9370db",VsHgYF:"3cb371",VUXe:"7b68ee",VsprRggYF:"fa9a",VQe:"48d1cc",VviTetYd:"c71585",midnightXe:"191970",mRtcYam:"f5fffa",mistyPse:"ffe4e1",moccasR:"ffe4b5",navajowEte:"ffdead",navy:"80",Tdlace:"fdf5e6",Tive:"808000",TivedBb:"6b8e23",Sange:"ffa500",SangeYd:"ff4500",ScEd:"da70d6",pOegTMnPd:"eee8aa",pOegYF:"98fb98",pOeQe:"afeeee",pOeviTetYd:"db7093",papayawEp:"ffefd5",pHKpuff:"ffdab9",peru:"cd853f",pRk:"ffc0cb",plum:"dda0dd",powMrXe:"b0e0e6",purpN:"800080",YbeccapurpN:"663399",Yd:"ff0000",Psybrown:"bc8f8f",PyOXe:"4169e1",saddNbPwn:"8b4513",sOmon:"fa8072",sandybPwn:"f4a460",sHgYF:"2e8b57",sHshell:"fff5ee",siFna:"a0522d",silver:"c0c0c0",skyXe:"87ceeb",UXe:"6a5acd",UWay:"708090",UgYy:"708090",snow:"fffafa",sprRggYF:"ff7f",stAlXe:"4682b4",tan:"d2b48c",teO:"8080",tEstN:"d8bfd8",tomato:"ff6347",Qe:"40e0d0",viTet:"ee82ee",JHt:"f5deb3",wEte:"ffffff",wEtesmoke:"f5f5f5",Lw:"ffff00",LwgYF:"9acd32"};let T;function P(t){T||(T=function(){const t={},e=Object.keys(O),n=Object.keys(_);let o,r,i,a,s;for(o=0;o<e.length;o++){for(a=s=e[o],r=0;r<n.length;r++)i=n[r],s=s.replace(i,_[i]);i=parseInt(O[a],16),t[s]=[i>>16&255,i>>8&255,255&i]}return t}(),T.transparent=[0,0,0,0]);const e=T[t.toLowerCase()];return e&&{r:e[0],g:e[1],b:e[2],a:4===e.length?e[3]:255}}const S=/^rgba?\(\s*([-+.\d]+)(%)?[\s,]+([-+.e\d]+)(%)?[\s,]+([-+.e\d]+)(%)?(?:[\s,/]+([-+.e\d]+)(%)?)?\s*\)$/;const R=t=>t<=.0031308?12.92*t:1.055*Math.pow(t,1/2.4)-.055,C=t=>t<=.04045?t/12.92:Math.pow((t+.055)/1.055,2.4);function j(t,e,n){if(t){let o=m(t);o[e]=Math.max(0,Math.min(o[e]+o[e]*n,0===e?360:1)),o=w(o),t.r=o[0],t.g=o[1],t.b=o[2]}}function I(t,e){return t?Object.assign(e||{},t):t}function A(t){var e={r:0,g:0,b:0,a:255};return Array.isArray(t)?t.length>=3&&(e={r:t[0],g:t[1],b:t[2],a:255},t.length>3&&(e.a=a(t[3]))):(e=I(t,{r:0,g:0,b:0,a:1})).a=a(e.a),e}function W(t){return"r"===t.charAt(0)?function(t){const e=S.exec(t);let n,o,a,s=255;if(e){if(e[7]!==n){const t=+e[7];s=e[8]?i(t):r(255*t,0,255)}return n=+e[1],o=+e[3],a=+e[5],n=255&(e[2]?i(n):r(n,0,255)),o=255&(e[4]?i(o):r(o,0,255)),a=255&(e[6]?i(a):r(a,0,255)),{r:n,g:o,b:a,a:s}}}(t):k(t)}class F{constructor(t){if(t instanceof F)return t;const e=typeof t;let n;var o,r,i;"object"===e?n=A(t):"string"===e&&(i=(o=t).length,"#"===o[0]&&(4===i||5===i?r={r:255&17*l[o[1]],g:255&17*l[o[2]],b:255&17*l[o[3]],a:5===i?17*l[o[4]]:255}:7!==i&&9!==i||(r={r:l[o[1]]<<4|l[o[2]],g:l[o[3]]<<4|l[o[4]],b:l[o[5]]<<4|l[o[6]],a:9===i?l[o[7]]<<4|l[o[8]]:255})),n=r||P(t)||W(t)),this._rgb=n,this._valid=!!n}get valid(){return this._valid}get rgb(){var t=I(this._rgb);return t&&(t.a=s(t.a)),t}set rgb(t){this._rgb=A(t)}rgbString(){return this._valid?(t=this._rgb)&&(t.a<255?`rgba(${t.r}, ${t.g}, ${t.b}, ${s(t.a)})`:`rgb(${t.r}, ${t.g}, ${t.b})`):void 0;var t}hexString(){return this._valid?g(this._rgb):void 0}hslString(){return this._valid?function(t){if(!t)return;const e=m(t),n=e[0],o=c(e[1]),r=c(e[2]);return t.a<255?`hsla(${n}, ${o}%, ${r}%, ${s(t.a)})`:`hsl(${n}, ${o}%, ${r}%)`}(this._rgb):void 0}mix(t,e){if(t){const n=this.rgb,o=t.rgb;let r;const i=e===r?.5:e,a=2*i-1,s=n.a-o.a,c=((a*s==-1?a:(a+s)/(1+a*s))+1)/2;r=1-c,n.r=255&c*n.r+r*o.r+.5,n.g=255&c*n.g+r*o.g+.5,n.b=255&c*n.b+r*o.b+.5,n.a=i*n.a+(1-i)*o.a,this.rgb=n}return this}interpolate(t,e){return t&&(this._rgb=function(t,e,n){const o=C(s(t.r)),r=C(s(t.g)),i=C(s(t.b));return{r:a(R(o+n*(C(s(e.r))-o))),g:a(R(r+n*(C(s(e.g))-r))),b:a(R(i+n*(C(s(e.b))-i))),a:t.a+n*(e.a-t.a)}}(this._rgb,t._rgb,e)),this}clone(){return new F(this.rgb)}alpha(t){return this._rgb.a=a(t),this}clearer(t){return this._rgb.a*=1-t,this}greyscale(){const t=this._rgb,e=o(.3*t.r+.59*t.g+.11*t.b);return t.r=t.g=t.b=e,this}opaquer(t){return this._rgb.a*=1+t,this}negate(){const t=this._rgb;return t.r=255-t.r,t.g=255-t.g,t.b=255-t.b,this}lighten(t){return j(this._rgb,2,t),this}darken(t){return j(this._rgb,2,-t),this}saturate(t){return j(this._rgb,1,t),this}desaturate(t){return j(this._rgb,1,-t),this}rotate(t){return function(t,e){var n=m(t);n[0]=M(n[0]+e),n=w(n),t.r=n[0],t.g=n[1],t.b=n[2]}(this._rgb,t),this}}},20288:(t,e,n)=>{n.a(t,(async(t,o)=>{try{n.d(e,{$:()=>oe,A:()=>ht,B:()=>ut,C:()=>ee,D:()=>nt,E:()=>xe,F:()=>v,G:()=>hn,H:()=>H,I:()=>tn,J:()=>pn,K:()=>gn,L:()=>mt,M:()=>Ge,N:()=>V,O:()=>p,P:()=>E,Q:()=>m,R:()=>we,S:()=>st,T:()=>N,U:()=>tt,V:()=>Vt,W:()=>ct,X:()=>Ut,Y:()=>ne,Z:()=>le,_:()=>yt,a:()=>ve,a0:()=>me,a1:()=>wt,a2:()=>Mt,a3:()=>$t,a4:()=>O,a5:()=>I,a6:()=>Xt,a7:()=>W,a8:()=>_e,a9:()=>ke,aA:()=>Mn,aB:()=>kt,aC:()=>kn,aD:()=>te,aE:()=>ot,aF:()=>l,aG:()=>J,aH:()=>Z,aI:()=>U,aJ:()=>q,aK:()=>et,aL:()=>s,aM:()=>z,aN:()=>Kt,aO:()=>dt,aP:()=>ft,aa:()=>Oe,ab:()=>T,ac:()=>f,ad:()=>vt,ae:()=>dn,af:()=>Jt,ag:()=>F,ah:()=>w,ai:()=>Y,aj:()=>lt,ak:()=>pe,al:()=>Je,am:()=>jn,an:()=>Sn,ao:()=>yn,ap:()=>xn,aq:()=>bn,ar:()=>re,as:()=>ie,at:()=>Gt,au:()=>fe,av:()=>be,aw:()=>ye,ax:()=>Pn,ay:()=>it,az:()=>wn,b:()=>h,c:()=>jt,d:()=>c,e:()=>Rt,f:()=>j,g:()=>g,h:()=>A,i:()=>d,j:()=>Me,k:()=>u,l:()=>pt,m:()=>y,n:()=>x,o:()=>Bt,p:()=>at,q:()=>_t,r:()=>xt,s:()=>Q,t:()=>G,u:()=>bt,v:()=>b,w:()=>Ot,x:()=>K,y:()=>He,z:()=>ln});var r=n(13265),i=(n(89655),n(24545),n(51855),n(82130),n(31743),n(22328),n(4959),n(62435),n(253),n(2075),n(54846),n(16891),n(5884)),a=t([r]);function l(){}r=(a.then?(await a)():a)[0];const f=(()=>{let t=0;return()=>t++})();function u(t){return null==t}function h(t){if(Array.isArray&&Array.isArray(t))return!0;const e=Object.prototype.toString.call(t);return"[object"===e.slice(0,7)&&"Array]"===e.slice(-6)}function d(t){return null!==t&&"[object Object]"===Object.prototype.toString.call(t)}function g(t){return("number"==typeof t||t instanceof Number)&&isFinite(+t)}function p(t,e){return g(t)?t:e}function b(t,e){return void 0===t?e:t}const y=(t,e)=>"string"==typeof t&&t.endsWith("%")?parseFloat(t)/100:+t/e,x=(t,e)=>"string"==typeof t&&t.endsWith("%")?parseFloat(t)/100*e:+t;function m(t,e,n){if(t&&"function"==typeof t.call)return t.apply(n,e)}function v(t,e,n,o){let r,i,a;if(h(t))if(i=t.length,o)for(r=i-1;r>=0;r--)e.call(n,t[r],r);else for(r=0;r<i;r++)e.call(n,t[r],r);else if(d(t))for(a=Object.keys(t),i=a.length,r=0;r<i;r++)e.call(n,t[a[r]],a[r])}function w(t,e){let n,o,r,i;if(!t||!e||t.length!==e.length)return!1;for(n=0,o=t.length;n<o;++n)if(r=t[n],i=e[n],r.datasetIndex!==i.datasetIndex||r.index!==i.index)return!1;return!0}function M(t){if(h(t))return t.map(M);if(d(t)){const e=Object.create(null),n=Object.keys(t),o=n.length;let r=0;for(;r<o;++r)e[n[r]]=M(t[n[r]]);return e}return t}function k(t){return-1===["__proto__","prototype","constructor"].indexOf(t)}function _(t,e,n,o){if(!k(t))return;const r=e[t],i=n[t];d(r)&&d(i)?O(r,i,o):e[t]=M(i)}function O(t,e,n){const o=h(e)?e:[e],r=o.length;if(!d(t))return t;const i=(n=n||{}).merger||_;let a;for(let e=0;e<r;++e){if(a=o[e],!d(a))continue;const r=Object.keys(a);for(let e=0,o=r.length;e<o;++e)i(r[e],t,a,n)}return t}function T(t,e){return O(t,e,{merger:P})}function P(t,e,n){if(!k(t))return;const o=e[t],r=n[t];d(o)&&d(r)?T(o,r):Object.prototype.hasOwnProperty.call(e,t)||(e[t]=M(r))}const S={"":t=>t,x:t=>t.x,y:t=>t.y};function R(t){const e=t.split("."),n=[];let o="";for(const t of e)o+=t,o.endsWith("\\")?o=o.slice(0,-1)+".":(n.push(o),o="");return n}function C(t){const e=R(t);return t=>{for(const n of e){if(""===n)break;t=t&&t[n]}return t}}function j(t,e){return(S[e]||(S[e]=C(e)))(t)}function I(t){return t.charAt(0).toUpperCase()+t.slice(1)}const A=t=>void 0!==t,W=t=>"function"==typeof t,F=(t,e)=>{if(t.size!==e.size)return!1;for(const n of t)if(!e.has(n))return!1;return!0};function Y(t){return"mouseup"===t.type||"click"===t.type||"contextmenu"===t.type}const E=Math.PI,N=2*E,B=N+E,D=Number.POSITIVE_INFINITY,L=E/180,H=E/2,$=E/4,X=2*E/3,z=Math.log10,Q=Math.sign;function q(t,e,n){return Math.abs(t-e)<n}function Z(t){const e=Math.round(t);t=q(t,e,t/1e3)?e:t;const n=Math.pow(10,Math.floor(z(t))),o=t/n;return(o<=1?1:o<=2?2:o<=5?5:10)*n}function V(t){const e=[],n=Math.sqrt(t);let o;for(o=1;o<n;o++)t%o==0&&(e.push(o),e.push(t/o));return n===(0|n)&&e.push(n),e.sort(((t,e)=>t-e)).pop(),e}function K(t){return!isNaN(parseFloat(t))&&isFinite(t)}function U(t,e){const n=Math.round(t);return n-e<=t&&n+e>=t}function J(t,e,n){let o,r,i;for(o=0,r=t.length;o<r;o++)i=t[o][n],isNaN(i)||(e.min=Math.min(e.min,i),e.max=Math.max(e.max,i))}function G(t){return t*(E/180)}function tt(t){return t*(180/E)}function et(t){if(!g(t))return;let e=1,n=0;for(;Math.round(t*e)/e!==t;)e*=10,n++;return n}function nt(t,e){const n=e.x-t.x,o=e.y-t.y,r=Math.sqrt(n*n+o*o);let i=Math.atan2(o,n);return i<-.5*E&&(i+=N),{angle:i,distance:r}}function ot(t,e){return Math.sqrt(Math.pow(e.x-t.x,2)+Math.pow(e.y-t.y,2))}function rt(t,e){return(t-e+B)%N-E}function it(t){return(t%N+N)%N}function at(t,e,n,o){const r=it(t),i=it(e),a=it(n),s=it(i-r),c=it(a-r),l=it(r-i),f=it(r-a);return r===i||r===a||o&&i===a||s>c&&l<f}function st(t,e,n){return Math.max(e,Math.min(n,t))}function ct(t){return st(t,-32768,32767)}function lt(t,e,n,o=1e-6){return t>=Math.min(e,n)-o&&t<=Math.max(e,n)+o}function ft(t,e,n){n=n||(n=>t[n]<e);let o,r=t.length-1,i=0;for(;r-i>1;)o=i+r>>1,n(o)?i=o:r=o;return{lo:i,hi:r}}const ut=(t,e,n,o)=>ft(t,n,o?o=>{const r=t[o][e];return r<n||r===n&&t[o+1][e]===n}:o=>t[o][e]<n),ht=(t,e,n)=>ft(t,n,(o=>t[o][e]>=n));function dt(t,e,n){let o=0,r=t.length;for(;o<r&&t[o]<e;)o++;for(;r>o&&t[r-1]>n;)r--;return o>0||r<t.length?t.slice(o,r):t}const gt=["push","pop","shift","splice","unshift"];function pt(t,e){t._chartjs?t._chartjs.listeners.push(e):(Object.defineProperty(t,"_chartjs",{configurable:!0,enumerable:!1,value:{listeners:[e]}}),gt.forEach((e=>{const n="_onData"+I(e),o=t[e];Object.defineProperty(t,e,{configurable:!0,enumerable:!1,value(...e){const r=o.apply(this,e);return t._chartjs.listeners.forEach((t=>{"function"==typeof t[n]&&t[n](...e)})),r}})})))}function bt(t,e){const n=t._chartjs;if(!n)return;const o=n.listeners,r=o.indexOf(e);-1!==r&&o.splice(r,1),o.length>0||(gt.forEach((e=>{delete t[e]})),delete t._chartjs)}function yt(t){const e=new Set(t);return e.size===t.length?t:Array.from(e)}const xt="undefined"==typeof window?function(t){return t()}:window.requestAnimationFrame;function mt(t,e){let n=[],o=!1;return function(...r){n=r,o||(o=!0,xt.call(window,(()=>{o=!1,t.apply(e,n)})))}}function vt(t,e){let n;return function(...o){return e?(clearTimeout(n),n=setTimeout(t,e,o)):t.apply(this,o),e}}const wt=t=>"start"===t?"left":"end"===t?"right":"center",Mt=(t,e,n)=>"start"===t?e:"end"===t?n:(e+n)/2,kt=(t,e,n,o)=>t===(o?"left":"right")?n:"center"===t?(e+n)/2:e;function _t(t,e,n){const o=e.length;let r=0,i=o;if(t._sorted){const{iScale:a,_parsed:s}=t,c=a.axis,{min:l,max:f,minDefined:u,maxDefined:h}=a.getUserBounds();u&&(r=st(Math.min(ut(s,c,l).lo,n?o:ut(e,c,a.getPixelForValue(l)).lo),0,o-1)),i=h?st(Math.max(ut(s,a.axis,f,!0).hi+1,n?0:ut(e,c,a.getPixelForValue(f),!0).hi+1),r,o)-r:o-r}return{start:r,count:i}}function Ot(t){const{xScale:e,yScale:n,_scaleRanges:o}=t,r={xmin:e.min,xmax:e.max,ymin:n.min,ymax:n.max};if(!o)return t._scaleRanges=r,!0;const i=o.xmin!==e.min||o.xmax!==e.max||o.ymin!==n.min||o.ymax!==n.max;return Object.assign(o,r),i}const Tt=t=>0===t||1===t,Pt=(t,e,n)=>-Math.pow(2,10*(t-=1))*Math.sin((t-e)*N/n),St=(t,e,n)=>Math.pow(2,-10*t)*Math.sin((t-e)*N/n)+1,Rt={linear:t=>t,easeInQuad:t=>t*t,easeOutQuad:t=>-t*(t-2),easeInOutQuad:t=>(t/=.5)<1?.5*t*t:-.5*(--t*(t-2)-1),easeInCubic:t=>t*t*t,easeOutCubic:t=>(t-=1)*t*t+1,easeInOutCubic:t=>(t/=.5)<1?.5*t*t*t:.5*((t-=2)*t*t+2),easeInQuart:t=>t*t*t*t,easeOutQuart:t=>-((t-=1)*t*t*t-1),easeInOutQuart:t=>(t/=.5)<1?.5*t*t*t*t:-.5*((t-=2)*t*t*t-2),easeInQuint:t=>t*t*t*t*t,easeOutQuint:t=>(t-=1)*t*t*t*t+1,easeInOutQuint:t=>(t/=.5)<1?.5*t*t*t*t*t:.5*((t-=2)*t*t*t*t+2),easeInSine:t=>1-Math.cos(t*H),easeOutSine:t=>Math.sin(t*H),easeInOutSine:t=>-.5*(Math.cos(E*t)-1),easeInExpo:t=>0===t?0:Math.pow(2,10*(t-1)),easeOutExpo:t=>1===t?1:1-Math.pow(2,-10*t),easeInOutExpo:t=>Tt(t)?t:t<.5?.5*Math.pow(2,10*(2*t-1)):.5*(2-Math.pow(2,-10*(2*t-1))),easeInCirc:t=>t>=1?t:-(Math.sqrt(1-t*t)-1),easeOutCirc:t=>Math.sqrt(1-(t-=1)*t),easeInOutCirc:t=>(t/=.5)<1?-.5*(Math.sqrt(1-t*t)-1):.5*(Math.sqrt(1-(t-=2)*t)+1),easeInElastic:t=>Tt(t)?t:Pt(t,.075,.3),easeOutElastic:t=>Tt(t)?t:St(t,.075,.3),easeInOutElastic(t){const e=.1125;return Tt(t)?t:t<.5?.5*Pt(2*t,e,.45):.5+.5*St(2*t-1,e,.45)},easeInBack(t){const e=1.70158;return t*t*((e+1)*t-e)},easeOutBack(t){const e=1.70158;return(t-=1)*t*((e+1)*t+e)+1},easeInOutBack(t){let e=1.70158;return(t/=.5)<1?t*t*((1+(e*=1.525))*t-e)*.5:.5*((t-=2)*t*((1+(e*=1.525))*t+e)+2)},easeInBounce:t=>1-Rt.easeOutBounce(1-t),easeOutBounce(t){const e=7.5625,n=2.75;return t<1/n?e*t*t:t<2/n?e*(t-=1.5/n)*t+.75:t<2.5/n?e*(t-=2.25/n)*t+.9375:e*(t-=2.625/n)*t+.984375},easeInOutBounce:t=>t<.5?.5*Rt.easeInBounce(2*t):.5*Rt.easeOutBounce(2*t-1)+.5};function Ct(t){if(t&&"object"==typeof t){const e=t.toString();return"[object CanvasPattern]"===e||"[object CanvasGradient]"===e}return!1}function jt(t){return Ct(t)?t:new i.Q1(t)}function It(t){return Ct(t)?t:new i.Q1(t).saturate(.5).darken(.1).hexString()}const At=["x","y","borderWidth","radius","tension"],Wt=["color","borderColor","backgroundColor"];function Ft(t){t.set("animation",{delay:void 0,duration:1e3,easing:"easeOutQuart",fn:void 0,from:void 0,loop:void 0,to:void 0,type:void 0}),t.describe("animation",{_fallback:!1,_indexable:!1,_scriptable:t=>"onProgress"!==t&&"onComplete"!==t&&"fn"!==t}),t.set("animations",{colors:{type:"color",properties:Wt},numbers:{type:"number",properties:At}}),t.describe("animations",{_fallback:"animation"}),t.set("transitions",{active:{animation:{duration:400}},resize:{animation:{duration:0}},show:{animations:{colors:{from:"transparent"},visible:{type:"boolean",duration:0}}},hide:{animations:{colors:{to:"transparent"},visible:{type:"boolean",easing:"linear",fn:t=>0|t}}}})}function Yt(t){t.set("layout",{autoPadding:!0,padding:{top:0,right:0,bottom:0,left:0}})}const Et=new Map;function Nt(t,e){e=e||{};const n=t+JSON.stringify(e);let o=Et.get(n);return o||(o=new Intl.NumberFormat(t,e),Et.set(n,o)),o}function Bt(t,e,n){return Nt(e,n).format(t)}const Dt={values:t=>h(t)?t:""+t,numeric(t,e,n){if(0===t)return"0";const o=this.chart.options.locale;let r,i=t;if(n.length>1){const e=Math.max(Math.abs(n[0].value),Math.abs(n[n.length-1].value));(e<1e-4||e>1e15)&&(r="scientific"),i=Lt(t,n)}const a=z(Math.abs(i)),s=isNaN(a)?1:Math.max(Math.min(-1*Math.floor(a),20),0),c={notation:r,minimumFractionDigits:s,maximumFractionDigits:s};return Object.assign(c,this.options.ticks.format),Bt(t,o,c)},logarithmic(t,e,n){if(0===t)return"0";const o=n[e].significand||t/Math.pow(10,Math.floor(z(t)));return[1,2,3,5,10,15].includes(o)||e>.8*n.length?Dt.numeric.call(this,t,e,n):""}};function Lt(t,e){let n=e.length>3?e[2].value-e[1].value:e[1].value-e[0].value;return Math.abs(n)>=1&&t!==Math.floor(t)&&(n=t-Math.floor(t)),n}var s={formatters:Dt};function Ht(t){t.set("scale",{display:!0,offset:!1,reverse:!1,beginAtZero:!1,bounds:"ticks",clip:!0,grace:0,grid:{display:!0,lineWidth:1,drawOnChartArea:!0,drawTicks:!0,tickLength:8,tickWidth:(t,e)=>e.lineWidth,tickColor:(t,e)=>e.color,offset:!1},border:{display:!0,dash:[],dashOffset:0,width:1},title:{display:!1,text:"",padding:{top:4,bottom:4}},ticks:{minRotation:0,maxRotation:50,mirror:!1,textStrokeWidth:0,textStrokeColor:"",padding:3,display:!0,autoSkip:!0,autoSkipPadding:3,labelOffset:0,callback:s.formatters.values,minor:{},major:{},align:"center",crossAlign:"near",showLabelBackdrop:!1,backdropColor:"rgba(255, 255, 255, 0.75)",backdropPadding:2}}),t.route("scale.ticks","color","","color"),t.route("scale.grid","color","","borderColor"),t.route("scale.border","color","","borderColor"),t.route("scale.title","color","","color"),t.describe("scale",{_fallback:!1,_scriptable:t=>!t.startsWith("before")&&!t.startsWith("after")&&"callback"!==t&&"parser"!==t,_indexable:t=>"borderDash"!==t&&"tickBorderDash"!==t&&"dash"!==t}),t.describe("scales",{_fallback:"scale"}),t.describe("scale.ticks",{_scriptable:t=>"backdropPadding"!==t&&"callback"!==t,_indexable:t=>"backdropPadding"!==t})}const $t=Object.create(null),Xt=Object.create(null);function zt(t,e){if(!e)return t;const n=e.split(".");for(let e=0,o=n.length;e<o;++e){const o=n[e];t=t[o]||(t[o]=Object.create(null))}return t}function Qt(t,e,n){return"string"==typeof e?O(zt(t,e),n):O(zt(t,""),e)}class qt{constructor(t,e){this.animation=void 0,this.backgroundColor="rgba(0,0,0,0.1)",this.borderColor="rgba(0,0,0,0.1)",this.color="#666",this.datasets={},this.devicePixelRatio=t=>t.chart.platform.getDevicePixelRatio(),this.elements={},this.events=["mousemove","mouseout","click","touchstart","touchmove"],this.font={family:"'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",size:12,style:"normal",lineHeight:1.2,weight:null},this.hover={},this.hoverBackgroundColor=(t,e)=>It(e.backgroundColor),this.hoverBorderColor=(t,e)=>It(e.borderColor),this.hoverColor=(t,e)=>It(e.color),this.indexAxis="x",this.interaction={mode:"nearest",intersect:!0,includeInvisible:!1},this.maintainAspectRatio=!0,this.onHover=null,this.onClick=null,this.parsing=!0,this.plugins={},this.responsive=!0,this.scale=void 0,this.scales={},this.showLine=!0,this.drawActiveElementsOnTop=!0,this.describe(t),this.apply(e)}set(t,e){return Qt(this,t,e)}get(t){return zt(this,t)}describe(t,e){return Qt(Xt,t,e)}override(t,e){return Qt($t,t,e)}route(t,e,n,o){const r=zt(this,t),i=zt(this,n),a="_"+e;Object.defineProperties(r,{[a]:{value:r[e],writable:!0},[e]:{enumerable:!0,get(){const t=this[a],e=i[o];return d(t)?Object.assign({},e,t):b(t,e)},set(t){this[a]=t}}})}apply(t){t.forEach((t=>t(this)))}}var c=new qt({_scriptable:t=>!t.startsWith("on"),_indexable:t=>"events"!==t,hover:{_fallback:"interaction"},interaction:{_scriptable:!1,_indexable:!1}},[Ft,Yt,Ht]);function Zt(t){return!t||u(t.size)||u(t.family)?null:(t.style?t.style+" ":"")+(t.weight?t.weight+" ":"")+t.size+"px "+t.family}function Vt(t,e,n,o,r){let i=e[r];return i||(i=e[r]=t.measureText(r).width,n.push(r)),i>o&&(o=i),o}function Kt(t,e,n,o){let r=(o=o||{}).data=o.data||{},i=o.garbageCollect=o.garbageCollect||[];o.font!==e&&(r=o.data={},i=o.garbageCollect=[],o.font=e),t.save(),t.font=e;let a=0;const s=n.length;let c,l,f,u,d;for(c=0;c<s;c++)if(u=n[c],null==u||h(u)){if(h(u))for(l=0,f=u.length;l<f;l++)d=u[l],null==d||h(d)||(a=Vt(t,r,i,a,d))}else a=Vt(t,r,i,a,u);t.restore();const g=i.length/2;if(g>n.length){for(c=0;c<g;c++)delete r[i[c]];i.splice(0,g)}return a}function Ut(t,e,n){const o=t.currentDevicePixelRatio,r=0!==n?Math.max(n/2,.5):0;return Math.round((e-r)*o)/o+r}function Jt(t,e){(e||t)&&((e=e||t.getContext("2d")).save(),e.resetTransform(),e.clearRect(0,0,t.width,t.height),e.restore())}function Gt(t,e,n,o){te(t,e,n,o,null)}function te(t,e,n,o,r){let i,a,s,c,l,f,u,h;const d=e.pointStyle,g=e.rotation,p=e.radius;let b=(g||0)*L;if(d&&"object"==typeof d&&(i=d.toString(),"[object HTMLImageElement]"===i||"[object HTMLCanvasElement]"===i))return t.save(),t.translate(n,o),t.rotate(b),t.drawImage(d,-d.width/2,-d.height/2,d.width,d.height),void t.restore();if(!(isNaN(p)||p<=0)){switch(t.beginPath(),d){default:r?t.ellipse(n,o,r/2,p,0,0,N):t.arc(n,o,p,0,N),t.closePath();break;case"triangle":f=r?r/2:p,t.moveTo(n+Math.sin(b)*f,o-Math.cos(b)*p),b+=X,t.lineTo(n+Math.sin(b)*f,o-Math.cos(b)*p),b+=X,t.lineTo(n+Math.sin(b)*f,o-Math.cos(b)*p),t.closePath();break;case"rectRounded":l=.516*p,c=p-l,a=Math.cos(b+$)*c,u=Math.cos(b+$)*(r?r/2-l:c),s=Math.sin(b+$)*c,h=Math.sin(b+$)*(r?r/2-l:c),t.arc(n-u,o-s,l,b-E,b-H),t.arc(n+h,o-a,l,b-H,b),t.arc(n+u,o+s,l,b,b+H),t.arc(n-h,o+a,l,b+H,b+E),t.closePath();break;case"rect":if(!g){c=Math.SQRT1_2*p,f=r?r/2:c,t.rect(n-f,o-c,2*f,2*c);break}b+=$;case"rectRot":u=Math.cos(b)*(r?r/2:p),a=Math.cos(b)*p,s=Math.sin(b)*p,h=Math.sin(b)*(r?r/2:p),t.moveTo(n-u,o-s),t.lineTo(n+h,o-a),t.lineTo(n+u,o+s),t.lineTo(n-h,o+a),t.closePath();break;case"crossRot":b+=$;case"cross":u=Math.cos(b)*(r?r/2:p),a=Math.cos(b)*p,s=Math.sin(b)*p,h=Math.sin(b)*(r?r/2:p),t.moveTo(n-u,o-s),t.lineTo(n+u,o+s),t.moveTo(n+h,o-a),t.lineTo(n-h,o+a);break;case"star":u=Math.cos(b)*(r?r/2:p),a=Math.cos(b)*p,s=Math.sin(b)*p,h=Math.sin(b)*(r?r/2:p),t.moveTo(n-u,o-s),t.lineTo(n+u,o+s),t.moveTo(n+h,o-a),t.lineTo(n-h,o+a),b+=$,u=Math.cos(b)*(r?r/2:p),a=Math.cos(b)*p,s=Math.sin(b)*p,h=Math.sin(b)*(r?r/2:p),t.moveTo(n-u,o-s),t.lineTo(n+u,o+s),t.moveTo(n+h,o-a),t.lineTo(n-h,o+a);break;case"line":a=r?r/2:Math.cos(b)*p,s=Math.sin(b)*p,t.moveTo(n-a,o-s),t.lineTo(n+a,o+s);break;case"dash":t.moveTo(n,o),t.lineTo(n+Math.cos(b)*(r?r/2:p),o+Math.sin(b)*p);break;case!1:t.closePath()}t.fill(),e.borderWidth>0&&t.stroke()}}function ee(t,e,n){return n=n||.5,!e||t&&t.x>e.left-n&&t.x<e.right+n&&t.y>e.top-n&&t.y<e.bottom+n}function ne(t,e){t.save(),t.beginPath(),t.rect(e.left,e.top,e.right-e.left,e.bottom-e.top),t.clip()}function oe(t){t.restore()}function re(t,e,n,o,r){if(!e)return t.lineTo(n.x,n.y);if("middle"===r){const o=(e.x+n.x)/2;t.lineTo(o,e.y),t.lineTo(o,n.y)}else"after"===r!=!!o?t.lineTo(e.x,n.y):t.lineTo(n.x,e.y);t.lineTo(n.x,n.y)}function ie(t,e,n,o){if(!e)return t.lineTo(n.x,n.y);t.bezierCurveTo(o?e.cp1x:e.cp2x,o?e.cp1y:e.cp2y,o?n.cp2x:n.cp1x,o?n.cp2y:n.cp1y,n.x,n.y)}function ae(t,e){e.translation&&t.translate(e.translation[0],e.translation[1]),u(e.rotation)||t.rotate(e.rotation),e.color&&(t.fillStyle=e.color),e.textAlign&&(t.textAlign=e.textAlign),e.textBaseline&&(t.textBaseline=e.textBaseline)}function se(t,e,n,o,r){if(r.strikethrough||r.underline){const i=t.measureText(o),a=e-i.actualBoundingBoxLeft,s=e+i.actualBoundingBoxRight,c=n-i.actualBoundingBoxAscent,l=n+i.actualBoundingBoxDescent,f=r.strikethrough?(c+l)/2:l;t.strokeStyle=t.fillStyle,t.beginPath(),t.lineWidth=r.decorationWidth||2,t.moveTo(a,f),t.lineTo(s,f),t.stroke()}}function ce(t,e){const n=t.fillStyle;t.fillStyle=e.color,t.fillRect(e.left,e.top,e.width,e.height),t.fillStyle=n}function le(t,e,n,o,r,i={}){const a=h(e)?e:[e],s=i.strokeWidth>0&&""!==i.strokeColor;let c,l;for(t.save(),t.font=r.string,ae(t,i),c=0;c<a.length;++c)l=a[c],i.backdrop&&ce(t,i.backdrop),s&&(i.strokeColor&&(t.strokeStyle=i.strokeColor),u(i.strokeWidth)||(t.lineWidth=i.strokeWidth),t.strokeText(l,n,o,i.maxWidth)),t.fillText(l,n,o,i.maxWidth),se(t,n,o,l,i),o+=Number(r.lineHeight);t.restore()}function fe(t,e){const{x:n,y:o,w:r,h:i,radius:a}=e;t.arc(n+a.topLeft,o+a.topLeft,a.topLeft,1.5*E,E,!0),t.lineTo(n,o+i-a.bottomLeft),t.arc(n+a.bottomLeft,o+i-a.bottomLeft,a.bottomLeft,E,H,!0),t.lineTo(n+r-a.bottomRight,o+i),t.arc(n+r-a.bottomRight,o+i-a.bottomRight,a.bottomRight,H,0,!0),t.lineTo(n+r,o+a.topRight),t.arc(n+r-a.topRight,o+a.topRight,a.topRight,0,-H,!0),t.lineTo(n+a.topLeft,o)}const ue=/^(normal|(\d+(?:\.\d+)?)(px|em|%)?)$/,he=/^(normal|italic|initial|inherit|unset|(oblique( -?[0-9]?[0-9]deg)?))$/;function de(t,e){const n=(""+t).match(ue);if(!n||"normal"===n[1])return 1.2*e;switch(t=+n[2],n[3]){case"px":return t;case"%":t/=100}return e*t}const ge=t=>+t||0;function pe(t,e){const n={},o=d(e),r=o?Object.keys(e):e,i=d(t)?o?n=>b(t[n],t[e[n]]):e=>t[e]:()=>t;for(const t of r)n[t]=ge(i(t));return n}function be(t){return pe(t,{top:"y",right:"x",bottom:"y",left:"x"})}function ye(t){return pe(t,["topLeft","topRight","bottomLeft","bottomRight"])}function xe(t){const e=be(t);return e.width=e.left+e.right,e.height=e.top+e.bottom,e}function me(t,e){t=t||{},e=e||c.font;let n=b(t.size,e.size);"string"==typeof n&&(n=parseInt(n,10));let o=b(t.style,e.style);o&&!(""+o).match(he)&&(console.warn('Invalid font style specified: "'+o+'"'),o=void 0);const r={family:b(t.family,e.family),lineHeight:de(b(t.lineHeight,e.lineHeight),n),size:n,style:o,weight:b(t.weight,e.weight),string:""};return r.string=Zt(r),r}function ve(t,e,n,o){let r,i,a,s=!0;for(r=0,i=t.length;r<i;++r)if(a=t[r],void 0!==a&&(void 0!==e&&"function"==typeof a&&(a=a(e),s=!1),void 0!==n&&h(a)&&(a=a[n%a.length],s=!1),void 0!==a))return o&&!s&&(o.cacheable=!1),a}function we(t,e,n){const{min:o,max:r}=t,i=x(e,(r-o)/2),a=(t,e)=>n&&0===t?0:t+e;return{min:a(o,-Math.abs(i)),max:a(r,i)}}function Me(t,e){return Object.assign(Object.create(t),e)}function ke(t,e=[""],n,o,r=()=>t[0]){const i=n||t;void 0===o&&(o=Be("_fallback",t));const a={[Symbol.toStringTag]:"Object",_cacheable:!0,_scopes:t,_rootScopes:i,_fallback:o,_getTarget:r,override:n=>ke([n,...t],e,i,o)};return new Proxy(a,{deleteProperty:(e,n)=>(delete e[n],delete e._keys,delete t[0][n],!0),get:(n,o)=>Se(n,o,(()=>Ne(o,e,t,n))),getOwnPropertyDescriptor:(t,e)=>Reflect.getOwnPropertyDescriptor(t._scopes[0],e),getPrototypeOf:()=>Reflect.getPrototypeOf(t[0]),has:(t,e)=>De(t).includes(e),ownKeys:t=>De(t),set(t,e,n){const o=t._storage||(t._storage=r());return t[e]=o[e]=n,delete t._keys,!0}})}function _e(t,e,n,o){const r={_cacheable:!1,_proxy:t,_context:e,_subProxy:n,_stack:new Set,_descriptors:Oe(t,o),setContext:e=>_e(t,e,n,o),override:r=>_e(t.override(r),e,n,o)};return new Proxy(r,{deleteProperty:(e,n)=>(delete e[n],delete t[n],!0),get:(t,e,n)=>Se(t,e,(()=>Re(t,e,n))),getOwnPropertyDescriptor:(e,n)=>e._descriptors.allKeys?Reflect.has(t,n)?{enumerable:!0,configurable:!0}:void 0:Reflect.getOwnPropertyDescriptor(t,n),getPrototypeOf:()=>Reflect.getPrototypeOf(t),has:(e,n)=>Reflect.has(t,n),ownKeys:()=>Reflect.ownKeys(t),set:(e,n,o)=>(t[n]=o,delete e[n],!0)})}function Oe(t,e={scriptable:!0,indexable:!0}){const{_scriptable:n=e.scriptable,_indexable:o=e.indexable,_allKeys:r=e.allKeys}=t;return{allKeys:r,scriptable:n,indexable:o,isScriptable:W(n)?n:()=>n,isIndexable:W(o)?o:()=>o}}const Te=(t,e)=>t?t+I(e):e,Pe=(t,e)=>d(e)&&"adapters"!==t&&(null===Object.getPrototypeOf(e)||e.constructor===Object);function Se(t,e,n){if(Object.prototype.hasOwnProperty.call(t,e)||"constructor"===e)return t[e];const o=n();return t[e]=o,o}function Re(t,e,n){const{_proxy:o,_context:r,_subProxy:i,_descriptors:a}=t;let s=o[e];return W(s)&&a.isScriptable(e)&&(s=Ce(e,s,t,n)),h(s)&&s.length&&(s=je(e,s,t,a.isIndexable)),Pe(e,s)&&(s=_e(s,r,i&&i[e],a)),s}function Ce(t,e,n,o){const{_proxy:r,_context:i,_subProxy:a,_stack:s}=n;if(s.has(t))throw new Error("Recursion detected: "+Array.from(s).join("->")+"->"+t);s.add(t);let c=e(i,a||o);return s.delete(t),Pe(t,c)&&(c=Fe(r._scopes,r,t,c)),c}function je(t,e,n,o){const{_proxy:r,_context:i,_subProxy:a,_descriptors:s}=n;if(void 0!==i.index&&o(t))return e[i.index%e.length];if(d(e[0])){const n=e,o=r._scopes.filter((t=>t!==n));e=[];for(const c of n){const n=Fe(o,r,t,c);e.push(_e(n,i,a&&a[t],s))}}return e}function Ie(t,e,n){return W(t)?t(e,n):t}const Ae=(t,e)=>!0===t?e:"string"==typeof t?j(e,t):void 0;function We(t,e,n,o,r){for(const i of e){const e=Ae(n,i);if(e){t.add(e);const i=Ie(e._fallback,n,r);if(void 0!==i&&i!==n&&i!==o)return i}else if(!1===e&&void 0!==o&&n!==o)return null}return!1}function Fe(t,e,n,o){const r=e._rootScopes,i=Ie(e._fallback,n,o),a=[...t,...r],s=new Set;s.add(o);let c=Ye(s,a,n,i||n,o);return null!==c&&((void 0===i||i===n||(c=Ye(s,a,i,c,o),null!==c))&&ke(Array.from(s),[""],r,i,(()=>Ee(e,n,o))))}function Ye(t,e,n,o,r){for(;n;)n=We(t,e,n,o,r);return n}function Ee(t,e,n){const o=t._getTarget();e in o||(o[e]={});const r=o[e];return h(r)&&d(n)?n:r||{}}function Ne(t,e,n,o){let r;for(const i of e)if(r=Be(Te(i,t),n),void 0!==r)return Pe(t,r)?Fe(n,o,t,r):r}function Be(t,e){for(const n of e){if(!n)continue;const e=n[t];if(void 0!==e)return e}}function De(t){let e=t._keys;return e||(e=t._keys=Le(t._scopes)),e}function Le(t){const e=new Set;for(const n of t)for(const t of Object.keys(n).filter((t=>!t.startsWith("_"))))e.add(t);return Array.from(e)}function He(t,e,n,o){const{iScale:r}=t,{key:i="r"}=this._parsing,a=new Array(o);let s,c,l,f;for(s=0,c=o;s<c;++s)l=s+n,f=e[l],a[s]={r:r.parse(j(f,i),l)};return a}const $e=Number.EPSILON||1e-14,Xe=(t,e)=>e<t.length&&!t[e].skip&&t[e],ze=t=>"x"===t?"y":"x";function Qe(t,e,n,o){const r=t.skip?e:t,i=e,a=n.skip?e:n,s=ot(i,r),c=ot(a,i);let l=s/(s+c),f=c/(s+c);l=isNaN(l)?0:l,f=isNaN(f)?0:f;const u=o*l,h=o*f;return{previous:{x:i.x-u*(a.x-r.x),y:i.y-u*(a.y-r.y)},next:{x:i.x+h*(a.x-r.x),y:i.y+h*(a.y-r.y)}}}function qe(t,e,n){const o=t.length;let r,i,a,s,c,l=Xe(t,0);for(let f=0;f<o-1;++f)c=l,l=Xe(t,f+1),c&&l&&(q(e[f],0,$e)?n[f]=n[f+1]=0:(r=n[f]/e[f],i=n[f+1]/e[f],s=Math.pow(r,2)+Math.pow(i,2),s<=9||(a=3/Math.sqrt(s),n[f]=r*a*e[f],n[f+1]=i*a*e[f])))}function Ze(t,e,n="x"){const o=ze(n),r=t.length;let i,a,s,c=Xe(t,0);for(let l=0;l<r;++l){if(a=s,s=c,c=Xe(t,l+1),!s)continue;const r=s[n],f=s[o];a&&(i=(r-a[n])/3,s[`cp1${n}`]=r-i,s[`cp1${o}`]=f-i*e[l]),c&&(i=(c[n]-r)/3,s[`cp2${n}`]=r+i,s[`cp2${o}`]=f+i*e[l])}}function Ve(t,e="x"){const n=ze(e),o=t.length,r=Array(o).fill(0),i=Array(o);let a,s,c,l=Xe(t,0);for(a=0;a<o;++a)if(s=c,c=l,l=Xe(t,a+1),c){if(l){const t=l[e]-c[e];r[a]=0!==t?(l[n]-c[n])/t:0}i[a]=s?l?Q(r[a-1])!==Q(r[a])?0:(r[a-1]+r[a])/2:r[a-1]:r[a]}qe(t,r,i),Ze(t,i,e)}function Ke(t,e,n){return Math.max(Math.min(t,n),e)}function Ue(t,e){let n,o,r,i,a,s=ee(t[0],e);for(n=0,o=t.length;n<o;++n)a=i,i=s,s=n<o-1&&ee(t[n+1],e),i&&(r=t[n],a&&(r.cp1x=Ke(r.cp1x,e.left,e.right),r.cp1y=Ke(r.cp1y,e.top,e.bottom)),s&&(r.cp2x=Ke(r.cp2x,e.left,e.right),r.cp2y=Ke(r.cp2y,e.top,e.bottom)))}function Je(t,e,n,o,r){let i,a,s,c;if(e.spanGaps&&(t=t.filter((t=>!t.skip))),"monotone"===e.cubicInterpolationMode)Ve(t,r);else{let n=o?t[t.length-1]:t[0];for(i=0,a=t.length;i<a;++i)s=t[i],c=Qe(n,s,t[Math.min(i+1,a-(o?0:1))%a],e.tension),s.cp1x=c.previous.x,s.cp1y=c.previous.y,s.cp2x=c.next.x,s.cp2y=c.next.y,n=s}e.capBezierPoints&&Ue(t,n)}function Ge(){return"undefined"!=typeof window&&"undefined"!=typeof document}function tn(t){let e=t.parentNode;return e&&"[object ShadowRoot]"===e.toString()&&(e=e.host),e}function en(t,e,n){let o;return"string"==typeof t?(o=parseInt(t,10),-1!==t.indexOf("%")&&(o=o/100*e.parentNode[n])):o=t,o}const nn=t=>t.ownerDocument.defaultView.getComputedStyle(t,null);function on(t,e){return nn(t).getPropertyValue(e)}const rn=["top","right","bottom","left"];function an(t,e,n){const o={};n=n?"-"+n:"";for(let r=0;r<4;r++){const i=rn[r];o[i]=parseFloat(t[e+"-"+i+n])||0}return o.width=o.left+o.right,o.height=o.top+o.bottom,o}const sn=(t,e,n)=>(t>0||e>0)&&(!n||!n.shadowRoot);function cn(t,e){const n=t.touches,o=n&&n.length?n[0]:t,{offsetX:r,offsetY:i}=o;let a,s,c=!1;if(sn(r,i,t.target))a=r,s=i;else{const t=e.getBoundingClientRect();a=o.clientX-t.left,s=o.clientY-t.top,c=!0}return{x:a,y:s,box:c}}function ln(t,e){if("native"in t)return t;const{canvas:n,currentDevicePixelRatio:o}=e,r=nn(n),i="border-box"===r.boxSizing,a=an(r,"padding"),s=an(r,"border","width"),{x:c,y:l,box:f}=cn(t,n),u=a.left+(f&&s.left),h=a.top+(f&&s.top);let{width:d,height:g}=e;return i&&(d-=a.width+s.width,g-=a.height+s.height),{x:Math.round((c-u)/d*n.width/o),y:Math.round((l-h)/g*n.height/o)}}function fn(t,e,n){let o,r;if(void 0===e||void 0===n){const i=t&&tn(t);if(i){const t=i.getBoundingClientRect(),a=nn(i),s=an(a,"border","width"),c=an(a,"padding");e=t.width-c.width-s.width,n=t.height-c.height-s.height,o=en(a.maxWidth,i,"clientWidth"),r=en(a.maxHeight,i,"clientHeight")}else e=t.clientWidth,n=t.clientHeight}return{width:e,height:n,maxWidth:o||D,maxHeight:r||D}}const un=t=>Math.round(10*t)/10;function hn(t,e,n,o){const r=nn(t),i=an(r,"margin"),a=en(r.maxWidth,t,"clientWidth")||D,s=en(r.maxHeight,t,"clientHeight")||D,c=fn(t,e,n);let{width:l,height:f}=c;if("content-box"===r.boxSizing){const t=an(r,"border","width"),e=an(r,"padding");l-=e.width+t.width,f-=e.height+t.height}l=Math.max(0,l-i.width),f=Math.max(0,o?l/o:f-i.height),l=un(Math.min(l,a,c.maxWidth)),f=un(Math.min(f,s,c.maxHeight)),l&&!f&&(f=un(l/2));return(void 0!==e||void 0!==n)&&o&&c.height&&f>c.height&&(f=c.height,l=un(Math.floor(f*o))),{width:l,height:f}}function dn(t,e,n){const o=e||1,r=Math.floor(t.height*o),i=Math.floor(t.width*o);t.height=Math.floor(t.height),t.width=Math.floor(t.width);const a=t.canvas;return a.style&&(n||!a.style.height&&!a.style.width)&&(a.style.height=`${t.height}px`,a.style.width=`${t.width}px`),(t.currentDevicePixelRatio!==o||a.height!==r||a.width!==i)&&(t.currentDevicePixelRatio=o,a.height=r,a.width=i,t.ctx.setTransform(o,0,0,o,0,0),!0)}const gn=function(){let t=!1;try{const e={get passive(){return t=!0,!1}};Ge()&&(window.addEventListener("test",null,e),window.removeEventListener("test",null,e))}catch(t){}return t}();function pn(t,e){const n=on(t,e),o=n&&n.match(/^(\d+)(\.\d+)?px$/);return o?+o[1]:void 0}function bn(t,e,n,o){return{x:t.x+n*(e.x-t.x),y:t.y+n*(e.y-t.y)}}function yn(t,e,n,o){return{x:t.x+n*(e.x-t.x),y:"middle"===o?n<.5?t.y:e.y:"after"===o?n<1?t.y:e.y:n>0?e.y:t.y}}function xn(t,e,n,o){const r={x:t.cp2x,y:t.cp2y},i={x:e.cp1x,y:e.cp1y},a=bn(t,r,n),s=bn(r,i,n),c=bn(i,e,n),l=bn(a,s,n),f=bn(s,c,n);return bn(l,f,n)}const mn=function(t,e){return{x:n=>t+t+e-n,setWidth(t){e=t},textAlign:t=>"center"===t?t:"right"===t?"left":"right",xPlus:(t,e)=>t-e,leftForLtr:(t,e)=>t-e}},vn=function(){return{x:t=>t,setWidth(t){},textAlign:t=>t,xPlus:(t,e)=>t+e,leftForLtr:(t,e)=>t}};function wn(t,e,n){return t?mn(e,n):vn()}function Mn(t,e){let n,o;"ltr"!==e&&"rtl"!==e||(n=t.canvas.style,o=[n.getPropertyValue("direction"),n.getPropertyPriority("direction")],n.setProperty("direction",e,"important"),t.prevTextDirection=o)}function kn(t,e){void 0!==e&&(delete t.prevTextDirection,t.canvas.style.setProperty("direction",e[0],e[1]))}function _n(t){return"angle"===t?{between:at,compare:rt,normalize:it}:{between:lt,compare:(t,e)=>t-e,normalize:t=>t}}function On({start:t,end:e,count:n,loop:o,style:r}){return{start:t%n,end:e%n,loop:o&&(e-t+1)%n==0,style:r}}function Tn(t,e,n){const{property:o,start:r,end:i}=n,{between:a,normalize:s}=_n(o),c=e.length;let l,f,{start:u,end:h,loop:d}=t;if(d){for(u+=c,h+=c,l=0,f=c;l<f&&a(s(e[u%c][o]),r,i);++l)u--,h--;u%=c,h%=c}return h<u&&(h+=c),{start:u,end:h,loop:d,style:t.style}}function Pn(t,e,n){if(!n)return[t];const{property:o,start:r,end:i}=n,a=e.length,{compare:s,between:c,normalize:l}=_n(o),{start:f,end:u,loop:h,style:d}=Tn(t,e,n),g=[];let p,b,y,x=!1,m=null;const v=()=>x||c(r,y,p)&&0!==s(r,y),w=()=>!x||0===s(i,p)||c(i,y,p);for(let t=f,n=f;t<=u;++t)b=e[t%a],b.skip||(p=l(b[o]),p!==y&&(x=c(p,r,i),null===m&&v()&&(m=0===s(p,r)?t:n),null!==m&&w()&&(g.push(On({start:m,end:t,loop:h,count:a,style:d})),m=null),n=t,y=p));return null!==m&&g.push(On({start:m,end:u,loop:h,count:a,style:d})),g}function Sn(t,e){const n=[],o=t.segments;for(let r=0;r<o.length;r++){const i=Pn(o[r],t.points,e);i.length&&n.push(...i)}return n}function Rn(t,e,n,o){let r=0,i=e-1;if(n&&!o)for(;r<e&&!t[r].skip;)r++;for(;r<e&&t[r].skip;)r++;for(r%=e,n&&(i+=r);i>r&&t[i%e].skip;)i--;return i%=e,{start:r,end:i}}function Cn(t,e,n,o){const r=t.length,i=[];let a,s=e,c=t[e];for(a=e+1;a<=n;++a){const n=t[a%r];n.skip||n.stop?c.skip||(o=!1,i.push({start:e%r,end:(a-1)%r,loop:o}),e=s=n.stop?a:null):(s=a,c.skip&&(e=a)),c=n}return null!==s&&i.push({start:e%r,end:s%r,loop:o}),i}function jn(t,e){const n=t.points,o=t.options.spanGaps,r=n.length;if(!r)return[];const i=!!t._loop,{start:a,end:s}=Rn(n,r,i,o);if(!0===o)return In(t,[{start:a,end:s,loop:i}],n,e);return In(t,Cn(n,a,s<a?s+r:s,!!t._fullLoop&&0===a&&s===r-1),n,e)}function In(t,e,n,o){return o&&o.setContext&&n?An(t,e,n,o):e}function An(t,e,n,o){const r=t._chart.getContext(),i=Wn(t.options),{_datasetIndex:a,options:{spanGaps:s}}=t,c=n.length,l=[];let f=i,u=e[0].start,h=u;function d(t,e,o,r){const i=s?-1:1;if(t!==e){for(t+=c;n[t%c].skip;)t-=i;for(;n[e%c].skip;)e+=i;t%c!=e%c&&(l.push({start:t%c,end:e%c,loop:o,style:r}),f=r,u=e%c)}}for(const t of e){u=s?u:t.start;let e,i=n[u%c];for(h=u+1;h<=t.end;h++){const s=n[h%c];e=Wn(o.setContext(Me(r,{type:"segment",p0:i,p1:s,p0DataIndex:(h-1)%c,p1DataIndex:h%c,datasetIndex:a}))),Fn(e,f)&&d(u,h-1,t.loop,f),i=s,f=e}u<h-1&&d(u,h-1,t.loop,f)}return l}function Wn(t){return{backgroundColor:t.backgroundColor,borderCapStyle:t.borderCapStyle,borderDash:t.borderDash,borderDashOffset:t.borderDashOffset,borderJoinStyle:t.borderJoinStyle,borderWidth:t.borderWidth,borderColor:t.borderColor}}function Fn(t,e){if(!e)return!1;const n=[],o=function(t,e){return Ct(e)?(n.includes(e)||n.push(e),n.indexOf(e)):e};return JSON.stringify(t,o)!==JSON.stringify(e,o)}o()}catch(Yn){o(Yn)}}))}};
//# sourceMappingURL=20288.SZMZHuFotcY.js.map