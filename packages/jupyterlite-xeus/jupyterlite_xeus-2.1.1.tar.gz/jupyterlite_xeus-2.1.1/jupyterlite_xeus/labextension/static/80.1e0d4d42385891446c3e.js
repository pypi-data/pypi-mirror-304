"use strict";(self.webpackChunk_jupyterlite_xeus=self.webpackChunk_jupyterlite_xeus||[]).push([[80],{80:(e,t,s)=>{s.r(t),s.d(t,{default:()=>k});var n=s(473),i=s(671),r=s(232),o=s(257),a=s(115),l=s.n(a),c=s(721),d=s(602),h=s(262);class p{constructor(e){this._contentsProcessor=void 0,this._isDisposed=!1,this._disposed=new d.Signal(this),this._executeDelegate=new h.PromiseDelegate,this._parentHeader=void 0,this._parent=void 0,this._ready=new h.PromiseDelegate;const{id:t,name:s,sendMessage:n,location:i,kernelSpec:r,contentsManager:o,empackEnvMetaLink:a}=e;this._id=t,this._name=s,this._location=i,this._kernelSpec=r,this._contentsManager=o,this._sendMessage=n,this._empackEnvMetaLink=a,this._worker=this.initWorker(e),this._remoteKernel=this.initRemote(e),this.initFileSystem(e)}initWorker(e){return crossOriginIsolated?new Worker(new URL(s.p+s.u(873),s.b),{type:void 0}):new Worker(new URL(s.p+s.u(950),s.b),{type:void 0})}initRemote(e){let t;return crossOriginIsolated?(this._worker.onmessage=this._processCoincidentWorkerMessage.bind(this),t=l()(this._worker),t.processDriveRequest=async e=>{if(!r.DriveContentsProcessor)throw new Error("File system calls over Atomics.wait is only supported with jupyterlite>=0.4.0a3");return void 0===this._contentsProcessor&&(this._contentsProcessor=new r.DriveContentsProcessor({contentsManager:this._contentsManager})),await this._contentsProcessor.processDriveRequest(e)}):(this._worker.onmessage=e=>{this._processComlinkWorkerMessage(e.data)},t=(0,c.wrap)(this._worker)),t.initialize({kernelSpec:this._kernelSpec,baseUrl:n.PageConfig.getBaseUrl(),mountDrive:e.mountDrive,empackEnvMetaLink:this._empackEnvMetaLink}).then(this._ready.resolve.bind(this._ready)),t}async handleMessage(e){this._parent=e,this._parentHeader=e.header,await this._sendMessageToWorker(e)}async _sendMessageToWorker(e){if("input_reply"!==e.header.msg_type&&(this._executeDelegate=new h.PromiseDelegate),await this._remoteKernel.processMessage({msg:e,parent:this.parent}),"input_reply"!==e.header.msg_type)return await this._executeDelegate.promise}get parentHeader(){return this._parentHeader}get parent(){return this._parent}get location(){return this._location}_processCoincidentWorkerMessage(e){var t,s,n,i,r;(null===(t=e.data)||void 0===t?void 0:t.header)&&(e.data.header.session=null!==(n=null===(s=this._parentHeader)||void 0===s?void 0:s.session)&&void 0!==n?n:"",e.data.session=null!==(r=null===(i=this._parentHeader)||void 0===i?void 0:i.session)&&void 0!==r?r:"",this._sendMessage(e.data),"status"===e.data.header.msg_type&&"idle"===e.data.content.execution_state&&this._executeDelegate.resolve())}_processComlinkWorkerMessage(e){var t,s,n,i;e.header&&(e.header.session=null!==(s=null===(t=this._parentHeader)||void 0===t?void 0:t.session)&&void 0!==s?s:"",e.session=null!==(i=null===(n=this._parentHeader)||void 0===n?void 0:n.session)&&void 0!==i?i:"",this._sendMessage(e),"status"===e.header.msg_type&&"idle"===e.content.execution_state&&this._executeDelegate.resolve())}get ready(){return this._ready.promise}get isDisposed(){return this._isDisposed}get disposed(){return this._disposed}dispose(){this.isDisposed||(this._worker.terminate(),this._worker=null,this._remoteKernel=null,this._isDisposed=!0,this._disposed.emit(void 0))}get id(){return this._id}get name(){return this._name}async initFileSystem(e){let t,s;if(e.location.includes(":")){const n=e.location.split(":");t=n[0],s=n[1]}else t="",s=e.location;await this._remoteKernel.ready(),await this._remoteKernel.mount(t,"/drive",n.PageConfig.getBaseUrl()),await this._remoteKernel.isDir("/files")?await this._remoteKernel.cd("/files"):await this._remoteKernel.cd(s)}}const u=new h.Token("@jupyterlite/xeus:IEmpackEnvMetaFile");function _(e){const t=n.URLExt.join(n.PageConfig.getBaseUrl(),e),s=new XMLHttpRequest;return s.open("GET",t,!1),s.send(null),JSON.parse(s.responseText)}let g=[];try{g=_("xeus/kernels.json")}catch(e){throw console.log(`Could not fetch xeus/kernels.json: ${e}`),e}const m=g.map((e=>({id:`@jupyterlite/xeus-${e}:register`,autoStart:!0,requires:[o.IKernelSpecs],optional:[i.IServiceWorkerManager,r.IBroadcastChannelWrapper,u],activate:(t,s,i,r,o)=>{const a=_("xeus/kernels/"+e+"/kernel.json");a.name=e,a.dir=e;for(const[e,t]of Object.entries(a.resources))a.resources[e]=n.URLExt.join(n.PageConfig.getBaseUrl(),t);const l=t.serviceManager.contents;s.register({spec:a,create:async e=>{const t=!!((null==i?void 0:i.enabled)&&(null==r?void 0:r.enabled)||crossOriginIsolated);t?console.info(`${a.name} contents will be synced with Jupyter Contents`):console.warn(`${a.name} contents will NOT be synced with Jupyter Contents`);const s=o?await o.getLink(a):"";return new p({...e,contentsManager:l,mountDrive:t,kernelSpec:a,empackEnvMetaLink:s})}})}}))),v={id:"@jupyterlite/xeus:empack-env-meta",autoStart:!0,provides:u,activate:()=>({getLink:async e=>{const t=e.name;return`${n.URLExt.join(n.PageConfig.getBaseUrl(),`xeus/kernels/${t}`)}`}})};m.push(v);const k=m}}]);