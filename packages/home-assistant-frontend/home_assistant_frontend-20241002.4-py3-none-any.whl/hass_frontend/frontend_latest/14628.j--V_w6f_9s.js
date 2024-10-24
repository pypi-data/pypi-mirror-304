/*! For license information please see 14628.j--V_w6f_9s.js.LICENSE.txt */
export const id=14628;export const ids=[14628];export const modules={83723:(t,e,n)=>{function o(t,e){if(t.closest)return t.closest(e);for(var n=t;n;){if(i(n,e))return n;n=n.parentElement}return null}function i(t,e){return(t.matches||t.webkitMatchesSelector||t.msMatchesSelector).call(t,e)}n.d(e,{cK:()=>i,kp:()=>o})},90410:(t,e,n)=>{n.d(e,{ZS:()=>l,is:()=>s.i});var o,i,r=n(79192),c=n(77706),s=n(19637);const a=null!==(i=null===(o=window.ShadyDOM)||void 0===o?void 0:o.inUse)&&void 0!==i&&i;class l extends s.O{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=t=>{this.disabled||this.setFormData(t.formData)}}findFormElement(){if(!this.shadowRoot||a)return null;const t=this.getRootNode().querySelectorAll("form");for(const e of Array.from(t))if(e.contains(this))return e;return null}connectedCallback(){var t;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}}l.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,r.__decorate)([(0,c.MZ)({type:Boolean})],l.prototype,"disabled",void 0)},20931:(t,e,n)=>{var o=n(79192),i=n(77706),r=(n(66731),n(34752)),c=n(25430),s=n(15112),a=n(10977);class l extends s.WF{constructor(){super(...arguments),this.disabled=!1,this.icon="",this.shouldRenderRipple=!1,this.rippleHandlers=new c.I((()=>(this.shouldRenderRipple=!0,this.ripple)))}renderRipple(){return this.shouldRenderRipple?s.qy` <mwc-ripple .disabled="${this.disabled}" unbounded> </mwc-ripple>`:""}focus(){const t=this.buttonElement;t&&(this.rippleHandlers.startFocus(),t.focus())}blur(){const t=this.buttonElement;t&&(this.rippleHandlers.endFocus(),t.blur())}render(){return s.qy`<button class="mdc-icon-button mdc-icon-button--display-flex" aria-label="${this.ariaLabel||this.icon}" aria-haspopup="${(0,a.J)(this.ariaHasPopup)}" ?disabled="${this.disabled}" @focus="${this.handleRippleFocus}" @blur="${this.handleRippleBlur}" @mousedown="${this.handleRippleMouseDown}" @mouseenter="${this.handleRippleMouseEnter}" @mouseleave="${this.handleRippleMouseLeave}" @touchstart="${this.handleRippleTouchStart}" @touchend="${this.handleRippleDeactivate}" @touchcancel="${this.handleRippleDeactivate}">${this.renderRipple()} ${this.icon?s.qy`<i class="material-icons">${this.icon}</i>`:""} <span><slot></slot></span> </button>`}handleRippleMouseDown(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.rippleHandlers.startPress(t)}handleRippleTouchStart(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,o.__decorate)([(0,i.MZ)({type:Boolean,reflect:!0})],l.prototype,"disabled",void 0),(0,o.__decorate)([(0,i.MZ)({type:String})],l.prototype,"icon",void 0),(0,o.__decorate)([r.T,(0,i.MZ)({type:String,attribute:"aria-label"})],l.prototype,"ariaLabel",void 0),(0,o.__decorate)([r.T,(0,i.MZ)({type:String,attribute:"aria-haspopup"})],l.prototype,"ariaHasPopup",void 0),(0,o.__decorate)([(0,i.P)("button")],l.prototype,"buttonElement",void 0),(0,o.__decorate)([(0,i.nJ)("mwc-ripple")],l.prototype,"ripple",void 0),(0,o.__decorate)([(0,i.wk)()],l.prototype,"shouldRenderRipple",void 0),(0,o.__decorate)([(0,i.Ls)({passive:!0})],l.prototype,"handleRippleMouseDown",null),(0,o.__decorate)([(0,i.Ls)({passive:!0})],l.prototype,"handleRippleTouchStart",null);const d=s.AH`.material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:400;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}.mdc-icon-button{font-size:24px;width:48px;height:48px;padding:12px}.mdc-icon-button .mdc-icon-button__focus-ring{display:none}.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{display:block;max-height:48px;max-width:48px}@media screen and (forced-colors:active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{pointer-events:none;border:2px solid transparent;border-radius:6px;box-sizing:content-box;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);height:100%;width:100%}}@media screen and (forced-colors:active)and (forced-colors:active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{border-color:CanvasText}}@media screen and (forced-colors:active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring::after,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring::after{content:"";border:2px solid transparent;border-radius:8px;display:block;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);height:calc(100% + 4px);width:calc(100% + 4px)}}@media screen and (forced-colors:active)and (forced-colors:active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring::after,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring::after{border-color:CanvasText}}.mdc-icon-button.mdc-icon-button--reduced-size .mdc-icon-button__ripple{width:40px;height:40px;margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}.mdc-icon-button.mdc-icon-button--reduced-size.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button.mdc-icon-button--reduced-size:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{max-height:40px;max-width:40px}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%,-50%)}.mdc-icon-button:disabled{color:rgba(0,0,0,.38);color:var(--mdc-theme-text-disabled-on-light,rgba(0,0,0,.38))}.mdc-icon-button img,.mdc-icon-button svg{width:24px;height:24px}.mdc-icon-button{display:inline-block;position:relative;box-sizing:border-box;border:none;outline:0;background-color:transparent;fill:currentColor;color:inherit;text-decoration:none;cursor:pointer;user-select:none;z-index:0;overflow:visible}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%,-50%)}.mdc-icon-button:disabled{cursor:default;pointer-events:none}.mdc-icon-button--display-flex{align-items:center;display:inline-flex;justify-content:center}.mdc-icon-button__icon{display:inline-block}.mdc-icon-button__icon.mdc-icon-button__icon--on{display:none}.mdc-icon-button--on .mdc-icon-button__icon{display:none}.mdc-icon-button--on .mdc-icon-button__icon.mdc-icon-button__icon--on{display:inline-block}.mdc-icon-button__link{height:100%;left:0;outline:0;position:absolute;top:0;width:100%}.mdc-icon-button{display:inline-block;position:relative;box-sizing:border-box;border:none;outline:0;background-color:transparent;fill:currentColor;color:inherit;text-decoration:none;cursor:pointer;user-select:none;z-index:0;overflow:visible}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%,-50%)}.mdc-icon-button:disabled{cursor:default;pointer-events:none}.mdc-icon-button--display-flex{align-items:center;display:inline-flex;justify-content:center}.mdc-icon-button__icon{display:inline-block}.mdc-icon-button__icon.mdc-icon-button__icon--on{display:none}.mdc-icon-button--on .mdc-icon-button__icon{display:none}.mdc-icon-button--on .mdc-icon-button__icon.mdc-icon-button__icon--on{display:inline-block}.mdc-icon-button__link{height:100%;left:0;outline:0;position:absolute;top:0;width:100%}:host{display:inline-block;outline:0}:host([disabled]){pointer-events:none}.mdc-icon-button ::slotted(*),.mdc-icon-button i,.mdc-icon-button img,.mdc-icon-button svg{display:block}:host{--mdc-ripple-color:currentcolor;-webkit-tap-highlight-color:transparent}.mdc-icon-button,:host{vertical-align:top}.mdc-icon-button{width:var(--mdc-icon-button-size,48px);height:var(--mdc-icon-button-size,48px);padding:calc((var(--mdc-icon-button-size,48px) - var(--mdc-icon-size,24px))/ 2)}.mdc-icon-button ::slotted(*),.mdc-icon-button i,.mdc-icon-button img,.mdc-icon-button svg{display:block;width:var(--mdc-icon-size,24px);height:var(--mdc-icon-size,24px)}`;let u=class extends l{};u.styles=[d],u=(0,o.__decorate)([(0,i.EM)("mwc-icon-button")],u)},68009:(t,e,n)=>{n.d(e,{A:()=>o});n(253),n(54846),n(16891);function o(t){if(!t||"object"!=typeof t)return t;if("[object Date]"==Object.prototype.toString.call(t))return new Date(t.getTime());if(Array.isArray(t))return t.map(o);var e={};return Object.keys(t).forEach((function(n){e[n]=o(t[n])})),e}},2586:(t,e,n)=>{var o=n(80674),i=n(82337),r=n(88138).f,c=o("unscopables"),s=Array.prototype;void 0===s[c]&&r(s,c,{configurable:!0,value:i(null)}),t.exports=function(t){s[c][t]=!0}},14767:(t,e,n)=>{var o=n(36565);t.exports=function(t,e,n){for(var i=0,r=arguments.length>2?n:o(e),c=new t(r);r>i;)c[i]=e[i++];return c}},88124:(t,e,n)=>{var o=n(66293),i=n(13113),r=n(88680),c=n(49940),s=n(80896),a=n(36565),l=n(82337),d=n(14767),u=Array,p=i([].push);t.exports=function(t,e,n,i){for(var m,b,h,f=c(t),g=r(f),v=o(e,n),_=l(null),y=a(g),x=0;y>x;x++)h=g[x],(b=s(v(h,x,f)))in _?p(_[b],h):_[b]=[h];if(i&&(m=i(f))!==u)for(b in _)_[b]=d(m,_[b]);return _}},12073:(t,e,n)=>{var o=n(41765),i=n(88124),r=n(2586);o({target:"Array",proto:!0},{group:function(t){return i(this,t,arguments.length>1?arguments[1]:void 0)}}),r("group")},36575:(t,e,n)=>{n.d(e,{LV:()=>p});n(253),n(16891),n(37679);const o=Symbol("Comlink.proxy"),i=Symbol("Comlink.endpoint"),r=Symbol("Comlink.releaseProxy"),c=Symbol("Comlink.finalizer"),s=Symbol("Comlink.thrown"),a=t=>"object"==typeof t&&null!==t||"function"==typeof t,l=new Map([["proxy",{canHandle:t=>a(t)&&t[o],serialize(t){const{port1:e,port2:n}=new MessageChannel;return d(t,e),[n,[n]]},deserialize:t=>(t.start(),p(t))}],["throw",{canHandle:t=>a(t)&&s in t,serialize({value:t}){let e;return e=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[e,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function d(t,e=globalThis,n=["*"]){e.addEventListener("message",(function i(r){if(!r||!r.data)return;if(!function(t,e){for(const n of t){if(e===n||"*"===n)return!0;if(n instanceof RegExp&&n.test(e))return!0}return!1}(n,r.origin))return void console.warn(`Invalid origin '${r.origin}' for comlink proxy`);const{id:a,type:l,path:p}=Object.assign({path:[]},r.data),m=(r.data.argumentList||[]).map(x);let b;try{const e=p.slice(0,-1).reduce(((t,e)=>t[e]),t),n=p.reduce(((t,e)=>t[e]),t);switch(l){case"GET":b=n;break;case"SET":e[p.slice(-1)[0]]=x(r.data.value),b=!0;break;case"APPLY":b=n.apply(e,m);break;case"CONSTRUCT":b=function(t){return Object.assign(t,{[o]:!0})}(new n(...m));break;case"ENDPOINT":{const{port1:e,port2:n}=new MessageChannel;d(t,n),b=function(t,e){return _.set(t,e),t}(e,[e])}break;case"RELEASE":b=void 0;break;default:return}}catch(t){b={value:t,[s]:0}}Promise.resolve(b).catch((t=>({value:t,[s]:0}))).then((n=>{const[o,r]=y(n);e.postMessage(Object.assign(Object.assign({},o),{id:a}),r),"RELEASE"===l&&(e.removeEventListener("message",i),u(e),c in t&&"function"==typeof t[c]&&t[c]())})).catch((t=>{const[n,o]=y({value:new TypeError("Unserializable return value"),[s]:0});e.postMessage(Object.assign(Object.assign({},n),{id:a}),o)}))})),e.start&&e.start()}function u(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function p(t,e){return g(t,[],e)}function m(t){if(t)throw new Error("Proxy has been released and is not useable")}function b(t){return w(t,{type:"RELEASE"}).then((()=>{u(t)}))}const h=new WeakMap,f="FinalizationRegistry"in globalThis&&new FinalizationRegistry((t=>{const e=(h.get(t)||0)-1;h.set(t,e),0===e&&b(t)}));function g(t,e=[],n=function(){}){let o=!1;const c=new Proxy(n,{get(n,i){if(m(o),i===r)return()=>{!function(t){f&&f.unregister(t)}(c),b(t),o=!0};if("then"===i){if(0===e.length)return{then:()=>c};const n=w(t,{type:"GET",path:e.map((t=>t.toString()))}).then(x);return n.then.bind(n)}return g(t,[...e,i])},set(n,i,r){m(o);const[c,s]=y(r);return w(t,{type:"SET",path:[...e,i].map((t=>t.toString())),value:c},s).then(x)},apply(n,r,c){m(o);const s=e[e.length-1];if(s===i)return w(t,{type:"ENDPOINT"}).then(x);if("bind"===s)return g(t,e.slice(0,-1));const[a,l]=v(c);return w(t,{type:"APPLY",path:e.map((t=>t.toString())),argumentList:a},l).then(x)},construct(n,i){m(o);const[r,c]=v(i);return w(t,{type:"CONSTRUCT",path:e.map((t=>t.toString())),argumentList:r},c).then(x)}});return function(t,e){const n=(h.get(e)||0)+1;h.set(e,n),f&&f.register(t,e,t)}(c,t),c}function v(t){const e=t.map(y);return[e.map((t=>t[0])),(n=e.map((t=>t[1])),Array.prototype.concat.apply([],n))];var n}const _=new WeakMap;function y(t){for(const[e,n]of l)if(n.canHandle(t)){const[o,i]=n.serialize(t);return[{type:"HANDLER",name:e,value:o},i]}return[{type:"RAW",value:t},_.get(t)||[]]}function x(t){switch(t.type){case"HANDLER":return l.get(t.name).deserialize(t.value);case"RAW":return t.value}}function w(t,e,n){return new Promise((o=>{const i=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");t.addEventListener("message",(function e(n){n.data&&n.data.id&&n.data.id===i&&(t.removeEventListener("message",e),o(n.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:i},e),n)}))}},32559:(t,e,n)=>{n.d(e,{Dx:()=>d,Jz:()=>f,KO:()=>h,Rt:()=>a,cN:()=>b,lx:()=>u,mY:()=>m,ps:()=>s,qb:()=>c,sO:()=>r});var o=n(2501);const{I:i}=o.ge,r=t=>null===t||"object"!=typeof t&&"function"!=typeof t,c=(t,e)=>void 0===e?void 0!==(null==t?void 0:t._$litType$):(null==t?void 0:t._$litType$)===e,s=t=>{var e;return null!=(null===(e=null==t?void 0:t._$litType$)||void 0===e?void 0:e.h)},a=t=>void 0===t.strings,l=()=>document.createComment(""),d=(t,e,n)=>{var o;const r=t._$AA.parentNode,c=void 0===e?t._$AB:e._$AA;if(void 0===n){const e=r.insertBefore(l(),c),o=r.insertBefore(l(),c);n=new i(e,o,t,t.options)}else{const e=n._$AB.nextSibling,i=n._$AM,s=i!==t;if(s){let e;null===(o=n._$AQ)||void 0===o||o.call(n,t),n._$AM=t,void 0!==n._$AP&&(e=t._$AU)!==i._$AU&&n._$AP(e)}if(e!==c||s){let t=n._$AA;for(;t!==e;){const e=t.nextSibling;r.insertBefore(t,c),t=e}}}return n},u=(t,e,n=t)=>(t._$AI(e,n),t),p={},m=(t,e=p)=>t._$AH=e,b=t=>t._$AH,h=t=>{var e;null===(e=t._$AP)||void 0===e||e.call(t,!1,!0);let n=t._$AA;const o=t._$AB.nextSibling;for(;n!==o;){const t=n.nextSibling;n.remove(),n=t}},f=t=>{t._$AR()}},67089:(t,e,n)=>{n.d(e,{OA:()=>o.OA,WL:()=>o.WL,u$:()=>o.u$});var o=n(68063)},63073:(t,e,n)=>{n.d(e,{W:()=>o.W});var o=n(49935)}};
//# sourceMappingURL=14628.j--V_w6f_9s.js.map