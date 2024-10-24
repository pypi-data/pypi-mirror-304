(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[36368],{80930:function(e,t,a){"use strict";a(71499),a(36016),a(98185),Object.defineProperty(t,"__esModule",{value:!0}),t.InitializeRelativeTimeFormat=void 0;var r=a(97555),n=a(70517),o=/^[a-z0-9]{3,8}(-[a-z0-9]{3,8})*$/i;t.InitializeRelativeTimeFormat=function(e,t,a,i){var l=i.getInternalSlots,u=i.availableLocales,s=i.relevantExtensionKeys,c=i.localeData,f=i.getDefaultLocale,v=l(e);v.initializedRelativeTimeFormat=!0;var d=(0,r.CanonicalizeLocaleList)(t),m=Object.create(null),p=(0,r.CoerceOptionsToObject)(a),y=(0,r.GetOption)(p,"localeMatcher","string",["best fit","lookup"],"best fit");m.localeMatcher=y;var b=(0,r.GetOption)(p,"numberingSystem","string",void 0,void 0);if(void 0!==b&&!o.test(b))throw new RangeError("Invalid numbering system ".concat(b));m.nu=b;var g=(0,n.ResolveLocale)(u,d,m,s,c,f),h=g.locale,w=g.nu;v.locale=h,v.style=(0,r.GetOption)(p,"style","string",["long","narrow","short"],"long"),v.numeric=(0,r.GetOption)(p,"numeric","string",["always","auto"],"always");var T=c[g.dataLocale];return(0,r.invariant)(!!T,"Missing locale data for ".concat(g.dataLocale)),v.fields=T,v.numberFormat=new Intl.NumberFormat(t),v.pluralRules=new Intl.PluralRules(t),v.numberingSystem=w,e}},36272:function(e,t,a){"use strict";a(89655),Object.defineProperty(t,"__esModule",{value:!0}),t.MakePartsList=void 0;var r=a(97555);t.MakePartsList=function(e,t,a){for(var n=[],o=0,i=(0,r.PartitionPattern)(e);o<i.length;o++){var l=i[o];if("literal"===l.type)n.push({type:"literal",value:l.value});else{(0,r.invariant)("0"===l.type,"Malformed pattern ".concat(e));for(var u=0,s=a;u<s.length;u++){var c=s[u];n.push({type:c.type,value:c.value,unit:t})}}}return n}},71197:function(e,t,a){"use strict";var r=a(22711).default;a(71499),Object.defineProperty(t,"__esModule",{value:!0}),t.PartitionRelativeTimePattern=void 0;var n=a(97555),o=a(93931),i=a(36272);t.PartitionRelativeTimePattern=function(e,t,a,l){var u=l.getInternalSlots;if((0,n.invariant)("Number"===(0,n.Type)(t),"value must be number, instead got ".concat(r(t)),TypeError),(0,n.invariant)("String"===(0,n.Type)(a),"unit must be number, instead got ".concat(r(t)),TypeError),isNaN(t)||!isFinite(t))throw new RangeError("Invalid value ".concat(t));var s=(0,o.SingularRelativeTimeUnit)(a),c=u(e),f=c.fields,v=c.style,d=c.numeric,m=c.pluralRules,p=c.numberFormat,y=s;"short"===v?y="".concat(s,"-short"):"narrow"===v&&(y="".concat(s,"-narrow")),y in f||(y=s);var b=f[y];if("auto"===d&&(0,n.ToString)(t)in b)return[{type:"literal",value:b[(0,n.ToString)(t)]}];var g="future";((0,n.SameValue)(t,-0)||t<0)&&(g="past");var h=b[g],w="function"==typeof p.formatToParts?p.formatToParts(Math.abs(t)):[{type:"literal",value:p.format(Math.abs(t)),unit:a}],T=h[m.select(t)];return(0,i.MakePartsList)(T,s,w)}},93931:function(e,t,a){"use strict";a(71499),Object.defineProperty(t,"__esModule",{value:!0}),t.SingularRelativeTimeUnit=void 0;var r=a(97555);t.SingularRelativeTimeUnit=function(e){if((0,r.invariant)("String"===(0,r.Type)(e),"unit must be a string"),"seconds"===e)return"second";if("minutes"===e)return"minute";if("hours"===e)return"hour";if("days"===e)return"day";if("weeks"===e)return"week";if("months"===e)return"month";if("quarters"===e)return"quarter";if("years"===e)return"year";if("second"!==e&&"minute"!==e&&"hour"!==e&&"day"!==e&&"week"!==e&&"month"!==e&&"quarter"!==e&&"year"!==e)throw new RangeError("invalid unit");return e}},13967:function(e,t,a){"use strict";a(95737),a(39790),a(99019),a(15129),a(96858),Object.defineProperty(t,"__esModule",{value:!0});var r=new WeakMap;t.default=function(e){var t=r.get(e);return t||(t=Object.create(null),r.set(e,t)),t}},92945:function(e,t,a){"use strict";var r=a(22711).default;a(42942),a(48062),a(30008),a(71499),a(95737),a(79243),a(97741),a(89682),a(45670),a(29193),a(39790),a(7760),a(74268),a(24545),a(51855),a(82130),a(31743),a(22328),a(4959),a(62435),a(99019),a(16891),a(96858),Object.defineProperty(t,"__esModule",{value:!0});var n=a(79192),o=a(97555),i=a(80930),l=a(71197),u=n.__importDefault(a(13967)),s=function(){function e(t,a){if(!(this&&this instanceof e?this.constructor:void 0))throw new TypeError("Intl.RelativeTimeFormat must be called with 'new'");return(0,i.InitializeRelativeTimeFormat)(this,t,a,{getInternalSlots:u.default,availableLocales:e.availableLocales,relevantExtensionKeys:e.relevantExtensionKeys,localeData:e.localeData,getDefaultLocale:e.getDefaultLocale})}return e.prototype.format=function(e,t){if("object"!==r(this))throw new TypeError("format was called on a non-object");if(!(0,u.default)(this).initializedRelativeTimeFormat)throw new TypeError("format was called on a invalid context");return(0,l.PartitionRelativeTimePattern)(this,Number(e),(0,o.ToString)(t),{getInternalSlots:u.default}).map((function(e){return e.value})).join("")},e.prototype.formatToParts=function(e,t){if("object"!==r(this))throw new TypeError("formatToParts was called on a non-object");if(!(0,u.default)(this).initializedRelativeTimeFormat)throw new TypeError("formatToParts was called on a invalid context");return(0,l.PartitionRelativeTimePattern)(this,Number(e),(0,o.ToString)(t),{getInternalSlots:u.default})},e.prototype.resolvedOptions=function(){if("object"!==r(this))throw new TypeError("resolvedOptions was called on a non-object");var e=(0,u.default)(this);if(!e.initializedRelativeTimeFormat)throw new TypeError("resolvedOptions was called on a invalid context");return{locale:e.locale,style:e.style,numeric:e.numeric,numberingSystem:e.numberingSystem}},e.supportedLocalesOf=function(t,a){return(0,o.SupportedLocales)(e.availableLocales,(0,o.CanonicalizeLocaleList)(t),a)},e.__addLocaleData=function(){for(var t=[],a=0;a<arguments.length;a++)t[a]=arguments[a];for(var r=0,n=t;r<n.length;r++){var o=n[r],i=o.data,l=o.locale,u=new Intl.Locale(l).minimize().toString();e.localeData[l]=e.localeData[u]=i,e.availableLocales.add(u),e.availableLocales.add(l),e.__defaultLocale||(e.__defaultLocale=u)}},e.getDefaultLocale=function(){return e.__defaultLocale},e.localeData={},e.availableLocales=new Set,e.__defaultLocale="",e.relevantExtensionKeys=["nu"],e.polyfilled=!0,e}();t.default=s;try{"undefined"!=typeof Symbol&&Object.defineProperty(s.prototype,Symbol.toStringTag,{value:"Intl.RelativeTimeFormat",writable:!1,enumerable:!1,configurable:!0}),Object.defineProperty(s.prototype.constructor,"length",{value:0,writable:!1,enumerable:!1,configurable:!0}),Object.defineProperty(s.supportedLocalesOf,"length",{value:1,writable:!1,enumerable:!1,configurable:!0})}catch(c){}},36368:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=a(79192).__importDefault(a(92945));Object.defineProperty(Intl,"RelativeTimeFormat",{value:r.default,writable:!0,enumerable:!1,configurable:!0})},22711:function(e,t,a){function r(t){return e.exports=r="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},e.exports.__esModule=!0,e.exports.default=e.exports,r(t)}a(42942),a(48062),a(67336),a(95737),a(39790),a(99019),a(96858),e.exports=r,e.exports.__esModule=!0,e.exports.default=e.exports}}]);
//# sourceMappingURL=36368.Or9OOp6xz-A.js.map