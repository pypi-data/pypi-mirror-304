export const id=57464;export const ids=[57464,20144];export const modules={79051:(e,t,o)=>{o.d(t,{d:()=>i});const i=e=>e.stopPropagation()},18409:(e,t,o)=>{o.d(t,{s:()=>i});const i=(e,t,o=!1)=>{let i;const a=(...a)=>{const r=o&&!i;clearTimeout(i),i=window.setTimeout((()=>{i=void 0,o||e(...a)}),t),r&&e(...a)};return a.cancel=()=>{clearTimeout(i)},a}},39891:(e,t,o)=>{o.d(t,{h:()=>i});const i=(e,t)=>{const o=new Promise(((t,o)=>{setTimeout((()=>{o(`Timed out in ${e} ms.`)}),e)}));return Promise.race([t,o])}},31979:(e,t,o)=>{var i=o(36312),a=o(68689),r=(o(89655),o(16891),o(15112)),d=o(77706),s=o(94100),n=o(34897),c=o(79051);o(20144);const l={key:"Mod-s",run:e=>((0,n.r)(e.dom,"editor-save"),!0)},f=e=>{const t=document.createElement("ha-icon");return t.icon=e.label,t};(0,i.A)([(0,d.EM)("ha-code-editor")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:"codemirror",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"mode",value:()=>"yaml"},{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"autofocus",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"readOnly",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"linewrap",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Boolean,attribute:"autocomplete-entities"})],key:"autocompleteEntities",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Boolean,attribute:"autocomplete-icons"})],key:"autocompleteIcons",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"error",value:()=>!1},{kind:"field",decorators:[(0,d.wk)()],key:"_value",value:()=>""},{kind:"field",key:"_loadedCodeMirror",value:void 0},{kind:"field",key:"_iconList",value:void 0},{kind:"set",key:"value",value:function(e){this._value=e}},{kind:"get",key:"value",value:function(){return this.codemirror?this.codemirror.state.doc.toString():this._value}},{kind:"get",key:"hasComments",value:function(){if(!this.codemirror||!this._loadedCodeMirror)return!1;const e=this._loadedCodeMirror.highlightingFor(this.codemirror.state,[this._loadedCodeMirror.tags.comment]);return!!this.renderRoot.querySelector(`span.${e}`)}},{kind:"method",key:"connectedCallback",value:function(){(0,a.A)(i,"connectedCallback",this,3)([]),this.hasUpdated&&this.requestUpdate(),this.addEventListener("keydown",c.d),this.codemirror&&!1!==this.autofocus&&this.codemirror.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.A)(i,"disconnectedCallback",this,3)([]),this.removeEventListener("keydown",c.d),this.updateComplete.then((()=>{this.codemirror.destroy(),delete this.codemirror}))}},{kind:"method",key:"scheduleUpdate",value:async function(){this._loadedCodeMirror??=await Promise.all([o.e(61060),o.e(96087),o.e(30008),o.e(61449)]).then(o.bind(o,61449)),(0,a.A)(i,"scheduleUpdate",this,3)([])}},{kind:"method",key:"update",value:function(e){if((0,a.A)(i,"update",this,3)([e]),!this.codemirror)return void this._createCodeMirror();const t=[];e.has("mode")&&t.push({effects:[this._loadedCodeMirror.langCompartment.reconfigure(this._mode),this._loadedCodeMirror.foldingCompartment.reconfigure(this._getFoldingExtensions())]}),e.has("readOnly")&&t.push({effects:this._loadedCodeMirror.readonlyCompartment.reconfigure(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly))}),e.has("linewrap")&&t.push({effects:this._loadedCodeMirror.linewrapCompartment.reconfigure(this.linewrap?this._loadedCodeMirror.EditorView.lineWrapping:[])}),e.has("_value")&&this._value!==this.value&&t.push({changes:{from:0,to:this.codemirror.state.doc.length,insert:this._value}}),t.length>0&&this.codemirror.dispatch(...t),e.has("error")&&this.classList.toggle("error-state",this.error)}},{kind:"get",key:"_mode",value:function(){return this._loadedCodeMirror.langs[this.mode]}},{kind:"method",key:"_createCodeMirror",value:function(){if(!this._loadedCodeMirror)throw new Error("Cannot create editor before CodeMirror is loaded");const e=[this._loadedCodeMirror.lineNumbers(),this._loadedCodeMirror.history(),this._loadedCodeMirror.drawSelection(),this._loadedCodeMirror.EditorState.allowMultipleSelections.of(!0),this._loadedCodeMirror.rectangularSelection(),this._loadedCodeMirror.crosshairCursor(),this._loadedCodeMirror.highlightSelectionMatches(),this._loadedCodeMirror.highlightActiveLine(),this._loadedCodeMirror.indentationMarkers({thickness:0,activeThickness:1,colors:{activeLight:"var(--secondary-text-color)",activeDark:"var(--secondary-text-color)"}}),this._loadedCodeMirror.keymap.of([...this._loadedCodeMirror.defaultKeymap,...this._loadedCodeMirror.searchKeymap,...this._loadedCodeMirror.historyKeymap,...this._loadedCodeMirror.tabKeyBindings,l]),this._loadedCodeMirror.langCompartment.of(this._mode),this._loadedCodeMirror.haTheme,this._loadedCodeMirror.haSyntaxHighlighting,this._loadedCodeMirror.readonlyCompartment.of(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly)),this._loadedCodeMirror.linewrapCompartment.of(this.linewrap?this._loadedCodeMirror.EditorView.lineWrapping:[]),this._loadedCodeMirror.EditorView.updateListener.of(this._onUpdate),this._loadedCodeMirror.foldingCompartment.of(this._getFoldingExtensions())];if(!this.readOnly){const t=[];this.autocompleteEntities&&this.hass&&t.push(this._entityCompletions.bind(this)),this.autocompleteIcons&&t.push(this._mdiCompletions.bind(this)),t.length>0&&e.push(this._loadedCodeMirror.autocompletion({override:t,maxRenderedOptions:10}))}this.codemirror=new this._loadedCodeMirror.EditorView({state:this._loadedCodeMirror.EditorState.create({doc:this._value,extensions:e}),parent:this.renderRoot})}},{kind:"field",key:"_getStates",value:()=>(0,s.A)((e=>{if(!e)return[];return Object.keys(e).map((t=>({type:"variable",label:t,detail:e[t].attributes.friendly_name,info:`State: ${e[t].state}`})))}))},{kind:"method",key:"_entityCompletions",value:function(e){const t=e.matchBefore(/[a-z_]{3,}\.\w*/);if(!t||t.from===t.to&&!e.explicit)return null;const o=this._getStates(this.hass.states);return o&&o.length?{from:Number(t.from),options:o,validFor:/^[a-z_]{3,}\.\w*$/}:null}},{kind:"field",key:"_getIconItems",value(){return async()=>{if(!this._iconList){let e;e=(await o.e(25143).then(o.t.bind(o,25143,19))).default,this._iconList=e.map((e=>({type:"variable",label:`mdi:${e.name}`,detail:e.keywords.join(", "),info:f})))}return this._iconList}}},{kind:"method",key:"_mdiCompletions",value:async function(e){const t=e.matchBefore(/mdi:\S*/);if(!t||t.from===t.to&&!e.explicit)return null;const o=await this._getIconItems();return{from:Number(t.from),options:o,validFor:/^mdi:\S*$/}}},{kind:"field",key:"_onUpdate",value(){return e=>{e.docChanged&&(this._value=e.state.doc.toString(),(0,n.r)(this,"value-changed",{value:this._value}))}}},{kind:"field",key:"_getFoldingExtensions",value(){return()=>"yaml"===this.mode?[this._loadedCodeMirror.foldGutter(),this._loadedCodeMirror.foldingOnIndent]:[]}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`:host(.error-state) .cm-gutters{border-color:var(--error-state-color,red)}`}}]}}),r.mN)},20144:(e,t,o)=>{o.r(t),o.d(t,{HaIcon:()=>_});var i=o(36312),a=o(68689),r=o(15112),d=o(77706),s=o(34897),n=o(18409),c=o(81235),l=(o(89655),o(253),o(54846),o(75702)),f=o(39891);const h=JSON.parse('{"version":"7.4.47","parts":[{"file":"7a7139d465f1f41cb26ab851a17caa21a9331234"},{"start":"account-supervisor-circle-","file":"9561286c4c1021d46b9006596812178190a7cc1c"},{"start":"alpha-r-c","file":"eb466b7087fb2b4d23376ea9bc86693c45c500fa"},{"start":"arrow-decision-o","file":"4b3c01b7e0723b702940c5ac46fb9e555646972b"},{"start":"baby-f","file":"2611401d85450b95ab448ad1d02c1a432b409ed2"},{"start":"battery-hi","file":"89bcd31855b34cd9d31ac693fb073277e74f1f6a"},{"start":"blur-r","file":"373709cd5d7e688c2addc9a6c5d26c2d57c02c48"},{"start":"briefcase-account-","file":"a75956cf812ee90ee4f656274426aafac81e1053"},{"start":"calendar-question-","file":"3253f2529b5ebdd110b411917bacfacb5b7063e6"},{"start":"car-lig","file":"74566af3501ad6ae58ad13a8b6921b3cc2ef879d"},{"start":"cellphone-co","file":"7677f1cfb2dd4f5562a2aa6d3ae43a2e6997b21a"},{"start":"circle-slice-2","file":"70d08c50ec4522dd75d11338db57846588263ee2"},{"start":"cloud-co","file":"141d2bfa55ca4c83f4bae2812a5da59a84fec4ff"},{"start":"cog-s","file":"5a640365f8e47c609005d5e098e0e8104286d120"},{"start":"cookie-l","file":"dd85b8eb8581b176d3acf75d1bd82e61ca1ba2fc"},{"start":"currency-eur-","file":"15362279f4ebfc3620ae55f79d2830ad86d5213e"},{"start":"delete-o","file":"239434ab8df61237277d7599ebe066c55806c274"},{"start":"draw-","file":"5605918a592070803ba2ad05a5aba06263da0d70"},{"start":"emoticon-po","file":"a838cfcec34323946237a9f18e66945f55260f78"},{"start":"fan","file":"effd56103b37a8c7f332e22de8e4d67a69b70db7"},{"start":"file-question-","file":"b2424b50bd465ae192593f1c3d086c5eec893af8"},{"start":"flask-off-","file":"3b76295cde006a18f0301dd98eed8c57e1d5a425"},{"start":"food-s","file":"1c6941474cbeb1755faaaf5771440577f4f1f9c6"},{"start":"gamepad-u","file":"c6efe18db6bc9654ae3540c7dee83218a5450263"},{"start":"google-f","file":"df341afe6ad4437457cf188499cb8d2df8ac7b9e"},{"start":"head-c","file":"282121c9e45ed67f033edcc1eafd279334c00f46"},{"start":"home-pl","file":"27e8e38fc7adcacf2a210802f27d841b49c8c508"},{"start":"inbox-","file":"0f0316ec7b1b7f7ce3eaabce26c9ef619b5a1694"},{"start":"key-v","file":"ea33462be7b953ff1eafc5dac2d166b210685a60"},{"start":"leaf-circle-","file":"33db9bbd66ce48a2db3e987fdbd37fb0482145a4"},{"start":"lock-p","file":"b89e27ed39e9d10c44259362a4b57f3c579d3ec8"},{"start":"message-s","file":"7b5ab5a5cadbe06e3113ec148f044aa701eac53a"},{"start":"moti","file":"01024d78c248d36805b565e343dd98033cc3bcaf"},{"start":"newspaper-variant-o","file":"22a6ec4a4fdd0a7c0acaf805f6127b38723c9189"},{"start":"on","file":"c73d55b412f394e64632e2011a59aa05e5a1f50d"},{"start":"paw-ou","file":"3f669bf26d16752dc4a9ea349492df93a13dcfbf"},{"start":"pigg","file":"0c24edb27eb1c90b6e33fc05f34ef3118fa94256"},{"start":"printer-pos-sy","file":"41a55cda866f90b99a64395c3bb18c14983dcf0a"},{"start":"read","file":"c7ed91552a3a64c9be88c85e807404cf705b7edf"},{"start":"robot-vacuum-variant-o","file":"917d2a35d7268c0ea9ad9ecab2778060e19d90e0"},{"start":"sees","file":"6e82d9861d8fac30102bafa212021b819f303bdb"},{"start":"shoe-f","file":"e2fe7ce02b5472301418cc90a0e631f187b9f238"},{"start":"snowflake-m","file":"a28ba9f5309090c8b49a27ca20ff582a944f6e71"},{"start":"st","file":"7e92d03f095ec27e137b708b879dfd273bd735ab"},{"start":"su","file":"61c74913720f9de59a379bdca37f1d2f0dc1f9db"},{"start":"tag-plus-","file":"8f3184156a4f38549cf4c4fffba73a6a941166ae"},{"start":"timer-a","file":"baab470d11cfb3a3cd3b063ee6503a77d12a80d0"},{"start":"transit-d","file":"8561c0d9b1ac03fab360fd8fe9729c96e8693239"},{"start":"vector-arrange-b","file":"c9a3439257d4bab33d3355f1f2e11842e8171141"},{"start":"water-ou","file":"02dbccfb8ca35f39b99f5a085b095fc1275005a0"},{"start":"webc","file":"57bafd4b97341f4f2ac20a609d023719f23a619c"},{"start":"zip","file":"65ae094e8263236fa50486584a08c03497a38d93"}]}'),u=(0,l.y$)("hass-icon-db","mdi-icon-store"),b=["mdi","hass","hassio","hademo"];let m=[];o(88400);const p={},v={};(async()=>{const e=await(0,l.Jt)("_version",u);e?e!==h.version&&(await(0,l.IU)(u),(0,l.hZ)("_version",h.version,u)):(0,l.hZ)("_version",h.version,u)})();const y=(0,n.s)((()=>(async e=>{const t=Object.keys(e),o=await Promise.all(Object.values(e));u("readwrite",(i=>{o.forEach(((o,a)=>{Object.entries(o).forEach((([e,t])=>{i.put(t,e)})),delete e[t[a]]}))}))})(v)),2e3),k={};let _=(0,i.A)([(0,d.EM)("ha-icon")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.MZ)()],key:"icon",value:void 0},{kind:"field",decorators:[(0,d.wk)()],key:"_path",value:void 0},{kind:"field",decorators:[(0,d.wk)()],key:"_secondaryPath",value:void 0},{kind:"field",decorators:[(0,d.wk)()],key:"_viewBox",value:void 0},{kind:"field",decorators:[(0,d.wk)()],key:"_legacy",value:()=>!1},{kind:"method",key:"willUpdate",value:function(e){(0,a.A)(i,"willUpdate",this,3)([e]),e.has("icon")&&(this._path=void 0,this._secondaryPath=void 0,this._viewBox=void 0,this._loadIcon())}},{kind:"method",key:"render",value:function(){return this.icon?this._legacy?r.qy` <iron-icon .icon="${this.icon}"></iron-icon>`:r.qy`<ha-svg-icon .path="${this._path}" .secondaryPath="${this._secondaryPath}" .viewBox="${this._viewBox}"></ha-svg-icon>`:r.s6}},{kind:"method",key:"_loadIcon",value:async function(){if(!this.icon)return;const e=this.icon,[t,i]=this.icon.split(":",2);let a,r=i;if(!t||!r)return;if(!b.includes(t)){const o=c.y[t];return o?void(o&&"function"==typeof o.getIcon&&this._setCustomPath(o.getIcon(r),e)):void(this._legacy=!0)}if(this._legacy=!1,r in p){const e=p[r];let o;e.newName?(o=`Icon ${t}:${r} was renamed to ${t}:${e.newName}, please change your config, it will be removed in version ${e.removeIn}.`,r=e.newName):o=`Icon ${t}:${r} was removed from MDI, please replace this icon with an other icon in your config, it will be removed in version ${e.removeIn}.`,console.warn(o),(0,s.r)(this,"write_log",{level:"warning",message:o})}if(r in k)return void(this._path=k[r]);if("home-assistant"===r){const t=(await o.e(82782).then(o.bind(o,82782))).mdiHomeAssistant;return this.icon===e&&(this._path=t),void(k[r]=t)}try{a=await(e=>new Promise(((t,o)=>{m.push([e,t,o]),m.length>1||(0,f.h)(1e3,u("readonly",(e=>{for(const[t,o,i]of m)(0,l.Yd)(e.get(t)).then((e=>o(e))).catch((e=>i(e)));m=[]}))).catch((e=>{for(const[,,t]of m)t(e);m=[]}))})))(r)}catch(e){a=void 0}if(a)return this.icon===e&&(this._path=a),void(k[r]=a);const d=(e=>{let t;for(const o of h.parts){if(void 0!==o.start&&e<o.start)break;t=o}return t.file})(r);if(d in v)return void this._setPath(v[d],r,e);const n=fetch(`/static/mdi/${d}.json`).then((e=>e.json()));v[d]=n,this._setPath(n,r,e),y()}},{kind:"method",key:"_setCustomPath",value:async function(e,t){const o=await e;this.icon===t&&(this._path=o.path,this._secondaryPath=o.secondaryPath,this._viewBox=o.viewBox)}},{kind:"method",key:"_setPath",value:async function(e,t,o){const i=await e;this.icon===o&&(this._path=i[t]),k[t]=i[t]}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`:host{fill:currentcolor}`}}]}}),r.WF)},31511:(e,t,o)=>{var i=o(36312),a=o(15112),r=o(77706);(0,i.A)([(0,r.EM)("ha-input-helper-text")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return a.qy`<slot></slot>`}},{kind:"field",static:!0,key:"styles",value:()=>a.AH`:host{display:block;color:var(--mdc-text-field-label-ink-color,rgba(0,0,0,.6));font-size:.75rem;padding-left:16px;padding-right:16px;padding-inline-start:16px;padding-inline-end:16px}`}]}}),a.WF)},57464:(e,t,o)=>{o.r(t),o.d(t,{HaTemplateSelector:()=>c});var i=o(36312),a=o(15112),r=o(77706),d=o(34897),s=o(84976);o(31979),o(31511),o(13292);const n=["template:","sensor:","state:","trigger: template"];let c=(0,i.A)([(0,r.EM)("ha-selector-template")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value:()=>!0},{kind:"field",decorators:[(0,r.wk)()],key:"warn",value(){}},{kind:"method",key:"render",value:function(){return a.qy` ${this.warn?a.qy`<ha-alert alert-type="warning">${this.hass.localize("ui.components.selectors.template.yaml_warning",{string:this.warn})} <br> <a target="_blank" rel="noopener noreferrer" href="${(0,s.o)(this.hass,"/docs/configuration/templating/")}">${this.hass.localize("ui.components.selectors.template.learn_more")}</a></ha-alert>`:a.s6} ${this.label?a.qy`<p>${this.label}${this.required?"*":""}</p>`:a.s6} <ha-code-editor mode="jinja2" .hass="${this.hass}" .value="${this.value}" .readOnly="${this.disabled}" autofocus autocomplete-entities autocomplete-icons @value-changed="${this._handleChange}" dir="ltr" linewrap></ha-code-editor> ${this.helper?a.qy`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:a.s6} `}},{kind:"method",key:"_handleChange",value:function(e){const t=e.target.value;this.value!==t&&(this.warn=n.find((e=>t.includes(e))),(0,d.r)(this,"value-changed",{value:t}))}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`p{margin-top:0}`}}]}}),a.WF)},81235:(e,t,o)=>{o.d(t,{y:()=>d});const i=window;"customIconsets"in i||(i.customIconsets={});const a=i.customIconsets,r=window;"customIcons"in r||(r.customIcons={});const d=new Proxy(r.customIcons,{get:(e,t)=>e[t]??(a[t]?{getIcon:a[t]}:void 0)})},84976:(e,t,o)=>{o.d(t,{o:()=>i});const i=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`},75702:(e,t,o)=>{o.d(t,{IU:()=>c,Jt:()=>s,Yd:()=>i,hZ:()=>n,y$:()=>a});o(89655),o(253),o(54846),o(16891);function i(e){return new Promise(((t,o)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>o(e.error)}))}function a(e,t){const o=indexedDB.open(e);o.onupgradeneeded=()=>o.result.createObjectStore(t);const a=i(o);return(e,o)=>a.then((i=>o(i.transaction(t,e).objectStore(t))))}let r;function d(){return r||(r=a("keyval-store","keyval")),r}function s(e,t=d()){return t("readonly",(t=>i(t.get(e))))}function n(e,t,o=d()){return o("readwrite",(o=>(o.put(t,e),i(o.transaction))))}function c(e=d()){return e("readwrite",(e=>(e.clear(),i(e.transaction))))}}};
//# sourceMappingURL=57464.rG2ccCAkeSM.js.map