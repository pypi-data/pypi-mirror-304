"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[87636],{87636:function(e,t,a){a.r(t),a.d(t,{HuiUpdateActionsCardFeatureEditor:function(){return _}});var n,i=a(64599),o=a(35806),s=a(71008),u=a(62193),c=a(2816),r=a(27927),l=(a(81027),a(97741),a(50693),a(26098),a(15112)),d=a(29818),h=a(94100),f=a(34897),k=(a(36185),a(42496)),p=a(2989),v=a(52924),_=(0,r.A)([(0,d.EM)("hui-update-actions-card-feature-editor")],(function(e,t){var a=function(t){function a(){var t;(0,s.A)(this,a);for(var n=arguments.length,i=new Array(n),o=0;o<n;o++)i[o]=arguments[o];return t=(0,u.A)(this,a,[].concat(i)),e(t),t}return(0,c.A)(a,t),(0,o.A)(a)}(t);return{F:a,d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"field",decorators:[(0,d.wk)()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"field",key:"_schema",value:function(){return(0,h.A)((function(e,t){return[{name:"backup",disabled:!t,selector:{select:{default:"yes",mode:"dropdown",options:["ask","yes","no"].map((function(t){return{value:t,label:e("ui.panel.lovelace.editor.features.types.update-actions.backup_options.".concat(t))}}))}}}]}))}},{kind:"get",key:"_stateObj",value:function(){var e,t;return null!==(e=this.context)&&void 0!==e&&e.entity_id?this.hass.states[null===(t=this.context)||void 0===t?void 0:t.entity_id]:void 0}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return l.s6;var e=null!=this._stateObj&&(0,k.$)(this._stateObj,p.TY.BACKUP),t=this._schema(this.hass.localize,e),a=Object.assign({},this._config);return!this._config.backup&&e&&(a.backup=v.J),(0,l.qy)(n||(n=(0,i.A)([' <ha-form .hass="','" .data="','" .schema="','" .computeLabel="','" .computeHelper="','" @value-changed="','"></ha-form> '])),this.hass,a,t,this._computeLabelCallback,this._computeHelperCallback,this._valueChanged)}},{kind:"method",key:"_valueChanged",value:function(e){(0,f.r)(this,"config-changed",{config:e.detail.value})}},{kind:"field",key:"_computeLabelCallback",value:function(){var e=this;return function(t){return"backup"===t.name?e.hass.localize("ui.panel.lovelace.editor.features.types.update-actions.".concat(t.name)):""}}},{kind:"field",key:"_computeHelperCallback",value:function(){var e=this;return function(t){var a=null!=e._stateObj&&(0,k.$)(e._stateObj,p.TY.BACKUP);if("backup"===t.name)return a?void 0:e.hass.localize("ui.panel.lovelace.editor.features.types.update-actions.backup_not_supported")}}}]}}),l.WF)}}]);
//# sourceMappingURL=87636.HdASz-jmawU.js.map