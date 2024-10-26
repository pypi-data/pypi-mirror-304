import{s as je,A as xe,e as c,k as A,t as W,c as h,a as p,d as u,o as B,b as j,f as a,i as ne,g as s,B as te,u as he,C as He,h as z,D as ze,E as Re,F as Ge,p as Je,j as Ke,n as Qe,G as Ve}from"./scheduler.BwES1eAZ.js";import{S as Xe,i as Ye,f as Ze,b as ie,d as re,m as ue,t as fe,a as de,e as ce}from"./index.JIjGThd1.js";import{g as $e}from"./entry.Dtt6bcfU.js";import{C as et}from"./CodeEditor.rAxbRICr.js";import{C as tt}from"./ConfirmDialog.56zgi8Co.js";import{B as nt}from"./Badge.LWAVLoO-.js";import{T as st}from"./Tooltip.Dj8C3DN2.js";import{C as ot}from"./ChevronLeft.bwOsKpyw.js";function lt(n){let e,t,i,r,f;return t=new ot({props:{strokeWidth:"2.5"}}),{c(){e=c("button"),ie(t.$$.fragment),this.h()},l(l){e=h(l,"BUTTON",{class:!0,type:!0});var _=p(e);re(t.$$.fragment,_),_.forEach(u),this.h()},h(){a(e,"class","w-full text-left text-sm py-1.5 px-1 rounded-lg dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-gray-850"),a(e,"type","button")},m(l,_){ne(l,e,_),ue(t,e,null),i=!0,r||(f=he(e,"click",n[14]),r=!0)},p:Qe,i(l){i||(fe(t.$$.fragment,l),i=!0)},o(l){de(t.$$.fragment,l),i=!1},d(l){l&&u(e),ce(t),r=!1,f()}}}function at(n){let e,t,i,r;return{c(){e=c("input"),this.h()},l(f){e=h(f,"INPUT",{class:!0,type:!0,placeholder:!0}),this.h()},h(){a(e,"class","w-full text-sm disabled:text-gray-500 bg-transparent outline-none"),a(e,"type","text"),a(e,"placeholder",t=n[9].t("Function ID (e.g. my_filter)")),e.required=!0,e.disabled=n[4]},m(f,l){ne(f,e,l),te(e,n[2]),i||(r=he(e,"input",n[16]),i=!0)},p(f,l){l&512&&t!==(t=f[9].t("Function ID (e.g. my_filter)"))&&a(e,"placeholder",t),l&16&&(e.disabled=f[4]),l&4&&e.value!==f[2]&&te(e,f[2])},d(f){f&&u(e),i=!1,r()}}}function it(n){let e,t;return{c(){e=c("div"),t=W(n[2]),this.h()},l(i){e=h(i,"DIV",{class:!0});var r=p(e);t=j(r,n[2]),r.forEach(u),this.h()},h(){a(e,"class","text-sm text-gray-500 flex-shrink-0")},m(i,r){ne(i,e,r),s(e,t)},p(i,r){r&4&&z(t,i[2])},d(i){i&&u(e)}}}function rt(n){let e,t,i,r=n[9].t("Please carefully review the following warnings:")+"",f,l,_,b,x=n[9].t("Functions allow arbitrary code execution.")+"",y,v,D,k=n[9].t("Do not install functions from sources you do not fully trust.")+"",F,C,V,E=n[9].t("I acknowledge that I have read and I understand the implications of my action. I am aware of the risks associated with executing arbitrary code and I have verified the trustworthiness of the source.")+"",M;return{c(){e=c("div"),t=c("div"),i=c("div"),f=W(r),l=A(),_=c("ul"),b=c("li"),y=W(x),v=A(),D=c("li"),F=W(k),C=A(),V=c("div"),M=W(E),this.h()},l(m){e=h(m,"DIV",{class:!0});var w=p(e);t=h(w,"DIV",{class:!0});var S=p(t);i=h(S,"DIV",{});var N=p(i);f=j(N,r),N.forEach(u),l=B(S),_=h(S,"UL",{class:!0});var I=p(_);b=h(I,"LI",{});var R=p(b);y=j(R,x),R.forEach(u),v=B(I),D=h(I,"LI",{});var T=p(D);F=j(T,k),T.forEach(u),I.forEach(u),S.forEach(u),C=B(w),V=h(w,"DIV",{class:!0});var U=p(V);M=j(U,E),U.forEach(u),w.forEach(u),this.h()},h(){a(_,"class","mt-1 list-disc pl-4 text-xs"),a(t,"class","bg-yellow-500/20 text-yellow-700 dark:text-yellow-200 rounded-lg px-4 py-3"),a(V,"class","my-3"),a(e,"class","text-sm text-gray-500")},m(m,w){ne(m,e,w),s(e,t),s(t,i),s(i,f),s(t,l),s(t,_),s(_,b),s(b,y),s(_,v),s(_,D),s(D,F),s(e,C),s(e,V),s(V,M)},p(m,w){w&512&&r!==(r=m[9].t("Please carefully review the following warnings:")+"")&&z(f,r),w&512&&x!==(x=m[9].t("Functions allow arbitrary code execution.")+"")&&z(y,x),w&512&&k!==(k=m[9].t("Do not install functions from sources you do not fully trust.")+"")&&z(F,k),w&512&&E!==(E=m[9].t("I acknowledge that I have read and I understand the implications of my action. I am aware of the risks associated with executing arbitrary code and I have verified the trustworthiness of the source.")+"")&&z(M,E)},d(m){m&&u(e)}}}function ut(n){let e,t,i,r,f,l,_,b,x,y,v,D,k,F,C,V,E,M,m,w,S,N,I,R,T,U,P,G,Q=n[9].t("Warning:")+"",Y,d,se=n[9].t("Functions allow arbitrary code execution")+"",me,we,Ie,ke,Z,oe=n[9].t("don't install random functions from sources you don't trust.")+"",pe,Ee,X,le=n[9].t("Save")+"",_e,ve,O,De,L,Fe,Ce;b=new st({props:{content:n[9].t("Back"),$$slots:{default:[lt]},$$scope:{ctx:n}}}),C=new nt({props:{type:"muted",content:n[9].t("Function")}});function Pe(o,g){return o[4]?it:at}let ge=Pe(n),q=ge(n),Le={value:n[1],lang:"python",boilerplate:n[11]};I=new et({props:Le}),n[18](I),I.$on("change",n[19]),I.$on("save",n[20]);function We(o){n[23](o)}let Te={$$slots:{default:[rt]},$$scope:{ctx:n}};return n[6]!==void 0&&(Te.show=n[6]),O=new tt({props:Te}),xe.push(()=>Ze(O,"show",We)),O.$on("confirm",n[24]),{c(){e=c("div"),t=c("div"),i=c("form"),r=c("div"),f=c("div"),l=c("div"),_=c("div"),ie(b.$$.fragment),x=A(),y=c("div"),v=c("input"),k=A(),F=c("div"),ie(C.$$.fragment),V=A(),E=c("div"),q.c(),M=A(),m=c("input"),S=A(),N=c("div"),ie(I.$$.fragment),R=A(),T=c("div"),U=c("div"),P=c("div"),G=c("span"),Y=W(Q),d=A(),me=W(se),we=A(),Ie=c("br"),ke=W(`—
							`),Z=c("span"),pe=W(oe),Ee=A(),X=c("button"),_e=W(le),ve=A(),ie(O.$$.fragment),this.h()},l(o){e=h(o,"DIV",{class:!0});var g=p(e);t=h(g,"DIV",{class:!0});var $=p(t);i=h($,"FORM",{class:!0});var ae=p(i);r=h(ae,"DIV",{class:!0});var H=p(r);f=h(H,"DIV",{class:!0});var J=p(f);l=h(J,"DIV",{class:!0});var ee=p(l);_=h(ee,"DIV",{class:!0});var Ae=p(_);re(b.$$.fragment,Ae),Ae.forEach(u),x=B(ee),y=h(ee,"DIV",{class:!0});var Be=p(y);v=h(Be,"INPUT",{class:!0,type:!0,placeholder:!0}),Be.forEach(u),k=B(ee),F=h(ee,"DIV",{});var Me=p(F);re(C.$$.fragment,Me),Me.forEach(u),ee.forEach(u),V=B(J),E=h(J,"DIV",{class:!0});var be=p(E);q.l(be),M=B(be),m=h(be,"INPUT",{class:!0,type:!0,placeholder:!0}),be.forEach(u),J.forEach(u),S=B(H),N=h(H,"DIV",{class:!0});var Ne=p(N);re(I.$$.fragment,Ne),Ne.forEach(u),R=B(H),T=h(H,"DIV",{class:!0});var ye=p(T);U=h(ye,"DIV",{class:!0});var Ue=p(U);P=h(Ue,"DIV",{class:!0});var K=p(P);G=h(K,"SPAN",{class:!0});var qe=p(G);Y=j(qe,Q),qe.forEach(u),d=B(K),me=j(K,se),we=B(K),Ie=h(K,"BR",{}),ke=j(K,`—
							`),Z=h(K,"SPAN",{class:!0});var Se=p(Z);pe=j(Se,oe),Se.forEach(u),K.forEach(u),Ue.forEach(u),Ee=B(ye),X=h(ye,"BUTTON",{class:!0,type:!0});var Oe=p(X);_e=j(Oe,le),Oe.forEach(u),ye.forEach(u),H.forEach(u),ae.forEach(u),$.forEach(u),g.forEach(u),ve=B(o),re(O.$$.fragment,o),this.h()},h(){a(_,"class","flex-shrink-0 mr-2"),a(v,"class","w-full text-2xl font-medium bg-transparent outline-none font-primary"),a(v,"type","text"),a(v,"placeholder",D=n[9].t("Function Name (e.g. My Filter)")),v.required=!0,a(y,"class","flex-1"),a(l,"class","flex w-full items-center"),a(m,"class","w-full text-sm bg-transparent outline-none"),a(m,"type","text"),a(m,"placeholder",w=n[9].t("Function Description (e.g. A filter to remove profanity from text)")),m.required=!0,a(E,"class","flex gap-2 px-1"),a(f,"class","w-full mb-2 flex flex-col gap-0.5"),a(N,"class","mb-2 flex-1 overflow-auto h-0 rounded-lg"),a(G,"class","font-semibold dark:text-gray-200"),a(Z,"class","font-medium dark:text-gray-400"),a(P,"class","text-xs text-gray-500 line-clamp-2"),a(U,"class","flex-1 pr-3"),a(X,"class","px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"),a(X,"type","submit"),a(T,"class","pb-3 flex justify-between"),a(r,"class","flex flex-col flex-1 overflow-auto h-0 rounded-lg"),a(i,"class","flex flex-col max-h-[100dvh] h-full"),a(t,"class","mx-auto w-full md:px-0 h-full"),a(e,"class","flex flex-col justify-between w-full overflow-y-auto h-full")},m(o,g){ne(o,e,g),s(e,t),s(t,i),s(i,r),s(r,f),s(f,l),s(l,_),ue(b,_,null),s(l,x),s(l,y),s(y,v),te(v,n[0]),s(l,k),s(l,F),ue(C,F,null),s(f,V),s(f,E),q.m(E,null),s(E,M),s(E,m),te(m,n[3].description),s(r,S),s(r,N),ue(I,N,null),s(r,R),s(r,T),s(T,U),s(U,P),s(P,G),s(G,Y),s(P,d),s(P,me),s(P,we),s(P,Ie),s(P,ke),s(P,Z),s(Z,pe),s(T,Ee),s(T,X),s(X,_e),n[21](i),ne(o,ve,g),ue(O,o,g),L=!0,Fe||(Ce=[he(v,"input",n[15]),he(m,"input",n[17]),he(i,"submit",He(n[22]))],Fe=!0)},p(o,[g]){const $={};g&512&&($.content=o[9].t("Back")),g&1073741824&&($.$$scope={dirty:g,ctx:o}),b.$set($),(!L||g&512&&D!==(D=o[9].t("Function Name (e.g. My Filter)")))&&a(v,"placeholder",D),g&1&&v.value!==o[0]&&te(v,o[0]);const ae={};g&512&&(ae.content=o[9].t("Function")),C.$set(ae),ge===(ge=Pe(o))&&q?q.p(o,g):(q.d(1),q=ge(o),q&&(q.c(),q.m(E,M))),(!L||g&512&&w!==(w=o[9].t("Function Description (e.g. A filter to remove profanity from text)")))&&a(m,"placeholder",w),g&8&&m.value!==o[3].description&&te(m,o[3].description);const H={};g&2&&(H.value=o[1]),I.$set(H),(!L||g&512)&&Q!==(Q=o[9].t("Warning:")+"")&&z(Y,Q),(!L||g&512)&&se!==(se=o[9].t("Functions allow arbitrary code execution")+"")&&z(me,se),(!L||g&512)&&oe!==(oe=o[9].t("don't install random functions from sources you don't trust.")+"")&&z(pe,oe),(!L||g&512)&&le!==(le=o[9].t("Save")+"")&&z(_e,le);const J={};g&1073742336&&(J.$$scope={dirty:g,ctx:o}),!De&&g&64&&(De=!0,J.show=o[6],ze(()=>De=!1)),O.$set(J)},i(o){L||(fe(b.$$.fragment,o),fe(C.$$.fragment,o),fe(I.$$.fragment,o),fe(O.$$.fragment,o),L=!0)},o(o){de(b.$$.fragment,o),de(C.$$.fragment,o),de(I.$$.fragment,o),de(O.$$.fragment,o),L=!1},d(o){o&&(u(e),u(ve)),ce(b),ce(C),q.d(),n[18](null),ce(I),n[21](null),ce(O,o),Fe=!1,Re(Ce)}}}function ft(n,e,t){let i;const r=Ge(),f=Je("i18n");Ke(n,f,d=>t(9,i=d));let l=null,_=!1,{edit:b=!1}=e,{clone:x=!1}=e,{id:y=""}=e,{name:v=""}=e,{meta:D={description:""}}=e,{content:k=""}=e,F="";const C=()=>{t(7,F=k)};let V,E=`"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
        )
        max_turns: int = Field(
            default=8, description="Maximum allowable conversation turns for a user."
        )
        pass

    class UserValves(BaseModel):
        max_turns: int = Field(
            default=4, description="Maximum allowable conversation turns for a user."
        )
        pass

    def __init__(self):
        # Indicates custom file handling logic. This flag helps disengage default routines in favor of custom
        # implementations, informing the WebUI to defer file-related operations to designated methods within this class.
        # Alternatively, you can remove the files directly from the body in from the inlet hook
        # self.file_handler = True

        # Initialize 'valves' with specific configurations. Using 'Valves' instance helps encapsulate settings,
        # which ensures settings are managed cohesively and not confused with operational flags like 'file_handler'.
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify the request body or validate it before processing by the chat completion API.
        # This function is the pre-processor for the API where various checks on the input can be performed.
        # It can also modify the request before sending it to the API.
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        print(f"inlet:user:{__user__}")

        if __user__.get("role", "admin") in ["user", "admin"]:
            messages = body.get("messages", [])

            max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)
            if len(messages) > max_turns:
                raise Exception(
                    f"Conversation turn limit exceeded. Max turns: {max_turns}"
                )

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify or analyze the response body after processing by the API.
        # This function is the post-processor for the API, which can be used to modify the response
        # or perform additional checks and analytics.
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        print(f"outlet:user:{__user__}")

        return body
`;const M=async()=>{r("save",{id:y,name:v,meta:D,content:k})},m=async()=>{if(V){t(1,k=F),await Ve();const d=await V.formatPythonCodeHandler();await Ve(),t(1,k=F),await Ve(),d&&(console.log("Code formatted successfully"),M())}},w=()=>{$e("/workspace/functions")};function S(){v=this.value,t(0,v)}function N(){y=this.value,t(2,y),t(0,v),t(4,b),t(13,x)}function I(){D.description=this.value,t(3,D)}function R(d){xe[d?"unshift":"push"](()=>{V=d,t(8,V)})}const T=d=>{t(7,F=d.detail.value)},U=async()=>{l&&l.requestSubmit()};function P(d){xe[d?"unshift":"push"](()=>{l=d,t(5,l)})}const G=()=>{b?m():t(6,_=!0)};function Q(d){_=d,t(6,_)}const Y=()=>{m()};return n.$$set=d=>{"edit"in d&&t(4,b=d.edit),"clone"in d&&t(13,x=d.clone),"id"in d&&t(2,y=d.id),"name"in d&&t(0,v=d.name),"meta"in d&&t(3,D=d.meta),"content"in d&&t(1,k=d.content)},n.$$.update=()=>{n.$$.dirty&2&&k&&C(),n.$$.dirty&8209&&v&&!b&&!x&&t(2,y=v.replace(/\s+/g,"_").toLowerCase())},[v,k,y,D,b,l,_,F,V,i,f,E,m,x,w,S,N,I,R,T,U,P,G,Q,Y]}class bt extends Xe{constructor(e){super(),Ye(this,e,ft,ut,je,{edit:4,clone:13,id:2,name:0,meta:3,content:1})}}export{bt as F};
//# sourceMappingURL=FunctionEditor.DWbZ8VOO.js.map
