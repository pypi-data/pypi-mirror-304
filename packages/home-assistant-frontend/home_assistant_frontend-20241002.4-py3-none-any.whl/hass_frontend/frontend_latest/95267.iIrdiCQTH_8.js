export const id=95267;export const ids=[95267];export const modules={95267:(e,t,a)=>{a.r(t),a.d(t,{HuiVacuumCommandsCardFeatureEditor:()=>u});var i=a(36312),s=(a(253),a(2075),a(16891),a(15112)),o=a(77706),n=a(94100),c=a(34897),d=a(82765),l=a(93501);let u=(0,i.A)([(0,o.EM)("hui-vacuum-commands-card-feature-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"field",key:"_schema",value:()=>(0,n.A)(((e,t)=>[{name:"commands",selector:{select:{multiple:!0,mode:"list",options:l.z.filter((e=>t&&(0,d.Fv)(t,e))).map((t=>({value:t,label:`${e(`ui.panel.lovelace.editor.features.types.vacuum-commands.commands_list.${t}`)}`})))}}}]))},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return s.s6;const e=this.context?.entity_id?this.hass.states[this.context?.entity_id]:void 0,t=this._schema(this.hass.localize,e);return s.qy` <ha-form .hass="${this.hass}" .data="${this._config}" .schema="${t}" .computeLabel="${this._computeLabelCallback}" @value-changed="${this._valueChanged}"></ha-form> `}},{kind:"method",key:"_valueChanged",value:function(e){(0,c.r)(this,"config-changed",{config:e.detail.value})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>"commands"===e.name?this.hass.localize(`ui.panel.lovelace.editor.features.types.vacuum-commands.${e.name}`):this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)}}]}}),s.WF)}};
//# sourceMappingURL=95267.iIrdiCQTH_8.js.map