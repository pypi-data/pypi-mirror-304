"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[70307],{52172:function(t,e,a){a(42942),a(48062),a(30008),a(71499),a(81027),a(39805),a(95737),a(89655),a(89682),a(45670),a(39790),a(7760),a(74268),a(24545),a(51855),a(82130),a(31743),a(22328),a(4959),a(62435),a(99019),a(15129),a(96858),Object.defineProperty(e,"__esModule",{value:!0});var n=a(79192),l=a(97555),r=a(70517);function o(t,e){if(!(t instanceof c))throw new TypeError("Method Intl.ListFormat.prototype.".concat(e," called on incompatible receiver ").concat(String(t)))}function i(t){if(void 0===t)return[];for(var e=[],a=0,n=t;a<n.length;a++){var l=n[a];if("string"!=typeof l)throw new TypeError("array list[".concat(t.indexOf(l),"] is not type String"));e.push(l)}return e}function s(t,e,a){var n=a.length;if(0===n)return[];if(2===n)return _((0,l.getInternalSlot)(t,e,"templatePair"),{0:{type:"element",value:a[0]},1:{type:"element",value:a[1]}});for(var r={type:"element",value:a[n-1]},o=n-2;o>=0;){r=_(0===o?(0,l.getInternalSlot)(t,e,"templateStart"):o<n-2?(0,l.getInternalSlot)(t,e,"templateMiddle"):(0,l.getInternalSlot)(t,e,"templateEnd"),{0:{type:"element",value:a[o]},1:r}),o--}return r}function _(t,e){for(var a=[],n=0,r=(0,l.PartitionPattern)(t);n<r.length;n++){var o=r[n],i=o.type;if((0,l.isLiteralPart)(o))a.push({type:"literal",value:o.value});else{(0,l.invariant)(i in e,"".concat(i," is missing from placables"));var s=e[i];Array.isArray(s)?a.push.apply(a,s):a.push(s)}}return a}var c=function(){function t(e,a){if(!(this&&this instanceof t?this.constructor:void 0))throw new TypeError("Intl.ListFormat must be called with 'new'");(0,l.setInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"initializedListFormat",!0);var n=(0,l.CanonicalizeLocaleList)(e),o=Object.create(null),i=(0,l.GetOptionsObject)(a),s=(0,l.GetOption)(i,"localeMatcher","string",["best fit","lookup"],"best fit");o.localeMatcher=s;var _=t.localeData,c=(0,r.ResolveLocale)(t.availableLocales,n,o,t.relevantExtensionKeys,_,t.getDefaultLocale);(0,l.setInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"locale",c.locale);var u=(0,l.GetOption)(i,"type","string",["conjunction","disjunction","unit"],"conjunction");(0,l.setInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"type",u);var p=(0,l.GetOption)(i,"style","string",["long","short","narrow"],"long");(0,l.setInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"style",p);var f=c.dataLocale,L=_[f];(0,l.invariant)(!!L,"Missing locale data for ".concat(f));var v=L[u][p];(0,l.setInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"templatePair",v.pair),(0,l.setInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"templateStart",v.start),(0,l.setInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"templateMiddle",v.middle),(0,l.setInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"templateEnd",v.end)}return t.prototype.format=function(e){o(this,"format");var a="",n=s(t.__INTERNAL_SLOT_MAP__,this,i(e));if(!Array.isArray(n))return n.value;for(var l=0,r=n;l<r.length;l++){a+=r[l].value}return a},t.prototype.formatToParts=function(e){o(this,"format");var a=s(t.__INTERNAL_SLOT_MAP__,this,i(e));if(!Array.isArray(a))return[a];for(var l=[],r=0,_=a;r<_.length;r++){var c=_[r];l.push(n.__assign({},c))}return l},t.prototype.resolvedOptions=function(){return o(this,"resolvedOptions"),{locale:(0,l.getInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"locale"),type:(0,l.getInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"type"),style:(0,l.getInternalSlot)(t.__INTERNAL_SLOT_MAP__,this,"style")}},t.supportedLocalesOf=function(e,a){return(0,l.SupportedLocales)(t.availableLocales,(0,l.CanonicalizeLocaleList)(e),a)},t.__addLocaleData=function(){for(var e=[],a=0;a<arguments.length;a++)e[a]=arguments[a];for(var n=0,l=e;n<l.length;n++){var r=l[n],o=r.data,i=r.locale,s=new Intl.Locale(i).minimize().toString();t.localeData[i]=t.localeData[s]=o,t.availableLocales.add(s),t.availableLocales.add(i),t.__defaultLocale||(t.__defaultLocale=s)}},t.getDefaultLocale=function(){return t.__defaultLocale},t.localeData={},t.availableLocales=new Set,t.__defaultLocale="",t.relevantExtensionKeys=[],t.polyfilled=!0,t.__INTERNAL_SLOT_MAP__=new WeakMap,t}();e.default=c;try{"undefined"!=typeof Symbol&&Object.defineProperty(c.prototype,Symbol.toStringTag,{value:"Intl.ListFormat",writable:!1,enumerable:!1,configurable:!0}),Object.defineProperty(c.prototype.constructor,"length",{value:0,writable:!1,enumerable:!1,configurable:!0}),Object.defineProperty(c.supportedLocalesOf,"length",{value:1,writable:!1,enumerable:!1,configurable:!0})}catch(u){}},70307:function(t,e,a){Object.defineProperty(e,"__esModule",{value:!0});var n=a(79192).__importDefault(a(52172));Object.defineProperty(Intl,"ListFormat",{value:n.default,writable:!0,enumerable:!1,configurable:!0})}}]);
//# sourceMappingURL=70307.qRPg6LJwvE4.js.map