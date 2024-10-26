import{s as We,A as qe,e as d,k as A,t as R,c,a as _,d as u,o as U,b as W,f as n,i as ae,g as r,B as te,u as me,C as Le,h as F,D as Fe,E as Ge,p as Ke,j as Ye,F as ze,n as Je,G as Ve}from"./scheduler.BwES1eAZ.js";import{S as Qe,i as Xe,f as Ze,b as le,d as ie,m as ue,t as fe,a as de,e as ce}from"./index.JIjGThd1.js";import{C as $e}from"./CodeEditor.rAxbRICr.js";import{g as et}from"./entry.Dtt6bcfU.js";import{C as tt}from"./ConfirmDialog.56zgi8Co.js";import{B as at}from"./Badge.LWAVLoO-.js";import{C as rt}from"./ChevronLeft.bwOsKpyw.js";import{T as ot}from"./Tooltip.Dj8C3DN2.js";function st(a){let e,t,l,i,m;return t=new rt({props:{strokeWidth:"2.5"}}),{c(){e=d("button"),le(t.$$.fragment),this.h()},l(s){e=c(s,"BUTTON",{class:!0,type:!0});var p=_(e);ie(t.$$.fragment,p),p.forEach(u),this.h()},h(){n(e,"class","w-full text-left text-sm py-1.5 px-1 rounded-lg dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-gray-850"),n(e,"type","button")},m(s,p){ae(s,e,p),ue(t,e,null),l=!0,i||(m=me(e,"click",a[14]),i=!0)},p:Je,i(s){l||(fe(t.$$.fragment,s),l=!0)},o(s){de(t.$$.fragment,s),l=!1},d(s){s&&u(e),ce(t),i=!1,m()}}}function nt(a){let e,t,l,i;return{c(){e=d("input"),this.h()},l(m){e=c(m,"INPUT",{class:!0,type:!0,placeholder:!0}),this.h()},h(){n(e,"class","w-full text-sm disabled:text-gray-500 bg-transparent outline-none"),n(e,"type","text"),n(e,"placeholder",t=a[9].t("Toolkit ID (e.g. my_toolkit)")),e.required=!0,e.disabled=a[4]},m(m,s){ae(m,e,s),te(e,a[2]),l||(i=me(e,"input",a[16]),l=!0)},p(m,s){s&512&&t!==(t=m[9].t("Toolkit ID (e.g. my_toolkit)"))&&n(e,"placeholder",t),s&16&&(e.disabled=m[4]),s&4&&e.value!==m[2]&&te(e,m[2])},d(m){m&&u(e),l=!1,i()}}}function lt(a){let e,t;return{c(){e=d("div"),t=R(a[2]),this.h()},l(l){e=c(l,"DIV",{class:!0});var i=_(e);t=W(i,a[2]),i.forEach(u),this.h()},h(){n(e,"class","text-sm text-gray-500 flex-shrink-0")},m(l,i){ae(l,e,i),r(e,t)},p(l,i){i&4&&F(t,l[2])},d(l){l&&u(e)}}}function it(a){let e,t,l,i=a[9].t("Please carefully review the following warnings:")+"",m,s,p,w,q=a[9].t("Tools have a function calling system that allows arbitrary code execution.")+"",b,v,T,E=a[9].t("Do not install tools from sources you do not fully trust.")+"",D,C,V,I=a[9].t("I acknowledge that I have read and I understand the implications of my action. I am aware of the risks associated with executing arbitrary code and I have verified the trustworthiness of the source.")+"",N;return{c(){e=d("div"),t=d("div"),l=d("div"),m=R(i),s=A(),p=d("ul"),w=d("li"),b=R(q),v=A(),T=d("li"),D=R(E),C=A(),V=d("div"),N=R(I),this.h()},l(h){e=c(h,"DIV",{class:!0});var y=_(e);t=c(y,"DIV",{class:!0});var H=_(t);l=c(H,"DIV",{});var B=_(l);m=W(B,i),B.forEach(u),s=U(H),p=c(H,"UL",{class:!0});var k=_(p);w=c(k,"LI",{});var G=_(w);b=W(G,q),G.forEach(u),v=U(k),T=c(k,"LI",{});var x=_(T);D=W(x,E),x.forEach(u),k.forEach(u),H.forEach(u),C=U(y),V=c(y,"DIV",{class:!0});var S=_(V);N=W(S,I),S.forEach(u),y.forEach(u),this.h()},h(){n(p,"class","mt-1 list-disc pl-4 text-xs"),n(t,"class","bg-yellow-500/20 text-yellow-700 dark:text-yellow-200 rounded-lg px-4 py-3"),n(V,"class","my-3"),n(e,"class","text-sm text-gray-500")},m(h,y){ae(h,e,y),r(e,t),r(t,l),r(l,m),r(t,s),r(t,p),r(p,w),r(w,b),r(p,v),r(p,T),r(T,D),r(e,C),r(e,V),r(V,N)},p(h,y){y&512&&i!==(i=h[9].t("Please carefully review the following warnings:")+"")&&F(m,i),y&512&&q!==(q=h[9].t("Tools have a function calling system that allows arbitrary code execution.")+"")&&F(b,q),y&512&&E!==(E=h[9].t("Do not install tools from sources you do not fully trust.")+"")&&F(D,E),y&512&&I!==(I=h[9].t("I acknowledge that I have read and I understand the implications of my action. I am aware of the risks associated with executing arbitrary code and I have verified the trustworthiness of the source.")+"")&&F(N,I)},d(h){h&&u(e)}}}function ut(a){let e,t,l,i,m,s,p,w,q,b,v,T,E,D,C,V,I,N,h,y,H,B,k,G,x,S,P,K,J=a[9].t("Warning:")+"",X,f,re=a[9].t("Tools are a function calling system with arbitrary code execution")+"",he,ye,ke,Ee,Z,oe=a[9].t("don't install random tools from sources you don't trust.")+"",_e,Ie,Q,se=a[9].t("Save")+"",pe,ve,M,Te,O,De,Ce;w=new ot({props:{content:a[9].t("Back"),$$slots:{default:[st]},$$scope:{ctx:a}}}),C=new at({props:{type:"muted",content:a[9].t("Tool")}});function Pe(o,g){return o[4]?lt:nt}let ge=Pe(a),j=ge(a),Oe={value:a[1],boilerplate:a[11],lang:"python"};k=new $e({props:Oe}),a[18](k),k.$on("change",a[19]),k.$on("save",a[20]);function Re(o){a[23](o)}let xe={$$slots:{default:[it]},$$scope:{ctx:a}};return a[6]!==void 0&&(xe.show=a[6]),M=new tt({props:xe}),qe.push(()=>Ze(M,"show",Re)),M.$on("confirm",a[24]),{c(){e=d("div"),t=d("div"),l=d("form"),i=d("div"),m=d("div"),s=d("div"),p=d("div"),le(w.$$.fragment),q=A(),b=d("div"),v=d("input"),E=A(),D=d("div"),le(C.$$.fragment),V=A(),I=d("div"),j.c(),N=A(),h=d("input"),H=A(),B=d("div"),le(k.$$.fragment),G=A(),x=d("div"),S=d("div"),P=d("div"),K=d("span"),X=R(J),f=A(),he=R(re),ye=A(),ke=d("br"),Ee=R(`—
							`),Z=d("span"),_e=R(oe),Ie=A(),Q=d("button"),pe=R(se),ve=A(),le(M.$$.fragment),this.h()},l(o){e=c(o,"DIV",{class:!0});var g=_(e);t=c(g,"DIV",{class:!0});var $=_(t);l=c($,"FORM",{class:!0});var ne=_(l);i=c(ne,"DIV",{class:!0});var L=_(i);m=c(L,"DIV",{class:!0});var Y=_(m);s=c(Y,"DIV",{class:!0});var ee=_(s);p=c(ee,"DIV",{class:!0});var Ae=_(p);ie(w.$$.fragment,Ae),Ae.forEach(u),q=U(ee),b=c(ee,"DIV",{class:!0});var Ue=_(b);v=c(Ue,"INPUT",{class:!0,type:!0,placeholder:!0}),Ue.forEach(u),E=U(ee),D=c(ee,"DIV",{});var Ne=_(D);ie(C.$$.fragment,Ne),Ne.forEach(u),ee.forEach(u),V=U(Y),I=c(Y,"DIV",{class:!0});var we=_(I);j.l(we),N=U(we),h=c(we,"INPUT",{class:!0,type:!0,placeholder:!0}),we.forEach(u),Y.forEach(u),H=U(L),B=c(L,"DIV",{class:!0});var Be=_(B);ie(k.$$.fragment,Be),Be.forEach(u),G=U(L),x=c(L,"DIV",{class:!0});var be=_(x);S=c(be,"DIV",{class:!0});var Se=_(S);P=c(Se,"DIV",{class:!0});var z=_(P);K=c(z,"SPAN",{class:!0});var je=_(K);X=W(je,J),je.forEach(u),f=U(z),he=W(z,re),ye=U(z),ke=c(z,"BR",{}),Ee=W(z,`—
							`),Z=c(z,"SPAN",{class:!0});var He=_(Z);_e=W(He,oe),He.forEach(u),z.forEach(u),Se.forEach(u),Ie=U(be),Q=c(be,"BUTTON",{class:!0,type:!0});var Me=_(Q);pe=W(Me,se),Me.forEach(u),be.forEach(u),L.forEach(u),ne.forEach(u),$.forEach(u),g.forEach(u),ve=U(o),ie(M.$$.fragment,o),this.h()},h(){n(p,"class","flex-shrink-0 mr-2"),n(v,"class","w-full text-2xl font-medium bg-transparent outline-none"),n(v,"type","text"),n(v,"placeholder",T=a[9].t("Toolkit Name (e.g. My ToolKit)")),v.required=!0,n(b,"class","flex-1"),n(s,"class","flex w-full items-center"),n(h,"class","w-full text-sm bg-transparent outline-none"),n(h,"type","text"),n(h,"placeholder",y=a[9].t("Toolkit Description (e.g. A toolkit for performing various operations)")),h.required=!0,n(I,"class","flex gap-2 px-1"),n(m,"class","w-full mb-2 flex flex-col gap-0.5"),n(B,"class","mb-2 flex-1 overflow-auto h-0 rounded-lg"),n(K,"class","font-semibold dark:text-gray-200"),n(Z,"class","font-medium dark:text-gray-400"),n(P,"class","text-xs text-gray-500 line-clamp-2"),n(S,"class","flex-1 pr-3"),n(Q,"class","px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"),n(Q,"type","submit"),n(x,"class","pb-3 flex justify-between"),n(i,"class","flex flex-col flex-1 overflow-auto h-0"),n(l,"class","flex flex-col max-h-[100dvh] h-full"),n(t,"class","mx-auto w-full md:px-0 h-full"),n(e,"class","flex flex-col justify-between w-full overflow-y-auto h-full")},m(o,g){ae(o,e,g),r(e,t),r(t,l),r(l,i),r(i,m),r(m,s),r(s,p),ue(w,p,null),r(s,q),r(s,b),r(b,v),te(v,a[0]),r(s,E),r(s,D),ue(C,D,null),r(m,V),r(m,I),j.m(I,null),r(I,N),r(I,h),te(h,a[3].description),r(i,H),r(i,B),ue(k,B,null),r(i,G),r(i,x),r(x,S),r(S,P),r(P,K),r(K,X),r(P,f),r(P,he),r(P,ye),r(P,ke),r(P,Ee),r(P,Z),r(Z,_e),r(x,Ie),r(x,Q),r(Q,pe),a[21](l),ae(o,ve,g),ue(M,o,g),O=!0,De||(Ce=[me(v,"input",a[15]),me(h,"input",a[17]),me(l,"submit",Le(a[22]))],De=!0)},p(o,[g]){const $={};g&512&&($.content=o[9].t("Back")),g&536870912&&($.$$scope={dirty:g,ctx:o}),w.$set($),(!O||g&512&&T!==(T=o[9].t("Toolkit Name (e.g. My ToolKit)")))&&n(v,"placeholder",T),g&1&&v.value!==o[0]&&te(v,o[0]);const ne={};g&512&&(ne.content=o[9].t("Tool")),C.$set(ne),ge===(ge=Pe(o))&&j?j.p(o,g):(j.d(1),j=ge(o),j&&(j.c(),j.m(I,N))),(!O||g&512&&y!==(y=o[9].t("Toolkit Description (e.g. A toolkit for performing various operations)")))&&n(h,"placeholder",y),g&8&&h.value!==o[3].description&&te(h,o[3].description);const L={};g&2&&(L.value=o[1]),k.$set(L),(!O||g&512)&&J!==(J=o[9].t("Warning:")+"")&&F(X,J),(!O||g&512)&&re!==(re=o[9].t("Tools are a function calling system with arbitrary code execution")+"")&&F(he,re),(!O||g&512)&&oe!==(oe=o[9].t("don't install random tools from sources you don't trust.")+"")&&F(_e,oe),(!O||g&512)&&se!==(se=o[9].t("Save")+"")&&F(pe,se);const Y={};g&536871424&&(Y.$$scope={dirty:g,ctx:o}),!Te&&g&64&&(Te=!0,Y.show=o[6],Fe(()=>Te=!1)),M.$set(Y)},i(o){O||(fe(w.$$.fragment,o),fe(C.$$.fragment,o),fe(k.$$.fragment,o),fe(M.$$.fragment,o),O=!0)},o(o){de(w.$$.fragment,o),de(C.$$.fragment,o),de(k.$$.fragment,o),de(M.$$.fragment,o),O=!1},d(o){o&&(u(e),u(ve)),ce(w),ce(C),j.d(),a[18](null),ce(k),a[21](null),ce(M,o),De=!1,Ge(Ce)}}}function ft(a,e,t){let l;const i=Ke("i18n");Ye(a,i,f=>t(9,l=f));const m=ze();let s=null,p=!1,{edit:w=!1}=e,{clone:q=!1}=e,{id:b=""}=e,{name:v=""}=e,{meta:T={description:""}}=e,{content:E=""}=e,D="";const C=()=>{t(7,D=E)};let V,I=`import os
import requests
from datetime import datetime


class Tools:
    def __init__(self):
        pass

    # Add your custom tools using pure Python code here, make sure to add type hints
    # Use Sphinx-style docstrings to document your tools, they will be used for generating tools specifications
    # Please refer to function_calling_filter_pipeline.py file from pipelines project for an example

    def get_user_name_and_email_and_id(self, __user__: dict = {}) -> str:
        """
        Get the user name, Email and ID from the user object.
        """

        # Do not include :param for __user__ in the docstring as it should not be shown in the tool's specification
        # The session user object will be passed as a parameter when the function is called

        print(__user__)
        result = ""

        if "name" in __user__:
            result += f"User: {__user__['name']}"
        if "id" in __user__:
            result += f" (ID: {__user__['id']})"
        if "email" in __user__:
            result += f" (Email: {__user__['email']})"

        if result == "":
            result = "User: Unknown"

        return result

    def get_current_time(self) -> str:
        """
        Get the current time in a more human-readable format.
        :return: The current time.
        """

        now = datetime.now()
        current_time = now.strftime("%I:%M:%S %p")  # Using 12-hour format with AM/PM
        current_date = now.strftime(
            "%A, %B %d, %Y"
        )  # Full weekday, month name, day, and year

        return f"Current Date and Time = {current_date}, {current_time}"

    def calculator(self, equation: str) -> str:
        """
        Calculate the result of an equation.
        :param equation: The equation to calculate.
        """

        # Avoid using eval in production code
        # https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
        try:
            result = eval(equation)
            return f"{equation} = {result}"
        except Exception as e:
            print(e)
            return "Invalid equation"

    def get_current_weather(self, city: str) -> str:
        """
        Get the current weather for a given city.
        :param city: The name of the city to get the weather for.
        :return: The current weather information or an error message.
        """
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return (
                "API key is not set in the environment variable 'OPENWEATHER_API_KEY'."
            )

        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Optional: Use 'imperial' for Fahrenheit
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            data = response.json()

            if data.get("cod") != 200:
                return f"Error fetching weather data: {data.get('message')}"

            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            return f"Weather in {city}: {temperature}°C"
        except requests.RequestException as e:
            return f"Error fetching weather data: {str(e)}"
`;const N=async()=>{m("save",{id:b,name:v,meta:T,content:E})},h=async()=>{if(V){t(1,E=D),await Ve();const f=await V.formatPythonCodeHandler();await Ve(),t(1,E=D),await Ve(),f&&(console.log("Code formatted successfully"),N())}},y=()=>{et("/workspace/tools")};function H(){v=this.value,t(0,v)}function B(){b=this.value,t(2,b),t(0,v),t(4,w),t(13,q)}function k(){T.description=this.value,t(3,T)}function G(f){qe[f?"unshift":"push"](()=>{V=f,t(8,V)})}const x=f=>{t(7,D=f.detail.value)},S=()=>{s&&s.requestSubmit()};function P(f){qe[f?"unshift":"push"](()=>{s=f,t(5,s)})}const K=()=>{w?h():t(6,p=!0)};function J(f){p=f,t(6,p)}const X=()=>{h()};return a.$$set=f=>{"edit"in f&&t(4,w=f.edit),"clone"in f&&t(13,q=f.clone),"id"in f&&t(2,b=f.id),"name"in f&&t(0,v=f.name),"meta"in f&&t(3,T=f.meta),"content"in f&&t(1,E=f.content)},a.$$.update=()=>{a.$$.dirty&2&&E&&C(),a.$$.dirty&8209&&v&&!w&&!q&&t(2,b=v.replace(/\s+/g,"_").toLowerCase())},[v,E,b,T,w,s,p,D,V,l,i,I,h,q,y,H,B,k,G,x,S,P,K,J,X]}class wt extends Qe{constructor(e){super(),Xe(this,e,ft,ut,We,{edit:4,clone:13,id:2,name:0,meta:3,content:1})}}export{wt as T};
//# sourceMappingURL=ToolkitEditor.CZF07AX3.js.map
