export const id=47054;export const ids=[47054];export const modules={47054:(e,t,i)=>{i.r(t),i.d(t,{default:()=>s});i(253),i(5186),i(2075),i(16891),i(4525),i(74860),i(71011),i(71174);class a{constructor(e,t,i,s,n){this._legacyCanvasSize=a.DEFAULT_CANVAS_SIZE,this._preferredCamera="environment",this._maxScansPerSecond=25,this._lastScanTimestamp=-1,this._destroyed=this._flashOn=this._paused=this._active=!1,this.$video=e,this.$canvas=document.createElement("canvas"),i&&"object"==typeof i?this._onDecode=t:(i||s||n?console.warn("You're using a deprecated version of the QrScanner constructor which will be removed in the future"):console.warn("Note that the type of the scan result passed to onDecode will change in the future. To already switch to the new api today, you can pass returnDetailedScanResult: true."),this._legacyOnDecode=t),t="object"==typeof i?i:{},this._onDecodeError=t.onDecodeError||("function"==typeof i?i:this._onDecodeError),this._calculateScanRegion=t.calculateScanRegion||("function"==typeof s?s:this._calculateScanRegion),this._preferredCamera=t.preferredCamera||n||this._preferredCamera,this._legacyCanvasSize="number"==typeof i?i:"number"==typeof s?s:this._legacyCanvasSize,this._maxScansPerSecond=t.maxScansPerSecond||this._maxScansPerSecond,this._onPlay=this._onPlay.bind(this),this._onLoadedMetaData=this._onLoadedMetaData.bind(this),this._onVisibilityChange=this._onVisibilityChange.bind(this),this._updateOverlay=this._updateOverlay.bind(this),e.disablePictureInPicture=!0,e.playsInline=!0,e.muted=!0;let r=!1;if(e.hidden&&(e.hidden=!1,r=!0),document.body.contains(e)||(document.body.appendChild(e),r=!0),i=e.parentElement,t.highlightScanRegion||t.highlightCodeOutline){if(s=!!t.overlay,this.$overlay=t.overlay||document.createElement("div"),(n=this.$overlay.style).position="absolute",n.display="none",n.pointerEvents="none",this.$overlay.classList.add("scan-region-highlight"),!s&&t.highlightScanRegion){this.$overlay.innerHTML='<svg class="scan-region-highlight-svg" viewBox="0 0 238 238" preserveAspectRatio="none" style="position:absolute;width:100%;height:100%;left:0;top:0;fill:none;stroke:#e9b213;stroke-width:4;stroke-linecap:round;stroke-linejoin:round"><path d="M31 2H10a8 8 0 0 0-8 8v21M207 2h21a8 8 0 0 1 8 8v21m0 176v21a8 8 0 0 1-8 8h-21m-176 0H10a8 8 0 0 1-8-8v-21"/></svg>';try{this.$overlay.firstElementChild.animate({transform:["scale(.98)","scale(1.01)"]},{duration:400,iterations:1/0,direction:"alternate",easing:"ease-in-out"})}catch(e){}i.insertBefore(this.$overlay,this.$video.nextSibling)}t.highlightCodeOutline&&(this.$overlay.insertAdjacentHTML("beforeend",'<svg class="code-outline-highlight" preserveAspectRatio="none" style="display:none;width:100%;height:100%;fill:none;stroke:#e9b213;stroke-width:5;stroke-dasharray:25;stroke-linecap:round;stroke-linejoin:round"><polygon/></svg>'),this.$codeOutlineHighlight=this.$overlay.lastElementChild)}this._scanRegion=this._calculateScanRegion(e),requestAnimationFrame((()=>{let t=window.getComputedStyle(e);"none"===t.display&&(e.style.setProperty("display","block","important"),r=!0),"visible"!==t.visibility&&(e.style.setProperty("visibility","visible","important"),r=!0),r&&(console.warn("QrScanner has overwritten the video hiding style to avoid Safari stopping the playback."),e.style.opacity="0",e.style.width="0",e.style.height="0",this.$overlay&&this.$overlay.parentElement&&this.$overlay.parentElement.removeChild(this.$overlay),delete this.$overlay,delete this.$codeOutlineHighlight),this.$overlay&&this._updateOverlay()})),e.addEventListener("play",this._onPlay),e.addEventListener("loadedmetadata",this._onLoadedMetaData),document.addEventListener("visibilitychange",this._onVisibilityChange),window.addEventListener("resize",this._updateOverlay),this._qrEnginePromise=a.createQrEngine()}static set WORKER_PATH(e){console.warn("Setting QrScanner.WORKER_PATH is not required and not supported anymore. Have a look at the README for new setup instructions.")}static async hasCamera(){try{return!!(await a.listCameras(!1)).length}catch(e){return!1}}static async listCameras(e=!1){if(!navigator.mediaDevices)return[];let t,i=async()=>(await navigator.mediaDevices.enumerateDevices()).filter((e=>"videoinput"===e.kind));try{e&&(await i()).every((e=>!e.label))&&(t=await navigator.mediaDevices.getUserMedia({audio:!1,video:!0}))}catch(e){}try{return(await i()).map(((e,t)=>({id:e.deviceId,label:e.label||(0===t?"Default Camera":`Camera ${t+1}`)})))}finally{t&&(console.warn("Call listCameras after successfully starting a QR scanner to avoid creating a temporary video stream"),a._stopVideoStream(t))}}async hasFlash(){let e;try{if(this.$video.srcObject){if(!(this.$video.srcObject instanceof MediaStream))return!1;e=this.$video.srcObject}else e=(await this._getCameraStream()).stream;return"torch"in e.getVideoTracks()[0].getSettings()}catch(e){return!1}finally{e&&e!==this.$video.srcObject&&(console.warn("Call hasFlash after successfully starting the scanner to avoid creating a temporary video stream"),a._stopVideoStream(e))}}isFlashOn(){return this._flashOn}async toggleFlash(){this._flashOn?await this.turnFlashOff():await this.turnFlashOn()}async turnFlashOn(){if(!this._flashOn&&!this._destroyed&&(this._flashOn=!0,this._active&&!this._paused))try{if(!await this.hasFlash())throw"No flash available";await this.$video.srcObject.getVideoTracks()[0].applyConstraints({advanced:[{torch:!0}]})}catch(e){throw this._flashOn=!1,e}}async turnFlashOff(){this._flashOn&&(this._flashOn=!1,await this._restartVideoStream())}destroy(){this.$video.removeEventListener("loadedmetadata",this._onLoadedMetaData),this.$video.removeEventListener("play",this._onPlay),document.removeEventListener("visibilitychange",this._onVisibilityChange),window.removeEventListener("resize",this._updateOverlay),this._destroyed=!0,this._flashOn=!1,this.stop(),a._postWorkerMessage(this._qrEnginePromise,"close")}async start(){if(this._destroyed)throw Error("The QR scanner can not be started as it had been destroyed.");if((!this._active||this._paused)&&("https:"!==window.location.protocol&&console.warn("The camera stream is only accessible if the page is transferred via https."),this._active=!0,!document.hidden))if(this._paused=!1,this.$video.srcObject)await this.$video.play();else try{let{stream:e,facingMode:t}=await this._getCameraStream();!this._active||this._paused?a._stopVideoStream(e):(this._setVideoMirror(t),this.$video.srcObject=e,await this.$video.play(),this._flashOn&&(this._flashOn=!1,this.turnFlashOn().catch((()=>{}))))}catch(e){if(!this._paused)throw this._active=!1,e}}stop(){this.pause(),this._active=!1}async pause(e=!1){if(this._paused=!0,!this._active)return!0;this.$video.pause(),this.$overlay&&(this.$overlay.style.display="none");let t=()=>{this.$video.srcObject instanceof MediaStream&&(a._stopVideoStream(this.$video.srcObject),this.$video.srcObject=null)};return e?(t(),!0):(await new Promise((e=>setTimeout(e,300))),!!this._paused&&(t(),!0))}async setCamera(e){e!==this._preferredCamera&&(this._preferredCamera=e,await this._restartVideoStream())}static async scanImage(e,t,i,s,n=!1,r=!1){let o,h=!1;t&&("scanRegion"in t||"qrEngine"in t||"canvas"in t||"disallowCanvasResizing"in t||"alsoTryWithoutScanRegion"in t||"returnDetailedScanResult"in t)?(o=t.scanRegion,i=t.qrEngine,s=t.canvas,n=t.disallowCanvasResizing||!1,r=t.alsoTryWithoutScanRegion||!1,h=!0):t||i||s||n||r?console.warn("You're using a deprecated api for scanImage which will be removed in the future."):console.warn("Note that the return type of scanImage will change in the future. To already switch to the new api today, you can pass returnDetailedScanResult: true."),t=!!i;try{let d,c,l;if([i,d]=await Promise.all([i||a.createQrEngine(),a._loadImage(e)]),[s,c]=a._drawToCanvas(d,o,s,n),i instanceof Worker){let e=i;t||a._postWorkerMessageSync(e,"inversionMode","both"),l=await new Promise(((t,i)=>{let n,r,h,d=-1;r=s=>{s.data.id===d&&(e.removeEventListener("message",r),e.removeEventListener("error",h),clearTimeout(n),null!==s.data.data?t({data:s.data.data,cornerPoints:a._convertPoints(s.data.cornerPoints,o)}):i(a.NO_QR_CODE_FOUND))},h=t=>{e.removeEventListener("message",r),e.removeEventListener("error",h),clearTimeout(n),i("Scanner error: "+(t?t.message||t:"Unknown Error"))},e.addEventListener("message",r),e.addEventListener("error",h),n=setTimeout((()=>h("timeout")),1e4);let l=c.getImageData(0,0,s.width,s.height);d=a._postWorkerMessageSync(e,"decode",l,[l.data.buffer])}))}else l=await Promise.race([new Promise(((e,t)=>window.setTimeout((()=>t("Scanner error: timeout")),1e4))),(async()=>{try{var[t]=await i.detect(s);if(!t)throw a.NO_QR_CODE_FOUND;return{data:t.rawValue,cornerPoints:a._convertPoints(t.cornerPoints,o)}}catch(i){if(t=i.message||i,/not implemented|service unavailable/.test(t))return a._disableBarcodeDetector=!0,a.scanImage(e,{scanRegion:o,canvas:s,disallowCanvasResizing:n,alsoTryWithoutScanRegion:r});throw`Scanner error: ${t}`}})()]);return h?l:l.data}catch(t){if(!o||!r)throw t;let d=await a.scanImage(e,{qrEngine:i,canvas:s,disallowCanvasResizing:n});return h?d:d.data}finally{t||a._postWorkerMessage(i,"close")}}setGrayscaleWeights(e,t,i,s=!0){a._postWorkerMessage(this._qrEnginePromise,"grayscaleWeights",{red:e,green:t,blue:i,useIntegerApproximation:s})}setInversionMode(e){a._postWorkerMessage(this._qrEnginePromise,"inversionMode",e)}static async createQrEngine(e){if(e&&console.warn("Specifying a worker path is not required and not supported anymore."),e=()=>i.e(76465).then(i.bind(i,76465)).then((e=>e.createWorker())),a._disableBarcodeDetector||!("BarcodeDetector"in window)||!BarcodeDetector.getSupportedFormats||!(await BarcodeDetector.getSupportedFormats()).includes("qr_code"))return e();let t=navigator.userAgentData;return t&&t.brands.some((({brand:e})=>/Chromium/i.test(e)))&&/mac ?OS/i.test(t.platform)&&await t.getHighEntropyValues(["architecture","platformVersion"]).then((({architecture:e,platformVersion:t})=>/arm/i.test(e||"arm")&&13<=parseInt(t||"13"))).catch((()=>!0))?e():new BarcodeDetector({formats:["qr_code"]})}_onPlay(){this._scanRegion=this._calculateScanRegion(this.$video),this._updateOverlay(),this.$overlay&&(this.$overlay.style.display=""),this._scanFrame()}_onLoadedMetaData(){this._scanRegion=this._calculateScanRegion(this.$video),this._updateOverlay()}_onVisibilityChange(){document.hidden?this.pause():this._active&&this.start()}_calculateScanRegion(e){let t=Math.round(2/3*Math.min(e.videoWidth,e.videoHeight));return{x:Math.round((e.videoWidth-t)/2),y:Math.round((e.videoHeight-t)/2),width:t,height:t,downScaledWidth:this._legacyCanvasSize,downScaledHeight:this._legacyCanvasSize}}_updateOverlay(){requestAnimationFrame((()=>{if(this.$overlay){var e=this.$video,t=e.videoWidth,i=e.videoHeight,a=e.offsetWidth,s=e.offsetHeight,n=e.offsetLeft,r=e.offsetTop,o=window.getComputedStyle(e),h=o.objectFit,d=t/i,c=a/s;switch(h){case"none":var l=t,g=i;break;case"fill":l=a,g=s;break;default:("cover"===h?d>c:d<c)?l=(g=s)*d:g=(l=a)/d,"scale-down"===h&&(l=Math.min(l,t),g=Math.min(g,i))}var[v,m]=o.objectPosition.split(" ").map(((e,t)=>{const i=parseFloat(e);return e.endsWith("%")?(t?s-g:a-l)*i/100:i}));o=this._scanRegion.width||t,c=this._scanRegion.height||i,h=this._scanRegion.x||0;var u=this._scanRegion.y||0;(d=this.$overlay.style).width=o/t*l+"px",d.height=c/i*g+"px",d.top=`${r+m+u/i*g}px`,i=/scaleX\(-1\)/.test(e.style.transform),d.left=`${n+(i?a-v-l:v)+(i?t-h-o:h)/t*l}px`,d.transform=e.style.transform}}))}static _convertPoints(e,t){if(!t)return e;let i=t.x||0,a=t.y||0,s=t.width&&t.downScaledWidth?t.width/t.downScaledWidth:1;t=t.height&&t.downScaledHeight?t.height/t.downScaledHeight:1;for(let n of e)n.x=n.x*s+i,n.y=n.y*t+a;return e}_scanFrame(){!this._active||this.$video.paused||this.$video.ended||("requestVideoFrameCallback"in this.$video?this.$video.requestVideoFrameCallback.bind(this.$video):requestAnimationFrame)((async()=>{if(!(1>=this.$video.readyState)){var e=Date.now()-this._lastScanTimestamp,t=1e3/this._maxScansPerSecond;e<t&&await new Promise((i=>setTimeout(i,t-e))),this._lastScanTimestamp=Date.now();try{var i=await a.scanImage(this.$video,{scanRegion:this._scanRegion,qrEngine:this._qrEnginePromise,canvas:this.$canvas})}catch(e){if(!this._active)return;this._onDecodeError(e)}!a._disableBarcodeDetector||await this._qrEnginePromise instanceof Worker||(this._qrEnginePromise=a.createQrEngine()),i?(this._onDecode?this._onDecode(i):this._legacyOnDecode&&this._legacyOnDecode(i.data),this.$codeOutlineHighlight&&(clearTimeout(this._codeOutlineHighlightRemovalTimeout),this._codeOutlineHighlightRemovalTimeout=void 0,this.$codeOutlineHighlight.setAttribute("viewBox",`${this._scanRegion.x||0} ${this._scanRegion.y||0} ${this._scanRegion.width||this.$video.videoWidth} ${this._scanRegion.height||this.$video.videoHeight}`),this.$codeOutlineHighlight.firstElementChild.setAttribute("points",i.cornerPoints.map((({x:e,y:t})=>`${e},${t}`)).join(" ")),this.$codeOutlineHighlight.style.display="")):this.$codeOutlineHighlight&&!this._codeOutlineHighlightRemovalTimeout&&(this._codeOutlineHighlightRemovalTimeout=setTimeout((()=>this.$codeOutlineHighlight.style.display="none"),100))}this._scanFrame()}))}_onDecodeError(e){e!==a.NO_QR_CODE_FOUND&&console.log(e)}async _getCameraStream(){if(!navigator.mediaDevices)throw"Camera not found.";let e=/^(environment|user)$/.test(this._preferredCamera)?"facingMode":"deviceId",t=[{width:{min:1024}},{width:{min:768}},{}],i=t.map((t=>Object.assign({},t,{[e]:{exact:this._preferredCamera}})));for(let e of[...i,...t])try{let t=await navigator.mediaDevices.getUserMedia({video:e,audio:!1});return{stream:t,facingMode:this._getFacingMode(t)||(e.facingMode?this._preferredCamera:"environment"===this._preferredCamera?"user":"environment")}}catch(e){}throw"Camera not found."}async _restartVideoStream(){let e=this._paused;await this.pause(!0)&&!e&&this._active&&await this.start()}static _stopVideoStream(e){for(let t of e.getTracks())t.stop(),e.removeTrack(t)}_setVideoMirror(e){this.$video.style.transform="scaleX("+("user"===e?-1:1)+")"}_getFacingMode(e){return(e=e.getVideoTracks()[0])?/rear|back|environment/i.test(e.label)?"environment":/front|user|face/i.test(e.label)?"user":null:null}static _drawToCanvas(e,t,i,a=!1){i=i||document.createElement("canvas");let s=t&&t.x?t.x:0,n=t&&t.y?t.y:0,r=t&&t.width?t.width:e.videoWidth||e.width,o=t&&t.height?t.height:e.videoHeight||e.height;return a||(a=t&&t.downScaledWidth?t.downScaledWidth:r,t=t&&t.downScaledHeight?t.downScaledHeight:o,i.width!==a&&(i.width=a),i.height!==t&&(i.height=t)),(t=i.getContext("2d",{alpha:!1})).imageSmoothingEnabled=!1,t.drawImage(e,s,n,r,o,0,0,i.width,i.height),[i,t]}static async _loadImage(e){if(e instanceof Image)return await a._awaitImageLoad(e),e;if(e instanceof HTMLVideoElement||e instanceof HTMLCanvasElement||e instanceof SVGImageElement||"OffscreenCanvas"in window&&e instanceof OffscreenCanvas||"ImageBitmap"in window&&e instanceof ImageBitmap)return e;if(!(e instanceof File||e instanceof Blob||e instanceof URL||"string"==typeof e))throw"Unsupported image type.";{let t=new Image;t.src=e instanceof File||e instanceof Blob?URL.createObjectURL(e):e.toString();try{return await a._awaitImageLoad(t),t}finally{(e instanceof File||e instanceof Blob)&&URL.revokeObjectURL(t.src)}}}static async _awaitImageLoad(e){e.complete&&0!==e.naturalWidth||await new Promise(((t,i)=>{let a=s=>{e.removeEventListener("load",a),e.removeEventListener("error",a),s instanceof ErrorEvent?i("Image load error"):t()};e.addEventListener("load",a),e.addEventListener("error",a)}))}static async _postWorkerMessage(e,t,i,s){return a._postWorkerMessageSync(await e,t,i,s)}static _postWorkerMessageSync(e,t,i,s){if(!(e instanceof Worker))return-1;let n=a._workerMessageId++;return e.postMessage({id:n,type:t,data:i},s),n}}a.DEFAULT_CANVAS_SIZE=400,a.NO_QR_CODE_FOUND="No QR code found",a._disableBarcodeDetector=!1,a._workerMessageId=0;const s=a},5186:(e,t,i)=>{var a=i(41765),s=i(73201),n=i(95689),r=i(56674),o=i(1370);a({target:"Iterator",proto:!0,real:!0},{every:function(e){r(this),n(e);var t=o(this),i=0;return!s(t,(function(t,a){if(!e(t,i++))return a()}),{IS_RECORD:!0,INTERRUPTED:!0}).stopped}})}};
//# sourceMappingURL=47054.Eh3XZn4dVD0.js.map