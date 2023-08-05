(window.webpackJsonp=window.webpackJsonp||[]).push([[259],{588:function(t,n,o){"use strict";o.r(n);var e=o(6),l=Object(e.a)({},(function(){var t=this,n=t.$createElement,o=t._self._c||n;return o("ContentSlotsDistributor",{attrs:{"slot-key":t.$parent.slotKey}},[o("h1",{attrs:{id:"point-style"}},[o("a",{staticClass:"header-anchor",attrs:{href:"#point-style"}},[t._v("#")]),t._v(" Point Style")]),t._v(" "),o("p",[t._v("This sample shows how to use the dataset point style in the tooltip instead of a rectangle to identify each dataset.")]),t._v(" "),o("chart-editor",{attrs:{code:"// <block:actions:2>\nconst actions = [\n  {\n    name: 'Toggle Tooltip Point Style',\n    handler(chart) {\n      chart.options.plugins.tooltip.usePointStyle = !chart.options.plugins.tooltip.usePointStyle;\n      chart.update();\n    }\n  },\n];\n// </block:actions>\n\n// <block:setup:1>\nconst DATA_COUNT = 7;\nconst NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};\nconst data = {\n  labels: Utils.months({count: DATA_COUNT}),\n  datasets: [\n    {\n      label: 'Triangles',\n      data: Utils.numbers(NUMBER_CFG),\n      fill: false,\n      borderColor: Utils.CHART_COLORS.red,\n      backgroundColor: Utils.transparentize(Utils.CHART_COLORS.red, 0.5),\n      pointStyle: 'triangle',\n      pointRadius: 6,\n    },\n    {\n      label: 'Circles',\n      data: Utils.numbers(NUMBER_CFG),\n      fill: false,\n      borderColor: Utils.CHART_COLORS.blue,\n      backgroundColor: Utils.transparentize(Utils.CHART_COLORS.blue, 0.5),\n      pointStyle: 'circle',\n      pointRadius: 6,\n    },\n    {\n      label: 'Stars',\n      data: Utils.numbers(NUMBER_CFG),\n      fill: false,\n      borderColor: Utils.CHART_COLORS.green,\n      backgroundColor: Utils.transparentize(Utils.CHART_COLORS.green, 0.5),\n      pointStyle: 'star',\n      pointRadius: 6,\n    }\n  ]\n};\n// </block:setup>\n\n// <block:config:0>\nconst config = {\n  type: 'line',\n  data: data,\n  options: {\n    interaction: {\n      mode: 'index',\n    },\n    plugins: {\n      title: {\n        display: true,\n        text: (ctx) => 'Tooltip point style: ' + ctx.chart.options.plugins.tooltip.usePointStyle,\n      },\n      tooltip: {\n        usePointStyle: true,\n      }\n    }\n  }\n};\n// </block:config>\n\nmodule.exports = {\n  actions: actions,\n  config: config,\n};\n"}}),o("h2",{attrs:{id:"docs"}},[o("a",{staticClass:"header-anchor",attrs:{href:"#docs"}},[t._v("#")]),t._v(" Docs")]),t._v(" "),o("ul",[o("li",[o("RouterLink",{attrs:{to:"/general/data-structures.html"}},[t._v("Data structures ("),o("code",[t._v("labels")]),t._v(")")])],1),t._v(" "),o("li",[o("RouterLink",{attrs:{to:"/charts/line.html"}},[t._v("Line")])],1),t._v(" "),o("li",[o("RouterLink",{attrs:{to:"/configuration/tooltip.html"}},[t._v("Tooltip")]),t._v(" "),o("ul",[o("li",[o("code",[t._v("usePointStyle")])])])],1),t._v(" "),o("li",[o("RouterLink",{attrs:{to:"/configuration/elements.html"}},[t._v("Elements")]),t._v(" "),o("ul",[o("li",[o("RouterLink",{attrs:{to:"/configuration/elements.html#point-styles"}},[t._v("Point Styles")])],1)])],1)])],1)}),[],!1,null,null,null);n.default=l.exports}}]);