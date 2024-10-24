"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[65082],{39299:function(e,t,a){var r=a(35806),n=a(71008),i=a(62193),o=a(2816),s=a(79192),l=a(29818),c=a(35890),u=(a(42942),a(48062),a(39790),a(15112)),d=a(3052),f=["focusin","focusout","pointerdown"],h=function(e){function t(){var e;return(0,n.A)(this,t),(e=(0,i.A)(this,t,arguments)).visible=!1,e.inward=!1,e.attachableController=new d.i(e,e.onControlChange.bind(e)),e}return(0,o.A)(t,e),(0,r.A)(t,[{key:"htmlFor",get:function(){return this.attachableController.htmlFor},set:function(e){this.attachableController.htmlFor=e}},{key:"control",get:function(){return this.attachableController.control},set:function(e){this.attachableController.control=e}},{key:"attach",value:function(e){this.attachableController.attach(e)}},{key:"detach",value:function(){this.attachableController.detach()}},{key:"connectedCallback",value:function(){(0,c.A)(t,"connectedCallback",this,3)([]),this.setAttribute("aria-hidden","true")}},{key:"handleEvent",value:function(e){var t,a;if(!e[v]){switch(e.type){default:return;case"focusin":this.visible=null!==(t=null===(a=this.control)||void 0===a?void 0:a.matches(":focus-visible"))&&void 0!==t&&t;break;case"focusout":case"pointerdown":this.visible=!1}e[v]=!0}}},{key:"onControlChange",value:function(e,t){if(!u.S$)for(var a=0,r=f;a<r.length;a++){var n=r[a];null==e||e.removeEventListener(n,this),null==t||t.addEventListener(n,this)}}},{key:"update",value:function(e){e.has("visible")&&this.dispatchEvent(new Event("visibility-changed")),(0,c.A)(t,"update",this,3)([e])}}])}(u.WF);(0,s.__decorate)([(0,l.MZ)({type:Boolean,reflect:!0})],h.prototype,"visible",void 0),(0,s.__decorate)([(0,l.MZ)({type:Boolean,reflect:!0})],h.prototype,"inward",void 0);var m,v=Symbol("handledByFocusRing"),p=a(64599),g=(0,u.AH)(m||(m=(0,p.A)([":host{animation-delay:0s,calc(var(--md-focus-ring-duration, 600ms)*.25);animation-duration:calc(var(--md-focus-ring-duration, 600ms)*.25),calc(var(--md-focus-ring-duration, 600ms)*.75);animation-timing-function:cubic-bezier(0.2,0,0,1);box-sizing:border-box;color:var(--md-focus-ring-color,var(--md-sys-color-secondary,#625b71));display:none;pointer-events:none;position:absolute}:host([visible]){display:flex}:host(:not([inward])){animation-name:outward-grow,outward-shrink;border-end-end-radius:calc(var(--md-focus-ring-shape-end-end,var(--md-focus-ring-shape,var(--md-sys-shape-corner-full,9999px))) + var(--md-focus-ring-outward-offset,2px));border-end-start-radius:calc(var(--md-focus-ring-shape-end-start,var(--md-focus-ring-shape,var(--md-sys-shape-corner-full,9999px))) + var(--md-focus-ring-outward-offset,2px));border-start-end-radius:calc(var(--md-focus-ring-shape-start-end,var(--md-focus-ring-shape,var(--md-sys-shape-corner-full,9999px))) + var(--md-focus-ring-outward-offset,2px));border-start-start-radius:calc(var(--md-focus-ring-shape-start-start,var(--md-focus-ring-shape,var(--md-sys-shape-corner-full,9999px))) + var(--md-focus-ring-outward-offset,2px));inset:calc(-1*var(--md-focus-ring-outward-offset,2px));outline:var(--md-focus-ring-width,3px) solid currentColor}:host([inward]){animation-name:inward-grow,inward-shrink;border-end-end-radius:calc(var(--md-focus-ring-shape-end-end,var(--md-focus-ring-shape,var(--md-sys-shape-corner-full,9999px))) - var(--md-focus-ring-inward-offset,0px));border-end-start-radius:calc(var(--md-focus-ring-shape-end-start,var(--md-focus-ring-shape,var(--md-sys-shape-corner-full,9999px))) - var(--md-focus-ring-inward-offset,0px));border-start-end-radius:calc(var(--md-focus-ring-shape-start-end,var(--md-focus-ring-shape,var(--md-sys-shape-corner-full,9999px))) - var(--md-focus-ring-inward-offset,0px));border-start-start-radius:calc(var(--md-focus-ring-shape-start-start,var(--md-focus-ring-shape,var(--md-sys-shape-corner-full,9999px))) - var(--md-focus-ring-inward-offset,0px));border:var(--md-focus-ring-width,3px) solid currentColor;inset:var(--md-focus-ring-inward-offset,0px)}@keyframes outward-grow{from{outline-width:0}to{outline-width:var(--md-focus-ring-active-width,8px)}}@keyframes outward-shrink{from{outline-width:var(--md-focus-ring-active-width,8px)}}@keyframes inward-grow{from{border-width:0}to{border-width:var(--md-focus-ring-active-width,8px)}}@keyframes inward-shrink{from{border-width:var(--md-focus-ring-active-width,8px)}}@media(prefers-reduced-motion){:host{animation:none}}"]))),y=function(e){function t(){return(0,n.A)(this,t),(0,i.A)(this,t,arguments)}return(0,o.A)(t,e),(0,r.A)(t)}(h);y.styles=[g],y=(0,s.__decorate)([(0,l.EM)("md-focus-ring")],y)},43044:function(e,t,a){a.d(t,{Ux:function(){return r},du:function(){return n}});a(33994),a(22858),a(95737),a(29193),a(39790),a(66457),a(36016),a(74268),a(24545),a(51855),a(82130),a(31743),a(22328),a(4959),a(62435),a(99019),a(29276),a(79641),a(96858);var r={STANDARD:"cubic-bezier(0.2, 0, 0, 1)",STANDARD_ACCELERATE:"cubic-bezier(.3,0,1,1)",STANDARD_DECELERATE:"cubic-bezier(0,0,0,1)",EMPHASIZED:"cubic-bezier(.3,0,0,1)",EMPHASIZED_ACCELERATE:"cubic-bezier(.3,0,.8,.15)",EMPHASIZED_DECELERATE:"cubic-bezier(.05,.7,.1,1)"};function n(){var e=null;return{start:function(){var t;return null===(t=e)||void 0===t||t.abort(),(e=new AbortController).signal},finish:function(){e=null}}}},55815:function(e,t,a){var r=a(658),n=a(62193),i=a(35890),o=a(2816),s=a(28880),l=a(35806),c=a(71008),u=a(41981),d=a(64782);a(67336),a(71499),a(81027),a(13025),a(52427),a(82386),a(39805),a(95737),a(79243),a(97741),a(89655),a(53165),a(33231),a(50693),a(26098),a(72488),a(25734),a(10507),a(60682),a(39790),a(36016),a(98185),a(7760),a(74268),a(24545),a(51855),a(82130),a(31743),a(22328),a(4959),a(62435),a(36604),a(99019),a(43037),a(15129),a(253),a(2075),a(54846),a(16891),a(66555),a(96858),a(98514),a(34902),a(99810);!function(e){var t=new WeakMap,a=new WeakMap,f=new WeakMap,h=new WeakMap,m=new WeakMap,v=new WeakMap,p=new WeakMap,g=new WeakMap,y=new WeakMap,b=new WeakMap,w=new WeakMap,E=new WeakMap,A=new WeakMap,k=new WeakMap,M=new WeakMap,x={ariaAtomic:"aria-atomic",ariaAutoComplete:"aria-autocomplete",ariaBusy:"aria-busy",ariaChecked:"aria-checked",ariaColCount:"aria-colcount",ariaColIndex:"aria-colindex",ariaColIndexText:"aria-colindextext",ariaColSpan:"aria-colspan",ariaCurrent:"aria-current",ariaDescription:"aria-description",ariaDisabled:"aria-disabled",ariaExpanded:"aria-expanded",ariaHasPopup:"aria-haspopup",ariaHidden:"aria-hidden",ariaInvalid:"aria-invalid",ariaKeyShortcuts:"aria-keyshortcuts",ariaLabel:"aria-label",ariaLevel:"aria-level",ariaLive:"aria-live",ariaModal:"aria-modal",ariaMultiLine:"aria-multiline",ariaMultiSelectable:"aria-multiselectable",ariaOrientation:"aria-orientation",ariaPlaceholder:"aria-placeholder",ariaPosInSet:"aria-posinset",ariaPressed:"aria-pressed",ariaReadOnly:"aria-readonly",ariaRelevant:"aria-relevant",ariaRequired:"aria-required",ariaRoleDescription:"aria-roledescription",ariaRowCount:"aria-rowcount",ariaRowIndex:"aria-rowindex",ariaRowIndexText:"aria-rowindextext",ariaRowSpan:"aria-rowspan",ariaSelected:"aria-selected",ariaSetSize:"aria-setsize",ariaSort:"aria-sort",ariaValueMax:"aria-valuemax",ariaValueMin:"aria-valuemin",ariaValueNow:"aria-valuenow",ariaValueText:"aria-valuetext",role:"role"};function C(e){var t=h.get(e),a=t.form;j(e,a,t),R(e,t.labels)}var T=function(e){for(var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1],a=document.createTreeWalker(e,NodeFilter.SHOW_ELEMENT,{acceptNode:function(e){return h.has(e)?NodeFilter.FILTER_ACCEPT:NodeFilter.FILTER_SKIP}}),r=a.nextNode(),n=!t||e.disabled;r;)r.formDisabledCallback&&n&&O(r,e.disabled),r=a.nextNode()},F={attributes:!0,attributeFilter:["disabled","name"]},S=B()?new MutationObserver((function(e){var t,a=(0,d.A)(e);try{for(a.s();!(t=a.n()).done;){var r=t.value,n=r.target;if("disabled"===r.attributeName&&(n.constructor.formAssociated?O(n,n.hasAttribute("disabled")):"fieldset"===n.localName&&T(n)),"name"===r.attributeName&&n.constructor.formAssociated){var i=h.get(n),o=y.get(n);i.setFormValue(o)}}}catch(s){a.e(s)}finally{a.f()}})):{};function I(e){e.forEach((function(e){var t=e.addedNodes,a=e.removedNodes,r=Array.from(t),n=Array.from(a);r.forEach((function(e){var t;if(h.has(e)&&e.constructor.formAssociated&&C(e),b.has(e)){var a=b.get(e);Object.keys(x).filter((function(e){return null!==a[e]})).forEach((function(t){e.setAttribute(x[t],a[t])})),b.delete(e)}if(M.has(e)){var r=M.get(e);e.setAttribute("internals-valid",r.validity.valid.toString()),e.setAttribute("internals-invalid",(!r.validity.valid).toString()),e.setAttribute("aria-invalid",(!r.validity.valid).toString()),M.delete(e)}if("form"===e.localName)for(var n=g.get(e),i=document.createTreeWalker(e,NodeFilter.SHOW_ELEMENT,{acceptNode:function(e){return!h.has(e)||!e.constructor.formAssociated||n&&n.has(e)?NodeFilter.FILTER_SKIP:NodeFilter.FILTER_ACCEPT}}),o=i.nextNode();o;)C(o),o=i.nextNode();"fieldset"===e.localName&&(null===(t=S.observe)||void 0===t||t.call(S,e,F),T(e,!0))})),n.forEach((function(e){var t=h.get(e);(t&&f.get(t)&&V(t),p.has(e))&&p.get(e).disconnect()}))}))}function L(e){e.forEach((function(e){e.removedNodes.forEach((function(t){var a=A.get(e.target);h.has(t)&&q(t),a.disconnect()}))}))}!B()||new MutationObserver(I);var N={childList:!0,subtree:!0},O=function(e,t){e.toggleAttribute("internals-disabled",t),t?e.setAttribute("aria-disabled","true"):e.removeAttribute("aria-disabled"),e.formDisabledCallback&&e.formDisabledCallback.apply(e,[t])},V=function(e){f.get(e).forEach((function(e){e.remove()})),f.set(e,[])},D=function(e,t){var a=document.createElement("input");return a.type="hidden",a.name=e.getAttribute("name"),e.after(a),f.get(t).push(a),a},R=function(e,t){if(t.length){Array.from(t).forEach((function(t){return t.addEventListener("click",e.click.bind(e))}));var a=t[0].id;t[0].id||(a="".concat(t[0].htmlFor,"_Label"),t[0].id=a),e.setAttribute("aria-labelledby",a)}},P=function(e){var t=Array.from(e.elements).filter((function(e){return!e.tagName.includes("-")&&e.validity})).map((function(e){return e.validity.valid})),a=g.get(e)||[],r=Array.from(a).filter((function(e){return e.isConnected})).map((function(e){return h.get(e).validity.valid})),n=[].concat((0,u.A)(t),(0,u.A)(r)).includes(!1);e.toggleAttribute("internals-invalid",n),e.toggleAttribute("internals-valid",!n)},H=function(e){P(z(e.target))},W=function(e){P(z(e.target))},_=function(e){var t=g.get(e.target);t&&t.size&&t.forEach((function(e){e.constructor.formAssociated&&e.formResetCallback&&e.formResetCallback.apply(e)}))},j=function(e,t,a){if(t){var r=g.get(t);if(r)r.add(e);else{var n=new Set;n.add(e),g.set(t,n),function(e){var t=["button[type=submit]","input[type=submit]","button:not([type])"].map((function(e){return"".concat(e,":not([disabled])")})).map((function(t){return"".concat(t,":not([form])").concat(e.id?",".concat(t,"[form='").concat(e.id,"']"):"")})).join(",");e.addEventListener("click",(function(a){if(a.target.closest(t)){var r=g.get(e);if(e.noValidate)return;r.size&&Array.from(r).reverse().map((function(e){return h.get(e).reportValidity()})).includes(!1)&&a.preventDefault()}}))}(t),t.addEventListener("reset",_),t.addEventListener("input",H),t.addEventListener("change",W)}v.set(t,{ref:e,internals:a}),e.constructor.formAssociated&&e.formAssociatedCallback&&setTimeout((function(){e.formAssociatedCallback.apply(e,[t])}),0),P(t)}},z=function(e){var t=e.parentNode;return t&&"FORM"!==t.tagName&&(t=z(t)),t},U=function(e,t){var a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:DOMException;if(!e.constructor.formAssociated)throw new a(t)},Z=function(e,t,a){var r=g.get(e);return r&&r.size&&r.forEach((function(e){h.get(e)[a]()||(t=!1)})),t},q=function(e){if(e.constructor.formAssociated){var t=h.get(e),a=t.labels,r=t.form;R(e,a),j(e,r,t)}};function B(){return"undefined"!=typeof MutationObserver}var K=(0,l.A)((function e(){(0,c.A)(this,e),this.badInput=!1,this.customError=!1,this.patternMismatch=!1,this.rangeOverflow=!1,this.rangeUnderflow=!1,this.stepMismatch=!1,this.tooLong=!1,this.tooShort=!1,this.typeMismatch=!1,this.valid=!0,this.valueMissing=!1,Object.seal(this)})),$=function(e){var t=!0;for(var a in e)"valid"!==a&&!1!==e[a]&&(t=!1);return t},G=new WeakMap;function J(e,t){e.toggleAttribute(t,!0),e.part&&e.part.add(t)}var Q,X=function(e){function t(e){var a;if((0,c.A)(this,t),a=(0,n.A)(this,t),!e||!e.tagName||-1===e.tagName.indexOf("-"))throw new TypeError("Illegal constructor");return G.set(a,e),a}return(0,o.A)(t,e),(0,l.A)(t,[{key:"add",value:function(e){if(!/^--/.test(e)||"string"!=typeof e)throw new DOMException("Failed to execute 'add' on 'CustomStateSet': The specified value ".concat(e," must start with '--'."));var a=(0,i.A)(t,"add",this,3)([e]),r=G.get(this),n="state".concat(e);return r.isConnected?J(r,n):setTimeout((function(){J(r,n)})),a}},{key:"clear",value:function(){var e,a=(0,d.A)(this.entries());try{for(a.s();!(e=a.n()).done;){var n=(0,r.A)(e.value,1)[0];this.delete(n)}}catch(o){a.e(o)}finally{a.f()}(0,i.A)(t,"clear",this,3)([])}},{key:"delete",value:function(e){var a=(0,i.A)(t,"delete",this,3)([e]),r=G.get(this);return r.isConnected?(r.toggleAttribute("state".concat(e),!1),r.part&&r.part.remove("state".concat(e))):setTimeout((function(){r.toggleAttribute("state".concat(e),!1),r.part&&r.part.remove("state".concat(e))})),a}}],[{key:"isPolyfilled",get:function(){return!0}}])}((0,s.A)(Set));function Y(e,t,a,r){if("a"===a&&!r)throw new TypeError("Private accessor was defined without a getter");if("function"==typeof t?e!==t||!r:!t.has(e))throw new TypeError("Cannot read private member from an object whose class did not declare it");return"m"===a?r:"a"===a?r.call(e):r?r.value:t.get(e)}var ee=function(e){return(0,l.A)((function e(t){(0,c.A)(this,e),Q.set(this,void 0),function(e,t,a,r,n){if("m"===r)throw new TypeError("Private method is not writable");if("a"===r&&!n)throw new TypeError("Private accessor was defined without a setter");if("function"==typeof t?e!==t||!n:!t.has(e))throw new TypeError("Cannot write private member to an object whose class did not declare it");"a"===r?n.call(e,a):n?n.value=a:t.set(e,a)}(this,Q,t,"f");for(var a=0;a<t.length;a++){var r=t[a];this[a]=r,r.hasAttribute("name")&&(this[r.getAttribute("name")]=r)}Object.freeze(this)}),[{key:"length",get:function(){return Y(this,Q,"f").length}},{key:e,value:function(){return Y(this,Q,"f")[Symbol.iterator]()}},{key:"item",value:function(e){return null==this[e]?null:this[e]}},{key:"namedItem",value:function(e){return null==this[e]?null:this[e]}}])}((Q=new WeakMap,Symbol.iterator));var te=function(){return(0,l.A)((function e(r){if((0,c.A)(this,e),!r||!r.tagName||-1===r.tagName.indexOf("-"))throw new TypeError("Illegal constructor");var n,i,o,s,l=r.getRootNode(),u=new K;this.states=new X(r),t.set(this,r),a.set(this,u),h.set(r,this),function(e,t){var a=function(){t[r]=null;var a=null,n=x[r];Object.defineProperty(t,r,{get:function(){return a},set:function(r){a=r,e.isConnected?e.setAttribute(n,r):b.set(e,t)}})};for(var r in x)a()}(r,this),function(e,t){var a;f.set(t,[]),null===(a=S.observe)||void 0===a||a.call(S,e,F)}(r,this),Object.seal(this),l instanceof DocumentFragment&&(n=l,s=new MutationObserver(L),(null===(i=null===window||void 0===window?void 0:window.ShadyDOM)||void 0===i?void 0:i.inUse)&&n.mode&&n.host&&(n=n.host),null===(o=s.observe)||void 0===o||o.call(s,n,{childList:!0}),A.set(n,s))}),[{key:"checkValidity",value:function(){var e=t.get(this);if(U(e,"Failed to execute 'checkValidity' on 'ElementInternals': The target element is not a form-associated custom element."),!this.willValidate)return!0;var r=a.get(this);if(!r.valid){var n=new Event("invalid",{bubbles:!1,cancelable:!0,composed:!1});e.dispatchEvent(n)}return r.valid}},{key:"form",get:function(){var e,a=t.get(this);return U(a,"Failed to read the 'form' property from 'ElementInternals': The target element is not a form-associated custom element."),!0===a.constructor.formAssociated&&(e=z(a)),e}},{key:"labels",get:function(){var e=t.get(this);U(e,"Failed to read the 'labels' property from 'ElementInternals': The target element is not a form-associated custom element.");var a=e.getAttribute("id"),r=e.getRootNode();return r&&a?r.querySelectorAll('[for="'.concat(a,'"]')):[]}},{key:"reportValidity",value:function(){var e=t.get(this);if(U(e,"Failed to execute 'reportValidity' on 'ElementInternals': The target element is not a form-associated custom element."),!this.willValidate)return!0;var a=this.checkValidity(),r=E.get(this);if(r&&!e.constructor.formAssociated)throw new DOMException("Failed to execute 'reportValidity' on 'ElementInternals': The target element is not a form-associated custom element.");return!a&&r&&(e.focus(),r.focus()),a}},{key:"setFormValue",value:function(e){var a=this,n=t.get(this);(U(n,"Failed to execute 'setFormValue' on 'ElementInternals': The target element is not a form-associated custom element."),V(this),null==e||e instanceof FormData)?null!=e&&e instanceof FormData&&Array.from(e).reverse().forEach((function(e){var t=(0,r.A)(e,2),i=t[0],o=t[1];if("string"==typeof o){var s=D(n,a);s.name=i,s.value=o}})):n.getAttribute("name")&&(D(n,this).value=e);y.set(n,e)}},{key:"setValidity",value:function(e,r,n){var i=t.get(this);if(U(i,"Failed to execute 'setValidity' on 'ElementInternals': The target element is not a form-associated custom element."),!e)throw new TypeError("Failed to execute 'setValidity' on 'ElementInternals': 1 argument required, but only 0 present.");E.set(this,n);var o,s=a.get(this),l={};for(var c in e)l[c]=e[c];0===Object.keys(l).length&&((o=s).badInput=!1,o.customError=!1,o.patternMismatch=!1,o.rangeOverflow=!1,o.rangeUnderflow=!1,o.stepMismatch=!1,o.tooLong=!1,o.tooShort=!1,o.typeMismatch=!1,o.valid=!0,o.valueMissing=!1);var u=Object.assign(Object.assign({},s),l);delete u.valid;var d=function(e,t,a){return e.valid=$(t),Object.keys(t).forEach((function(a){return e[a]=t[a]})),a&&P(a),e}(s,u,this.form),f=d.valid;if(!f&&!r)throw new DOMException("Failed to execute 'setValidity' on 'ElementInternals': The second argument should not be empty if one or more flags in the first argument are true.");m.set(this,f?"":r),i.isConnected?(i.toggleAttribute("internals-invalid",!f),i.toggleAttribute("internals-valid",f),i.setAttribute("aria-invalid","".concat(!f))):M.set(i,this)}},{key:"shadowRoot",get:function(){var e=t.get(this),a=w.get(e);return a||null}},{key:"validationMessage",get:function(){var e=t.get(this);return U(e,"Failed to read the 'validationMessage' property from 'ElementInternals': The target element is not a form-associated custom element."),m.get(this)}},{key:"validity",get:function(){var e=t.get(this);return U(e,"Failed to read the 'validity' property from 'ElementInternals': The target element is not a form-associated custom element."),a.get(this)}},{key:"willValidate",get:function(){var e=t.get(this);return U(e,"Failed to read the 'willValidate' property from 'ElementInternals': The target element is not a form-associated custom element."),!(e.disabled||e.hasAttribute("disabled")||e.hasAttribute("readonly"))}}],[{key:"isPolyfilled",get:function(){return!0}}])}();var ae=!1,re=!1;function ne(e){re||(re=!0,window.CustomStateSet=X,e&&(HTMLElement.prototype.attachInternals=function(){for(var t=arguments.length,a=new Array(t),r=0;r<t;r++)a[r]=arguments[r];var n=e.call(this,a);return n.states=new X(this),n}))}function ie(){var e=!(arguments.length>0&&void 0!==arguments[0])||arguments[0];if(!ae){if(ae=!0,"undefined"!=typeof window&&(window.ElementInternals=te),"undefined"!=typeof CustomElementRegistry){var t=CustomElementRegistry.prototype.define;CustomElementRegistry.prototype.define=function(e,a,r){if(a.formAssociated){var n=a.prototype.connectedCallback;a.prototype.connectedCallback=function(){k.has(this)||(k.set(this,!0),this.hasAttribute("disabled")&&O(this,!0)),null!=n&&n.apply(this),q(this)}}t.call(this,e,a,r)}}if("undefined"!=typeof HTMLElement&&(HTMLElement.prototype.attachInternals=function(){if(!this.tagName)return{};if(-1===this.tagName.indexOf("-"))throw new Error("Failed to execute 'attachInternals' on 'HTMLElement': Unable to attach ElementInternals to non-custom elements.");if(h.has(this))throw new DOMException("DOMException: Failed to execute 'attachInternals' on 'HTMLElement': ElementInternals for the specified element was already attached.");return new te(this)}),"undefined"!=typeof Element){function r(){for(var e=arguments.length,t=new Array(e),r=0;r<e;r++)t[r]=arguments[r];var n=a.apply(this,t);if(w.set(this,n),B()){var i=new MutationObserver(I);window.ShadyDOM?i.observe(this,N):i.observe(n,N),p.set(this,i)}return n}var a=Element.prototype.attachShadow;Element.prototype.attachShadow=r}if(B()&&"undefined"!=typeof document)new MutationObserver(I).observe(document.documentElement,N);"undefined"!=typeof HTMLFormElement&&function(){var e=HTMLFormElement.prototype.checkValidity;HTMLFormElement.prototype.checkValidity=function(){for(var t=arguments.length,a=new Array(t),r=0;r<t;r++)a[r]=arguments[r];var n=e.apply(this,a);return Z(this,n,"checkValidity")};var t=HTMLFormElement.prototype.reportValidity;HTMLFormElement.prototype.reportValidity=function(){for(var e=arguments.length,a=new Array(e),r=0;r<e;r++)a[r]=arguments[r];var n=t.apply(this,a);return Z(this,n,"reportValidity")};var a=Object.getOwnPropertyDescriptor(HTMLFormElement.prototype,"elements").get;Object.defineProperty(HTMLFormElement.prototype,"elements",{get:function(){for(var e=arguments.length,t=new Array(e),r=0;r<e;r++)t[r]=arguments[r];var n=a.call.apply(a,[this].concat(t)),i=Array.from(g.get(this)||[]);if(0===i.length)return n;var o=Array.from(n).concat(i).sort((function(e,t){return e.compareDocumentPosition?2&e.compareDocumentPosition(t)?1:-1:0}));return new ee(o)}})}(),(e||"undefined"!=typeof window&&!window.CustomStateSet)&&ne()}}!!customElements.polyfillWrapFlushCallback||(!function(){if("undefined"==typeof window||!window.ElementInternals||!HTMLElement.prototype.attachInternals)return!1;var e=function(e){function t(){var e;return(0,c.A)(this,t),(e=(0,n.A)(this,t)).internals=e.attachInternals(),e}return(0,o.A)(t,e),(0,l.A)(t)}((0,s.A)(HTMLElement)),t="element-internals-feature-detection-".concat(Math.random().toString(36).replace(/[^a-z]+/g,""));customElements.define(t,e);var a=new e;return["shadowRoot","form","willValidate","validity","validationMessage","labels","setFormValue","setValidity","checkValidity","reportValidity"].every((function(e){return e in a.internals}))}()?ie(!1):"undefined"==typeof window||window.CustomStateSet||ne(HTMLElement.prototype.attachInternals)),e.forceCustomStateSetPolyfill=ne,e.forceElementInternalsPolyfill=ie,Object.defineProperty(e,"__esModule",{value:!0})}({})}}]);
//# sourceMappingURL=65082.98iX0whqnnE.js.map