export const id=44297;export const ids=[44297];export const modules={44297:(t,i,e)=>{e.r(i),e.d(i,{DEFAULT_DAYS_TO_SHOW:()=>l,HuiStatisticsGraphCard:()=>u});var s=e(36312),a=e(68689),n=(e(89655),e(253),e(94438),e(54846),e(15112)),h=e(77706),c=e(85323),o=(e(13082),e(4826)),d=e(18102),r=e(7934),_=e(62241);const l=30;let u=(0,s.A)([(0,h.EM)("hui-statistics-graph-card")],(function(t,i){class s extends i{constructor(...i){super(...i),t(this)}}return{F:s,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([e.e(94131),e.e(40319),e.e(15313),e.e(55792),e.e(67184),e.e(18174)]).then(e.bind(e,80780)),document.createElement("hui-statistics-graph-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(t,i,e){const s=(0,d.B)(t,1,i,e,["sensor"],(t=>"state_class"in t.attributes));return{type:"statistics-graph",entities:s.length?[s[0]]:[]}}},{kind:"field",decorators:[(0,h.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,h.wk)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,h.wk)()],key:"_statistics",value:void 0},{kind:"field",decorators:[(0,h.wk)()],key:"_metadata",value:void 0},{kind:"field",decorators:[(0,h.wk)()],key:"_unit",value:void 0},{kind:"field",key:"_entities",value:()=>[]},{kind:"field",key:"_names",value:()=>({})},{kind:"field",key:"_interval",value:void 0},{kind:"field",key:"_statTypes",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.A)(s,"disconnectedCallback",this,3)([]),this._interval&&(clearInterval(this._interval),this._interval=void 0)}},{kind:"method",key:"connectedCallback",value:function(){(0,a.A)(s,"connectedCallback",this,3)([]),this.hasUpdated&&this._setFetchStatisticsTimer()}},{kind:"method",key:"getCardSize",value:function(){return 5+(this._config?.title?2:0)+(this._config?.hide_legend?0:this._entities?.length||0)}},{kind:"method",key:"setConfig",value:function(t){if(!t.entities||!Array.isArray(t.entities))throw new Error("Entities need to be an array");if(!t.entities.length)throw new Error("You must include at least one entity");const i=t.entities?(0,_.L)(t.entities,!1):[];this._entities=[],i.forEach((t=>{this._entities.push(t.entity),t.name&&(this._names[t.entity]=t.name)})),"string"==typeof t.stat_types?this._statTypes=[t.stat_types]:t.stat_types?this._statTypes=t.stat_types:this._statTypes=["change","state","sum","min","max","mean"],this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return(0,r.pY)(this,t)||t.size>1||!t.has("hass")}},{kind:"method",key:"willUpdate",value:function(t){if((0,a.A)(s,"willUpdate",this,3)([t]),!this._config||!t.has("_config"))return;const i=t.get("_config");t.has("_config")&&i?.entities!==this._config.entities?this._getStatisticsMetaData(this._entities).then((()=>{this._setFetchStatisticsTimer()})):!t.has("_config")||i?.stat_types===this._config.stat_types&&i?.days_to_show===this._config.days_to_show&&i?.period===this._config.period&&i?.unit===this._config.unit||this._setFetchStatisticsTimer()}},{kind:"method",key:"_setFetchStatisticsTimer",value:function(){this._getStatistics(),clearInterval(this._interval),this._interval=window.setInterval((()=>this._getStatistics()),this._intervalTimeout)}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?n.qy` <ha-card .header="${this._config.title}"> <div class="content ${(0,c.H)({"has-header":!!this._config.title})}"> <statistics-chart .hass="${this.hass}" .isLoadingData="${!this._statistics}" .statisticsData="${this._statistics}" .metadata="${this._metadata}" .period="${this._config.period}" .chartType="${this._config.chart_type||"line"}" .statTypes="${this._statTypes}" .names="${this._names}" .unit="${this._unit}" .hideLegend="${this._config.hide_legend||!1}" .logarithmicScale="${this._config.logarithmic_scale||!1}"></statistics-chart> </div> </ha-card> `:n.s6}},{kind:"get",key:"_intervalTimeout",value:function(){return 1e3*("5minute"===this._config?.period?5:60)*60}},{kind:"method",key:"_getStatisticsMetaData",value:async function(t){const i=await(0,o.Wr)(this.hass,t),e={};i.forEach((t=>{e[t.statistic_id]=t})),this._metadata=e}},{kind:"method",key:"_getStatistics",value:async function(){const t=new Date;t.setTime(t.getTime()-36e5*(24*(this._config.days_to_show||l)+1));try{let i;if(this._config.unit&&this._metadata){const t=Object.values(this._metadata).find((t=>(0,o.JE)(this.hass,t?.statistic_id,t)===this._config.unit));t&&(i=t.unit_class,this._unit=this._config.unit)}if(!i&&this._metadata){const t=this._metadata[this._entities[0]];i=t?.unit_class,this._unit=i&&(0,o.JE)(this.hass,t.statistic_id,t)||void 0}const e=i?{[i]:this._unit}:void 0,s=await(0,o.sz)(this.hass,t,void 0,this._entities,this._config.period,e,this._statTypes);this._statistics={},this._entities.forEach((t=>{t in s&&(this._statistics[t]=s[t])}))}catch(t){this._statistics=void 0}}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`ha-card{height:100%}.content{padding:16px}.has-header{padding-top:0}`}}]}}),n.WF)}};
//# sourceMappingURL=44297.-Sfw5gRkCZU.js.map