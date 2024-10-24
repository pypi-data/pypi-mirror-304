import{ap as I,u as $,x as B,aq as L,c as v,z as F,h as M,A,M as z,Z as y,o as n,j as k,s as x,ar as E,e as l,b as R,a as m,t as u,k as r,$ as V}from"./index-74bdc7d1.js";const q={class:"v-step__buttons"},D=["onClick"],O=["onClick"],Y=["onClick"],G={__name:"Tutorial",props:{tutorial:{type:String,default:"home"}},setup(S){const{t}=I({useScope:"global"}),p=$(),j=B(),d=L("tours"),N=S,T=[{target:"#main-menu",content:t("tutorial.step-1"),params:{placement:"top"}},{target:"#create-project",content:t("tutorial.step-2"),hideNext:!0,params:{placement:"right"}},{target:"#select-folder",content:t("tutorial.step-3"),hideNext:!0,params:{placement:"top"}},{target:"#confirm-modal",content:t("tutorial.step-3a"),hideNext:!0,before:()=>new Promise((o,s)=>{setTimeout(()=>o("foo"),300)}),params:{placement:"right"}},{target:"#confirm-create",hideNext:!0,content:t("tutorial.step-3b")}],P=[{target:"#add_folder",content:t("tutorial.step-4"),hideNext:!0,before:()=>new Promise((o,s)=>{setTimeout(()=>o("foo"),300)}),params:{placement:"bottom"}},{target:"#confirm-modal",content:t("tutorial.step-4b"),hideNext:!0,before:()=>new Promise((o,s)=>{setTimeout(()=>o("foo"),300)}),params:{placement:"bottom"}},{target:"#import",before:()=>new Promise((o,s)=>{setTimeout(()=>o("foo"),300)}),content:t("tutorial.step-5"),params:{placement:"right"}},{target:"#add-property",content:t("tutorial.step-6"),hideNext:!0,params:{placement:"right"}},{target:"#select-property",content:t("tutorial.step-7"),hideNext:!0,before:()=>new Promise((o,s)=>{setTimeout(()=>o("foo"),250)}),params:{placement:"right"}},{target:"#confirm-property",content:t("tutorial.step-8"),hideNext:!0,params:{placement:"right"}},{target:"#main-content",content:t("tutorial.step-9"),params:{placement:"bottom"}},{target:"#main-content",content:t("tutorial.step-10"),params:{placement:"bottom"}},{target:"#add-group-button",content:t("tutorial.step-11"),params:{placement:"bottom"},hideNext:!0},{target:"#main-content",content:t("tutorial.step-12"),params:{placement:"bottom"}},{target:"#main-content",content:t("tutorial.step-13"),params:{placement:"bottom"}},{target:"#main-content",content:t("tutorial.step-13a"),params:{placement:"bottom"}},{target:"#selection-stamp",content:t("tutorial.step-13b"),params:{placement:"bottom"}},{target:"#remove-group-button",content:t("tutorial.step-14"),params:{placement:"top"}},{target:"#add-tab-button",content:t("tutorial.step-14b"),params:{placement:"bottom"}},{target:"#group-action-button",content:t("tutorial.step-15"),params:{placement:"bottom"}},{target:"#main-content",content:t("tutorial.step-16"),params:{placement:"bottom"}},{target:"#main-content",content:t("tutorial.step-17"),params:{placement:"bottom"}}],i=N.tutorial==="home"?T:P;let a=parseInt(localStorage.getItem("currentStep")||"0");const b=v(()=>Array.isArray(p.data.status.projects)&&p.data.status.projects.length>0),c=v(()=>!b.value&&p.data.init||j.showTutorial);F(c,async()=>{_()}),M(()=>{_()});async function _(){c.value&&(b.value||localStorage.setItem("tutorialFinished","false"),await A(),console.log(a),a===5&&p.openModalId===z.PROPERTY&&i.length-1>a?d.myTour.start(a):d.myTour.start())}function g(o){o!==-1&&o&&(a=o)}function h(){localStorage.setItem("tutorialFinished","true")}return(o,s)=>{const C=y("v-step"),w=y("v-tour");return c.value?(n(),k(w,{key:0,name:"myTour",steps:l(i),options:{enabledButtons:{buttonPrevious:!1}}},{default:x(e=>[e.steps[e.currentStep]?(n(),k(C,{key:e.currentStep,step:e.steps[e.currentStep],"previous-step":e.previousStep,"next-step":e.nextStep,stop:e.stop,skip:e.skip,"is-first":e.isFirst,"is-last":e.isLast,labels:e.labels,id:e.currentStep},E({_:2},[l(i)[e.currentStep].hideNext===!0||e.isLast?{name:"actions",fn:x(()=>[R("div",q,[e.isLast?r("",!0):(n(),m("button",{key:0,onClick:f=>{e.skip(),g(-1),h()},class:"v-step__button v-step__button-skip"},u(o.$t("tutorial.buttons.skip")),9,D)),e.isLast?r("",!0):(n(),m("button",{key:1,onClick:f=>{e.nextStep(),g(e.currentStep+1)},class:"v-step__button v-step__button-next",style:V(l(i)[e.currentStep].hideNext?"display: none !important":"")},u(o.$t("tutorial.buttons.next")),13,O)),e.isLast?(n(),m("button",{key:2,class:"v-step__button v-step__button-stop",onClick:f=>{e.stop(),h()}},u(o.$t("tutorial.buttons.finish")),9,Y)):r("",!0)])]),key:"0"}:void 0]),1032,["step","previous-step","next-step","stop","skip","is-first","is-last","labels","id"])):r("",!0)]),_:1},8,["steps"])):r("",!0)}}};export{G as _};
