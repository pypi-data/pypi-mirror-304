export const id=85750;export const ids=[85750];export const modules={85750:(e,t,i)=>{i.a(e,(async(e,n)=>{try{i.r(t),i.d(t,{HuiPictureElementsCardEditor:()=>k});var a=i(36312),s=i(15112),o=i(77706),l=i(66419),c=i(94100),d=i(34897),r=(i(13082),i(36185),i(20144),i(59588),i(54581)),m=i(56124),h=i(3532),u=i(1040),g=e([r,u]);[r,u]=g.then?(await g)():g;const f=(0,l.NW)({type:(0,l.Yj)()}),_=(0,l.kp)(m.H,(0,l.Ik)({image:(0,l.lq)((0,l.Yj)()),camera_image:(0,l.lq)((0,l.Yj)()),camera_view:(0,l.lq)((0,l.Yj)()),elements:(0,l.YO)(f),title:(0,l.lq)((0,l.Yj)()),state_filter:(0,l.lq)((0,l.bz)()),theme:(0,l.lq)((0,l.Yj)()),dark_mode_image:(0,l.lq)((0,l.Yj)()),dark_mode_filter:(0,l.lq)((0,l.bz)())}));let k=(0,a.A)([(0,o.EM)("hui-picture-elements-card-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_subElementEditorConfig",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,l.vA)(e,_),this._config=e}},{kind:"field",key:"_schema",value:()=>(0,c.A)((e=>[{name:"",type:"expandable",title:e("ui.panel.lovelace.editor.card.picture-elements.card_options"),schema:[{name:"title",selector:{text:{}}},{name:"image",selector:{image:{}}},{name:"dark_mode_image",selector:{image:{}}},{name:"camera_image",selector:{entity:{domain:"camera"}}},{name:"camera_view",selector:{select:{options:["auto","live"]}}},{name:"theme",selector:{theme:{}}},{name:"state_filter",selector:{object:{}}},{name:"dark_mode_filter",selector:{object:{}}}]}]))},{kind:"method",key:"render",value:function(){return this.hass&&this._config?this._subElementEditorConfig?s.qy` <hui-sub-element-editor .hass="${this.hass}" .config="${this._subElementEditorConfig}" @go-back="${this._goBack}" @config-changed="${this._handleSubElementChanged}"> </hui-sub-element-editor> `:s.qy` <ha-form .hass="${this.hass}" .data="${this._config}" .schema="${this._schema(this.hass.localize)}" .computeLabel="${this._computeLabelCallback}" @value-changed="${this._formChanged}"></ha-form> <hui-picture-elements-card-row-editor .hass="${this.hass}" .elements="${this._config.elements}" @elements-changed="${this._elementsChanged}" @edit-detail-element="${this._editDetailElement}"></hui-picture-elements-card-row-editor> `:s.s6}},{kind:"method",key:"_formChanged",value:function(e){e.stopPropagation(),this._config&&this.hass&&(0,d.r)(this,"config-changed",{config:e.detail.value})}},{kind:"method",key:"_elementsChanged",value:function(e){e.stopPropagation();const t=this._config?.elements?.length||0,i={...this._config,elements:e.detail.elements};(0,d.r)(this,"config-changed",{config:i});const n=e.detail.elements?.length||0;if(n===t+1){const t=n-1;this._subElementEditorConfig={index:t,type:"element",elementConfig:{...e.detail.elements[t]}}}}},{kind:"method",key:"_handleSubElementChanged",value:function(e){if(e.stopPropagation(),!this._config||!this.hass)return;const t=this._subElementEditorConfig?.type,i=e.detail.config;if("element"===t){const e=this._config.elements.concat();i?e[this._subElementEditorConfig.index]=i:(e.splice(this._subElementEditorConfig.index,1),this._goBack()),this._config={...this._config,elements:e}}this._subElementEditorConfig={...this._subElementEditorConfig,elementConfig:i},(0,d.r)(this,"config-changed",{config:this._config})}},{kind:"method",key:"_editDetailElement",value:function(e){this._subElementEditorConfig=e.detail.subElementConfig}},{kind:"method",key:"_goBack",value:function(){this._subElementEditorConfig=void 0}},{kind:"field",key:"_computeLabelCallback",value(){return e=>{switch(e.name){case"dark_mode_image":case"state_filter":case"dark_mode_filter":return this.hass.localize(`ui.panel.lovelace.editor.card.picture-elements.${e.name}`)||e.name;default:return this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)||e.name}}}},{kind:"get",static:!0,key:"styles",value:function(){return[h.U]}}]}}),s.WF);n()}catch(e){n(e)}}))},56124:(e,t,i)=>{i.d(t,{H:()=>a});var n=i(66419);const a=(0,n.Ik)({type:(0,n.Yj)(),view_layout:(0,n.bz)(),layout_options:(0,n.bz)(),visibility:(0,n.bz)()})}};
//# sourceMappingURL=85750.sguls_AEbFU.js.map