export const id=38406;export const ids=[38406,57540];export const modules={43106:(e,t,i)=>{i.a(e,(async(e,t)=>{try{var s=i(36312),a=i(68689),n=(i(16891),i(15112)),o=i(77706),l=i(63073),r=i(57636),h=i(33984),c=i(61441),d=i(62370),u=e([r]);r=(u.then?(await u)():u)[0];const f=(e,t,i)=>180*(0,d.NN)((0,d.S8)(e,t,i),t,i)/100;(0,s.A)([(0,o.EM)("ha-gauge")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"min",value:()=>0},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"max",value:()=>100},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"value",value:()=>0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"formatOptions",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:String})],key:"valueText",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"locale",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"needle",value:()=>!1},{kind:"field",decorators:[(0,o.MZ)({type:Array})],key:"levels",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:()=>""},{kind:"field",decorators:[(0,o.wk)()],key:"_angle",value:()=>0},{kind:"field",decorators:[(0,o.wk)()],key:"_updated",value:()=>!1},{kind:"field",decorators:[(0,o.wk)()],key:"_segment_label",value:()=>""},{kind:"method",key:"firstUpdated",value:function(e){(0,a.A)(i,"firstUpdated",this,3)([e]),(0,c.m)((()=>{this._updated=!0,this._angle=f(this.value,this.min,this.max),this._segment_label=this.getSegmentLabel(),this._rescale_svg()}))}},{kind:"method",key:"updated",value:function(e){(0,a.A)(i,"updated",this,3)([e]),this._updated&&(e.has("value")||e.has("label")||e.has("_segment_label"))&&(this._angle=f(this.value,this.min,this.max),this._segment_label=this.getSegmentLabel(),this._rescale_svg())}},{kind:"method",key:"render",value:function(){return n.JW` <svg viewBox="-50 -50 100 50" class="gauge"> ${this.needle&&this.levels?"":n.JW`<path class="dial" d="M -40 0 A 40 40 0 0 1 40 0"></path>`} ${this.levels?this.levels.sort(((e,t)=>e.level-t.level)).map(((e,t)=>{let i;if(0===t&&e.level!==this.min){const e=f(this.min,this.min,this.max);i=n.JW`<path stroke="var(--info-color)" class="level" d="M
                          ${0-40*Math.cos(e*Math.PI/180)}
                          ${0-40*Math.sin(e*Math.PI/180)}
                         A 40 40 0 0 1 40 0
                        "></path>`}const s=f(e.level,this.min,this.max);return n.JW`${i}<path stroke="${e.stroke}" class="level" d="M
                        ${0-40*Math.cos(s*Math.PI/180)}
                        ${0-40*Math.sin(s*Math.PI/180)}
                       A 40 40 0 0 1 40 0
                      "></path>`})):""} ${this.needle?n.JW`<path class="needle" d="M -25 -2.5 L -47.5 0 L -25 2.5 z" style="${(0,l.W)({transform:`rotate(${this._angle}deg)`})}"> </path>`:n.JW`<path class="value" d="M -40 0 A 40 40 0 1 0 40 0" style="${(0,l.W)({transform:`rotate(${this._angle}deg)`})}"></path>`}  </svg> <svg class="text"> <text class="value-text"> ${this._segment_label?this._segment_label:this.valueText||(0,r.ZV)(this.value,this.locale,this.formatOptions)}${this._segment_label?"":"%"===this.label?(0,h.d)(this.locale)+"%":` ${this.label}`} </text> </svg>`}},{kind:"method",key:"_rescale_svg",value:function(){const e=this.shadowRoot.querySelector(".text"),t=e.querySelector("text").getBBox();e.setAttribute("viewBox",`${t.x} ${t.y} ${t.width} ${t.height}`)}},{kind:"method",key:"getSegmentLabel",value:function(){if(this.levels){this.levels.sort(((e,t)=>e.level-t.level));for(let e=this.levels.length-1;e>=0;e--)if(this.value>=this.levels[e].level)return this.levels[e].label}return""}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`:host{position:relative}.dial{fill:none;stroke:var(--primary-background-color);stroke-width:15}.value{fill:none;stroke-width:15;stroke:var(--gauge-color);transition:all 1s ease 0s}.needle{fill:var(--primary-text-color);transition:all 1s ease 0s}.level{fill:none;stroke-width:15}.gauge{display:block}.text{position:absolute;max-height:40%;max-width:55%;left:50%;bottom:-6%;transform:translate(-50%,0%)}.value-text{font-size:50px;fill:var(--primary-text-color);text-anchor:middle;direction:ltr}`}}]}}),n.WF);t()}catch(e){t(e)}}))},20712:(e,t,i)=>{i.d(t,{E:()=>o});var s=i(36312),a=i(68689),n=i(77706);const o=e=>(0,s.A)(null,(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,a.A)(i,"connectedCallback",this,3)([]),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if((0,a.A)(i,"disconnectedCallback",this,3)([]),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){if((0,a.A)(i,"updated",this,3)([e]),e.has("hass"))this.__checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const t of e.keys())if(this.hassSubscribeRequiredHostProps.includes(t))return void this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&!this.hassSubscribeRequiredHostProps?.some((e=>void 0===this[e]))&&(this.__unsubs=this.hassSubscribe())}}]}}),e)},16025:(e,t,i)=>{i.a(e,(async(e,s)=>{try{i.r(t);var a=i(36312),n=(i(16891),i(7986),i(15112)),o=i(77706),l=i(63073),r=(i(13082),i(43106)),h=(i(88400),i(47076)),c=i(4826),d=i(20712),u=i(57540),f=i(7934),g=e([r,h,u]);[r,h,u]=g.then?(await g)():g;const v="M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z",m={maximumFractionDigits:0};(0,a.A)([(0,o.EM)("hui-energy-self-sufficiency-gauge-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_data",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:()=>["_config"]},{kind:"method",key:"hassSubscribe",value:function(){return[(0,h.tb)(this.hass,{key:this._config?.collection_key}).subscribe((e=>{this._data=e}))]}},{kind:"method",key:"getCardSize",value:function(){return 4}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"shouldUpdate",value:function(e){return(0,f.xP)(this,e)||e.size>1||!e.has("hass")}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return n.s6;if(!this._data)return n.qy`${this.hass.localize("ui.panel.lovelace.cards.energy.loading")}`;const e=this._data.prefs,t=(0,h.E$)(e),i=void 0!==t.solar,s=void 0!==t.battery,a=t.grid[0].flow_to.length>0,o=(0,c.gF)(this._data.stats,t.grid[0].flow_from.map((e=>e.stat_energy_from)))??0;let r=null;i&&(r=(0,c.gF)(this._data.stats,t.solar.map((e=>e.stat_energy_from)))||0);let d=null,u=null;s&&(d=(0,c.gF)(this._data.stats,t.battery.map((e=>e.stat_energy_to)))||0,u=(0,c.gF)(this._data.stats,t.battery.map((e=>e.stat_energy_from)))||0);let f=null;a&&(f=(0,c.gF)(this._data.stats,t.grid[0].flow_to.map((e=>e.stat_energy_to)))||0);let g=null;i&&(g=(r||0)-(f||0)-(d||0));let y=null,_=null;null!==g&&g<0&&(s&&(y=-1*g,y>o&&(_=y-o,y=o)),g=0);let k=null;s&&(k=(u||0)-(_||0));const p=Math.max(0,o-(y||0)),b=Math.max(0,p+(g||0)+(k||0));let x;return null!==o&&null!==b&&b>0&&(x=100*(1-o/b)),n.qy` <ha-card> ${void 0!==x?n.qy` <ha-svg-icon id="info" .path="${v}"></ha-svg-icon> <simple-tooltip animation-delay="0" for="info" position="left"> <span> ${this.hass.localize("ui.panel.lovelace.cards.energy.self_sufficiency_gauge.card_indicates_self_sufficiency_quota")} </span> </simple-tooltip> <ha-gauge min="0" max="100" .value="${x}" label="%" .formatOptions="${m}" .locale="${this.hass.locale}" style="${(0,l.W)({"--gauge-color":this._computeSeverity(x)})}"></ha-gauge> <div class="name"> ${this.hass.localize("ui.panel.lovelace.cards.energy.self_sufficiency_gauge.self_sufficiency_quota")} </div> `:this.hass.localize("ui.panel.lovelace.cards.energy.self_sufficiency_gauge.self_sufficiency_could_not_calc")} </ha-card> `}},{kind:"method",key:"_computeSeverity",value:function(e){return e>75?u.severityMap.green:e<50?u.severityMap.yellow:u.severityMap.normal}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`ha-card{height:100%;overflow:hidden;padding:16px;display:flex;align-items:center;justify-content:center;flex-direction:column;box-sizing:border-box}ha-gauge{width:100%;max-width:250px;direction:ltr}.name{text-align:center;line-height:initial;color:var(--primary-text-color);width:100%;font-size:15px;margin-top:8px}ha-svg-icon{position:absolute;right:4px;inset-inline-end:4px;inset-inline-start:initial;top:4px;color:var(--secondary-text-color)}simple-tooltip>span{font-size:12px;line-height:12px}simple-tooltip{width:80%;max-width:250px;top:8px!important}`}}]}}),(0,d.E)(n.WF));s()}catch(e){s(e)}}))},57540:(e,t,i)=>{i.a(e,(async(e,s)=>{try{i.r(t),i.d(t,{DEFAULT_MAX:()=>M,DEFAULT_MIN:()=>w,severityMap:()=>A});var a=i(36312),n=i(68689),o=(i(16891),i(15112)),l=i(77706),r=i(10977),h=i(85323),c=i(63073),d=i(38962),u=i(19244),f=i(26175),g=i(57636),v=(i(13082),i(43106)),m=i(9883),y=i(25319),_=i(18102),k=i(63582),p=i(562),b=i(7934),x=i(46645),$=e([g,v]);[g,v]=$.then?(await $)():$;const w=0,M=100,A={red:"var(--error-color)",green:"var(--success-color)",yellow:"var(--warning-color)",normal:"var(--info-color)"};(0,a.A)([(0,l.EM)("hui-gauge-card")],(function(e,t){class s extends t{constructor(...t){super(...t),e(this)}}return{F:s,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await i.e(59149).then(i.bind(i,59149)),document.createElement("hui-gauge-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,i){return{type:"gauge",entity:(0,_.B)(e,1,t,i,["counter","input_number","number","sensor"],(e=>!isNaN(Number(e.state))))[0]||""}}},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_config",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 4}},{kind:"method",key:"setConfig",value:function(e){if(!e.entity)throw new Error("Entity must be specified");if(!(0,f.n)(e.entity))throw new Error("Invalid entity");this._config={min:w,max:M,...e}}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return o.s6;const e=this.hass.states[this._config.entity];if(!e)return o.qy` <hui-warning> ${(0,x.j)(this.hass,this._config.entity)} </hui-warning> `;const t=Number(e.state);if(e.state===m.Hh)return o.qy` <hui-warning>${this.hass.localize("ui.panel.lovelace.warning.entity_unavailable",{entity:this._config.entity})}</hui-warning> `;if(isNaN(t))return o.qy` <hui-warning>${this.hass.localize("ui.panel.lovelace.warning.entity_non_numeric",{entity:this._config.entity})}</hui-warning> `;const i=this._config.name??(0,u.u)(e);return o.qy` <ha-card class="${(0,h.H)({action:(0,p.A)(this._config)})}" @action="${this._handleAction}" .actionHandler="${(0,y.T)({hasHold:(0,p.h)(this._config.hold_action),hasDoubleClick:(0,p.h)(this._config.double_tap_action)})}" tabindex="${(0,r.J)(!this._config.tap_action||(0,p.h)(this._config.tap_action)?"0":void 0)}"> <ha-gauge .min="${this._config.min}" .max="${this._config.max}" .value="${e.state}" .formatOptions="${(0,g.ZQ)(e,this.hass.entities[e.entity_id])}" .locale="${this.hass.locale}" .label="${this._config.unit||this.hass?.states[this._config.entity].attributes.unit_of_measurement||""}" style="${(0,c.W)({"--gauge-color":this._computeSeverity(t)})}" .needle="${this._config.needle}" .levels="${this._config.needle?this._severityLevels():void 0}"></ha-gauge> <div class="name" .title="${i}">${i}</div> </ha-card> `}},{kind:"method",key:"shouldUpdate",value:function(e){return(0,b.LX)(this,e)}},{kind:"method",key:"updated",value:function(e){if((0,n.A)(s,"updated",this,3)([e]),!this._config||!this.hass)return;const t=e.get("hass"),i=e.get("_config");t&&i&&t.themes===this.hass.themes&&i.theme===this._config.theme||(0,d.Q)(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"_computeSeverity",value:function(e){if(this._config.needle)return;let t=this._config.segments;if(t){t=[...t].sort(((e,t)=>e.from-t.from));for(let i=0;i<t.length;i++){const s=t[i];if(s&&e>=s.from&&(i+1===t.length||e<t[i+1]?.from))return s.color}return A.normal}const i=this._config.severity;if(!i)return A.normal;const s=Object.keys(i).map((e=>[e,i[e]]));for(const e of s)if(null==A[e[0]]||isNaN(e[1]))return A.normal;return s.sort(((e,t)=>e[1]-t[1])),e>=s[0][1]&&e<s[1][1]?A[s[0][0]]:e>=s[1][1]&&e<s[2][1]?A[s[1][0]]:e>=s[2][1]?A[s[2][0]]:A.normal}},{kind:"method",key:"_severityLevels",value:function(){const e=this._config.segments;if(e)return e.map((e=>({level:e?.from,stroke:e?.color,label:e?.label})));const t=this._config.severity;if(!t)return[{level:0,stroke:A.normal}];return Object.keys(t).map((e=>({level:t[e],stroke:A[e]})))}},{kind:"method",key:"_handleAction",value:function(e){(0,k.$)(this,this.hass,this._config,e.detail.action)}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`ha-card{height:100%;overflow:hidden;padding:16px;display:flex;align-items:center;justify-content:center;flex-direction:column;box-sizing:border-box}ha-card.action{cursor:pointer}ha-card:focus{outline:0}ha-gauge{width:100%;max-width:250px}.name{text-align:center;line-height:initial;color:var(--primary-text-color);width:100%;font-size:15px;margin-top:8px}`}}]}}),o.WF);s()}catch(e){s(e)}}))},62370:(e,t,i)=>{i.d(t,{NN:()=>a,S8:()=>s,gN:()=>n});const s=(e,t,i)=>isNaN(e)||isNaN(t)||isNaN(i)?0:e>i?i:e<t?t:e,a=(e,t,i)=>100*(e-t)/(i-t),n=e=>Math.round(10*e)/10}};
//# sourceMappingURL=38406.0WZaJMNcu-8.js.map