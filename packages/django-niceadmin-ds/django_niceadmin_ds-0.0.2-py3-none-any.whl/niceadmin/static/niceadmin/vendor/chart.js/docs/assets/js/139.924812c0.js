(window.webpackJsonp=window.webpackJsonp||[]).push([[139],{468:function(n,a,e){"use strict";e.r(a);var t=e(6),s=Object(t.a)({},(function(){var n=this,a=n.$createElement,e=n._self._c||a;return e("ContentSlotsDistributor",{attrs:{"slot-key":n.$parent.slotKey}},[e("h1",{attrs:{id:"radial-axes"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#radial-axes"}},[n._v("#")]),n._v(" Radial Axes")]),n._v(" "),e("p",[n._v("Radial axes are used specifically for the radar and polar area chart types. These axes overlay the chart area, rather than being positioned on one of the edges. One radial axis is included by default in Chart.js.")]),n._v(" "),e("ul",[e("li",[e("RouterLink",{attrs:{to:"/axes/radial/linear.html"}},[n._v("radialLinear")])],1)]),n._v(" "),e("h2",{attrs:{id:"visual-components"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#visual-components"}},[n._v("#")]),n._v(" Visual Components")]),n._v(" "),e("p",[n._v("A radial axis is composed of visual components that can be individually configured. These components are:")]),n._v(" "),e("ul",[e("li",[e("a",{attrs:{href:"#angle-lines"}},[n._v("angle lines")])]),n._v(" "),e("li",[e("a",{attrs:{href:"#grid-lines"}},[n._v("grid lines")])]),n._v(" "),e("li",[e("a",{attrs:{href:"#point-labels"}},[n._v("point labels")])]),n._v(" "),e("li",[e("a",{attrs:{href:"#ticks"}},[n._v("ticks")])])]),n._v(" "),e("h3",{attrs:{id:"angle-lines"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#angle-lines"}},[n._v("#")]),n._v(" Angle Lines")]),n._v(" "),e("p",[n._v("The grid lines for an axis are drawn on the chart area. They stretch out from the center towards the edge of the canvas. In the example below, they are red.")]),n._v(" "),e("chart-editor",{attrs:{code:"// <block:setup:1>\nconst labels = Utils.months({count: 7});\nconst data = {\n  labels: labels,\n  datasets: [{\n    label: 'My First dataset',\n    backgroundColor: 'rgba(54, 162, 235, 0.5)',\n    borderColor: 'rgb(54, 162, 235)',\n    borderWidth: 1,\n    data: [10, 20, 30, 40, 50, 0, 5],\n  }]\n};\n// </block:setup>\n\n// <block:config:0>\nconst config = {\n  type: 'radar',\n  data,\n  options: {\n    scales: {\n      r: {\n        angleLines: {\n          color: 'red'\n        }\n      }\n    }\n  }\n};\n// </block:config>\n\nmodule.exports = {\n  actions: [],\n  config: config,\n};\n"}}),e("h3",{attrs:{id:"grid-lines"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#grid-lines"}},[n._v("#")]),n._v(" Grid Lines")]),n._v(" "),e("p",[n._v("The grid lines for an axis are drawn on the chart area. In the example below, they are red.")]),n._v(" "),e("chart-editor",{attrs:{code:"// <block:setup:1>\nconst labels = Utils.months({count: 7});\nconst data = {\n  labels: labels,\n  datasets: [{\n    label: 'My First dataset',\n    backgroundColor: 'rgba(54, 162, 235, 0.5)',\n    borderColor: 'rgb(54, 162, 235)',\n    borderWidth: 1,\n    data: [10, 20, 30, 40, 50, 0, 5],\n  }]\n};\n// </block:setup>\n\n// <block:config:0>\nconst config = {\n  type: 'radar',\n  data,\n  options: {\n    scales: {\n      r: {\n        grid: {\n          color: 'red'\n        }\n      }\n    }\n  }\n};\n// </block:config>\n\nmodule.exports = {\n  actions: [],\n  config: config,\n};\n"}}),e("h3",{attrs:{id:"point-labels"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#point-labels"}},[n._v("#")]),n._v(" Point Labels")]),n._v(" "),e("p",[n._v("The point labels indicate the value for each angle line. In the example below, they are red.")]),n._v(" "),e("chart-editor",{attrs:{code:"// <block:setup:1>\nconst labels = Utils.months({count: 7});\nconst data = {\n  labels: labels,\n  datasets: [{\n    label: 'My First dataset',\n    backgroundColor: 'rgba(54, 162, 235, 0.5)',\n    borderColor: 'rgb(54, 162, 235)',\n    borderWidth: 1,\n    data: [10, 20, 30, 40, 50, 0, 5],\n  }]\n};\n// </block:setup>\n\n// <block:config:0>\nconst config = {\n  type: 'radar',\n  data,\n  options: {\n    scales: {\n      r: {\n        pointLabels: {\n          color: 'red'\n        }\n      }\n    }\n  }\n};\n// </block:config>\n\nmodule.exports = {\n  actions: [],\n  config: config,\n};\n"}}),e("h3",{attrs:{id:"ticks"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#ticks"}},[n._v("#")]),n._v(" Ticks")]),n._v(" "),e("p",[n._v("The ticks are used to label values based on how far they are from the center of the axis. In the example below, they are red.")]),n._v(" "),e("chart-editor",{attrs:{code:"// <block:setup:1>\nconst labels = Utils.months({count: 7});\nconst data = {\n  labels: labels,\n  datasets: [{\n    label: 'My First dataset',\n    backgroundColor: 'rgba(54, 162, 235, 0.5)',\n    borderColor: 'rgb(54, 162, 235)',\n    borderWidth: 1,\n    data: [10, 20, 30, 40, 50, 0, 5],\n  }]\n};\n// </block:setup>\n\n// <block:config:0>\nconst config = {\n  type: 'radar',\n  data,\n  options: {\n    scales: {\n      r: {\n        ticks: {\n          color: 'red'\n        }\n      }\n    }\n  }\n};\n// </block:config>\n\nmodule.exports = {\n  actions: [],\n  config: config,\n};\n"}})],1)}),[],!1,null,null,null);a.default=s.exports}}]);