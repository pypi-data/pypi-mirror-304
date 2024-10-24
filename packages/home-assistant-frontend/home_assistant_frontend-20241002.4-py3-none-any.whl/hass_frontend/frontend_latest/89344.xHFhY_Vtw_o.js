export const id=89344;export const ids=[89344];export const modules={6482:(e,t,i)=>{var a=i(36312),s=i(15112),n=i(77706),o=i(34897);i(54223);(0,a.A)([(0,n.EM)("ha-aliases-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"aliases",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"method",key:"render",value:function(){return this.aliases?s.qy` <ha-multi-textfield .hass="${this.hass}" .value="${this.aliases}" .disabled="${this.disabled}" .label="${this.hass.localize("ui.dialogs.aliases.label")}" .removeLabel="${this.hass.localize("ui.dialogs.aliases.remove")}" .addLabel="${this.hass.localize("ui.dialogs.aliases.add")}" item-index @value-changed="${this._aliasesChanged}"> </ha-multi-textfield> `:s.s6}},{kind:"method",key:"_aliasesChanged",value:function(e){(0,o.r)(this,"value-changed",{value:e})}}]}}),s.WF)},77372:(e,t,i)=>{var a=i(36312),s=i(72606),n=i(15112),o=i(77706),l=i(49141);(0,a.A)([(0,o.EM)("ha-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value:()=>[l.R,n.AH`::slotted([slot=icon]){margin-inline-start:0px;margin-inline-end:8px;direction:var(--direction);display:block}.mdc-button{height:var(--button-height,36px)}.trailing-icon{display:flex}.slot-container{overflow:var(--button-slot-container-overflow,visible)}`]}]}}),s.Button)},98515:(e,t,i)=>{var a=i(36312),s=i(68689),n=i(15112),o=i(6811),l=i(43385),d=i(43389),r=i(77706),c=i(34897);(0,a.A)([(0,r.EM)("ha-check-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"onChange",value:async function(e){(0,s.A)(i,"onChange",this,3)([e]),(0,c.r)(this,e.type)}},{kind:"field",static:!0,key:"styles",value:()=>[d.R,l.R,n.AH`:host{--mdc-theme-secondary:var(--primary-color)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic{margin-inline-end:var(--mdc-list-item-graphic-margin,16px);margin-inline-start:0px;direction:var(--direction)}.mdc-deprecated-list-item__meta{flex-shrink:0;direction:var(--direction);margin-inline-start:auto;margin-inline-end:0}.mdc-deprecated-list-item__graphic{margin-top:var(--check-list-item-graphic-margin-top)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{margin-inline-start:0;margin-inline-end:var(--mdc-list-item-graphic-margin,32px)}`]}]}}),o.h)},54223:(e,t,i)=>{var a=i(36312),s=(i(16891),i(15112)),n=i(77706),o=i(34897),l=i(55321);i(77372),i(28066),i(90431);(0,a.A)([(0,n.EM)("ha-multi-textfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"inputType",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"inputSuffix",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"inputPrefix",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"autocomplete",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"addLabel",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"removeLabel",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"item-index",type:Boolean})],key:"itemIndex",value:()=>!1},{kind:"method",key:"render",value:function(){return s.qy` ${this._items.map(((e,t)=>{const i=""+(this.itemIndex?` ${t+1}`:"");return s.qy` <div class="layout horizontal center-center row"> <ha-textfield .suffix="${this.inputSuffix}" .prefix="${this.inputPrefix}" .type="${this.inputType}" .autocomplete="${this.autocomplete}" .disabled="${this.disabled}" dialogInitialFocus="${t}" .index="${t}" class="flex-auto" .label="${""+(this.label?`${this.label}${i}`:"")}" .value="${e}" ?data-last="${t===this._items.length-1}" @input="${this._editItem}" @keydown="${this._keyDown}"></ha-textfield> <ha-icon-button .disabled="${this.disabled}" .index="${t}" slot="navigationIcon" .label="${this.removeLabel??this.hass?.localize("ui.common.remove")??"Remove"}" @click="${this._removeItem}" .path="${"M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19M8,9H16V19H8V9M15.5,4L14.5,3H9.5L8.5,4H5V6H19V4H15.5Z"}"></ha-icon-button> </div> `}))} <div class="layout horizontal center-center"> <ha-button @click="${this._addItem}" .disabled="${this.disabled}"> ${this.addLabel??this.hass?.localize("ui.common.add")??"Add"} <ha-svg-icon slot="icon" .path="${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}"></ha-svg-icon> </ha-button> </div> `}},{kind:"get",key:"_items",value:function(){return this.value??[]}},{kind:"method",key:"_addItem",value:async function(){const e=[...this._items,""];this._fireChanged(e),await this.updateComplete;const t=this.shadowRoot?.querySelector("ha-textfield[data-last]");t?.focus()}},{kind:"method",key:"_editItem",value:async function(e){const t=e.target.index,i=[...this._items];i[t]=e.target.value,this._fireChanged(i)}},{kind:"method",key:"_keyDown",value:async function(e){"Enter"===e.key&&(e.stopPropagation(),this._addItem())}},{kind:"method",key:"_removeItem",value:async function(e){const t=e.target.index,i=[...this._items];i.splice(t,1),this._fireChanged(i)}},{kind:"method",key:"_fireChanged",value:function(e){this.value=e,(0,o.r)(this,"value-changed",{value:e})}},{kind:"get",static:!0,key:"styles",value:function(){return[l.RF,s.AH`.row{margin-bottom:8px}ha-textfield{display:block}ha-icon-button{display:block}ha-button{margin-left:8px;margin-inline-start:8px;margin-inline-end:initial}`]}}]}}),s.WF)},24640:(e,t,i)=>{var a=i(36312),s=i(15112),n=i(77706);(0,a.A)([(0,n.EM)("ha-settings-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"three-line"})],key:"threeLine",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"wrap-heading",reflect:!0})],key:"wrapHeading",value:()=>!1},{kind:"method",key:"render",value:function(){return s.qy` <div class="prefix-wrap"> <slot name="prefix"></slot> <div class="body" ?two-line="${!this.threeLine}" ?three-line="${this.threeLine}"> <slot name="heading"></slot> <div class="secondary"><slot name="description"></slot></div> </div> </div> <div class="content"><slot></slot></div> `}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`:host{display:flex;padding:0 16px;align-content:normal;align-self:auto;align-items:center}.body{padding-top:8px;padding-bottom:8px;padding-left:0;padding-inline-start:0;padding-right:16x;padding-inline-end:16px;overflow:hidden;display:var(--layout-vertical_-_display);flex-direction:var(--layout-vertical_-_flex-direction);justify-content:var(--layout-center-justified_-_justify-content);flex:var(--layout-flex_-_flex);flex-basis:var(--layout-flex_-_flex-basis)}.body[three-line]{min-height:var(--paper-item-body-three-line-min-height,88px)}:host(:not([wrap-heading])) body>*{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.body>.secondary{display:block;padding-top:4px;font-family:var(
          --mdc-typography-body2-font-family,
          var(--mdc-typography-font-family, Roboto, sans-serif)
        );-webkit-font-smoothing:antialiased;font-size:var(--mdc-typography-body2-font-size, .875rem);font-weight:var(--mdc-typography-body2-font-weight,400);line-height:normal;color:var(--secondary-text-color)}.body[two-line]{min-height:calc(var(--paper-item-body-two-line-min-height,72px) - 16px);flex:1}.content{display:contents}:host(:not([narrow])) .content{display:var(--settings-row-content-display,flex);justify-content:flex-end;flex:1;padding:16px 0}.content ::slotted(*){width:var(--settings-row-content-width)}:host([narrow]){align-items:normal;flex-direction:column;border-top:1px solid var(--divider-color);padding-bottom:8px}::slotted(ha-switch){padding:16px 0}.secondary{white-space:normal}.prefix-wrap{display:var(--settings-row-prefix-display)}:host([narrow]) .prefix-wrap{display:flex;align-items:center}`}}]}}),s.WF)},59588:(e,t,i)=>{var a=i(36312),s=i(68689),n=i(71204),o=i(15031),l=i(15112),d=i(77706),r=i(39914);(0,a.A)([(0,d.EM)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){(0,s.A)(i,"firstUpdated",this,3)([]),this.addEventListener("change",(()=>{this.haptic&&(0,r.j)("light")}))}},{kind:"field",static:!0,key:"styles",value:()=>[o.R,l.AH`:host{--mdc-theme-secondary:var(--switch-checked-color)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:var(--switch-checked-button-color);border-color:var(--switch-checked-button-color)}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:var(--switch-checked-track-color);border-color:var(--switch-checked-track-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:var(--switch-unchecked-button-color);border-color:var(--switch-unchecked-button-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:var(--switch-unchecked-track-color);border-color:var(--switch-unchecked-track-color)}`]}]}}),n.U)},89344:(e,t,i)=>{i.r(t);var a=i(36312),s=(i(253),i(2075),i(16891),i(4525),i(72606),i(63893),i(15112)),n=i(77706),o=i(10977),l=i(94100),d=i(34897),r=i(19244),c=(i(98515),i(72829),i(47572)),h=i(55321);i(28019);(0,a.A)([(0,n.EM)("dialog-expose-entity")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_filter",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_selected",value:()=>[]},{kind:"method",key:"showDialog",value:async function(e){this._params=e}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._selected=[],this._filter=void 0,(0,d.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params)return s.s6;const e=this.hass.localize("ui.panel.config.voice_assistants.expose.expose_dialog.header"),t=this._filterEntities(this._params.exposedEntities,this._filter);return s.qy` <ha-dialog open @closed="${this.closeDialog}" .heading="${e}"> <ha-dialog-header slot="heading" show-border> <h2 class="header" slot="title"> ${e} <span class="subtitle"> ${this.hass.localize("ui.panel.config.voice_assistants.expose.expose_dialog.expose_to",{assistants:this._params.filterAssistants.map((e=>c.aK[e].name)).join(", ")})} </span> </h2> <ha-icon-button .label="${this.hass.localize("ui.dialogs.generic.close")}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" dialogAction="close" slot="navigationIcon"></ha-icon-button> <search-input .hass="${this.hass}" .filter="${this._filter}" @value-changed="${this._filterChanged}"></search-input> </ha-dialog-header> <mwc-list multi> <lit-virtualizer scroller class="ha-scrollbar" @click="${this._itemClicked}" .items="${t}" .renderItem="${this._renderItem}"> </lit-virtualizer> </mwc-list> <mwc-button slot="primaryAction" @click="${this._expose}" .disabled="${0===this._selected.length}"> ${this.hass.localize("ui.panel.config.voice_assistants.expose.expose_dialog.expose_entities",{count:this._selected.length})} </mwc-button> </ha-dialog> `}},{kind:"field",key:"_handleSelected",value(){return e=>{const t=e.target.value;if(e.detail.selected){if(this._selected.includes(t))return;this._selected=[...this._selected,t]}else this._selected=this._selected.filter((e=>e!==t))}}},{kind:"method",key:"_itemClicked",value:function(e){const t=e.target.closest("ha-check-list-item");t.selected=!t.selected}},{kind:"method",key:"_filterChanged",value:function(e){this._filter=e.detail.value}},{kind:"field",key:"_filterEntities",value(){return(0,l.A)(((e,t)=>{const i=t?.toLowerCase();return Object.values(this.hass.states).filter((t=>this._params.filterAssistants.some((i=>!e[t.entity_id]?.[i]))&&(!i||t.entity_id.toLowerCase().includes(i)||(0,r.u)(t)?.toLowerCase().includes(i))))}))}},{kind:"field",key:"_renderItem",value(){return e=>s.qy` <ha-check-list-item graphic="icon" twoLine .value="${e.entity_id}" .selected="${this._selected.includes(e.entity_id)}" @request-selected="${this._handleSelected}"> <ha-state-icon title="${(0,o.J)(e?.state)}" slot="graphic" .hass="${this.hass}" .stateObj="${e}"></ha-state-icon> ${(0,r.u)(e)} <span slot="secondary">${e.entity_id}</span> </ha-check-list-item> `}},{kind:"method",key:"_expose",value:function(){this._params.exposeEntities(this._selected),this.closeDialog()}},{kind:"get",static:!0,key:"styles",value:function(){return[h.RF,s.AH`ha-dialog{--dialog-content-padding:0;--mdc-dialog-min-width:500px;--mdc-dialog-max-width:600px}mwc-list{position:relative}lit-virtualizer{height:500px}search-input{width:100%;display:block;box-sizing:border-box;--text-field-suffix-padding-left:8px}.header{margin:0;pointer-events:auto;-webkit-font-smoothing:antialiased;font-weight:inherit;font-size:inherit;box-sizing:border-box;display:flex;flex-direction:column;margin:-4px 0}.subtitle{color:var(--secondary-text-color);font-size:1rem;line-height:normal}lit-virtualizer{width:100%;contain:size layout!important}ha-check-list-item{width:100%;height:72px}ha-check-list-item ha-state-icon{margin-left:24px;margin-inline-start:24px;margin-inline-end:initial}@media all and (max-height:800px){lit-virtualizer{height:334px}}@media all and (max-height:600px){lit-virtualizer{height:238px}}@media all and (max-width:500px),all and (max-height:500px){ha-dialog{--mdc-dialog-min-width:calc(
              100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
            );--mdc-dialog-max-width:calc(
              100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
            );--mdc-dialog-min-height:100%;--mdc-dialog-max-height:100%;--vertical-align-dialog:flex-end;--ha-dialog-border-radius:0px}lit-virtualizer{height:calc(100vh - 198px)}search-input{--text-field-suffix-padding-left:unset}ha-check-list-item ha-state-icon{margin-left:8px;margin-inline-start:8px;margin-inline-end:initial}}`]}}]}}),s.WF)},28019:(e,t,i)=>{var a=i(36312),s=(i(253),i(2075),i(16891),i(4525),i(15112)),n=i(77706),o=i(94100),l=i(33922),d=i(34897),r=i(92389),c=(i(6482),i(24640),i(59588),i(86181)),h=i(86127),u=i(94929),p=i(53368),g=i(47572),m=i(20712),y=i(55321),v=i(51842),f=i(84976);(0,a.A)([(0,n.EM)("entity-voice-settings")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"entityId",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"exposed",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"entry",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_cloudStatus",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_aliases",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_googleEntity",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_unsupported",value:()=>({})},{kind:"method",key:"willUpdate",value:function(e){(0,l.x)(this.hass,"cloud")&&(e.has("entityId")&&this.entityId&&this._fetchEntities(),this.hasUpdated||(0,h.eN)(this.hass).then((e=>{this._cloudStatus=e})))}},{kind:"method",key:"_fetchEntities",value:async function(){try{const e=await(0,p.kz)(this.hass,this.entityId);this._googleEntity=e,this.requestUpdate("_googleEntity")}catch(e){"not_supported"===e.code&&(this._unsupported["cloud.google_assistant"]=!0,this.requestUpdate("_unsupported"))}try{await(0,c.Gk)(this.hass,this.entityId)}catch(e){"not_supported"===e.code&&(this._unsupported["cloud.alexa"]=!0,this.requestUpdate("_unsupported"))}}},{kind:"field",key:"_getEntityFilterFuncs",value:()=>(0,o.A)(((e,t)=>({google:(0,r._)(e.include_domains,e.include_entities,e.exclude_domains,e.exclude_entities),alexa:(0,r._)(t.include_domains,t.include_entities,t.exclude_domains,t.exclude_entities)})))},{kind:"method",key:"render",value:function(){const e=!0===this._cloudStatus?.logged_in&&!0===this._cloudStatus.prefs.google_enabled,t=!0===this._cloudStatus?.logged_in&&!0===this._cloudStatus.prefs.alexa_enabled,i=[...Object.keys(g.aK)],a=[...i],n=t&&!(0,r.e)(this._cloudStatus.alexa_entities),o=e&&!(0,r.e)(this._cloudStatus.google_entities);e?o&&a.splice(a.indexOf("cloud.google_assistant"),1):(i.splice(i.indexOf("cloud.google_assistant"),1),a.splice(i.indexOf("cloud.google_assistant"),1)),t?n&&a.splice(a.indexOf("cloud.alexa"),1):(i.splice(i.indexOf("cloud.alexa"),1),a.splice(a.indexOf("cloud.alexa"),1));const l=a.some((e=>this.exposed[e]));let d;(n||o)&&(d=this._getEntityFilterFuncs(this._cloudStatus.google_entities,this._cloudStatus.alexa_entities));const c=n&&d.alexa(this.entityId),h=o&&d.google(this.entityId),u=l||c||h;return s.qy` <ha-settings-row> <h3 slot="heading"> ${this.hass.localize("ui.dialogs.voice-settings.expose_header")} </h3> <ha-switch @change="${this._toggleAll}" .assistants="${a}" .checked="${u}"></ha-switch> </ha-settings-row> ${u?i.map((e=>{const t=!this._unsupported[e],i=n&&"cloud.alexa"===e?c:o&&"cloud.google_assistant"===e?h:this.exposed[e],a=n&&"cloud.alexa"===e||o&&"cloud.google_assistant"===e,l="cloud.google_assistant"===e&&!o&&t&&this._googleEntity?.might_2fa;return s.qy` <ha-settings-row .threeLine="${!t&&a}"> <img alt="" src="${(0,v.MR)({domain:g.aK[e].domain,type:"icon",darkOptimized:this.hass.themes?.darkMode})}" crossorigin="anonymous" referrerpolicy="no-referrer" slot="prefix"> <span slot="heading">${g.aK[e].name}</span> ${t?s.s6:s.qy`<div slot="description" class="unsupported"> <ha-svg-icon .path="${"M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"}"></ha-svg-icon> ${this.hass.localize("ui.dialogs.voice-settings.unsupported")} </div>`} ${a?s.qy` <div slot="description"> ${this.hass.localize("ui.dialogs.voice-settings.manual_config")} </div> `:s.s6} ${l?s.qy` <ha-formfield slot="description" .label="${this.hass.localize("ui.dialogs.voice-settings.ask_pin")}"> <ha-checkbox .checked="${!this._googleEntity.disable_2fa}" @change="${this._2faChanged}"></ha-checkbox> </ha-formfield> `:s.s6} <ha-switch .assistant="${e}" @change="${this._toggleAssistant}" .disabled="${a||!i&&!t}" .checked="${i}"></ha-switch> </ha-settings-row> `})):s.s6} <h3 class="header"> ${this.hass.localize("ui.dialogs.voice-settings.aliases_header")} </h3> <p class="description"> ${this.hass.localize("ui.dialogs.voice-settings.aliases_description")} </p> ${this.entry?s.qy`<ha-aliases-editor .hass="${this.hass}" .aliases="${this._aliases??this.entry.aliases}" @value-changed="${this._aliasesChanged}" @blur="${this._saveAliases}"></ha-aliases-editor>`:s.qy`<ha-alert alert-type="warning"> ${this.hass.localize("ui.dialogs.voice-settings.aliases_no_unique_id",{faq_link:s.qy`<a href="${(0,f.o)(this.hass,"/faq/unique_id")}" target="_blank" rel="noreferrer">${this.hass.localize("ui.dialogs.entity_registry.faq")}</a>`})} </ha-alert>`} `}},{kind:"method",key:"_aliasesChanged",value:function(e){const t=this._aliases?.length??this.entry?.aliases?.length??0;this._aliases=e.detail.value,t>e.detail.value.length&&this._saveAliases()}},{kind:"method",key:"_2faChanged",value:async function(e){try{await(0,h.p1)(this.hass,this.entityId,!e.target.checked)}catch(t){e.target.checked=!e.target.checked}}},{kind:"method",key:"_saveAliases",value:async function(){if(!this._aliases)return;const e=await(0,u.G_)(this.hass,this.entityId,{aliases:this._aliases.map((e=>e.trim())).filter((e=>e))});(0,d.r)(this,"entity-entry-updated",e.entity_entry)}},{kind:"method",key:"_toggleAssistant",value:async function(e){if((0,g.ij)(this.hass,[e.target.assistant],[this.entityId],e.target.checked),this.entry){const e=await(0,u.v)(this.hass,this.entityId);(0,d.r)(this,"entity-entry-updated",e)}(0,d.r)(this,"exposed-entities-changed")}},{kind:"method",key:"_toggleAll",value:async function(e){const t=e.target.checked?e.target.assistants.filter((e=>!this._unsupported[e])):e.target.assistants;if((0,g.ij)(this.hass,t,[this.entityId],e.target.checked),this.entry){const e=await(0,u.v)(this.hass,this.entityId);(0,d.r)(this,"entity-entry-updated",e)}(0,d.r)(this,"exposed-entities-changed")}},{kind:"get",static:!0,key:"styles",value:function(){return[y.RF,s.AH`:host{display:block;margin:32px;margin-top:0;--settings-row-prefix-display:contents;--settings-row-content-display:contents}ha-settings-row{padding:0}img{height:32px;width:32px;margin-right:16px;margin-inline-end:16px;margin-inline-start:initial}ha-aliases-editor{display:block}ha-alert{display:block;margin-top:16px}ha-formfield{margin-left:-8px;margin-inline-start:-8px;margin-inline-end:initial}ha-checkbox{--mdc-checkbox-state-layer-size:40px}.unsupported{display:flex;align-items:center}.unsupported ha-svg-icon{color:var(--error-color);--mdc-icon-size:16px;margin-right:4px;margin-inline-end:4px;margin-inline-start:initial}.header{margin-top:8px;margin-bottom:4px}.description{color:var(--secondary-text-color);font-size:14px;line-height:20px;margin-top:0;margin-bottom:16px}`]}}]}}),(0,m.E)(s.WF))},84976:(e,t,i)=>{i.d(t,{o:()=>a});const a=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}};
//# sourceMappingURL=89344.xHFhY_Vtw_o.js.map