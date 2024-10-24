"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[40052],{90410:function(t,n,e){e.d(n,{ZS:function(){return v},is:function(){return f.i}});var i,r,o=e(71008),a=e(35806),u=e(62193),s=e(35890),d=e(2816),l=(e(52427),e(99019),e(79192)),c=e(29818),f=e(19637),h=null!==(r=null===(i=window.ShadyDOM)||void 0===i?void 0:i.inUse)&&void 0!==r&&r,v=function(t){function n(){var t;return(0,o.A)(this,n),(t=(0,u.A)(this,n,arguments)).disabled=!1,t.containingForm=null,t.formDataListener=function(n){t.disabled||t.setFormData(n.formData)},t}return(0,d.A)(n,t),(0,a.A)(n,[{key:"findFormElement",value:function(){if(!this.shadowRoot||h)return null;for(var t=this.getRootNode().querySelectorAll("form"),n=0,e=Array.from(t);n<e.length;n++){var i=e[n];if(i.contains(this))return i}return null}},{key:"connectedCallback",value:function(){var t;(0,s.A)(n,"connectedCallback",this,3)([]),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}},{key:"disconnectedCallback",value:function(){var t;(0,s.A)(n,"disconnectedCallback",this,3)([]),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}},{key:"click",value:function(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}},{key:"firstUpdated",value:function(){var t=this;(0,s.A)(n,"firstUpdated",this,3)([]),this.shadowRoot&&this.mdcRoot.addEventListener("change",(function(n){t.dispatchEvent(new Event("change",n))}))}}])}(f.O);v.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,l.__decorate)([(0,c.MZ)({type:Boolean})],v.prototype,"disabled",void 0)},67056:function(t,n,e){var i=e(35806),r=e(71008),o=e(62193),a=e(2816),u=e(79192),s=e(29818),d=e(30116),l=e(43389),c=function(t){function n(){return(0,r.A)(this,n),(0,o.A)(this,n,arguments)}return(0,a.A)(n,t),(0,i.A)(n)}(d.J);c.styles=[l.R],c=(0,u.__decorate)([(0,s.EM)("mwc-list-item")],c)},79051:function(t,n,e){e.d(n,{d:function(){return i}});var i=function(t){return t.stopPropagation()}},18409:function(t,n,e){e.d(n,{s:function(){return i}});var i=function(t,n){var e,i=arguments.length>2&&void 0!==arguments[2]&&arguments[2],r=function(){for(var r=arguments.length,o=new Array(r),a=0;a<r;a++)o[a]=arguments[a];var u=i&&!e;clearTimeout(e),e=window.setTimeout((function(){e=void 0,i||t.apply(void 0,o)}),n),u&&t.apply(void 0,o)};return r.cancel=function(){clearTimeout(e)},r}},61441:function(t,n,e){e.d(n,{E:function(){return r},m:function(){return i}});e(39790),e(66457);var i=function(t){requestAnimationFrame((function(){return setTimeout(t,0)}))},r=function(){return new Promise((function(t){i(t)}))}},48473:function(t,n,e){var i,r=e(64599),o=e(35806),a=e(71008),u=e(62193),s=e(2816),d=e(27927),l=(e(81027),e(29193),e(26098),e(15112)),c=e(29818),f=e(34897);e(76994),(0,d.A)([(0,c.EM)("ha-duration-input")],(function(t,n){var e=function(n){function e(){var n;(0,a.A)(this,e);for(var i=arguments.length,r=new Array(i),o=0;o<i;o++)r[o]=arguments[o];return n=(0,u.A)(this,e,[].concat(r)),t(n),n}return(0,s.A)(e,n),(0,o.A)(e)}(n);return{F:e,d:[{kind:"field",decorators:[(0,c.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,c.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,c.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,c.MZ)({type:Boolean})],key:"required",value:function(){return!1}},{kind:"field",decorators:[(0,c.MZ)({type:Boolean})],key:"enableMillisecond",value:function(){return!1}},{kind:"field",decorators:[(0,c.MZ)({type:Boolean})],key:"enableDay",value:function(){return!1}},{kind:"field",decorators:[(0,c.MZ)({type:Boolean})],key:"disabled",value:function(){return!1}},{kind:"field",decorators:[(0,c.P)("paper-time-input",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return(0,l.qy)(i||(i=(0,r.A)([' <ha-base-time-input .label="','" .helper="','" .required="','" .autoValidate="','" .disabled="','" errorMessage="Required" enableSecond .enableMillisecond="','" .enableDay="','" format="24" .days="','" .hours="','" .minutes="','" .seconds="','" .milliseconds="','" @value-changed="','" noHoursLimit dayLabel="dd" hourLabel="hh" minLabel="mm" secLabel="ss" millisecLabel="ms"></ha-base-time-input> '])),this.label,this.helper,this.required,this.required,this.disabled,this.enableMillisecond,this.enableDay,this._days,this._hours,this._minutes,this._seconds,this._milliseconds,this._durationChanged)}},{kind:"get",key:"_days",value:function(){var t;return null!==(t=this.data)&&void 0!==t&&t.days?Number(this.data.days):0}},{kind:"get",key:"_hours",value:function(){var t;return null!==(t=this.data)&&void 0!==t&&t.hours?Number(this.data.hours):0}},{kind:"get",key:"_minutes",value:function(){var t;return null!==(t=this.data)&&void 0!==t&&t.minutes?Number(this.data.minutes):0}},{kind:"get",key:"_seconds",value:function(){var t;return null!==(t=this.data)&&void 0!==t&&t.seconds?Number(this.data.seconds):0}},{kind:"get",key:"_milliseconds",value:function(){var t;return null!==(t=this.data)&&void 0!==t&&t.milliseconds?Number(this.data.milliseconds):0}},{kind:"method",key:"_durationChanged",value:function(t){t.stopPropagation();var n,e=Object.assign({},t.detail.value);(this.enableMillisecond||e.milliseconds?e.milliseconds>999&&(e.seconds+=Math.floor(e.milliseconds/1e3),e.milliseconds%=1e3):delete e.milliseconds,e.seconds>59&&(e.minutes+=Math.floor(e.seconds/60),e.seconds%=60),e.minutes>59&&(e.hours+=Math.floor(e.minutes/60),e.minutes%=60),this.enableDay&&e.hours>24)&&(e.days=(null!==(n=e.days)&&void 0!==n?n:0)+Math.floor(e.hours/24),e.hours%=24);(0,f.r)(this,"value-changed",{value:e})}}]}}),l.WF)},24280:function(t,n,e){e.r(n),e.d(n,{HaFormTimePeriod:function(){return f}});var i,r=e(64599),o=e(35806),a=e(71008),u=e(62193),s=e(2816),d=e(27927),l=(e(81027),e(15112)),c=e(29818),f=(e(48473),(0,d.A)([(0,c.EM)("ha-form-positive_time_period_dict")],(function(t,n){var e=function(n){function e(){var n;(0,a.A)(this,e);for(var i=arguments.length,r=new Array(i),o=0;o<i;o++)r[o]=arguments[o];return n=(0,u.A)(this,e,[].concat(r)),t(n),n}return(0,s.A)(e,n),(0,o.A)(e)}(n);return{F:e,d:[{kind:"field",decorators:[(0,c.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,c.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,c.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,c.MZ)({type:Boolean})],key:"disabled",value:function(){return!1}},{kind:"field",decorators:[(0,c.P)("ha-time-input",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return(0,l.qy)(i||(i=(0,r.A)([' <ha-duration-input .label="','" ?required="','" .data="','" .disabled="','"></ha-duration-input> '])),this.label,this.schema.required,this.data,this.disabled)}}]}}),l.WF))},14767:function(t,n,e){var i=e(36565);t.exports=function(t,n,e){for(var r=0,o=arguments.length>2?e:i(n),a=new t(o);o>r;)a[r]=n[r++];return a}},88124:function(t,n,e){var i=e(66293),r=e(13113),o=e(88680),a=e(49940),u=e(80896),s=e(36565),d=e(82337),l=e(14767),c=Array,f=r([].push);t.exports=function(t,n,e,r){for(var h,v,m,p=a(t),k=o(p),y=i(n,e),g=d(null),b=s(k),A=0;b>A;A++)m=k[A],(v=u(y(m,A,p)))in g?f(g[v],m):g[v]=[m];if(r&&(h=r(p))!==c)for(v in g)g[v]=l(h,g[v]);return g}},32350:function(t,n,e){var i=e(32174),r=e(23444),o=e(33616),a=e(36565),u=e(87149),s=Math.min,d=[].lastIndexOf,l=!!d&&1/[1].lastIndexOf(1,-0)<0,c=u("lastIndexOf"),f=l||!c;t.exports=f?function(t){if(l)return i(d,this,arguments)||0;var n=r(this),e=a(n);if(0===e)return-1;var u=e-1;for(arguments.length>1&&(u=s(u,o(arguments[1]))),u<0&&(u=e+u);u>=0;u--)if(u in n&&n[u]===t)return u||0;return-1}:d},73909:function(t,n,e){var i=e(13113),r=e(22669),o=e(53138),a=/"/g,u=i("".replace);t.exports=function(t,n,e,i){var s=o(r(t)),d="<"+n;return""!==e&&(d+=" "+e+'="'+u(o(i),a,"&quot;")+'"'),d+">"+s+"</"+n+">"}},75022:function(t,n,e){var i=e(26906);t.exports=function(t){return i((function(){var n=""[t]('"');return n!==n.toLowerCase()||n.split('"').length>3}))}},54630:function(t,n,e){var i=e(72148);t.exports=/Version\/10(?:\.\d+){1,2}(?: [\w./]+)?(?: Mobile\/\w+)? Safari\//.test(i)},36686:function(t,n,e){var i=e(13113),r=e(93187),o=e(53138),a=e(90924),u=e(22669),s=i(a),d=i("".slice),l=Math.ceil,c=function(t){return function(n,e,i){var a,c,f=o(u(n)),h=r(e),v=f.length,m=void 0===i?" ":o(i);return h<=v||""===m?f:((c=s(m,l((a=h-v)/m.length))).length>a&&(c=d(c,0,a)),t?f+c:c+f)}};t.exports={start:c(!1),end:c(!0)}},90924:function(t,n,e){var i=e(33616),r=e(53138),o=e(22669),a=RangeError;t.exports=function(t){var n=r(o(this)),e="",u=i(t);if(u<0||u===1/0)throw new a("Wrong number of repetitions");for(;u>0;(u>>>=1)&&(n+=n))1&u&&(e+=n);return e}},34465:function(t,n,e){var i=e(54935).PROPER,r=e(26906),o=e(69329);t.exports=function(t){return r((function(){return!!o[t]()||"​᠎"!=="​᠎"[t]()||i&&o[t].name!==t}))}},15814:function(t,n,e){var i=e(41765),r=e(32350);i({target:"Array",proto:!0,forced:r!==[].lastIndexOf},{lastIndexOf:r})},82115:function(t,n,e){var i=e(41765),r=e(13113),o=e(33616),a=e(64849),u=e(90924),s=e(26906),d=RangeError,l=String,c=Math.floor,f=r(u),h=r("".slice),v=r(1..toFixed),m=function(t,n,e){return 0===n?e:n%2==1?m(t,n-1,e*t):m(t*t,n/2,e)},p=function(t,n,e){for(var i=-1,r=e;++i<6;)r+=n*t[i],t[i]=r%1e7,r=c(r/1e7)},k=function(t,n){for(var e=6,i=0;--e>=0;)i+=t[e],t[e]=c(i/n),i=i%n*1e7},y=function(t){for(var n=6,e="";--n>=0;)if(""!==e||0===n||0!==t[n]){var i=l(t[n]);e=""===e?i:e+f("0",7-i.length)+i}return e};i({target:"Number",proto:!0,forced:s((function(){return"0.000"!==v(8e-5,3)||"1"!==v(.9,0)||"1.25"!==v(1.255,2)||"1000000000000000128"!==v(0xde0b6b3a7640080,0)}))||!s((function(){v({})}))},{toFixed:function(t){var n,e,i,r,u=a(this),s=o(t),c=[0,0,0,0,0,0],v="",g="0";if(s<0||s>20)throw new d("Incorrect fraction digits");if(u!=u)return"NaN";if(u<=-1e21||u>=1e21)return l(u);if(u<0&&(v="-",u=-u),u>1e-21)if(e=(n=function(t){for(var n=0,e=t;e>=4096;)n+=12,e/=4096;for(;e>=2;)n+=1,e/=2;return n}(u*m(2,69,1))-69)<0?u*m(2,-n,1):u/m(2,n,1),e*=4503599627370496,(n=52-n)>0){for(p(c,0,e),i=s;i>=7;)p(c,1e7,0),i-=7;for(p(c,m(10,i,1),0),i=n-1;i>=23;)k(c,1<<23),i-=23;k(c,1<<i),p(c,1,1),k(c,2),g=y(c)}else p(c,0,e),p(c,1<<-n,0),g=y(c)+f("0",s);return g=s>0?v+((r=g.length)<=s?"0."+f("0",s-r)+g:h(g,0,r-s)+"."+h(g,r-s)):v+g}})},33628:function(t,n,e){var i=e(41765),r=e(73909);i({target:"String",proto:!0,forced:e(75022)("anchor")},{anchor:function(t){return r(this,"a","name",t)}})},79977:function(t,n,e){var i=e(41765),r=e(36686).start;i({target:"String",proto:!0,forced:e(54630)},{padStart:function(t){return r(this,t,arguments.length>1?arguments[1]:void 0)}})},79641:function(t,n,e){var i=e(41765),r=e(38971).trim;i({target:"String",proto:!0,forced:e(34465)("trim")},{trim:function(){return r(this)}})},12073:function(t,n,e){var i=e(41765),r=e(88124),o=e(2586);i({target:"Array",proto:!0},{group:function(t){return r(this,t,arguments.length>1?arguments[1]:void 0)}}),o("group")}}]);
//# sourceMappingURL=40052.y6YAu2pJonA.js.map