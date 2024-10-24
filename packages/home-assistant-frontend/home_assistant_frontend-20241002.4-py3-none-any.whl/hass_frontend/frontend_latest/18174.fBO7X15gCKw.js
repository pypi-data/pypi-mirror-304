export const id=18174;export const ids=[18174];export const modules={46999:(t,e,i)=>{i.d(e,{Vy:()=>d,fI:()=>n});var a=i(3254);const s=["#4269d0","#f4bd4a","#ff725c","#6cc5b0","#a463f2","#ff8ab7","#9c6b4e","#97bbf5","#01ab63","#9498a0","#094bad","#c99000","#d84f3e","#49a28f","#048732","#d96895","#8043ce","#7599d1","#7a4c31","#74787f","#6989f4","#ffd444","#ff957c","#8fe9d3","#62cc71","#ffadda","#c884ff","#badeff","#bf8b6d","#b6bac2","#927acc","#97ee3f","#bf3947","#9f5b00","#f48758","#8caed6","#f2b94f","#eff26e","#e43872","#d9b100","#9d7a00","#698cff","#d9d9d9","#00d27e","#d06800","#009f82","#c49200","#cbe8ff","#fecddf","#c27eb6","#8cd2ce","#c4b8d9","#f883b0","#a49100","#f48800","#27d0df","#a04a9b"];function d(t){return s[t%s.length]}function n(t,e){const i=e.getPropertyValue(`--graph-color-${t+1}`)||d(t);return(0,a.RQ)(i)}},56136:(t,e,i)=>{i.d(e,{a:()=>a});const a=t=>!(t.native instanceof MouseEvent)||t.native instanceof PointerEvent&&"mouse"!==t.native.pointerType},90701:(t,e,i)=>{i.d(e,{p:()=>p});var a=i(36312),s=i(68689),d=(i(24545),i(51855),i(82130),i(31743),i(22328),i(4959),i(62435),i(253),i(54846),i(16891),i(15112)),n=i(77706),o=i(85323),l=i(63073),r=i(34897),h=i(69678),c=i(18409);const p=3e5;(0,a.A)([(0,n.EM)("ha-chart-base")],(function(t,e){class a extends e{constructor(...e){super(...e),t(this)}}return{F:a,d:[{kind:"field",key:"chart",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"chart-type",reflect:!0})],key:"chartType",value:()=>"line"},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"data",value:()=>({datasets:[]})},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"extraData",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"plugins",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"height",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"paddingYAxis",value:()=>0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"externalHidden",value:()=>!1},{kind:"field",decorators:[(0,n.wk)()],key:"_chartHeight",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_tooltip",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_hiddenDatasets",value:()=>new Set},{kind:"field",key:"_paddingUpdateCount",value:()=>0},{kind:"field",key:"_paddingUpdateLock",value:()=>!1},{kind:"field",key:"_paddingYAxisInternal",value:()=>0},{kind:"field",key:"_datasetOrder",value:()=>[]},{kind:"method",key:"disconnectedCallback",value:function(){(0,s.A)(a,"disconnectedCallback",this,3)([]),this._releaseCanvas()}},{kind:"method",key:"connectedCallback",value:function(){(0,s.A)(a,"connectedCallback",this,3)([]),this.hasUpdated&&(this._releaseCanvas(),this._setupChart())}},{kind:"field",key:"updateChart",value(){return t=>{this.chart?.update(t)}}},{kind:"field",key:"resize",value(){return t=>{t?.aspectRatio&&!t.height?t.height=Math.round((t.width??this.clientWidth)/t.aspectRatio):t?.aspectRatio&&!t.width&&(t.width=Math.round((t.height??this.clientHeight)*t.aspectRatio)),this.chart?.resize(t?.width??this.clientWidth,t?.height??this.clientHeight)}}},{kind:"method",key:"firstUpdated",value:function(){this._setupChart(),this.data.datasets.forEach(((t,e)=>{t.hidden&&this._hiddenDatasets.add(e)}))}},{kind:"method",key:"shouldUpdate",value:function(t){return!this._paddingUpdateLock||1!==t.size||!t.has("paddingYAxis")}},{kind:"field",key:"_debouncedClearUpdates",value(){return(0,c.s)((()=>{this._paddingUpdateCount=0}),2e3,!1)}},{kind:"method",key:"willUpdate",value:function(t){if((0,s.A)(a,"willUpdate",this,3)([t]),this._paddingUpdateLock||(this._paddingYAxisInternal=this.paddingYAxis,1===t.size&&t.has("paddingYAxis")&&(this._paddingUpdateCount++,this._paddingUpdateCount>300?(this._paddingUpdateLock=!0,console.error("Detected excessive chart padding updates, possibly an infinite loop. Disabling axis padding.")):this._debouncedClearUpdates())),t.has("data")&&(this._datasetOrder=this.data.datasets.map(((t,e)=>e)),this.data?.datasets.some((t=>t.order))&&this._datasetOrder.sort(((t,e)=>(this.data.datasets[t].order||0)-(this.data.datasets[e].order||0))),this.externalHidden&&(this._hiddenDatasets=new Set,this.data?.datasets&&this.data.datasets.forEach(((t,e)=>{t.hidden&&this._hiddenDatasets.add(e)})))),this.hasUpdated&&this.chart){if(t.has("plugins")||t.has("chartType"))return this._releaseCanvas(),void this._setupChart();t.has("data")&&(this._hiddenDatasets.size&&!this.externalHidden&&this.data.datasets.forEach(((t,e)=>{t.hidden=this._hiddenDatasets.has(e)})),this.chart.data=this.data),t.has("options")&&(this.chart.options=this._createOptions()),this.chart.update("none")}}},{kind:"method",key:"render",value:function(){return d.qy` ${!0===this.options?.plugins?.legend?.display?d.qy`<div class="chartLegend"> <ul> ${this._datasetOrder.map((t=>{const e=this.data.datasets[t];return!1===this.extraData?.[t]?.show_legend?d.s6:d.qy`<li .datasetIndex="${t}" @click="${this._legendClick}" class="${(0,o.H)({hidden:this._hiddenDatasets.has(t)})}" .title="${this.extraData?.[t]?.legend_label??e.label}"> <div class="bullet" style="${(0,l.W)({backgroundColor:e.backgroundColor,borderColor:e.borderColor})}"></div> <div class="label"> ${this.extraData?.[t]?.legend_label??e.label} </div> </li>`}))} </ul> </div>`:""} <div class="animationContainer" style="${(0,l.W)({height:`${this.height||this._chartHeight||0}px`,overflow:this._chartHeight?"initial":"hidden"})}"> <div class="chartContainer" style="${(0,l.W)({height:`${this.height??this._chartHeight??this.clientWidth/2}px`,"padding-left":`${this._paddingYAxisInternal}px`,"padding-right":0,"padding-inline-start":`${this._paddingYAxisInternal}px`,"padding-inline-end":0})}"> <canvas></canvas> ${this._tooltip?d.qy`<div class="chartTooltip ${(0,o.H)({[this._tooltip.yAlign]:!0})}" style="${(0,l.W)({top:this._tooltip.top,left:this._tooltip.left})}"> <div class="title">${this._tooltip.title}</div> ${this._tooltip.beforeBody?d.qy`<div class="beforeBody"> ${this._tooltip.beforeBody} </div>`:""} <div> <ul> ${this._tooltip.body.map(((t,e)=>d.qy`<li> <div class="bullet" style="${(0,l.W)({backgroundColor:this._tooltip.labelColors[e].backgroundColor,borderColor:this._tooltip.labelColors[e].borderColor})}"></div> ${t.lines.join("\n")} </li>`))} </ul> </div> ${this._tooltip.footer.length?d.qy`<div class="footer"> ${this._tooltip.footer.map((t=>d.qy`${t}<br>`))} </div>`:""} </div>`:""} </div> </div> `}},{kind:"field",key:"_loading",value:()=>!1},{kind:"method",key:"_setupChart",value:async function(){if(this._loading)return;const t=this.renderRoot.querySelector("canvas").getContext("2d");this._loading=!0;try{const e=(await Promise.all([i.e(20288),i.e(28177),i.e(21200)]).then(i.bind(i,21200))).Chart,a=getComputedStyle(this);e.defaults.borderColor=a.getPropertyValue("--divider-color"),e.defaults.color=a.getPropertyValue("--secondary-text-color"),e.defaults.font.family=a.getPropertyValue("--mdc-typography-body1-font-family")||a.getPropertyValue("--mdc-typography-font-family")||"Roboto, Noto, sans-serif",this.chart=new e(t,{type:this.chartType,data:this.data,options:this._createOptions(),plugins:this._createPlugins()})}finally{this._loading=!1}}},{kind:"method",key:"_createOptions",value:function(){return{maintainAspectRatio:!1,...this.options,plugins:{...this.options?.plugins,tooltip:{...this.options?.plugins?.tooltip,enabled:!1,external:t=>this._handleTooltip(t)},legend:{...this.options?.plugins?.legend,display:!1}}}}},{kind:"method",key:"_createPlugins",value:function(){return[...this.plugins||[],{id:"resizeHook",resize:t=>{const e=t.height-(this._chartHeight??0);(!this._chartHeight||e>12||e<-12)&&(this._chartHeight=t.height)},legend:{...this.options?.plugins?.legend,display:!1}}]}},{kind:"method",key:"_legendClick",value:function(t){if(!this.chart)return;const e=t.currentTarget.datasetIndex;this.chart.isDatasetVisible(e)?(this.chart.setDatasetVisibility(e,!1),this._hiddenDatasets.add(e),this.externalHidden&&(0,r.r)(this,"dataset-hidden",{index:e})):(this.chart.setDatasetVisibility(e,!0),this._hiddenDatasets.delete(e),this.externalHidden&&(0,r.r)(this,"dataset-unhidden",{index:e})),this.chart.update("none"),this.requestUpdate("_hiddenDatasets")}},{kind:"method",key:"_handleTooltip",value:function(t){0!==t.tooltip.opacity?this._tooltip={...t.tooltip,top:this.chart.canvas.offsetTop+t.tooltip.caretY+12+"px",left:this.chart.canvas.offsetLeft+(0,h.q)(t.tooltip.caretX,100,this.clientWidth-100-this._paddingYAxisInternal)-100+"px"}:this._tooltip=void 0}},{kind:"method",key:"_releaseCanvas",value:function(){this.chart&&this.chart.destroy()}},{kind:"get",static:!0,key:"styles",value:function(){return d.AH`:host{display:block;position:var(--chart-base-position,relative)}.animationContainer{overflow:hidden;height:0;transition:height .3s cubic-bezier(.4, 0, .2, 1)}canvas{max-height:var(--chart-max-height,400px)}.chartLegend{text-align:center}.chartLegend li{cursor:pointer;display:inline-grid;grid-auto-flow:column;padding:0 8px;box-sizing:border-box;align-items:center;color:var(--secondary-text-color)}.chartLegend .hidden{text-decoration:line-through}.chartLegend .label{text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.chartLegend .bullet,.chartTooltip .bullet{border-width:1px;border-style:solid;border-radius:50%;display:inline-block;height:16px;margin-right:6px;width:16px;flex-shrink:0;box-sizing:border-box;margin-inline-end:6px;margin-inline-start:initial;direction:var(--direction)}.chartTooltip .bullet{align-self:baseline}.chartTooltip{padding:8px;font-size:90%;position:absolute;background:rgba(80,80,80,.9);color:#fff;border-radius:4px;pointer-events:none;z-index:1;-ms-user-select:none;-webkit-user-select:none;-moz-user-select:none;width:200px;box-sizing:border-box;direction:var(--direction)}.chartLegend ul,.chartTooltip ul{display:inline-block;padding:0 0px;margin:8px 0 0 0;width:100%}.chartTooltip ul{margin:0 4px}.chartTooltip li{display:flex;white-space:pre-line;word-break:break-word;align-items:center;line-height:16px;padding:4px 0}.chartTooltip .title{text-align:center;font-weight:500;word-break:break-word;direction:ltr}.chartTooltip .footer{font-weight:500}.chartTooltip .beforeBody{text-align:center;font-weight:300;word-break:break-all}`}}]}}),d.WF)},14511:(t,e,i)=>{i.a(t,(async(t,a)=>{try{i.d(e,{n:()=>g});var s=i(36312),d=(i(89655),i(24545),i(51855),i(82130),i(31743),i(22328),i(4959),i(62435),i(253),i(54846),i(16891),i(15112)),n=i(77706),o=i(94100),l=i(46999),r=i(33922),h=i(34897),c=i(57636),p=i(4826),u=(i(90701),i(56136)),f=t([c]);c=(f.then?(await f)():f)[0];const g={mean:"mean",min:"min",max:"max",sum:"sum",state:"sum",change:"sum"};(0,s.A)([(0,n.EM)("statistics-chart")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"statisticsData",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"metadata",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"names",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"unit",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"endTime",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"statTypes",value:()=>["sum","min","mean","max"]},{kind:"field",decorators:[(0,n.MZ)()],key:"chartType",value:()=>"line"},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"hideLegend",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"logarithmicScale",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"isLoadingData",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"clickForMoreInfo",value:()=>!0},{kind:"field",decorators:[(0,n.MZ)()],key:"period",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_chartData",value:()=>({datasets:[]})},{kind:"field",decorators:[(0,n.wk)()],key:"_chartDatasetExtra",value:()=>[]},{kind:"field",decorators:[(0,n.wk)()],key:"_statisticIds",value:()=>[]},{kind:"field",decorators:[(0,n.wk)()],key:"_chartOptions",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_hiddenStats",value:()=>new Set},{kind:"field",decorators:[(0,n.P)("ha-chart-base")],key:"_chart",value:void 0},{kind:"field",key:"_computedStyle",value:void 0},{kind:"field",key:"resize",value(){return t=>{this._chart?.resize(t)}}},{kind:"method",key:"shouldUpdate",value:function(t){return t.size>1||!t.has("hass")}},{kind:"method",key:"willUpdate",value:function(t){t.has("legendMode")&&this._hiddenStats.clear(),(!this.hasUpdated||t.has("unit")||t.has("period")||t.has("chartType")||t.has("logarithmicScale")||t.has("hideLegend"))&&this._createOptions(),(t.has("statisticsData")||t.has("statTypes")||t.has("chartType")||t.has("hideLegend")||t.has("_hiddenStats"))&&this._generateData()}},{kind:"method",key:"firstUpdated",value:function(){this._computedStyle=getComputedStyle(this)}},{kind:"method",key:"render",value:function(){return(0,r.x)(this.hass,"history")?this.isLoadingData&&!this.statisticsData?d.qy`<div class="info"> ${this.hass.localize("ui.components.statistics_charts.loading_statistics")} </div>`:this.statisticsData&&Object.keys(this.statisticsData).length?d.qy` <ha-chart-base externalHidden .hass="${this.hass}" .data="${this._chartData}" .extraData="${this._chartDatasetExtra}" .options="${this._chartOptions}" .chartType="${this.chartType}" @dataset-hidden="${this._datasetHidden}" @dataset-unhidden="${this._datasetUnhidden}"></ha-chart-base> `:d.qy`<div class="info"> ${this.hass.localize("ui.components.statistics_charts.no_statistics_found")} </div>`:d.qy`<div class="info"> ${this.hass.localize("ui.components.history_charts.history_disabled")} </div>`}},{kind:"method",key:"_datasetHidden",value:function(t){t.stopPropagation(),this._hiddenStats.add(this._statisticIds[t.detail.index]),this.requestUpdate("_hiddenStats")}},{kind:"method",key:"_datasetUnhidden",value:function(t){t.stopPropagation(),this._hiddenStats.delete(this._statisticIds[t.detail.index]),this.requestUpdate("_hiddenStats")}},{kind:"method",key:"_createOptions",value:function(t){this._chartOptions={parsing:!1,animation:!1,interaction:{mode:"nearest",axis:"x"},scales:{x:{type:"time",adapters:{date:{locale:this.hass.locale,config:this.hass.config}},ticks:{source:"bar"===this.chartType?"data":void 0,maxRotation:0,sampleSize:5,autoSkipPadding:20,major:{enabled:!0},font:t=>t.tick&&t.tick.major?{weight:"bold"}:{}},time:{tooltipFormat:"datetime",unit:"bar"===this.chartType&&this.period&&["hour","day","week","month"].includes(this.period)?this.period:void 0}},y:{beginAtZero:"bar"===this.chartType,ticks:{maxTicksLimit:7},title:{display:t||this.unit,text:t||this.unit},type:this.logarithmicScale?"logarithmic":"linear"}},plugins:{tooltip:{callbacks:{label:t=>`${t.dataset.label}: ${(0,c.ZV)(t.parsed.y,this.hass.locale,(0,c.ZQ)(void 0,this.hass.entities[this._statisticIds[t.datasetIndex]]))} ${t.dataset.unit||""}`}},filler:{propagate:!0},legend:{display:!this.hideLegend,labels:{usePointStyle:!0}}},elements:{line:{tension:.4,cubicInterpolationMode:"monotone",borderWidth:1.5},bar:{borderWidth:1.5,borderRadius:4},point:{hitRadius:50}},locale:(0,c.Yf)(this.hass.locale),onClick:t=>{if(!this.clickForMoreInfo||(0,u.a)(t))return;const e=t.chart,i=e.getElementsAtEventForMode(t,"nearest",{intersect:!0},!0);if(i.length){const t=i[0],a=this._statisticIds[t.datasetIndex];(0,p.OQ)(a)||((0,h.r)(this,"hass-more-info",{entityId:a}),e.canvas.dispatchEvent(new Event("mouseout")))}}}}},{kind:"field",key:"_getStatisticsMetaData",value(){return(0,o.A)((async t=>{const e=await(0,p.Wr)(this.hass,t),i={};return e.forEach((t=>{i[t.statistic_id]=t})),i}))}},{kind:"method",key:"_generateData",value:async function(){if(!this.statisticsData)return;const t=this.metadata||await this._getStatisticsMetaData(Object.keys(this.statisticsData));let e=0;const i=Object.entries(this.statisticsData),a=[],s=[],d=[];let n,o;if(0===i.length)return;n=this.endTime||new Date(Math.max(...i.map((([t,e])=>new Date(e[e.length-1].start).getTime())))),n>new Date&&(n=new Date);const r=this.names||{};i.forEach((([i,n])=>{const h=t?.[i];let c=r[i];void 0===c&&(c=(0,p.$O)(this.hass,i,h)),this.unit||(void 0===o?o=(0,p.JE)(this.hass,i,h):null!==o&&o!==(0,p.JE)(this.hass,i,h)&&(o=null));let u,f=null;const g=[],m=[],y=(t,e,i)=>{i&&(t>e||(g.forEach(((e,a)=>{"line"===this.chartType&&u&&f&&u.getTime()!==t.getTime()&&(e.data.push({x:u.getTime(),y:f[a]}),e.data.push({x:u.getTime(),y:null})),e.data.push({x:t.getTime(),y:i[a]})})),f=i,u=e))},v=(0,l.fI)(e,this._computedStyle||getComputedStyle(this));e++;const k=[],_=this.statTypes.includes("mean")&&(0,p.iY)(n,"mean"),x=_||this.statTypes.includes("min")&&(0,p.iY)(n,"min")&&this.statTypes.includes("max")&&(0,p.iY)(n,"max"),b=x?[...this.statTypes].sort(((t,e)=>"min"===t||"max"===e?-1:"max"===t||"min"===e?1:0)):this.statTypes;let w=!1;b.forEach((t=>{if((0,p.iY)(n,t)){const e=x&&("min"===t||"max"===t);if(!this.hideLegend){const e=_?"mean"===t:!1===w;m.push({legend_label:c,show_legend:e}),w=w||e}k.push(t),g.push({label:c?`${c} (${this.hass.localize(`ui.components.statistics_charts.statistic_types.${t}`)})\n            `:this.hass.localize(`ui.components.statistics_charts.statistic_types.${t}`),fill:!!x&&("min"===t&&_?"+1":"max"===t&&"-1"),borderColor:e&&_?v+(this.hideLegend?"00":"7F"):v,backgroundColor:e?v+"3F":v+"7F",pointRadius:0,hidden:!this.hideLegend&&this._hiddenStats.has(i),data:[],unit:h?.unit_of_measurement,band:e}),d.push(i)}}));let $=null,C=null;n.forEach((t=>{const e=new Date(t.start);if($===e)return;$=e;const i=[];k.forEach((e=>{let a;"sum"===e?null==C?(a=0,C=t.sum):a=(t.sum||0)-C:a=t[e],i.push(a??null)})),y(e,new Date(t.end),i)})),Array.prototype.push.apply(a,g),Array.prototype.push.apply(s,m)})),o&&this._createOptions(o),this._chartData={datasets:a},this._chartDatasetExtra=s,this._statisticIds=d}},{kind:"get",static:!0,key:"styles",value:function(){return d.AH`:host{display:block;min-height:60px}.info{text-align:center;line-height:60px;color:var(--secondary-text-color)}`}}]}}),d.WF);a()}catch(t){a(t)}}))},90431:(t,e,i)=>{var a=i(36312),s=i(68689),d=i(44331),n=i(67449),o=i(15112),l=i(77706),r=i(74005);(0,a.A)([(0,l.EM)("ha-textfield")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"invalid",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"icon",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"iconTrailing",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)()],key:"autocomplete",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"autocorrect",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:"input-spellcheck"})],key:"inputSpellcheck",value:void 0},{kind:"field",decorators:[(0,l.P)("input")],key:"formElement",value:void 0},{kind:"method",key:"updated",value:function(t){(0,s.A)(i,"updated",this,3)([t]),(t.has("invalid")||t.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||t.has("invalid")&&void 0!==t.get("invalid"))&&this.reportValidity()),t.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),t.has("autocorrect")&&(this.autocorrect?this.formElement.setAttribute("autocorrect",this.autocorrect):this.formElement.removeAttribute("autocorrect")),t.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}},{kind:"method",key:"renderIcon",value:function(t,e=!1){const i=e?"trailing":"leading";return o.qy` <span class="mdc-text-field__icon mdc-text-field__icon--${i}" tabindex="${e?1:-1}"> <slot name="${i}Icon"></slot> </span> `}},{kind:"field",static:!0,key:"styles",value:()=>[n.R,o.AH`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){text-overflow:ellipsis;width:inherit;padding-right:30px;padding-inline-end:30px;padding-inline-start:initial;box-sizing:border-box;direction:var(--direction)}input{text-align:var(--text-field-text-align,start)}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start)}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}`,"rtl"===r.G.document.dir?o.AH`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}`:o.AH``]}]}}),d.J)},45003:(t,e,i)=>{i.d(e,{j:()=>a});const a=["relative","total","date","time","datetime"]},80780:(t,e,i)=>{i.a(t,(async(t,a)=>{try{i.r(e),i.d(e,{HuiStatisticsGraphCardEditor:()=>w});var s=i(36312),d=(i(89655),i(24545),i(51855),i(82130),i(31743),i(22328),i(4959),i(62435),i(253),i(2075),i(94438),i(16891),i(4525),i(15112)),n=i(77706),o=i(94100),l=i(66419),r=i(21863),h=i(34897),c=i(16569),p=i(14511),u=(i(67184),i(36185),i(4826)),f=i(62241),g=i(56124),m=i(93161),y=i(44297),v=t([p]);p=(v.then?(await v)():v)[0];const k=(0,l.KC)([(0,l.eu)("state"),(0,l.eu)("sum"),(0,l.eu)("change"),(0,l.eu)("min"),(0,l.eu)("max"),(0,l.eu)("mean")]),_=(0,l.kp)(g.H,(0,l.Ik)({entities:(0,l.YO)(m.l),title:(0,l.lq)((0,l.Yj)()),days_to_show:(0,l.lq)((0,l.ai)()),period:(0,l.lq)((0,l.KC)([(0,l.eu)("5minute"),(0,l.eu)("hour"),(0,l.eu)("day"),(0,l.eu)("week"),(0,l.eu)("month")])),chart_type:(0,l.lq)((0,l.KC)([(0,l.eu)("bar"),(0,l.eu)("line")])),stat_types:(0,l.lq)((0,l.KC)([(0,l.YO)(k),k])),unit:(0,l.lq)((0,l.Yj)()),hide_legend:(0,l.lq)((0,l.zM)()),logarithmic_scale:(0,l.lq)((0,l.zM)())})),x=["5minute","hour","day","week","month"],b=["mean","min","max","sum","state","change"];let w=(0,s.A)([(0,n.EM)("hui-statistics-graph-card-editor")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_configEntities",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_metaDatas",value:void 0},{kind:"method",key:"setConfig",value:function(t){(0,l.vA)(t,_),this._config=t,this._configEntities=t.entities?(0,f.L)(t.entities,!1).map((t=>t.entity)):[]}},{kind:"field",key:"_getStatisticsMetaData",value(){return async t=>{this._metaDatas=await(0,u.Wr)(this.hass,t||[])}}},{kind:"method",key:"willUpdate",value:function(t){t.has("_configEntities")&&!(0,c.b)(this._configEntities,t.get("_configEntities"))&&(this._metaDatas=void 0,this._configEntities?.length&&this._getStatisticsMetaData(this._configEntities))}},{kind:"field",key:"_schema",value(){return(0,o.A)(((t,e,i)=>{const a=new Set;i?.forEach((t=>{const e=(0,u.JE)(this.hass,t.statistic_id,t);e&&a.add(e)}));const s=[{name:"title",selector:{text:{}}},{name:"",type:"grid",schema:[{name:"period",required:!0,selector:{select:{options:x.map((i=>({value:i,label:t(`ui.panel.lovelace.editor.card.statistics-graph.periods.${i}`),disabled:"5minute"===i&&e?.some((t=>(0,u.OQ)(t)))})))}}},{name:"days_to_show",default:y.DEFAULT_DAYS_TO_SHOW,selector:{number:{min:1,mode:"box"}}},{name:"stat_types",required:!0,selector:{select:{multiple:!0,mode:"list",options:b.map((e=>({value:e,label:t(`ui.panel.lovelace.editor.card.statistics-graph.stat_type_labels.${e}`),disabled:!i||!i.some((t=>(0,u.nN)(t,p.n[e])))})))}}},{name:"chart_type",required:!0,type:"select",options:[["line","Line"],["bar","Bar"]]},{name:"hide_legend",required:!1,selector:{boolean:{}}},{name:"logarithmic_scale",required:!1,selector:{boolean:{}}}]}];return a.size>1&&s[1].schema.push({name:"unit",required:!1,selector:{select:{options:Array.from(a).map((t=>({value:t,label:t})))}}}),s}))}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return d.s6;const t=this._schema(this.hass.localize,this._configEntities,this._metaDatas),e=this._config.stat_types?(0,r.e)(this._config.stat_types):b.filter((t=>this._metaDatas?.some((e=>(0,u.nN)(e,t))))),i={chart_type:"line",period:"hour",...this._config,stat_types:e},a=this._metaDatas?.[0]?.unit_class,s=a?void 0:this._metaDatas?.[0]?.statistics_unit_of_measurement;return d.qy` <ha-form .hass="${this.hass}" .data="${i}" .schema="${t}" .computeLabel="${this._computeLabelCallback}" @value-changed="${this._valueChanged}"></ha-form> <ha-statistics-picker allow-custom-entity .hass="${this.hass}" .pickStatisticLabel="${this.hass.localize("ui.panel.lovelace.editor.card.statistics-graph.pick_statistic")}" .pickedStatisticLabel="${this.hass.localize("ui.panel.lovelace.editor.card.statistics-graph.picked_statistic")}" .includeStatisticsUnitOfMeasurement="${s}" .includeUnitClass="${a}" .ignoreRestrictionsOnFirstStatistic="${!0}" .value="${this._configEntities}" .configValue="${"entities"}" @value-changed="${this._entitiesChanged}"></ha-statistics-picker> `}},{kind:"method",key:"_valueChanged",value:function(t){(0,h.r)(this,"config-changed",{config:t.detail.value})}},{kind:"method",key:"_entitiesChanged",value:async function(t){const e=t.detail.value,i=e.map((t=>this._config.entities.find((e=>"string"!=typeof e&&e.entity===t))??t)),a={...this._config,entities:i};e?.some((t=>(0,u.OQ)(t)))&&"5minute"===a.period&&delete a.period;const s=a.stat_types||a.unit?await(0,u.Wr)(this.hass,e):void 0;a.stat_types&&a.entities.length&&(a.stat_types=(0,r.e)(a.stat_types).filter((t=>s.some((e=>(0,u.nN)(e,t))))),a.stat_types.length||delete a.stat_types),a.unit&&!s.some((t=>(0,u.JE)(this.hass,t?.statistic_id,t)===a.unit))&&delete a.unit,(0,h.r)(this,"config-changed",{config:a})}},{kind:"field",key:"_computeLabelCallback",value(){return t=>{switch(t.name){case"chart_type":case"stat_types":case"period":case"unit":case"hide_legend":case"logarithmic_scale":return this.hass.localize(`ui.panel.lovelace.editor.card.statistics-graph.${t.name}`);default:return this.hass.localize(`ui.panel.lovelace.editor.card.generic.${t.name}`)}}}},{kind:"field",static:!0,key:"styles",value:()=>d.AH`ha-statistics-picker{width:100%}`}]}}),d.WF);a()}catch(t){a(t)}}))},56124:(t,e,i)=>{i.d(e,{H:()=>s});var a=i(66419);const s=(0,a.Ik)({type:(0,a.Yj)(),view_layout:(0,a.bz)(),layout_options:(0,a.bz)(),visibility:(0,a.bz)()})},93161:(t,e,i)=>{i.d(e,{l:()=>n});var a=i(66419),s=i(45003),d=i(76914);const n=(0,a.KC)([(0,a.Ik)({entity:(0,a.Yj)(),name:(0,a.lq)((0,a.Yj)()),icon:(0,a.lq)((0,a.Yj)()),image:(0,a.lq)((0,a.Yj)()),secondary_info:(0,a.lq)((0,a.Yj)()),format:(0,a.lq)((0,a.vP)(s.j)),state_color:(0,a.lq)((0,a.zM)()),tap_action:(0,a.lq)(d.k),hold_action:(0,a.lq)(d.k),double_tap_action:(0,a.lq)(d.k)}),(0,a.Yj)()])}};
//# sourceMappingURL=18174.fBO7X15gCKw.js.map