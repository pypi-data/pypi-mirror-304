export const id=47083;export const ids=[47083];export const modules={47083:(t,e,i)=>{i.a(t,(async(t,s)=>{try{i.r(e),i.d(e,{HuiStatisticCard:()=>p});var n=i(36312),a=i(68689),o=i(15112),r=i(77706),h=i(38962),c=i(34897),d=i(26175),l=i(57636),f=(i(13292),i(13082),i(70857),i(4826)),u=i(42183),_=i(18102),v=i(7934),m=i(32064),y=t([l]);l=(y.then?(await y)():y)[0];let p=(0,n.A)([(0,r.EM)("hui-statistic-card")],(function(t,e){class s extends e{constructor(...e){super(...e),t(this)}}return{F:s,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await i.e(89052).then(i.bind(i,89052)),document.createElement("hui-statistic-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(t,e,i){return{entity:(0,_.B)(t,1,e,i,["sensor"],(t=>"state_class"in t.attributes))[0]||"",period:{calendar:{period:"month"}}}}},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_value",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_metadata",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_error",value:void 0},{kind:"field",key:"_interval",value:void 0},{kind:"field",key:"_footerElement",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.A)(s,"disconnectedCallback",this,3)([]),clearInterval(this._interval)}},{kind:"method",key:"setConfig",value:function(t){if(!t.entity)throw new Error("Entity must be specified");if(!t.stat_type)throw new Error("Statistic type must be specified");if(!t.period)throw new Error("Period must be specified");if(t.entity&&!(0,f.OQ)(t.entity)&&!(0,d.n)(t.entity))throw new Error("Invalid entity");this._config=t,this._error=void 0,this._fetchStatistic(),this._fetchMetadata(),this._config.footer?this._footerElement=(0,m.x)(this._config.footer):this._footerElement&&(this._footerElement=void 0)}},{kind:"method",key:"getCardSize",value:async function(){let t=2;if(this._footerElement){const e=(0,u.Z)(this._footerElement);t+=e instanceof Promise?await e:e}return t}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return o.s6;if(this._error)return o.qy` <ha-alert alert-type="error">${this._error}</ha-alert> `;const t=this.hass.states[this._config.entity],e=this._config.name||(0,f.$O)(this.hass,this._config.entity,this._metadata);return o.qy` <ha-card @click="${this._handleClick}" tabindex="0"> <div class="header"> <div class="name" .title="${e}">${e}</div> <div class="icon"> <ha-state-icon .icon="${this._config.icon}" .stateObj="${t}" .hass="${this.hass}"></ha-state-icon> </div> </div> <div class="info"> <span class="value">${void 0===this._value?"":null===this._value?"?":(0,l.ZV)(this._value,this.hass.locale)}</span> <span class="measurement">${this._config.unit||(0,f.JE)(this.hass,this._config.entity,this._metadata)}</span> </div> ${this._footerElement} </ha-card> `}},{kind:"method",key:"shouldUpdate",value:function(t){return this._footerElement&&(this._footerElement.hass=this.hass),!!(t.has("_value")||t.has("_metadata")||t.has("_error"))||(!this._config||(0,v.LX)(this,t))}},{kind:"method",key:"firstUpdated",value:function(){this._fetchStatistic(),this._fetchMetadata()}},{kind:"method",key:"updated",value:function(t){if((0,a.A)(s,"updated",this,3)([t]),!this._config||!this.hass)return;const e=t.get("hass"),i=t.get("_config");e&&i&&e.themes===this.hass.themes&&i.theme===this._config.theme||(0,h.Q)(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"_fetchStatistic",value:async function(){if(this.hass&&this._config){clearInterval(this._interval),this._interval=window.setInterval((()=>this._fetchStatistic()),3e5);try{const t=await(0,f.pJ)(this.hass,this._config.entity,this._config.period);this._value=t[this._config.stat_type],this._error=void 0}catch(t){this._error=t.message}}}},{kind:"method",key:"_fetchMetadata",value:async function(){if(this.hass&&this._config)try{this._metadata=(await(0,f.Wr)(this.hass,[this._config.entity]))?.[0]}catch(t){this._error=t.message}}},{kind:"method",key:"_handleClick",value:function(){(0,c.r)(this,"hass-more-info",{entityId:this._config.entity})}},{kind:"method",key:"getLayoutOptions",value:function(){return{grid_columns:2,grid_rows:2,grid_min_columns:2,grid_min_rows:2}}},{kind:"get",static:!0,key:"styles",value:function(){return[o.AH`ha-card{height:100%;display:flex;flex-direction:column;justify-content:space-between;cursor:pointer;outline:0}.header{display:flex;padding:8px 16px 0;justify-content:space-between}.name{color:var(--secondary-text-color);line-height:40px;font-weight:500;font-size:16px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}.icon{color:var(--state-icon-color,#44739e);line-height:40px}.info{padding:0px 16px 16px;margin-top:-4px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;line-height:28px}.value{font-size:28px;margin-right:4px;margin-inline-end:4px;margin-inline-start:initial}.measurement{font-size:18px;color:var(--secondary-text-color)}`]}}]}}),o.WF);s()}catch(t){s(t)}}))}};
//# sourceMappingURL=47083.BSS8hcBkNEY.js.map