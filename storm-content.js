/* Static, versioned web content. Reproduce: node scripts/build-web-content.cjs */
(function(root){
const data={
 "version": 2,
 "chapters": [
  [
   "Harbor apprentice",
   "港湾学徒"
  ],
  [
   "Coastal planner",
   "海岸规划师"
  ],
  [
   "Tidal workshop",
   "潮汐工坊"
  ],
  [
   "Ridge expedition",
   "山脊探险"
  ],
  [
   "Beacon network",
   "灯塔网络"
  ],
  [
   "Island master",
   "全岛总工程师"
  ]
 ],
 "levels": {
  "harbor": {
   "info": {
    "id": "harbor",
    "en": "Room on board",
    "zh": "留一点船位",
    "tag": [
     "Harbor apprentice",
     "港湾学徒"
    ],
    "description": [
     "Chapter 1: plan, test and revise. Every mission has an optional hint.",
     "第 1 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Room on board",
      "留一点船位"
     ],
     "power": [
      "Jetty light",
      "码头灯光"
     ],
     "robot": [
      "Two seed stops",
      "两次采样"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     }
    ],
    "capacity": 12,
    "maxTrips": 4,
    "maxItems": null,
    "before": [
     [
      0,
      1
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 4,
    "source": 8,
    "targets": [
     3
    ],
    "fixed": [],
    "initial": [
     12,
     5,
     5,
     8,
     10,
     0,
     0,
     0,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     9
    ],
    "solution": [
     6,
     10,
     10,
     8,
     5,
     0,
     0,
     0,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     3
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     2,
     0,
     1
    ],
    "goal": [
     0,
     2
    ],
    "samples": [
     [
      2,
      2
     ],
     [
      0,
      2
     ]
    ],
    "road": [
     [
      2,
      0
     ],
     [
      2,
      1
     ],
     [
      2,
      2
     ],
     [
      1,
      2
     ],
     [
      0,
      2
     ]
    ],
    "budget": 7
   },
   "hints": {
    "cargo": [
     [
      0,
      3
     ],
     [
      1,
      2
     ],
     [
      4,
      5
     ]
    ],
    "robot": {
     "main": [
      "F",
      "F",
      "P",
      "L",
      "F",
      "F",
      "P"
     ],
     "body": [],
     "repeat": 2
    }
   }
  },
  "cove": {
   "info": {
    "id": "cove",
    "en": "Balance the boat",
    "zh": "平衡运输",
    "tag": [
     "Harbor apprentice",
     "港湾学徒"
    ],
    "description": [
     "Chapter 1: plan, test and revise. Every mission has an optional hint.",
     "第 1 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Balance the boat",
      "平衡运输"
     ],
     "power": [
      "Cove cable",
      "海湾电缆"
     ],
     "robot": [
      "Turn at the cove",
      "海湾转弯"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 3,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     }
    ],
    "capacity": 11,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 4,
    "source": 8,
    "targets": [
     3
    ],
    "fixed": [],
    "initial": [
     0,
     9,
     5,
     8,
     3,
     12,
     0,
     0,
     1,
     0,
     0,
     0,
     6,
     0,
     0,
     5
    ],
    "solution": [
     0,
     6,
     10,
     8,
     6,
     9,
     0,
     0,
     1,
     0,
     0,
     0,
     12,
     0,
     0,
     10
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     1,
     0,
     1
    ],
    "goal": [
     0,
     4
    ],
    "samples": [
     [
      0,
      2
     ],
     [
      0,
      4
     ]
    ],
    "road": [
     [
      1,
      0
     ],
     [
      1,
      1
     ],
     [
      1,
      2
     ],
     [
      0,
      2
     ],
     [
      0,
      3
     ],
     [
      0,
      4
     ]
    ],
    "budget": 9
   },
   "hints": {
    "cargo": [
     [
      0,
      3
     ],
     [
      1,
      2
     ],
     [
      4,
      5
     ]
    ],
    "robot": {
     "main": [
      "F",
      "F",
      "L",
      "F",
      "P",
      "R",
      "F",
      "F",
      "P"
     ],
     "body": [],
     "repeat": 2
    }
   }
  },
  "garden": {
   "info": {
    "id": "garden",
    "en": "Garden supplies",
    "zh": "花园补给",
    "tag": [
     "Harbor apprentice",
     "港湾学徒"
    ],
    "description": [
     "Chapter 1: plan, test and revise. Every mission has an optional hint.",
     "第 1 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Garden supplies",
      "花园补给"
     ],
     "power": [
      "Garden lamps",
      "花园灯串"
     ],
     "robot": [
      "Garden zigzag",
      "花园折线"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 5,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     }
    ],
    "capacity": 11,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 4,
    "source": 8,
    "targets": [
     3
    ],
    "fixed": [],
    "initial": [
     5,
     3,
     5,
     8,
     0,
     5,
     9,
     0,
     2,
     3,
     0,
     0,
     0,
     0,
     0,
     0
    ],
    "solution": [
     10,
     6,
     10,
     8,
     0,
     5,
     12,
     0,
     2,
     9,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     2,
     0,
     1
    ],
    "goal": [
     0,
     4
    ],
    "samples": [
     [
      1,
      2
     ],
     [
      0,
      4
     ]
    ],
    "road": [
     [
      2,
      0
     ],
     [
      2,
      1
     ],
     [
      2,
      2
     ],
     [
      1,
      2
     ],
     [
      1,
      3
     ],
     [
      1,
      4
     ],
     [
      0,
      4
     ]
    ],
    "budget": 11
   },
   "hints": {
    "cargo": [
     [
      0,
      3
     ],
     [
      1,
      2
     ],
     [
      4,
      5
     ]
    ],
    "robot": {
     "main": [
      "F",
      "F",
      "L",
      "F",
      "P",
      "R",
      "F",
      "F",
      "L",
      "F",
      "P"
     ],
     "body": [],
     "repeat": 2
    }
   }
  },
  "quay": {
   "info": {
    "id": "quay",
    "en": "Last crate",
    "zh": "最后一箱",
    "tag": [
     "Harbor apprentice",
     "港湾学徒"
    ],
    "description": [
     "Chapter 1: plan, test and revise. Every mission has an optional hint.",
     "第 1 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Last crate",
      "最后一箱"
     ],
     "power": [
      "Quay junction",
      "码头分岔"
     ],
     "robot": [
      "Return to the jetty",
      "返回码头"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 3,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     }
    ],
    "capacity": 12,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 4,
    "source": 8,
    "targets": [
     3
    ],
    "fixed": [],
    "initial": [
     0,
     3,
     10,
     8,
     3,
     3,
     0,
     0,
     1,
     0,
     0,
     12,
     0,
     0,
     0,
     0
    ],
    "solution": [
     0,
     6,
     10,
     8,
     6,
     9,
     0,
     0,
     1,
     0,
     0,
     6,
     0,
     0,
     0,
     0
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     2,
     0,
     1
    ],
    "goal": [
     0,
     0
    ],
    "samples": [
     [
      2,
      3
     ],
     [
      0,
      0
     ]
    ],
    "road": [
     [
      2,
      0
     ],
     [
      2,
      1
     ],
     [
      2,
      2
     ],
     [
      2,
      3
     ],
     [
      1,
      0
     ],
     [
      0,
      0
     ]
    ],
    "budget": 13
   },
   "hints": {
    "cargo": [
     [
      0,
      3
     ],
     [
      1,
      4
     ],
     [
      6,
      2,
      5
     ]
    ],
    "robot": {
     "main": [
      "F",
      "F",
      "F",
      "P",
      "L",
      "L",
      "F",
      "F",
      "F",
      "R",
      "F",
      "F",
      "P"
     ],
     "body": [],
     "repeat": 2
    }
   }
  },
  "orchard": {
   "info": {
    "id": "orchard",
    "en": "Orchard order",
    "zh": "果园顺序",
    "tag": [
     "Coastal planner",
     "海岸规划师"
    ],
    "description": [
     "Chapter 2: plan, test and revise. Every mission has an optional hint.",
     "第 2 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Orchard order",
      "果园顺序"
     ],
     "power": [
      "Orchard split",
      "果园分流"
     ],
     "robot": [
      "Short stairs",
      "短阶梯"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     }
    ],
    "capacity": 10,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 5,
    "source": 10,
    "targets": [
     4,
     24
    ],
    "fixed": [],
    "initial": [
     3,
     0,
     5,
     0,
     4,
     0,
     3,
     5,
     5,
     6,
     2,
     14,
     0,
     0,
     0,
     0,
     12,
     10,
     5,
     9,
     0,
     0,
     0,
     10,
     1
    ],
    "solution": [
     12,
     0,
     10,
     0,
     4,
     0,
     6,
     10,
     10,
     9,
     2,
     13,
     0,
     0,
     0,
     0,
     3,
     10,
     10,
     12,
     0,
     0,
     0,
     10,
     1
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     2,
     0,
     1
    ],
    "goal": [
     0,
     2
    ],
    "samples": [
     [
      1,
      1
     ],
     [
      0,
      2
     ]
    ],
    "road": [
     [
      2,
      0
     ],
     [
      2,
      1
     ],
     [
      1,
      1
     ],
     [
      1,
      2
     ],
     [
      0,
      2
     ]
    ],
    "budget": 6
   },
   "hints": {
    "cargo": [
     [
      0,
      3
     ],
     [
      1,
      4
     ],
     [
      6,
      2,
      5
     ]
    ],
    "robot": {
     "main": [
      "Q"
     ],
     "body": [
      "F",
      "L",
      "F",
      "P",
      "R"
     ],
     "repeat": 2
    }
   }
  },
  "canal": {
   "info": {
    "id": "canal",
    "en": "Canal convoy",
    "zh": "运河船队",
    "tag": [
     "Coastal planner",
     "海岸规划师"
    ],
    "description": [
     "Chapter 2: plan, test and revise. Every mission has an optional hint.",
     "第 2 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Canal convoy",
      "运河船队"
     ],
     "power": [
      "Canal crossing",
      "运河交汇"
     ],
     "robot": [
      "Wide stairs",
      "宽阶梯"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 3,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     }
    ],
    "capacity": 11,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 5,
    "source": 10,
    "targets": [
     4,
     24
    ],
    "fixed": [],
    "initial": [
     12,
     5,
     5,
     10,
     8,
     5,
     0,
     0,
     0,
     0,
     3,
     3,
     0,
     0,
     5,
     3,
     6,
     3,
     5,
     0,
     3,
     0,
     9,
     5,
     8
    ],
    "solution": [
     6,
     10,
     10,
     10,
     8,
     5,
     0,
     0,
     0,
     0,
     3,
     12,
     0,
     0,
     10,
     6,
     3,
     12,
     5,
     0,
     6,
     0,
     3,
     10,
     8
    ]
   },
   "robot": {
    "n": 6,
    "start": [
     5,
     0,
     1
    ],
    "goal": [
     0,
     4
    ],
    "samples": [
     [
      3,
      2
     ],
     [
      1,
      4
     ]
    ],
    "road": [
     [
      5,
      0
     ],
     [
      5,
      1
     ],
     [
      5,
      2
     ],
     [
      4,
      2
     ],
     [
      3,
      2
     ],
     [
      3,
      3
     ],
     [
      3,
      4
     ],
     [
      2,
      4
     ],
     [
      1,
      4
     ],
     [
      0,
      4
     ]
    ],
    "budget": 10
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      2
     ],
     [
      6,
      3,
      4
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "L",
      "F"
     ],
     "body": [
      "F",
      "F",
      "L",
      "F",
      "F",
      "P",
      "R"
     ],
     "repeat": 2
    }
   }
  },
  "cliff": {
   "info": {
    "id": "cliff",
    "en": "Cliff crane",
    "zh": "悬崖起重机",
    "tag": [
     "Coastal planner",
     "海岸规划师"
    ],
    "description": [
     "Chapter 2: plan, test and revise. Every mission has an optional hint.",
     "第 2 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Cliff crane",
      "悬崖起重机"
     ],
     "power": [
      "Cliff relays",
      "崖边接点"
     ],
     "robot": [
      "Narrow ascent",
      "窄路攀登"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 5,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     }
    ],
    "capacity": 11,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      2
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 5,
    "source": 10,
    "targets": [
     4,
     24
    ],
    "fixed": [],
    "initial": [
     3,
     5,
     10,
     5,
     8,
     5,
     0,
     0,
     0,
     9,
     5,
     0,
     0,
     0,
     0,
     10,
     0,
     0,
     0,
     0,
     12,
     5,
     5,
     5,
     8
    ],
    "solution": [
     6,
     10,
     10,
     10,
     8,
     5,
     0,
     0,
     0,
     6,
     5,
     0,
     0,
     0,
     0,
     5,
     0,
     0,
     0,
     0,
     3,
     10,
     10,
     10,
     8
    ]
   },
   "robot": {
    "n": 7,
    "start": [
     6,
     0,
     1
    ],
    "goal": [
     0,
     3
    ],
    "samples": [
     [
      4,
      1
     ],
     [
      2,
      2
     ],
     [
      0,
      3
     ]
    ],
    "road": [
     [
      6,
      0
     ],
     [
      6,
      1
     ],
     [
      5,
      1
     ],
     [
      4,
      1
     ],
     [
      4,
      2
     ],
     [
      3,
      2
     ],
     [
      2,
      2
     ],
     [
      2,
      3
     ],
     [
      1,
      3
     ],
     [
      0,
      3
     ]
    ],
    "budget": 7
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      2
     ],
     [
      6,
      3,
      4
     ]
    ],
    "robot": {
     "main": [
      "Q"
     ],
     "body": [
      "F",
      "L",
      "F",
      "F",
      "P",
      "R"
     ],
     "repeat": 3
    }
   }
  },
  "bridge": {
   "info": {
    "id": "bridge",
    "en": "Bridge builders",
    "zh": "搭桥工队",
    "tag": [
     "Coastal planner",
     "海岸规划师"
    ],
    "description": [
     "Chapter 2: plan, test and revise. Every mission has an optional hint.",
     "第 2 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Bridge builders",
      "搭桥工队"
     ],
     "power": [
      "Bridge lights",
      "桥头灯光"
     ],
     "robot": [
      "Three landings",
      "三段平台"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 3,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     }
    ],
    "capacity": 11,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      2
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {
     "5": 1
    }
   },
   "power": {
    "n": 5,
    "source": 10,
    "targets": [
     4,
     24
    ],
    "fixed": [],
    "initial": [
     0,
     0,
     0,
     9,
     8,
     3,
     5,
     10,
     6,
     0,
     5,
     0,
     0,
     0,
     0,
     10,
     0,
     5,
     3,
     0,
     12,
     5,
     10,
     5,
     8
    ],
    "solution": [
     0,
     0,
     0,
     6,
     8,
     6,
     10,
     10,
     9,
     0,
     5,
     0,
     0,
     0,
     0,
     5,
     0,
     10,
     6,
     0,
     3,
     10,
     10,
     10,
     8
    ]
   },
   "robot": {
    "n": 7,
    "start": [
     4,
     0,
     1
    ],
    "goal": [
     0,
     6
    ],
    "samples": [
     [
      3,
      2
     ],
     [
      2,
      4
     ],
     [
      1,
      6
     ],
     [
      0,
      6
     ]
    ],
    "road": [
     [
      4,
      0
     ],
     [
      4,
      1
     ],
     [
      4,
      2
     ],
     [
      3,
      2
     ],
     [
      3,
      3
     ],
     [
      3,
      4
     ],
     [
      2,
      4
     ],
     [
      2,
      5
     ],
     [
      2,
      6
     ],
     [
      1,
      6
     ],
     [
      0,
      6
     ]
    ],
    "budget": 10
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      2
     ],
     [
      6,
      3,
      4
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "L",
      "F",
      "P"
     ],
     "body": [
      "F",
      "F",
      "L",
      "F",
      "P",
      "R"
     ],
     "repeat": 3
    }
   }
  },
  "marsh": {
   "info": {
    "id": "marsh",
    "en": "Marsh pump",
    "zh": "湿地水泵",
    "tag": [
     "Tidal workshop",
     "潮汐工坊"
    ],
    "description": [
     "Chapter 3: plan, test and revise. Every mission has an optional hint.",
     "第 3 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Marsh pump",
      "湿地水泵"
     ],
     "power": [
      "Marsh branches",
      "湿地支路"
     ],
     "robot": [
      "Small survey",
      "小环巡查"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     }
    ],
    "capacity": 14,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 6,
    "source": 18,
    "targets": [
     0,
     5,
     35
    ],
    "fixed": [
     10
    ],
    "initial": [
     2,
     3,
     0,
     12,
     0,
     4,
     5,
     12,
     3,
     0,
     6,
     12,
     0,
     3,
     13,
     5,
     7,
     0,
     2,
     3,
     0,
     0,
     10,
     0,
     0,
     0,
     0,
     0,
     6,
     6,
     0,
     0,
     0,
     0,
     6,
     1
    ],
    "solution": [
     2,
     12,
     0,
     6,
     0,
     4,
     5,
     3,
     12,
     0,
     6,
     9,
     0,
     6,
     11,
     10,
     13,
     0,
     2,
     9,
     0,
     0,
     5,
     0,
     0,
     0,
     0,
     0,
     3,
     12,
     0,
     0,
     0,
     0,
     3,
     1
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     2,
     0,
     1
    ],
    "goal": [
     2,
     0
    ],
    "samples": [
     [
      2,
      2
     ],
     [
      0,
      2
     ],
     [
      0,
      0
     ],
     [
      2,
      0
     ]
    ],
    "road": [
     [
      2,
      0
     ],
     [
      2,
      1
     ],
     [
      2,
      2
     ],
     [
      1,
      2
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ]
    ],
    "budget": 5
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      2
     ],
     [
      1,
      8,
      5
     ],
     [
      3,
      4,
      6
     ]
    ],
    "robot": {
     "main": [
      "Q"
     ],
     "body": [
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 4
    }
   }
  },
  "delta": {
   "info": {
    "id": "delta",
    "en": "Delta deliveries",
    "zh": "三角洲运送",
    "tag": [
     "Tidal workshop",
     "潮汐工坊"
    ],
    "description": [
     "Chapter 3: plan, test and revise. Every mission has an optional hint.",
     "第 3 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Delta deliveries",
      "三角洲运送"
     ],
     "power": [
      "Delta network",
      "三角洲网络"
     ],
     "robot": [
      "Long rectangle",
      "长方形巡查"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 3,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     }
    ],
    "capacity": 13,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 6,
    "source": 18,
    "targets": [
     0,
     5,
     35
    ],
    "fixed": [
     6
    ],
    "initial": [
     2,
     6,
     0,
     9,
     10,
     8,
     6,
     14,
     5,
     12,
     0,
     9,
     10,
     0,
     0,
     0,
     0,
     0,
     3,
     6,
     5,
     0,
     0,
     0,
     0,
     9,
     10,
     3,
     0,
     9,
     0,
     0,
     0,
     9,
     5,
     8
    ],
    "solution": [
     2,
     12,
     0,
     6,
     10,
     8,
     6,
     11,
     10,
     9,
     0,
     6,
     5,
     0,
     0,
     0,
     0,
     0,
     3,
     12,
     5,
     0,
     0,
     0,
     0,
     3,
     10,
     12,
     0,
     6,
     0,
     0,
     0,
     3,
     10,
     8
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     2,
     0,
     1
    ],
    "goal": [
     2,
     0
    ],
    "samples": [
     [
      2,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      0
     ],
     [
      2,
      0
     ]
    ],
    "road": [
     [
      2,
      0
     ],
     [
      2,
      1
     ],
     [
      2,
      2
     ],
     [
      2,
      3
     ],
     [
      1,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ]
    ],
    "budget": 10
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      2
     ],
     [
      1,
      8,
      5
     ],
     [
      3,
      4,
      6
     ]
    ],
    "robot": {
     "main": [
      "Q"
     ],
     "body": [
      "F",
      "F",
      "F",
      "P",
      "L",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 2
    }
   }
  },
  "grove": {
   "info": {
    "id": "grove",
    "en": "Grove relay",
    "zh": "林地接力",
    "tag": [
     "Tidal workshop",
     "潮汐工坊"
    ],
    "description": [
     "Chapter 3: plan, test and revise. Every mission has an optional hint.",
     "第 3 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Grove relay",
      "林地接力"
     ],
     "power": [
      "Grove stations",
      "林间站点"
     ],
     "robot": [
      "Two sides at once",
      "两边一组"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 5,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     }
    ],
    "capacity": 13,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {
     "2": 1
    }
   },
   "power": {
    "n": 6,
    "source": 18,
    "targets": [
     0,
     5,
     35
    ],
    "fixed": [
     7
    ],
    "initial": [
     4,
     0,
     0,
     12,
     5,
     8,
     13,
     10,
     5,
     12,
     0,
     0,
     10,
     3,
     0,
     10,
     0,
     0,
     5,
     0,
     0,
     0,
     0,
     5,
     6,
     9,
     6,
     12,
     0,
     0,
     0,
     6,
     5,
     10,
     5,
     8
    ],
    "solution": [
     4,
     0,
     0,
     6,
     10,
     8,
     7,
     10,
     10,
     9,
     0,
     0,
     5,
     12,
     0,
     5,
     0,
     0,
     5,
     0,
     0,
     0,
     0,
     10,
     3,
     12,
     3,
     3,
     0,
     0,
     0,
     3,
     10,
     10,
     10,
     8
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     1,
     0,
     1
    ],
    "goal": [
     1,
     0
    ],
    "samples": [
     [
      1,
      4
     ],
     [
      0,
      4
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ]
    ],
    "road": [
     [
      1,
      0
     ],
     [
      1,
      1
     ],
     [
      1,
      2
     ],
     [
      1,
      3
     ],
     [
      1,
      4
     ],
     [
      0,
      4
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ]
    ],
    "budget": 10
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      2
     ],
     [
      1,
      8,
      5
     ],
     [
      3,
      4,
      6
     ]
    ],
    "robot": {
     "main": [
      "Q"
     ],
     "body": [
      "F",
      "F",
      "F",
      "F",
      "P",
      "L",
      "F",
      "P",
      "L"
     ],
     "repeat": 2
    }
   }
  },
  "inlet": {
   "info": {
    "id": "inlet",
    "en": "Inlet priority",
    "zh": "海口优先",
    "tag": [
     "Tidal workshop",
     "潮汐工坊"
    ],
    "description": [
     "Chapter 3: plan, test and revise. Every mission has an optional hint.",
     "第 3 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Inlet priority",
      "海口优先"
     ],
     "power": [
      "Inlet switches",
      "海口转接"
     ],
     "robot": [
      "Survey checkpoints",
      "沿途采样"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 3,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     }
    ],
    "capacity": 14,
    "maxTrips": 3,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ]
    ],
    "apart": [
     [
      2,
      3
     ]
    ],
    "by": {
     "2": 1
    }
   },
   "power": {
    "n": 6,
    "source": 18,
    "targets": [
     0,
     5,
     35
    ],
    "fixed": [
     10
    ],
    "initial": [
     4,
     5,
     0,
     0,
     0,
     4,
     9,
     9,
     12,
     9,
     10,
     12,
     12,
     13,
     5,
     6,
     0,
     9,
     3,
     9,
     9,
     0,
     10,
     10,
     0,
     9,
     5,
     5,
     9,
     0,
     0,
     0,
     0,
     10,
     12,
     8
    ],
    "solution": [
     4,
     5,
     0,
     0,
     0,
     4,
     3,
     12,
     6,
     6,
     10,
     9,
     6,
     11,
     10,
     9,
     0,
     12,
     3,
     12,
     6,
     0,
     5,
     5,
     0,
     3,
     10,
     10,
     12,
     0,
     0,
     0,
     0,
     5,
     3,
     8
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     3,
     0,
     1
    ],
    "goal": [
     3,
     0
    ],
    "samples": [
     [
      3,
      1
     ],
     [
      3,
      3
     ],
     [
      2,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      3,
      0
     ]
    ],
    "road": [
     [
      3,
      0
     ],
     [
      3,
      1
     ],
     [
      3,
      2
     ],
     [
      3,
      3
     ],
     [
      2,
      3
     ],
     [
      1,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      0
     ]
    ],
    "budget": 7
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      2
     ],
     [
      1,
      8,
      5
     ],
     [
      3,
      4,
      6
     ]
    ],
    "robot": {
     "main": [
      "Q"
     ],
     "body": [
      "F",
      "P",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 4
    }
   }
  },
  "terrace": {
   "info": {
    "id": "terrace",
    "en": "Terrace sequence",
    "zh": "梯田工序",
    "tag": [
     "Ridge expedition",
     "山脊探险"
    ],
    "description": [
     "Chapter 4: plan, test and revise. Every mission has an optional hint.",
     "第 4 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Terrace sequence",
      "梯田工序"
     ],
     "power": [
      "Terrace current",
      "梯田电流"
     ],
     "robot": [
      "Survey then dock",
      "巡查后停靠"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     }
    ],
    "capacity": 12,
    "maxTrips": 4,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 6,
    "source": 18,
    "targets": [
     0,
     5,
     35,
     30
    ],
    "fixed": [
     10,
     25
    ],
    "initial": [
     4,
     0,
     0,
     10,
     3,
     8,
     9,
     9,
     3,
     9,
     5,
     9,
     3,
     13,
     5,
     5,
     3,
     0,
     5,
     0,
     10,
     3,
     0,
     0,
     14,
     10,
     3,
     0,
     0,
     0,
     1,
     0,
     9,
     10,
     10,
     8
    ],
    "solution": [
     4,
     0,
     0,
     5,
     6,
     8,
     3,
     12,
     6,
     3,
     5,
     3,
     6,
     11,
     10,
     10,
     9,
     0,
     5,
     0,
     5,
     12,
     0,
     0,
     7,
     10,
     12,
     0,
     0,
     0,
     1,
     0,
     3,
     10,
     10,
     8
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     3,
     0,
     1
    ],
    "goal": [
     2,
     1
    ],
    "samples": [
     [
      3,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      0
     ],
     [
      3,
      0
     ],
     [
      2,
      1
     ]
    ],
    "road": [
     [
      3,
      0
     ],
     [
      3,
      1
     ],
     [
      3,
      2
     ],
     [
      3,
      3
     ],
     [
      2,
      3
     ],
     [
      1,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      0
     ],
     [
      2,
      1
     ]
    ],
    "budget": 11
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8
     ],
     [
      6,
      3
     ],
     [
      9,
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "L",
      "F",
      "R",
      "F",
      "P"
     ],
     "body": [
      "F",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 4
    }
   }
  },
  "ravine": {
   "info": {
    "id": "ravine",
    "en": "Ravine deck",
    "zh": "峡谷甲板",
    "tag": [
     "Ridge expedition",
     "山脊探险"
    ],
    "description": [
     "Chapter 4: plan, test and revise. Every mission has an optional hint.",
     "第 4 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Ravine deck",
      "峡谷甲板"
     ],
     "power": [
      "Ravine forks",
      "峡谷分岔"
     ],
     "robot": [
      "Return to the center",
      "回到中心"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 3,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     }
    ],
    "capacity": 11,
    "maxTrips": 4,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ]
    ],
    "by": {}
   },
   "power": {
    "n": 6,
    "source": 18,
    "targets": [
     0,
     5,
     35,
     30
    ],
    "fixed": [
     11,
     22
    ],
    "initial": [
     2,
     9,
     0,
     5,
     12,
     4,
     0,
     12,
     3,
     0,
     0,
     5,
     0,
     0,
     10,
     0,
     12,
     3,
     6,
     5,
     7,
     13,
     9,
     0,
     10,
     5,
     0,
     6,
     9,
     0,
     1,
     9,
     9,
     0,
     9,
     8
    ],
    "solution": [
     2,
     12,
     0,
     10,
     6,
     4,
     0,
     3,
     12,
     0,
     0,
     5,
     0,
     0,
     5,
     0,
     6,
     9,
     6,
     10,
     11,
     14,
     9,
     0,
     5,
     10,
     0,
     3,
     12,
     0,
     1,
     3,
     6,
     0,
     3,
     8
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     4,
     0,
     1
    ],
    "goal": [
     2,
     2
    ],
    "samples": [
     [
      4,
      4
     ],
     [
      0,
      4
     ],
     [
      0,
      0
     ],
     [
      4,
      0
     ],
     [
      2,
      2
     ]
    ],
    "road": [
     [
      4,
      0
     ],
     [
      4,
      1
     ],
     [
      4,
      2
     ],
     [
      4,
      3
     ],
     [
      4,
      4
     ],
     [
      3,
      4
     ],
     [
      2,
      4
     ],
     [
      1,
      4
     ],
     [
      0,
      4
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      0
     ],
     [
      3,
      0
     ],
     [
      2,
      1
     ],
     [
      2,
      2
     ]
    ],
    "budget": 14
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8
     ],
     [
      6,
      3
     ],
     [
      9,
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "L",
      "F",
      "F",
      "R",
      "F",
      "F",
      "P"
     ],
     "body": [
      "F",
      "F",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 4
    }
   }
  },
  "plateau": {
   "info": {
    "id": "plateau",
    "en": "Plateau relay",
    "zh": "高原接力",
    "tag": [
     "Ridge expedition",
     "山脊探险"
    ],
    "description": [
     "Chapter 4: plan, test and revise. Every mission has an optional hint.",
     "第 4 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Plateau relay",
      "高原接力"
     ],
     "power": [
      "Plateau grid",
      "高原电网"
     ],
     "robot": [
      "Samples on every side",
      "每边都采样"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 5,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     }
    ],
    "capacity": 11,
    "maxTrips": 4,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ]
    ],
    "by": {
     "5": 1
    }
   },
   "power": {
    "n": 6,
    "source": 18,
    "targets": [
     0,
     5,
     35,
     30
    ],
    "fixed": [
     8,
     26
    ],
    "initial": [
     2,
     9,
     0,
     0,
     3,
     8,
     0,
     13,
     10,
     5,
     3,
     9,
     9,
     10,
     0,
     0,
     0,
     0,
     6,
     3,
     0,
     0,
     5,
     0,
     6,
     7,
     10,
     5,
     5,
     6,
     2,
     12,
     0,
     0,
     0,
     1
    ],
    "solution": [
     2,
     12,
     0,
     0,
     6,
     8,
     0,
     7,
     10,
     10,
     9,
     12,
     3,
     5,
     0,
     0,
     0,
     0,
     6,
     9,
     0,
     0,
     10,
     0,
     3,
     14,
     10,
     10,
     10,
     12,
     2,
     9,
     0,
     0,
     0,
     1
    ]
   },
   "robot": {
    "n": 5,
    "start": [
     4,
     0,
     1
    ],
    "goal": [
     3,
     2
    ],
    "samples": [
     [
      4,
      2
     ],
     [
      4,
      4
     ],
     [
      2,
      4
     ],
     [
      0,
      4
     ],
     [
      0,
      2
     ],
     [
      0,
      0
     ],
     [
      2,
      0
     ],
     [
      4,
      0
     ],
     [
      3,
      2
     ]
    ],
    "road": [
     [
      4,
      0
     ],
     [
      4,
      1
     ],
     [
      4,
      2
     ],
     [
      4,
      3
     ],
     [
      4,
      4
     ],
     [
      3,
      4
     ],
     [
      2,
      4
     ],
     [
      1,
      4
     ],
     [
      0,
      4
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      0
     ],
     [
      3,
      0
     ],
     [
      3,
      1
     ],
     [
      3,
      2
     ]
    ],
    "budget": 14
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8
     ],
     [
      6,
      3
     ],
     [
      9,
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "L",
      "F",
      "R",
      "F",
      "F",
      "P"
     ],
     "body": [
      "F",
      "F",
      "P",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 4
    }
   }
  },
  "waterfall": {
   "info": {
    "id": "waterfall",
    "en": "Waterfall works",
    "zh": "瀑布工程",
    "tag": [
     "Ridge expedition",
     "山脊探险"
    ],
    "description": [
     "Chapter 4: plan, test and revise. Every mission has an optional hint.",
     "第 4 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Waterfall works",
      "瀑布工程"
     ],
     "power": [
      "Waterfall lights",
      "瀑布灯网"
     ],
     "robot": [
      "The side laboratory",
      "侧边实验室"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 3,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     }
    ],
    "capacity": 11,
    "maxTrips": 4,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ],
     [
      3,
      4
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ]
    ],
    "by": {
     "5": 1
    }
   },
   "power": {
    "n": 6,
    "source": 18,
    "targets": [
     0,
     5,
     35,
     30
    ],
    "fixed": [
     4,
     34
    ],
    "initial": [
     6,
     5,
     5,
     5,
     10,
     8,
     10,
     0,
     0,
     6,
     0,
     0,
     5,
     0,
     9,
     0,
     0,
     10,
     5,
     12,
     0,
     5,
     0,
     5,
     5,
     6,
     9,
     9,
     0,
     9,
     3,
     5,
     5,
     5,
     10,
     8
    ],
    "solution": [
     6,
     10,
     10,
     10,
     10,
     8,
     5,
     0,
     0,
     12,
     0,
     0,
     5,
     0,
     6,
     0,
     0,
     10,
     5,
     6,
     0,
     5,
     0,
     5,
     5,
     12,
     3,
     3,
     0,
     3,
     3,
     10,
     10,
     10,
     10,
     8
    ]
   },
   "robot": {
    "n": 6,
    "start": [
     5,
     0,
     1
    ],
    "goal": [
     3,
     1
    ],
    "samples": [
     [
      5,
      5
     ],
     [
      0,
      5
     ],
     [
      0,
      0
     ],
     [
      5,
      0
     ],
     [
      3,
      1
     ]
    ],
    "road": [
     [
      5,
      0
     ],
     [
      5,
      1
     ],
     [
      5,
      2
     ],
     [
      5,
      3
     ],
     [
      5,
      4
     ],
     [
      5,
      5
     ],
     [
      4,
      5
     ],
     [
      3,
      5
     ],
     [
      2,
      5
     ],
     [
      1,
      5
     ],
     [
      0,
      5
     ],
     [
      0,
      4
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      0
     ],
     [
      3,
      0
     ],
     [
      4,
      0
     ],
     [
      3,
      1
     ]
    ],
    "budget": 14
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8
     ],
     [
      6,
      3
     ],
     [
      9,
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "L",
      "F",
      "F",
      "R",
      "F",
      "P"
     ],
     "body": [
      "F",
      "F",
      "F",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 4
    }
   }
  },
  "observatory": {
   "info": {
    "id": "observatory",
    "en": "Observatory cargo",
    "zh": "观测台补给",
    "tag": [
     "Beacon network",
     "灯塔网络"
    ],
    "description": [
     "Chapter 5: plan, test and revise. Every mission has an optional hint.",
     "第 5 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Observatory cargo",
      "观测台补给"
     ],
     "power": [
      "Observatory link",
      "观测台连线"
     ],
     "robot": [
      "Twin outposts",
      "双前哨巡查"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     },
     {
      "id": 10,
      "en": "Cable",
      "zh": "电缆",
      "weight": 2,
      "icon": "bolt"
     }
    ],
    "capacity": 14,
    "maxTrips": 4,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ]
    ],
    "by": {
     "5": 1
    }
   },
   "power": {
    "n": 7,
    "source": 21,
    "targets": [
     0,
     6,
     48,
     42
    ],
    "fixed": [
     5,
     29,
     47
    ],
    "initial": [
     2,
     9,
     0,
     9,
     10,
     10,
     8,
     10,
     14,
     5,
     3,
     0,
     10,
     0,
     9,
     12,
     0,
     0,
     5,
     0,
     3,
     5,
     0,
     10,
     0,
     9,
     12,
     0,
     6,
     12,
     0,
     0,
     0,
     0,
     0,
     9,
     13,
     5,
     3,
     10,
     9,
     0,
     1,
     0,
     5,
     12,
     5,
     10,
     8
    ],
    "solution": [
     2,
     12,
     0,
     6,
     10,
     10,
     8,
     5,
     7,
     10,
     9,
     0,
     5,
     0,
     6,
     9,
     0,
     0,
     10,
     0,
     6,
     5,
     0,
     5,
     0,
     3,
     6,
     0,
     3,
     12,
     0,
     0,
     0,
     0,
     0,
     6,
     11,
     10,
     12,
     5,
     12,
     0,
     1,
     0,
     10,
     3,
     10,
     10,
     8
    ]
   },
   "robot": {
    "n": 7,
    "start": [
     2,
     0,
     1
    ],
    "goal": [
     2,
     4
    ],
    "samples": [
     [
      2,
      2
     ],
     [
      0,
      2
     ],
     [
      0,
      0
     ],
     [
      2,
      0
     ],
     [
      2,
      6
     ],
     [
      0,
      6
     ],
     [
      0,
      4
     ],
     [
      2,
      4
     ]
    ],
    "road": [
     [
      2,
      0
     ],
     [
      2,
      1
     ],
     [
      2,
      2
     ],
     [
      1,
      2
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      3
     ],
     [
      2,
      4
     ],
     [
      2,
      5
     ],
     [
      2,
      6
     ],
     [
      1,
      6
     ],
     [
      0,
      6
     ],
     [
      0,
      5
     ],
     [
      0,
      4
     ],
     [
      1,
      4
     ]
    ],
    "budget": 10
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8,
      10
     ],
     [
      6,
      3
     ],
     [
      9,
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "F",
      "F",
      "F",
      "F",
      "Q"
     ],
     "body": [
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 4
    }
   }
  },
  "estuary": {
   "info": {
    "id": "estuary",
    "en": "Estuary schedule",
    "zh": "河口调度",
    "tag": [
     "Beacon network",
     "灯塔网络"
    ],
    "description": [
     "Chapter 5: plan, test and revise. Every mission has an optional hint.",
     "第 5 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Estuary schedule",
      "河口调度"
     ],
     "power": [
      "Estuary relays",
      "河口接力"
     ],
     "robot": [
      "Wide twin camps",
      "宽营地巡查"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 3,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     },
     {
      "id": 10,
      "en": "Cable",
      "zh": "电缆",
      "weight": 2,
      "icon": "bolt"
     }
    ],
    "capacity": 13,
    "maxTrips": 4,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ],
     [
      3,
      4
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ]
    ],
    "by": {
     "5": 1
    }
   },
   "power": {
    "n": 7,
    "source": 21,
    "targets": [
     0,
     6,
     48,
     42
    ],
    "fixed": [
     4,
     30,
     46
    ],
    "initial": [
     4,
     3,
     10,
     5,
     10,
     5,
     8,
     13,
     6,
     0,
     0,
     0,
     0,
     0,
     10,
     0,
     12,
     9,
     3,
     0,
     6,
     5,
     0,
     12,
     0,
     0,
     0,
     0,
     14,
     5,
     12,
     12,
     0,
     5,
     9,
     10,
     0,
     10,
     3,
     6,
     12,
     10,
     1,
     0,
     6,
     12,
     3,
     5,
     8
    ],
    "solution": [
     4,
     6,
     10,
     10,
     10,
     10,
     8,
     7,
     9,
     0,
     0,
     0,
     0,
     0,
     5,
     0,
     3,
     12,
     6,
     0,
     12,
     5,
     0,
     3,
     0,
     0,
     0,
     0,
     7,
     10,
     12,
     6,
     0,
     10,
     3,
     5,
     0,
     5,
     6,
     12,
     6,
     5,
     1,
     0,
     3,
     9,
     3,
     10,
     8
    ]
   },
   "robot": {
    "n": 9,
    "start": [
     3,
     0,
     1
    ],
    "goal": [
     3,
     5
    ],
    "samples": [
     [
      3,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      0
     ],
     [
      3,
      0
     ],
     [
      3,
      8
     ],
     [
      0,
      8
     ],
     [
      0,
      5
     ],
     [
      3,
      5
     ]
    ],
    "road": [
     [
      3,
      0
     ],
     [
      3,
      1
     ],
     [
      3,
      2
     ],
     [
      3,
      3
     ],
     [
      2,
      3
     ],
     [
      1,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      0
     ],
     [
      3,
      4
     ],
     [
      3,
      5
     ],
     [
      3,
      6
     ],
     [
      3,
      7
     ],
     [
      3,
      8
     ],
     [
      2,
      8
     ],
     [
      1,
      8
     ],
     [
      0,
      8
     ],
     [
      0,
      7
     ],
     [
      0,
      6
     ],
     [
      0,
      5
     ],
     [
      1,
      5
     ],
     [
      2,
      5
     ]
    ],
    "budget": 12
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8,
      10
     ],
     [
      6,
      3
     ],
     [
      9,
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "F",
      "F",
      "F",
      "F",
      "F",
      "Q"
     ],
     "body": [
      "F",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 4
    }
   }
  },
  "lighthouse": {
   "info": {
    "id": "lighthouse",
    "en": "Lighthouse chain",
    "zh": "灯塔建造链",
    "tag": [
     "Beacon network",
     "灯塔网络"
    ],
    "description": [
     "Chapter 5: plan, test and revise. Every mission has an optional hint.",
     "第 5 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Lighthouse chain",
      "灯塔建造链"
     ],
     "power": [
      "Lighthouse mesh",
      "灯塔联通"
     ],
     "robot": [
      "Two rectangular camps",
      "双矩形营地"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 5,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     },
     {
      "id": 10,
      "en": "Cable",
      "zh": "电缆",
      "weight": 2,
      "icon": "bolt"
     }
    ],
    "capacity": 13,
    "maxTrips": 4,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ],
     [
      3,
      4
     ],
     [
      7,
      10
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ],
     [
      2,
      10
     ]
    ],
    "by": {
     "5": 1
    }
   },
   "power": {
    "n": 7,
    "source": 21,
    "targets": [
     0,
     6,
     48,
     42
    ],
    "fixed": [
     5,
     24,
     40
    ],
    "initial": [
     2,
     9,
     5,
     12,
     5,
     10,
     8,
     0,
     10,
     0,
     10,
     5,
     10,
     0,
     12,
     10,
     0,
     10,
     3,
     9,
     0,
     6,
     13,
     5,
     9,
     0,
     0,
     0,
     5,
     0,
     0,
     0,
     0,
     0,
     0,
     11,
     5,
     5,
     5,
     5,
     12,
     0,
     1,
     5,
     0,
     0,
     10,
     9,
     8
    ],
    "solution": [
     2,
     12,
     10,
     6,
     10,
     10,
     8,
     0,
     5,
     0,
     5,
     10,
     10,
     0,
     6,
     5,
     0,
     5,
     6,
     3,
     0,
     6,
     11,
     10,
     9,
     0,
     0,
     0,
     5,
     0,
     0,
     0,
     0,
     0,
     0,
     7,
     10,
     10,
     10,
     10,
     12,
     0,
     1,
     10,
     0,
     0,
     10,
     3,
     8
    ]
   },
   "robot": {
    "n": 9,
    "start": [
     2,
     0,
     1
    ],
    "goal": [
     2,
     5
    ],
    "samples": [
     [
      2,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      0
     ],
     [
      2,
      0
     ],
     [
      2,
      8
     ],
     [
      0,
      8
     ],
     [
      0,
      5
     ],
     [
      2,
      5
     ]
    ],
    "road": [
     [
      2,
      0
     ],
     [
      2,
      1
     ],
     [
      2,
      2
     ],
     [
      2,
      3
     ],
     [
      1,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      4
     ],
     [
      2,
      5
     ],
     [
      2,
      6
     ],
     [
      2,
      7
     ],
     [
      2,
      8
     ],
     [
      1,
      8
     ],
     [
      0,
      8
     ],
     [
      0,
      7
     ],
     [
      0,
      6
     ],
     [
      0,
      5
     ],
     [
      1,
      5
     ]
    ],
    "budget": 16
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8,
      10
     ],
     [
      6,
      3
     ],
     [
      9,
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "F",
      "F",
      "F",
      "F",
      "F",
      "Q"
     ],
     "body": [
      "F",
      "F",
      "F",
      "P",
      "L",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 2
    }
   }
  },
  "reservoir": {
   "info": {
    "id": "reservoir",
    "en": "Reservoir plan",
    "zh": "水库规划",
    "tag": [
     "Beacon network",
     "灯塔网络"
    ],
    "description": [
     "Chapter 5: plan, test and revise. Every mission has an optional hint.",
     "第 5 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Reservoir plan",
      "水库规划"
     ],
     "power": [
      "Reservoir branches",
      "水库分支"
     ],
     "robot": [
      "Return from two camps",
      "双营地返航"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 3,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     },
     {
      "id": 10,
      "en": "Cable",
      "zh": "电缆",
      "weight": 2,
      "icon": "bolt"
     }
    ],
    "capacity": 13,
    "maxTrips": 4,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ],
     [
      3,
      4
     ],
     [
      7,
      10
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ],
     [
      2,
      10
     ]
    ],
    "by": {
     "5": 1,
     "8": 2
    }
   },
   "power": {
    "n": 7,
    "source": 21,
    "targets": [
     0,
     6,
     48,
     42
    ],
    "fixed": [
     11,
     28,
     46
    ],
    "initial": [
     4,
     0,
     0,
     5,
     3,
     5,
     8,
     10,
     10,
     0,
     6,
     5,
     0,
     0,
     10,
     0,
     0,
     9,
     3,
     3,
     0,
     7,
     5,
     10,
     6,
     5,
     9,
     0,
     7,
     6,
     3,
     0,
     0,
     0,
     6,
     10,
     5,
     0,
     0,
     0,
     0,
     5,
     1,
     12,
     5,
     5,
     10,
     5,
     8
    ],
    "solution": [
     4,
     0,
     0,
     10,
     6,
     10,
     8,
     5,
     5,
     0,
     12,
     5,
     0,
     0,
     5,
     0,
     0,
     6,
     9,
     12,
     0,
     7,
     10,
     10,
     9,
     5,
     6,
     0,
     7,
     12,
     6,
     0,
     0,
     0,
     12,
     5,
     5,
     0,
     0,
     0,
     0,
     10,
     1,
     3,
     10,
     10,
     10,
     10,
     8
    ]
   },
   "robot": {
    "n": 7,
    "start": [
     2,
     0,
     1
    ],
    "goal": [
     1,
     5
    ],
    "samples": [
     [
      2,
      2
     ],
     [
      0,
      2
     ],
     [
      0,
      0
     ],
     [
      2,
      0
     ],
     [
      2,
      6
     ],
     [
      0,
      6
     ],
     [
      0,
      4
     ],
     [
      2,
      4
     ],
     [
      1,
      5
     ]
    ],
    "road": [
     [
      2,
      0
     ],
     [
      2,
      1
     ],
     [
      2,
      2
     ],
     [
      1,
      2
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      3
     ],
     [
      2,
      4
     ],
     [
      2,
      5
     ],
     [
      2,
      6
     ],
     [
      1,
      6
     ],
     [
      0,
      6
     ],
     [
      0,
      5
     ],
     [
      0,
      4
     ],
     [
      1,
      4
     ],
     [
      1,
      5
     ]
    ],
    "budget": 15
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8,
      10
     ],
     [
      6,
      3
     ],
     [
      9,
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "F",
      "F",
      "F",
      "F",
      "Q",
      "L",
      "F",
      "R",
      "F",
      "P"
     ],
     "body": [
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 4
    }
   }
  },
  "citadel": {
   "info": {
    "id": "citadel",
    "en": "Citadel convoy",
    "zh": "堡垒船队",
    "tag": [
     "Island master",
     "全岛总工程师"
    ],
    "description": [
     "Chapter 6: plan, test and revise. Every mission has an optional hint.",
     "第 6 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Citadel convoy",
      "堡垒船队"
     ],
     "power": [
      "Citadel power",
      "堡垒电路"
     ],
     "robot": [
      "Survey and climb",
      "巡查再攀登"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     },
     {
      "id": 10,
      "en": "Cable",
      "zh": "电缆",
      "weight": 2,
      "icon": "bolt"
     },
     {
      "id": 11,
      "en": "Antenna",
      "zh": "天线",
      "weight": 4,
      "icon": "sensor"
     }
    ],
    "capacity": 12,
    "maxTrips": 5,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ],
     [
      3,
      4
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ]
    ],
    "by": {
     "5": 1
    }
   },
   "power": {
    "n": 8,
    "source": 32,
    "targets": [
     0,
     7,
     63,
     56,
     39
    ],
    "fixed": [
     23,
     34,
     50
    ],
    "initial": [
     4,
     5,
     0,
     5,
     12,
     10,
     9,
     4,
     5,
     12,
     0,
     0,
     0,
     5,
     0,
     10,
     10,
     5,
     0,
     0,
     0,
     0,
     0,
     5,
     5,
     10,
     12,
     6,
     3,
     5,
     5,
     14,
     7,
     5,
     10,
     10,
     6,
     6,
     0,
     1,
     11,
     10,
     6,
     9,
     0,
     0,
     9,
     12,
     10,
     10,
     3,
     10,
     5,
     5,
     10,
     3,
     1,
     10,
     0,
     10,
     0,
     6,
     5,
     1
    ],
    "solution": [
     4,
     5,
     0,
     10,
     6,
     10,
     12,
     4,
     5,
     6,
     0,
     0,
     0,
     5,
     0,
     5,
     5,
     10,
     0,
     0,
     0,
     0,
     0,
     5,
     5,
     5,
     3,
     12,
     6,
     10,
     10,
     13,
     7,
     10,
     10,
     10,
     9,
     3,
     0,
     1,
     7,
     10,
     12,
     6,
     0,
     0,
     3,
     3,
     5,
     5,
     3,
     10,
     10,
     10,
     10,
     12,
     1,
     10,
     0,
     10,
     0,
     12,
     10,
     1
    ]
   },
   "robot": {
    "n": 9,
    "start": [
     4,
     0,
     1
    ],
    "goal": [
     0,
     5
    ],
    "samples": [
     [
      4,
      3
     ],
     [
      1,
      3
     ],
     [
      1,
      0
     ],
     [
      4,
      0
     ],
     [
      4,
      8
     ],
     [
      1,
      8
     ],
     [
      1,
      5
     ],
     [
      4,
      5
     ],
     [
      0,
      5
     ]
    ],
    "road": [
     [
      4,
      0
     ],
     [
      4,
      1
     ],
     [
      4,
      2
     ],
     [
      4,
      3
     ],
     [
      3,
      3
     ],
     [
      2,
      3
     ],
     [
      1,
      3
     ],
     [
      1,
      2
     ],
     [
      1,
      1
     ],
     [
      1,
      0
     ],
     [
      2,
      0
     ],
     [
      3,
      0
     ],
     [
      4,
      4
     ],
     [
      4,
      5
     ],
     [
      4,
      6
     ],
     [
      4,
      7
     ],
     [
      4,
      8
     ],
     [
      3,
      8
     ],
     [
      2,
      8
     ],
     [
      1,
      8
     ],
     [
      1,
      7
     ],
     [
      1,
      6
     ],
     [
      1,
      5
     ],
     [
      2,
      5
     ],
     [
      3,
      5
     ],
     [
      0,
      5
     ]
    ],
    "budget": 18
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8
     ],
     [
      6,
      3,
      11
     ],
     [
      9,
      10
     ],
     [
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "F",
      "F",
      "F",
      "F",
      "F",
      "Q",
      "L",
      "F",
      "F",
      "F",
      "F",
      "P"
     ],
     "body": [
      "F",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 4
    }
   }
  },
  "aurora": {
   "info": {
    "id": "aurora",
    "en": "Aurora expedition",
    "zh": "极光远征",
    "tag": [
     "Island master",
     "全岛总工程师"
    ],
    "description": [
     "Chapter 6: plan, test and revise. Every mission has an optional hint.",
     "第 6 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Aurora expedition",
      "极光远征"
     ],
     "power": [
      "Aurora network",
      "极光网络"
     ],
     "robot": [
      "Conditional corners",
      "条件转弯"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 3,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     },
     {
      "id": 10,
      "en": "Cable",
      "zh": "电缆",
      "weight": 2,
      "icon": "bolt"
     },
     {
      "id": 11,
      "en": "Antenna",
      "zh": "天线",
      "weight": 4,
      "icon": "sensor"
     }
    ],
    "capacity": 11,
    "maxTrips": 5,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ],
     [
      3,
      4
     ],
     [
      7,
      10
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ],
     [
      2,
      10
     ],
     [
      6,
      9
     ]
    ],
    "by": {
     "5": 1
    }
   },
   "power": {
    "n": 8,
    "source": 32,
    "targets": [
     0,
     7,
     63,
     56,
     39
    ],
    "fixed": [
     15,
     34,
     46
    ],
    "initial": [
     2,
     6,
     6,
     0,
     0,
     3,
     10,
     4,
     3,
     3,
     0,
     10,
     9,
     0,
     9,
     5,
     10,
     0,
     0,
     0,
     0,
     0,
     9,
     10,
     5,
     12,
     9,
     0,
     6,
     6,
     12,
     3,
     7,
     10,
     10,
     9,
     0,
     3,
     11,
     8,
     10,
     0,
     0,
     9,
     10,
     7,
     9,
     0,
     10,
     0,
     12,
     0,
     6,
     12,
     10,
     9,
     1,
     0,
     9,
     10,
     9,
     0,
     0,
     1
    ],
    "solution": [
     2,
     12,
     3,
     0,
     0,
     12,
     5,
     4,
     6,
     9,
     0,
     5,
     6,
     0,
     12,
     5,
     5,
     0,
     0,
     0,
     0,
     0,
     12,
     5,
     5,
     3,
     6,
     0,
     12,
     12,
     6,
     9,
     7,
     10,
     10,
     12,
     0,
     12,
     7,
     8,
     5,
     0,
     0,
     3,
     10,
     14,
     9,
     0,
     5,
     0,
     3,
     0,
     3,
     3,
     10,
     12,
     1,
     0,
     12,
     5,
     6,
     0,
     0,
     1
    ]
   },
   "robot": {
    "n": 6,
    "start": [
     5,
     0,
     1
    ],
    "goal": [
     5,
     0
    ],
    "samples": [
     [
      5,
      2
     ],
     [
      5,
      5
     ],
     [
      3,
      5
     ],
     [
      0,
      5
     ],
     [
      0,
      3
     ],
     [
      0,
      0
     ],
     [
      2,
      0
     ],
     [
      5,
      0
     ]
    ],
    "road": [
     [
      5,
      0
     ],
     [
      5,
      1
     ],
     [
      5,
      2
     ],
     [
      5,
      3
     ],
     [
      5,
      4
     ],
     [
      5,
      5
     ],
     [
      4,
      5
     ],
     [
      3,
      5
     ],
     [
      2,
      5
     ],
     [
      1,
      5
     ],
     [
      0,
      5
     ],
     [
      0,
      4
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      0
     ],
     [
      3,
      0
     ],
     [
      4,
      0
     ]
    ],
    "budget": 9
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8
     ],
     [
      6,
      3,
      11
     ],
     [
      9,
      10
     ],
     [
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q"
     ],
     "body": [
      "F",
      "F",
      "P",
      "F",
      "F",
      "F",
      "P",
      "I"
     ],
     "repeat": 4
    }
   }
  },
  "horizon": {
   "info": {
    "id": "horizon",
    "en": "Horizon logistics",
    "zh": "天际调度",
    "tag": [
     "Island master",
     "全岛总工程师"
    ],
    "description": [
     "Chapter 6: plan, test and revise. Every mission has an optional hint.",
     "第 6 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Horizon logistics",
      "天际调度"
     ],
     "power": [
      "Horizon current",
      "天际电流"
     ],
     "robot": [
      "Two surveys and a detour",
      "双巡查与绕行"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 5,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 2,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     },
     {
      "id": 10,
      "en": "Cable",
      "zh": "电缆",
      "weight": 2,
      "icon": "bolt"
     },
     {
      "id": 11,
      "en": "Antenna",
      "zh": "天线",
      "weight": 4,
      "icon": "sensor"
     }
    ],
    "capacity": 11,
    "maxTrips": 5,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ],
     [
      3,
      4
     ],
     [
      7,
      10
     ],
     [
      11,
      10
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ],
     [
      2,
      10
     ],
     [
      6,
      9
     ]
    ],
    "by": {
     "5": 1,
     "8": 2
    }
   },
   "power": {
    "n": 8,
    "source": 32,
    "targets": [
     0,
     7,
     63,
     56,
     39
    ],
    "fixed": [
     6,
     19,
     40,
     51
    ],
    "initial": [
     2,
     3,
     0,
     0,
     12,
     10,
     10,
     8,
     3,
     6,
     0,
     12,
     6,
     5,
     0,
     5,
     5,
     10,
     12,
     9,
     0,
     9,
     12,
     0,
     5,
     5,
     10,
     0,
     6,
     0,
     9,
     5,
     7,
     5,
     3,
     0,
     6,
     9,
     10,
     8,
     3,
     7,
     5,
     11,
     10,
     12,
     0,
     5,
     0,
     5,
     0,
     3,
     5,
     10,
     10,
     9,
     2,
     3,
     5,
     12,
     9,
     10,
     9,
     1
    ],
    "solution": [
     2,
     12,
     0,
     0,
     6,
     10,
     10,
     8,
     6,
     9,
     0,
     6,
     9,
     10,
     0,
     5,
     5,
     5,
     6,
     9,
     0,
     6,
     3,
     0,
     5,
     10,
     5,
     0,
     3,
     0,
     3,
     10,
     7,
     10,
     9,
     0,
     12,
     6,
     10,
     8,
     3,
     14,
     10,
     14,
     10,
     9,
     0,
     10,
     0,
     5,
     0,
     3,
     10,
     10,
     10,
     12,
     2,
     9,
     10,
     6,
     6,
     10,
     12,
     1
    ]
   },
   "robot": {
    "n": 9,
    "start": [
     2,
     0,
     1
    ],
    "goal": [
     1,
     7
    ],
    "samples": [
     [
      2,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      0
     ],
     [
      2,
      0
     ],
     [
      2,
      8
     ],
     [
      0,
      8
     ],
     [
      0,
      5
     ],
     [
      2,
      5
     ],
     [
      1,
      7
     ]
    ],
    "road": [
     [
      2,
      0
     ],
     [
      2,
      1
     ],
     [
      2,
      2
     ],
     [
      2,
      3
     ],
     [
      1,
      3
     ],
     [
      0,
      3
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      4
     ],
     [
      2,
      5
     ],
     [
      2,
      6
     ],
     [
      2,
      7
     ],
     [
      2,
      8
     ],
     [
      1,
      8
     ],
     [
      0,
      8
     ],
     [
      0,
      7
     ],
     [
      0,
      6
     ],
     [
      0,
      5
     ],
     [
      1,
      5
     ],
     [
      1,
      6
     ],
     [
      1,
      7
     ]
    ],
    "budget": 22
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8
     ],
     [
      6,
      3,
      11
     ],
     [
      9,
      10
     ],
     [
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "F",
      "F",
      "F",
      "F",
      "F",
      "Q",
      "L",
      "F",
      "R",
      "F",
      "F",
      "P"
     ],
     "body": [
      "F",
      "F",
      "F",
      "P",
      "L",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 2
    }
   }
  },
  "islandheart": {
   "info": {
    "id": "islandheart",
    "en": "Island lifeline",
    "zh": "全岛生命线",
    "tag": [
     "Island master",
     "全岛总工程师"
    ],
    "description": [
     "Chapter 6: plan, test and revise. Every mission has an optional hint.",
     "第 6 章：规划、测试、改进。每关都有可选提示。"
    ],
    "titles": {
     "cargo": [
      "Island lifeline",
      "全岛生命线"
     ],
     "power": [
      "Island power web",
      "全岛电网"
     ],
     "robot": [
      "The final sample",
      "最后的样本"
     ]
    }
   },
   "cargo": {
    "items": [
     {
      "id": 0,
      "en": "Crane",
      "zh": "起重机",
      "weight": 7,
      "icon": "crane"
     },
     {
      "id": 1,
      "en": "Beams",
      "zh": "木梁",
      "weight": 6,
      "icon": "beams"
     },
     {
      "id": 2,
      "en": "Battery",
      "zh": "电池",
      "weight": 4,
      "icon": "bolt"
     },
     {
      "id": 3,
      "en": "Water",
      "zh": "清水",
      "weight": 3,
      "icon": "drop"
     },
     {
      "id": 4,
      "en": "Seeds",
      "zh": "种子",
      "weight": 2,
      "icon": "leaf"
     },
     {
      "id": 5,
      "en": "Medicine",
      "zh": "药箱",
      "weight": 3,
      "icon": "medical"
     },
     {
      "id": 6,
      "en": "Solar panels",
      "zh": "太阳能板",
      "weight": 4,
      "icon": "spark"
     },
     {
      "id": 7,
      "en": "Tools",
      "zh": "工具箱",
      "weight": 1,
      "icon": "book"
     },
     {
      "id": 8,
      "en": "Pump",
      "zh": "水泵",
      "weight": 5,
      "icon": "sensor"
     },
     {
      "id": 9,
      "en": "Radio",
      "zh": "电台",
      "weight": 3,
      "icon": "bot"
     },
     {
      "id": 10,
      "en": "Cable",
      "zh": "电缆",
      "weight": 2,
      "icon": "bolt"
     },
     {
      "id": 11,
      "en": "Antenna",
      "zh": "天线",
      "weight": 4,
      "icon": "sensor"
     }
    ],
    "capacity": 11,
    "maxTrips": 5,
    "maxItems": 3,
    "before": [
     [
      0,
      1
     ],
     [
      0,
      4
     ],
     [
      1,
      6
     ],
     [
      7,
      8
     ],
     [
      8,
      3
     ],
     [
      1,
      3
     ],
     [
      6,
      9
     ],
     [
      3,
      4
     ],
     [
      7,
      10
     ],
     [
      11,
      10
     ],
     [
      3,
      10
     ],
     [
      10,
      4
     ],
     [
      6,
      2
     ]
    ],
    "apart": [
     [
      2,
      3
     ],
     [
      8,
      9
     ],
     [
      2,
      10
     ],
     [
      6,
      9
     ]
    ],
    "by": {
     "5": 1,
     "8": 2
    }
   },
   "power": {
    "n": 8,
    "source": 32,
    "targets": [
     0,
     7,
     63,
     56,
     39
    ],
    "fixed": [
     14,
     24,
     40,
     47
    ],
    "initial": [
     4,
     0,
     5,
     0,
     5,
     12,
     12,
     4,
     5,
     12,
     12,
     0,
     12,
     10,
     10,
     12,
     14,
     5,
     5,
     10,
     12,
     0,
     0,
     0,
     5,
     0,
     0,
     6,
     0,
     0,
     10,
     0,
     7,
     10,
     10,
     5,
     5,
     5,
     10,
     8,
     7,
     5,
     5,
     5,
     5,
     5,
     10,
     12,
     10,
     0,
     0,
     3,
     0,
     9,
     12,
     10,
     1,
     0,
     0,
     10,
     0,
     0,
     0,
     1
    ],
    "solution": [
     4,
     0,
     10,
     0,
     10,
     6,
     3,
     4,
     5,
     3,
     3,
     0,
     6,
     10,
     10,
     9,
     7,
     10,
     10,
     10,
     9,
     0,
     0,
     0,
     5,
     0,
     0,
     12,
     0,
     0,
     5,
     0,
     7,
     10,
     10,
     10,
     10,
     10,
     10,
     8,
     7,
     10,
     10,
     10,
     10,
     10,
     10,
     12,
     5,
     0,
     0,
     6,
     0,
     3,
     6,
     5,
     1,
     0,
     0,
     10,
     0,
     0,
     0,
     1
    ]
   },
   "robot": {
    "n": 7,
    "start": [
     3,
     0,
     1
    ],
    "goal": [
     1,
     5
    ],
    "samples": [
     [
      3,
      2
     ],
     [
      0,
      2
     ],
     [
      0,
      0
     ],
     [
      3,
      0
     ],
     [
      3,
      6
     ],
     [
      0,
      6
     ],
     [
      0,
      4
     ],
     [
      3,
      4
     ],
     [
      1,
      5
     ]
    ],
    "road": [
     [
      3,
      0
     ],
     [
      3,
      1
     ],
     [
      3,
      2
     ],
     [
      2,
      2
     ],
     [
      1,
      2
     ],
     [
      0,
      2
     ],
     [
      0,
      1
     ],
     [
      0,
      0
     ],
     [
      1,
      0
     ],
     [
      2,
      0
     ],
     [
      3,
      3
     ],
     [
      3,
      4
     ],
     [
      3,
      5
     ],
     [
      3,
      6
     ],
     [
      2,
      6
     ],
     [
      1,
      6
     ],
     [
      0,
      6
     ],
     [
      0,
      5
     ],
     [
      0,
      4
     ],
     [
      1,
      4
     ],
     [
      2,
      4
     ],
     [
      1,
      5
     ]
    ],
    "budget": 21
   },
   "hints": {
    "cargo": [
     [
      0,
      7,
      5
     ],
     [
      1,
      8
     ],
     [
      6,
      3,
      11
     ],
     [
      9,
      10
     ],
     [
      4,
      2
     ]
    ],
    "robot": {
     "main": [
      "Q",
      "F",
      "F",
      "F",
      "F",
      "Q",
      "L",
      "F",
      "F",
      "R",
      "F",
      "P"
     ],
     "body": [
      "F",
      "F",
      "P",
      "L",
      "F",
      "F",
      "F",
      "P",
      "L"
     ],
     "repeat": 2
    }
   }
  }
 }
};
root.QuestContent=data;if(typeof module!=='undefined'&&module.exports)module.exports=data;
})(typeof window!=='undefined'?window:globalThis);
