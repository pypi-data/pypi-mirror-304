export const id=9185;export const ids=[9185,13292];export const modules={13292:(e,t,i)=>{i.r(t);var o=i(36312),a=i(15112),n=i(77706),s=i(85323),r=i(34897);i(28066),i(88400);const l={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};(0,o.A)([(0,n.EM)("ha-alert")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)()],key:"title",value:()=>""},{kind:"field",decorators:[(0,n.MZ)({attribute:"alert-type"})],key:"alertType",value:()=>"info"},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"dismissable",value:()=>!1},{kind:"method",key:"render",value:function(){return a.qy` <div class="issue-type ${(0,s.H)({[this.alertType]:!0})}" role="alert"> <div class="icon ${this.title?"":"no-title"}"> <slot name="icon"> <ha-svg-icon .path="${l[this.alertType]}"></ha-svg-icon> </slot> </div> <div class="content"> <div class="main-content"> ${this.title?a.qy`<div class="title">${this.title}</div>`:""} <slot></slot> </div> <div class="action"> <slot name="action"> ${this.dismissable?a.qy`<ha-icon-button @click="${this._dismiss_clicked}" label="Dismiss alert" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}"></ha-icon-button>`:""} </slot> </div> </div> </div> `}},{kind:"method",key:"_dismiss_clicked",value:function(){(0,r.r)(this,"alert-dismissed-clicked")}},{kind:"field",static:!0,key:"styles",value:()=>a.AH`.issue-type{position:relative;padding:8px;display:flex}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:4px}.icon{z-index:1}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:0}.title{margin-top:2px;font-weight:700}.action ha-icon-button,.action mwc-button{--mdc-theme-primary:var(--primary-text-color);--mdc-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}`}]}}),a.WF)},43536:(e,t,i)=>{var o=i(36312),a=i(68689),n=(i(253),i(54846),i(64077)),s=(i(57597),i(68711)),r=i(15112),l=i(77706),d=i(10977),c=i(34897);i(28066),i(13830),i(90431);(0,s.SF)("vaadin-combo-box-item",r.AH`:host{padding:0!important}:host([focused]:not([disabled])){background-color:rgba(var(--rgb-primary-text-color,0,0,0),.12)}:host([selected]:not([disabled])){background-color:transparent;color:var(--mdc-theme-primary);--mdc-ripple-color:var(--mdc-theme-primary);--mdc-theme-text-primary-on-background:var(--mdc-theme-primary)}:host([selected]:not([disabled])):before{background-color:var(--mdc-theme-primary);opacity:.12;content:"";position:absolute;top:0;left:0;width:100%;height:100%}:host([selected][focused]:not([disabled])):before{opacity:.24}:host(:hover:not([disabled])){background-color:transparent}[part=content]{width:100%}[part=checkmark]{display:none}`);(0,o.A)([(0,l.EM)("ha-combo-box")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"validationMessage",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"invalid",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"icon",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"items",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"filteredItems",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"dataProvider",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:"allow-custom-value",type:Boolean})],key:"allowCustomValue",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({attribute:"item-value-path"})],key:"itemValuePath",value:()=>"value"},{kind:"field",decorators:[(0,l.MZ)({attribute:"item-label-path"})],key:"itemLabelPath",value:()=>"label"},{kind:"field",decorators:[(0,l.MZ)({attribute:"item-id-path"})],key:"itemIdPath",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"renderer",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({type:Boolean,reflect:!0})],key:"opened",value:()=>!1},{kind:"field",decorators:[(0,l.P)("vaadin-combo-box-light",!0)],key:"_comboBox",value:void 0},{kind:"field",decorators:[(0,l.P)("ha-textfield",!0)],key:"_inputElement",value:void 0},{kind:"field",key:"_overlayMutationObserver",value:void 0},{kind:"field",key:"_bodyMutationObserver",value:void 0},{kind:"method",key:"open",value:async function(){await this.updateComplete,this._comboBox?.open()}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this._inputElement?.updateComplete),this._inputElement?.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.A)(i,"disconnectedCallback",this,3)([]),this._overlayMutationObserver&&(this._overlayMutationObserver.disconnect(),this._overlayMutationObserver=void 0),this._bodyMutationObserver&&(this._bodyMutationObserver.disconnect(),this._bodyMutationObserver=void 0)}},{kind:"get",key:"selectedItem",value:function(){return this._comboBox.selectedItem}},{kind:"method",key:"setInputValue",value:function(e){this._comboBox.value=e}},{kind:"method",key:"render",value:function(){return r.qy` <vaadin-combo-box-light .itemValuePath="${this.itemValuePath}" .itemIdPath="${this.itemIdPath}" .itemLabelPath="${this.itemLabelPath}" .items="${this.items}" .value="${this.value||""}" .filteredItems="${this.filteredItems}" .dataProvider="${this.dataProvider}" .allowCustomValue="${this.allowCustomValue}" .disabled="${this.disabled}" .required="${this.required}" ${(0,n.d)(this.renderer||this._defaultRowRenderer)} @opened-changed="${this._openedChanged}" @filter-changed="${this._filterChanged}" @value-changed="${this._valueChanged}" attr-for-value="value"> <ha-textfield label="${(0,d.J)(this.label)}" placeholder="${(0,d.J)(this.placeholder)}" ?disabled="${this.disabled}" ?required="${this.required}" validationMessage="${(0,d.J)(this.validationMessage)}" .errorMessage="${this.errorMessage}" class="input" autocapitalize="none" autocomplete="off" autocorrect="off" input-spellcheck="false" .suffix="${r.qy`<div style="width:28px" role="none presentation"></div>`}" .icon="${this.icon}" .invalid="${this.invalid}" .helper="${this.helper}" helperPersistent> <slot name="icon" slot="leadingIcon"></slot> </ha-textfield> ${this.value?r.qy`<ha-svg-icon role="button" tabindex="-1" aria-label="${(0,d.J)(this.hass?.localize("ui.common.clear"))}" class="clear-button" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" @click="${this._clearValue}"></ha-svg-icon>`:""} <ha-svg-icon role="button" tabindex="-1" aria-label="${(0,d.J)(this.label)}" aria-expanded="${this.opened?"true":"false"}" class="toggle-button" .path="${this.opened?"M7,15L12,10L17,15H7Z":"M7,10L12,15L17,10H7Z"}" @click="${this._toggleOpen}"></ha-svg-icon> </vaadin-combo-box-light> `}},{kind:"field",key:"_defaultRowRenderer",value(){return e=>r.qy`<ha-list-item> ${this.itemLabelPath?e[this.itemLabelPath]:e} </ha-list-item>`}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),(0,c.r)(this,"value-changed",{value:void 0})}},{kind:"method",key:"_toggleOpen",value:function(e){this.opened?(this._comboBox?.close(),e.stopPropagation()):this._comboBox?.inputElement.focus()}},{kind:"method",key:"_openedChanged",value:function(e){e.stopPropagation();const t=e.detail.value;if(setTimeout((()=>{this.opened=t}),0),(0,c.r)(this,"opened-changed",{value:e.detail.value}),t){const e=document.querySelector("vaadin-combo-box-overlay");e&&this._removeInert(e),this._observeBody()}else this._bodyMutationObserver?.disconnect(),this._bodyMutationObserver=void 0}},{kind:"method",key:"_observeBody",value:function(){"MutationObserver"in window&&!this._bodyMutationObserver&&(this._bodyMutationObserver=new MutationObserver((e=>{e.forEach((e=>{e.addedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&this._removeInert(e)})),e.removedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0)}))}))})),this._bodyMutationObserver.observe(document.body,{childList:!0}))}},{kind:"method",key:"_removeInert",value:function(e){if(e.inert)return e.inert=!1,this._overlayMutationObserver?.disconnect(),void(this._overlayMutationObserver=void 0);"MutationObserver"in window&&!this._overlayMutationObserver&&(this._overlayMutationObserver=new MutationObserver((e=>{e.forEach((e=>{if("inert"===e.attributeName){const t=e.target;t.inert&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0,t.inert=!1)}}))})),this._overlayMutationObserver.observe(e,{attributes:!0}))}},{kind:"method",key:"_filterChanged",value:function(e){e.stopPropagation(),(0,c.r)(this,"filter-changed",{value:e.detail.value})}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this.allowCustomValue||(this._comboBox._closeOnBlurIsPrevented=!0);const t=e.detail.value;t!==this.value&&(0,c.r)(this,"value-changed",{value:t||void 0})}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`:host{display:block;width:100%}vaadin-combo-box-light{position:relative;--vaadin-combo-box-overlay-max-height:calc(45vh - 56px)}ha-textfield{width:100%}ha-textfield>ha-icon-button{--mdc-icon-button-size:24px;padding:2px;color:var(--secondary-text-color)}ha-svg-icon{color:var(--input-dropdown-icon-color);position:absolute;cursor:pointer}.toggle-button{right:12px;top:-10px;inset-inline-start:initial;inset-inline-end:12px;direction:var(--direction)}:host([opened]) .toggle-button{color:var(--primary-color)}.clear-button{--mdc-icon-size:20px;top:-7px;right:36px;inset-inline-start:initial;inset-inline-end:36px;direction:var(--direction)}`}}]}}),r.WF)},85288:(e,t,i)=>{i.r(t),i.d(t,{HaIconPicker:()=>v});var o=i(36312),a=(i(89655),i(24545),i(51855),i(82130),i(31743),i(22328),i(4959),i(62435),i(253),i(2075),i(54846),i(16891),i(4525),i(15112)),n=i(77706),s=i(94100),r=i(34897),l=i(81235);i(43536),i(13830),i(20144);let d=[],c=!1;const h=async e=>{try{const t=l.y[e].getIconList;if("function"!=typeof t)return[];const i=await t();return i.map((t=>({icon:`${e}:${t.name}`,parts:new Set(t.name.split("-")),keywords:t.keywords??[]})))}catch(t){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},u=e=>a.qy`<ha-list-item graphic="avatar"> <ha-icon .icon="${e.icon}" slot="graphic"></ha-icon> ${e.icon} </ha-list-item>`;let v=(0,o.A)([(0,n.EM)("ha-icon-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"invalid",value:()=>!1},{kind:"method",key:"render",value:function(){return a.qy` <ha-combo-box .hass="${this.hass}" item-value-path="icon" item-label-path="icon" .value="${this._value}" allow-custom-value .dataProvider="${c?this._iconProvider:void 0}" .label="${this.label}" .helper="${this.helper}" .disabled="${this.disabled}" .required="${this.required}" .placeholder="${this.placeholder}" .errorMessage="${this.errorMessage}" .invalid="${this.invalid}" .renderer="${u}" icon @opened-changed="${this._openedChanged}" @value-changed="${this._valueChanged}"> ${this._value||this.placeholder?a.qy` <ha-icon .icon="${this._value||this.placeholder}" slot="icon"> </ha-icon> `:a.qy`<slot slot="icon" name="fallback"></slot>`} </ha-combo-box> `}},{kind:"field",key:"_filterIcons",value:()=>(0,s.A)(((e,t=d)=>{if(!e)return t;const i=[],o=(e,t)=>i.push({icon:e,rank:t});for(const i of t)i.parts.has(e)?o(i.icon,1):i.keywords.includes(e)?o(i.icon,2):i.icon.includes(e)?o(i.icon,3):i.keywords.some((t=>t.includes(e)))&&o(i.icon,4);return 0===i.length&&o(e,0),i.sort(((e,t)=>e.rank-t.rank))}))},{kind:"field",key:"_iconProvider",value(){return(e,t)=>{const i=this._filterIcons(e.filter.toLowerCase(),d),o=e.page*e.pageSize,a=o+e.pageSize;t(i.slice(o,a),i.length)}}},{kind:"method",key:"_openedChanged",value:async function(e){e.detail.value&&!c&&(await(async()=>{c=!0;const e=await i.e(25143).then(i.t.bind(i,25143,19));d=e.default.map((e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords})));const t=[];Object.keys(l.y).forEach((e=>{t.push(h(e))})),(await Promise.all(t)).forEach((e=>{d.push(...e)}))})(),this.requestUpdate())}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this._setValue(e.detail.value)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,(0,r.r)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`[slot=icon]{color:var(--primary-text-color);position:relative;bottom:2px}[slot=prefix]{margin-right:8px;margin-inline-end:8px;margin-inline-start:initial}`}}]}}),a.WF)},24640:(e,t,i)=>{var o=i(36312),a=i(15112),n=i(77706);(0,o.A)([(0,n.EM)("ha-settings-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"three-line"})],key:"threeLine",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"wrap-heading",reflect:!0})],key:"wrapHeading",value:()=>!1},{kind:"method",key:"render",value:function(){return a.qy` <div class="prefix-wrap"> <slot name="prefix"></slot> <div class="body" ?two-line="${!this.threeLine}" ?three-line="${this.threeLine}"> <slot name="heading"></slot> <div class="secondary"><slot name="description"></slot></div> </div> </div> <div class="content"><slot></slot></div> `}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`:host{display:flex;padding:0 16px;align-content:normal;align-self:auto;align-items:center}.body{padding-top:8px;padding-bottom:8px;padding-left:0;padding-inline-start:0;padding-right:16x;padding-inline-end:16px;overflow:hidden;display:var(--layout-vertical_-_display);flex-direction:var(--layout-vertical_-_flex-direction);justify-content:var(--layout-center-justified_-_justify-content);flex:var(--layout-flex_-_flex);flex-basis:var(--layout-flex_-_flex-basis)}.body[three-line]{min-height:var(--paper-item-body-three-line-min-height,88px)}:host(:not([wrap-heading])) body>*{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.body>.secondary{display:block;padding-top:4px;font-family:var(
          --mdc-typography-body2-font-family,
          var(--mdc-typography-font-family, Roboto, sans-serif)
        );-webkit-font-smoothing:antialiased;font-size:var(--mdc-typography-body2-font-size, .875rem);font-weight:var(--mdc-typography-body2-font-weight,400);line-height:normal;color:var(--secondary-text-color)}.body[two-line]{min-height:calc(var(--paper-item-body-two-line-min-height,72px) - 16px);flex:1}.content{display:contents}:host(:not([narrow])) .content{display:var(--settings-row-content-display,flex);justify-content:flex-end;flex:1;padding:16px 0}.content ::slotted(*){width:var(--settings-row-content-width)}:host([narrow]){align-items:normal;flex-direction:column;border-top:1px solid var(--divider-color);padding-bottom:8px}::slotted(ha-switch){padding:16px 0}.secondary{white-space:normal}.prefix-wrap{display:var(--settings-row-prefix-display)}:host([narrow]) .prefix-wrap{display:flex;align-items:center}`}}]}}),a.WF)},19401:(e,t,i)=>{var o=i(36312),a=(i(72606),i(15112)),n=i(77706),s=i(34897),r=(i(13292),i(3276)),l=(i(85288),i(24640),i(90431),i(94929)),d=i(55321),c=(i(89655),i(16891),i(85323)),h=i(94100),u=i(55792),v=(i(43536),i(28066),i(13830),i(88400),i(8640)),p=i(20712),y=i(34336);const m="___ADD_NEW___",g="___NO_CATEGORIES___",k="___ADD_NEW_SUGGESTION___",f=e=>a.qy`<ha-list-item graphic="icon" class="${(0,c.H)({"add-new":e.category_id===m})}"> ${e.icon?a.qy`<ha-icon slot="graphic" .icon="${e.icon}"></ha-icon>`:a.qy`<ha-svg-icon .path="${"M5.5,7A1.5,1.5 0 0,1 4,5.5A1.5,1.5 0 0,1 5.5,4A1.5,1.5 0 0,1 7,5.5A1.5,1.5 0 0,1 5.5,7M21.41,11.58L12.41,2.58C12.05,2.22 11.55,2 11,2H4C2.89,2 2,2.89 2,4V11C2,11.55 2.22,12.05 2.59,12.41L11.58,21.41C11.95,21.77 12.45,22 13,22C13.55,22 14.05,21.77 14.41,21.41L21.41,14.41C21.78,14.05 22,13.55 22,13C22,12.44 21.77,11.94 21.41,11.58Z"}" slot="graphic"></ha-svg-icon>`} ${e.name} </ha-list-item>`;(0,o.A)([(0,n.EM)("ha-category-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"scope",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"no-add"})],key:"noAdd",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[(0,n.wk)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_categories",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:()=>["scope"]},{kind:"method",key:"hassSubscribe",value:function(){return[(0,v.Ar)(this.hass.connection,this.scope,(e=>{this._categories=e}))]}},{kind:"field",key:"_suggestion",value:void 0},{kind:"field",key:"_init",value:()=>!1},{kind:"method",key:"open",value:async function(){await this.updateComplete,await(this.comboBox?.open())}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this.comboBox?.focus())}},{kind:"field",key:"_getCategories",value(){return(0,h.A)(((e,t)=>{const i=e?[...e]:[];return i?.length||i.push({category_id:g,name:this.hass.localize("ui.components.category-picker.no_categories"),icon:null}),t?i:[...i,{category_id:m,name:this.hass.localize("ui.components.category-picker.add_new"),icon:"mdi:plus"}]}))}},{kind:"method",key:"updated",value:function(e){if(!this._init&&this.hass&&this._categories||this._init&&e.has("_opened")&&this._opened){this._init=!0;const e=this._getCategories(this._categories,this.noAdd).map((e=>({...e,strings:[e.name]})));this.comboBox.items=e,this.comboBox.filteredItems=e}}},{kind:"method",key:"render",value:function(){return this._categories?a.qy` <ha-combo-box .hass="${this.hass}" .helper="${this.helper}" item-value-path="category_id" item-id-path="category_id" item-label-path="name" .value="${this._value}" .disabled="${this.disabled}" .required="${this.required}" .label="${void 0===this.label&&this.hass?this.hass.localize("ui.components.category-picker.category"):this.label}" .placeholder="${this.placeholder}" .renderer="${f}" @filter-changed="${this._filterChanged}" @opened-changed="${this._openedChanged}" @value-changed="${this._categoryChanged}"> </ha-combo-box> `:a.s6}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.target,i=e.detail.value;if(!i)return void(this.comboBox.filteredItems=this.comboBox.items);const o=(0,u.H)(i,t.items?.filter((e=>![g,m].includes(e.category_id)))||[]);0===o?.length?this.noAdd?this.comboBox.filteredItems=[{category_id:g,name:this.hass.localize("ui.components.category-picker.no_match"),icon:null}]:(this._suggestion=i,this.comboBox.filteredItems=[{category_id:k,name:this.hass.localize("ui.components.category-picker.add_new_sugestion",{name:this._suggestion}),icon:"mdi:plus"}]):this.comboBox.filteredItems=o}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_categoryChanged",value:function(e){e.stopPropagation();let t=e.detail.value;if(t===g)return t="",void this.comboBox.setInputValue("");[k,m].includes(t)?(e.target.value=this._value,this.hass.loadFragmentTranslation("config"),(0,y.S)(this,{scope:this.scope,suggestedName:t===k?this._suggestion:"",createEntry:async e=>{const t=await(0,v.s_)(this.hass,this.scope,e);return this._categories=[...this._categories,t],this.comboBox.filteredItems=this._getCategories(this._categories,this.noAdd),await this.updateComplete,await this.comboBox.updateComplete,this._setValue(t.category_id),t}}),this._suggestion=void 0,this.comboBox.setInputValue("")):t!==this._value&&this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,s.r)(this,"value-changed",{value:e}),(0,s.r)(this,"change")}),0)}}]}}),(0,p.E)(a.WF)),(0,o.A)([(0,n.EM)("dialog-assign-category")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_scope",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_category",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_submitting",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._scope=e.scope,this._category=e.entityReg.categories[e.scope],this._error=void 0}},{kind:"method",key:"closeDialog",value:function(){this._error="",this._params=void 0,(0,s.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params)return a.s6;const e=this._params.entityReg.categories[this._params.scope];return a.qy` <ha-dialog open @closed="${this.closeDialog}" .heading="${(0,r.l)(this.hass,e?this.hass.localize("ui.panel.config.category.assign.edit"):this.hass.localize("ui.panel.config.category.assign.assign"))}"> <div> ${this._error?a.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""} <div class="form"> <ha-category-picker .hass="${this.hass}" .scope="${this._scope}" .value="${this._category}" @value-changed="${this._categoryChanged}"></ha-category-picker> </div> </div> <mwc-button slot="secondaryAction" @click="${this.closeDialog}"> ${this.hass.localize("ui.common.cancel")} </mwc-button> <mwc-button slot="primaryAction" @click="${this._updateEntry}" .disabled="${this._submitting}"> ${this.hass.localize("ui.common.save")} </mwc-button> </ha-dialog> `}},{kind:"method",key:"_categoryChanged",value:function(e){e.detail.value||(this._category=void 0),this._category=e.detail.value}},{kind:"method",key:"_updateEntry",value:async function(){this._submitting=!0,this._error=void 0;try{await(0,l.G_)(this.hass,this._params.entityReg.entity_id,{categories:{[this._scope]:this._category||null}}),this.closeDialog()}catch(e){this._error=e.message||this.hass.localize("ui.panel.config.category.assign.unknown_error")}finally{this._submitting=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return[d.nA,a.AH`ha-icon-picker,ha-textfield{display:block;margin-bottom:16px}`]}}]}}),a.WF)},25517:(e,t,i)=>{var o=i(18816),a=i(56674),n=i(1370),s=i(36810);e.exports=function(e,t){t&&"string"==typeof e||a(e);var i=s(e);return n(a(void 0!==i?o(i,e):e))}},32137:(e,t,i)=>{var o=i(41765),a=i(18816),n=i(95689),s=i(56674),r=i(1370),l=i(25517),d=i(78211),c=i(91228),h=i(53982),u=d((function(){for(var e,t,i=this.iterator,o=this.mapper;;){if(t=this.inner)try{if(!(e=s(a(t.next,t.iterator))).done)return e.value;this.inner=null}catch(e){c(i,"throw",e)}if(e=s(a(this.next,i)),this.done=!!e.done)return;try{this.inner=l(o(e.value,this.counter++),!1)}catch(e){c(i,"throw",e)}}}));o({target:"Iterator",proto:!0,real:!0,forced:h},{flatMap:function(e){return s(this),n(e),new u(r(this),{mapper:e,inner:null})}})}};
//# sourceMappingURL=9185.Dc1zAY2Z2NE.js.map