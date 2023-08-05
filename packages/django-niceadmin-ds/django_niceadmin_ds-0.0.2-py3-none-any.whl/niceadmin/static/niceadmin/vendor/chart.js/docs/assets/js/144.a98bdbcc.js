(window.webpackJsonp=window.webpackJsonp||[]).push([[144],{474:function(t,e,a){"use strict";a.r(e);var r=a(6),o=Object(r.a)({},(function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("ContentSlotsDistributor",{attrs:{"slot-key":t.$parent.slotKey}},[a("h1",{attrs:{id:"bubble-chart"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#bubble-chart"}},[t._v("#")]),t._v(" Bubble Chart")]),t._v(" "),a("p",[t._v("A bubble chart is used to display three dimensions of data at the same time. The location of the bubble is determined by the first two dimensions and the corresponding horizontal and vertical axes. The third dimension is represented by the size of the individual bubbles.")]),t._v(" "),a("chart-editor",{attrs:{code:"// <block:setup:1>\nconst data = {\n  datasets: [{\n    label: 'First Dataset',\n    data: [{\n      x: 20,\n      y: 30,\n      r: 15\n    }, {\n      x: 40,\n      y: 10,\n      r: 10\n    }],\n    backgroundColor: 'rgb(255, 99, 132)'\n  }]\n};\n// </block:setup>\n\n// <block:config:0>\nconst config = {\n  type: 'bubble',\n  data: data,\n  options: {}\n};\n// </block:config>\n\nmodule.exports = {\n  actions: [],\n  config: config,\n};\n"}}),a("h2",{attrs:{id:"dataset-properties"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#dataset-properties"}},[t._v("#")]),t._v(" Dataset Properties")]),t._v(" "),a("p",[t._v("Namespaces:")]),t._v(" "),a("ul",[a("li",[a("code",[t._v("data.datasets[index]")]),t._v(" - options for this dataset only")]),t._v(" "),a("li",[a("code",[t._v("options.datasets.bubble")]),t._v(" - options for all bubble datasets")]),t._v(" "),a("li",[a("code",[t._v("options.elements.point")]),t._v(" - options for all "),a("RouterLink",{attrs:{to:"/configuration/elements.html#point-configuration"}},[t._v("point elements")])],1),t._v(" "),a("li",[a("code",[t._v("options")]),t._v(" - options for the whole chart")])]),t._v(" "),a("p",[t._v("The bubble chart allows a number of properties to be specified for each dataset. These are used to set display properties for a specific dataset. For example, the colour of the bubbles is generally set this way.")]),t._v(" "),a("table",[a("thead",[a("tr",[a("th",[t._v("Name")]),t._v(" "),a("th",[t._v("Type")]),t._v(" "),a("th",{staticStyle:{"text-align":"center"}},[a("RouterLink",{attrs:{to:"/general/options.html#scriptable-options"}},[t._v("Scriptable")])],1),t._v(" "),a("th",{staticStyle:{"text-align":"center"}},[a("RouterLink",{attrs:{to:"/general/options.html#indexable-options"}},[t._v("Indexable")])],1),t._v(" "),a("th",[t._v("Default")])])]),t._v(" "),a("tbody",[a("tr",[a("td",[a("a",{attrs:{href:"#styling"}},[a("code",[t._v("backgroundColor")])])]),t._v(" "),a("td",[a("RouterLink",{attrs:{to:"/general/colors.html"}},[a("code",[t._v("Color")])])],1),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("'rgba(0, 0, 0, 0.1)'")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#styling"}},[a("code",[t._v("borderColor")])])]),t._v(" "),a("td",[a("RouterLink",{attrs:{to:"/general/colors.html"}},[a("code",[t._v("Color")])])],1),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("'rgba(0, 0, 0, 0.1)'")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#styling"}},[a("code",[t._v("borderWidth")])])]),t._v(" "),a("td",[a("code",[t._v("number")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("3")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#general"}},[a("code",[t._v("clip")])])]),t._v(" "),a("td",[a("code",[t._v("number")]),t._v("|"),a("code",[t._v("object")]),t._v("|"),a("code",[t._v("false")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("-")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("-")]),t._v(" "),a("td",[a("code",[t._v("undefined")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#data-structure"}},[a("code",[t._v("data")])])]),t._v(" "),a("td",[a("code",[t._v("object[]")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("-")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("-")]),t._v(" "),a("td",[a("strong",[t._v("required")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#general"}},[a("code",[t._v("drawActiveElementsOnTop")])])]),t._v(" "),a("td",[a("code",[t._v("boolean")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("true")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#interactions"}},[a("code",[t._v("hoverBackgroundColor")])])]),t._v(" "),a("td",[a("RouterLink",{attrs:{to:"/general/colors.html"}},[a("code",[t._v("Color")])])],1),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("undefined")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#interactions"}},[a("code",[t._v("hoverBorderColor")])])]),t._v(" "),a("td",[a("RouterLink",{attrs:{to:"/general/colors.html"}},[a("code",[t._v("Color")])])],1),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("undefined")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#interactions"}},[a("code",[t._v("hoverBorderWidth")])])]),t._v(" "),a("td",[a("code",[t._v("number")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("1")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#interactions"}},[a("code",[t._v("hoverRadius")])])]),t._v(" "),a("td",[a("code",[t._v("number")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("4")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#interactions"}},[a("code",[t._v("hitRadius")])])]),t._v(" "),a("td",[a("code",[t._v("number")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("1")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#general"}},[a("code",[t._v("label")])])]),t._v(" "),a("td",[a("code",[t._v("string")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("-")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("-")]),t._v(" "),a("td",[a("code",[t._v("undefined")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#general"}},[a("code",[t._v("order")])])]),t._v(" "),a("td",[a("code",[t._v("number")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("-")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("-")]),t._v(" "),a("td",[a("code",[t._v("0")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#styling"}},[a("code",[t._v("pointStyle")])])]),t._v(" "),a("td",[a("RouterLink",{attrs:{to:"/configuration/elements.html#types"}},[a("code",[t._v("pointStyle")])])],1),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("'circle'")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#styling"}},[a("code",[t._v("rotation")])])]),t._v(" "),a("td",[a("code",[t._v("number")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("0")])])]),t._v(" "),a("tr",[a("td",[a("a",{attrs:{href:"#styling"}},[a("code",[t._v("radius")])])]),t._v(" "),a("td",[a("code",[t._v("number")])]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",{staticStyle:{"text-align":"center"}},[t._v("Yes")]),t._v(" "),a("td",[a("code",[t._v("3")])])])])]),t._v(" "),a("p",[t._v("All these values, if "),a("code",[t._v("undefined")]),t._v(", fallback to the scopes described in "),a("a",{attrs:{href:"../general/options"}},[t._v("option resolution")])]),t._v(" "),a("h3",{attrs:{id:"general"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#general"}},[t._v("#")]),t._v(" General")]),t._v(" "),a("table",[a("thead",[a("tr",[a("th",[t._v("Name")]),t._v(" "),a("th",[t._v("Description")])])]),t._v(" "),a("tbody",[a("tr",[a("td",[a("code",[t._v("clip")])]),t._v(" "),a("td",[t._v("How to clip relative to chartArea. Positive value allows overflow, negative value clips that many pixels inside chartArea. "),a("code",[t._v("0")]),t._v(" = clip at chartArea. Clipping can also be configured per side: "),a("code",[t._v("clip: {left: 5, top: false, right: -2, bottom: 0}")])])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("drawActiveElementsOnTop")])]),t._v(" "),a("td",[t._v("Draw the active bubbles of a dataset over the other bubbles of the dataset")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("label")])]),t._v(" "),a("td",[t._v("The label for the dataset which appears in the legend and tooltips.")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("order")])]),t._v(" "),a("td",[t._v("The drawing order of dataset. Also affects order for tooltip and legend. "),a("RouterLink",{attrs:{to:"/charts/mixed.html#drawing-order"}},[t._v("more")])],1)])])]),t._v(" "),a("h3",{attrs:{id:"styling"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#styling"}},[t._v("#")]),t._v(" Styling")]),t._v(" "),a("p",[t._v("The style of each bubble can be controlled with the following properties:")]),t._v(" "),a("table",[a("thead",[a("tr",[a("th",[t._v("Name")]),t._v(" "),a("th",[t._v("Description")])])]),t._v(" "),a("tbody",[a("tr",[a("td",[a("code",[t._v("backgroundColor")])]),t._v(" "),a("td",[t._v("bubble background color.")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("borderColor")])]),t._v(" "),a("td",[t._v("bubble border color.")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("borderWidth")])]),t._v(" "),a("td",[t._v("bubble border width (in pixels).")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("pointStyle")])]),t._v(" "),a("td",[t._v("bubble "),a("RouterLink",{attrs:{to:"/configuration/elements.html#point-styles"}},[t._v("shape style")]),t._v(".")],1)]),t._v(" "),a("tr",[a("td",[a("code",[t._v("rotation")])]),t._v(" "),a("td",[t._v("bubble rotation (in degrees).")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("radius")])]),t._v(" "),a("td",[t._v("bubble radius (in pixels).")])])])]),t._v(" "),a("p",[t._v("All these values, if "),a("code",[t._v("undefined")]),t._v(", fallback to the associated "),a("RouterLink",{attrs:{to:"/configuration/elements.html#point-configuration"}},[a("code",[t._v("elements.point.*")])]),t._v(" options.")],1),t._v(" "),a("h3",{attrs:{id:"interactions"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#interactions"}},[t._v("#")]),t._v(" Interactions")]),t._v(" "),a("p",[t._v("The interaction with each bubble can be controlled with the following properties:")]),t._v(" "),a("table",[a("thead",[a("tr",[a("th",[t._v("Name")]),t._v(" "),a("th",[t._v("Description")])])]),t._v(" "),a("tbody",[a("tr",[a("td",[a("code",[t._v("hitRadius")])]),t._v(" "),a("td",[t._v("bubble "),a("strong",[t._v("additional")]),t._v(" radius for hit detection (in pixels).")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("hoverBackgroundColor")])]),t._v(" "),a("td",[t._v("bubble background color when hovered.")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("hoverBorderColor")])]),t._v(" "),a("td",[t._v("bubble border color when hovered.")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("hoverBorderWidth")])]),t._v(" "),a("td",[t._v("bubble border width when hovered (in pixels).")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("hoverRadius")])]),t._v(" "),a("td",[t._v("bubble "),a("strong",[t._v("additional")]),t._v(" radius when hovered (in pixels).")])])])]),t._v(" "),a("p",[t._v("All these values, if "),a("code",[t._v("undefined")]),t._v(", fallback to the associated "),a("RouterLink",{attrs:{to:"/configuration/elements.html#point-configuration"}},[a("code",[t._v("elements.point.*")])]),t._v(" options.")],1),t._v(" "),a("h2",{attrs:{id:"default-options"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#default-options"}},[t._v("#")]),t._v(" Default Options")]),t._v(" "),a("p",[t._v("We can also change the default values for the Bubble chart type. Doing so will give all bubble charts created after this point the new defaults. The default configuration for the bubble chart can be accessed at "),a("code",[t._v("Chart.overrides.bubble")]),t._v(".")]),t._v(" "),a("h2",{attrs:{id:"data-structure"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#data-structure"}},[t._v("#")]),t._v(" Data Structure")]),t._v(" "),a("p",[t._v("Bubble chart datasets need to contain a "),a("code",[t._v("data")]),t._v(" array of points, each point represented by an object containing the following properties:")]),t._v(" "),a("div",{staticClass:"language-javascript extra-class"},[a("pre",{pre:!0,attrs:{class:"language-javascript"}},[a("code",[a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("// X Value")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token literal-property property"}},[t._v("x")]),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),t._v(" number"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n\n    "),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("// Y Value")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token literal-property property"}},[t._v("y")]),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),t._v(" number"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n\n    "),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("// Bubble radius in pixels (not scaled).")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token literal-property property"}},[t._v("r")]),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),t._v(" number\n"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n")])])]),a("p",[a("strong",[t._v("Important:")]),t._v(" the radius property, "),a("code",[t._v("r")]),t._v(" is "),a("strong",[t._v("not")]),t._v(" scaled by the chart, it is the raw radius in pixels of the bubble that is drawn on the canvas.")]),t._v(" "),a("h2",{attrs:{id:"internal-data-format"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#internal-data-format"}},[t._v("#")]),t._v(" Internal data format")]),t._v(" "),a("p",[a("code",[t._v("{x, y, _custom}")]),t._v(" where "),a("code",[t._v("_custom")]),t._v(" is the radius.")])],1)}),[],!1,null,null,null);e.default=o.exports}}]);