
/* ─── DN INTOCÁVEIS × GRUPO PROVEDOR ────────────────────────────────────────
   Gerado por calcula_dn_intoc_grupos.py  v2
   Fonte: vendas por EAN novo.xlsx
   FYTD25 = Jul/2024–Mar/2025 | FYTD26 = Jul/2025–Mar/2026
   total  = PDVs ativos no período (qualquer produto com venda > 0)
   pdvs   = PDVs que venderam o SKU Intocável no período
   dn     = pdvs / total × 100
────────────────────────────────────────────────────────────────────────────── */
const DN_INTOC_GRUPOS = {
  "ARAUJO": {
    "fytd25": {
      "soma": {
        "total": 363,
        "algum": 338,
        "dnAlgum": 93.1,
        "dois": 338,
        "dnDois": 93.1,
        "todos": 52,
        "dnTodos": 14.3
      },
      "kids200": {
        "total": 363,
        "pdvs": 338,
        "dn": 93.1
      },
      "spray170": {
        "total": 363,
        "pdvs": 52,
        "dn": 14.3
      },
      "locao200": {
        "total": 363,
        "pdvs": 338,
        "dn": 93.1
      }
    },
    "fytd26": {
      "soma": {
        "total": 363,
        "algum": 360,
        "dnAlgum": 99.2,
        "dois": 360,
        "dnDois": 99.2,
        "todos": 358,
        "dnTodos": 98.6
      },
      "kids200": {
        "total": 363,
        "pdvs": 359,
        "dn": 98.9
      },
      "spray170": {
        "total": 363,
        "pdvs": 358,
        "dn": 98.6
      },
      "locao200": {
        "total": 363,
        "pdvs": 360,
        "dn": 99.2
      }
    },
    "janabr25": {
      "soma": {
        "total": 363,
        "algum": 337,
        "dnAlgum": 92.8,
        "dois": 337,
        "dnDois": 92.8,
        "todos": 335,
        "dnTodos": 92.3
      },
      "kids200": {
        "total": 363,
        "pdvs": 337,
        "dn": 92.8
      },
      "spray170": {
        "total": 363,
        "pdvs": 335,
        "dn": 92.3
      },
      "locao200": {
        "total": 363,
        "pdvs": 337,
        "dn": 92.8
      }
    },
    "janabr26": {
      "soma": {
        "total": 363,
        "algum": 358,
        "dnAlgum": 98.6,
        "dois": 358,
        "dnDois": 98.6,
        "todos": 357,
        "dnTodos": 98.3
      },
      "kids200": {
        "total": 363,
        "pdvs": 357,
        "dn": 98.3
      },
      "spray170": {
        "total": 363,
        "pdvs": 358,
        "dn": 98.6
      },
      "locao200": {
        "total": 363,
        "pdvs": 357,
        "dn": 98.3
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 363,
          "algum": 345,
          "dnAlgum": 95.0,
          "dois": 345,
          "dnDois": 95.0,
          "todos": 343,
          "dnTodos": 94.5
        },
        "kids200": {
          "total": 363,
          "pdvs": 345,
          "dn": 95.0
        },
        "spray170": {
          "total": 363,
          "pdvs": 343,
          "dn": 94.5
        },
        "locao200": {
          "total": 363,
          "pdvs": 345,
          "dn": 95.0
        }
      },
      "202508": {
        "soma": {
          "total": 363,
          "algum": 347,
          "dnAlgum": 95.6,
          "dois": 347,
          "dnDois": 95.6,
          "todos": 345,
          "dnTodos": 95.0
        },
        "kids200": {
          "total": 363,
          "pdvs": 347,
          "dn": 95.6
        },
        "spray170": {
          "total": 363,
          "pdvs": 345,
          "dn": 95.0
        },
        "locao200": {
          "total": 363,
          "pdvs": 347,
          "dn": 95.6
        }
      },
      "202509": {
        "soma": {
          "total": 363,
          "algum": 348,
          "dnAlgum": 95.9,
          "dois": 348,
          "dnDois": 95.9,
          "todos": 346,
          "dnTodos": 95.3
        },
        "kids200": {
          "total": 363,
          "pdvs": 348,
          "dn": 95.9
        },
        "spray170": {
          "total": 363,
          "pdvs": 346,
          "dn": 95.3
        },
        "locao200": {
          "total": 363,
          "pdvs": 348,
          "dn": 95.9
        }
      },
      "202510": {
        "soma": {
          "total": 363,
          "algum": 352,
          "dnAlgum": 97.0,
          "dois": 352,
          "dnDois": 97.0,
          "todos": 350,
          "dnTodos": 96.4
        },
        "kids200": {
          "total": 363,
          "pdvs": 352,
          "dn": 97.0
        },
        "spray170": {
          "total": 363,
          "pdvs": 350,
          "dn": 96.4
        },
        "locao200": {
          "total": 363,
          "pdvs": 352,
          "dn": 97.0
        }
      },
      "202511": {
        "soma": {
          "total": 363,
          "algum": 355,
          "dnAlgum": 97.8,
          "dois": 355,
          "dnDois": 97.8,
          "todos": 353,
          "dnTodos": 97.2
        },
        "kids200": {
          "total": 363,
          "pdvs": 355,
          "dn": 97.8
        },
        "spray170": {
          "total": 363,
          "pdvs": 353,
          "dn": 97.2
        },
        "locao200": {
          "total": 363,
          "pdvs": 355,
          "dn": 97.8
        }
      },
      "202512": {
        "soma": {
          "total": 363,
          "algum": 358,
          "dnAlgum": 98.6,
          "dois": 358,
          "dnDois": 98.6,
          "todos": 356,
          "dnTodos": 98.1
        },
        "kids200": {
          "total": 363,
          "pdvs": 358,
          "dn": 98.6
        },
        "spray170": {
          "total": 363,
          "pdvs": 356,
          "dn": 98.1
        },
        "locao200": {
          "total": 363,
          "pdvs": 358,
          "dn": 98.6
        }
      },
      "202601": {
        "soma": {
          "total": 363,
          "algum": 359,
          "dnAlgum": 98.9,
          "dois": 359,
          "dnDois": 98.9,
          "todos": 357,
          "dnTodos": 98.3
        },
        "kids200": {
          "total": 363,
          "pdvs": 359,
          "dn": 98.9
        },
        "spray170": {
          "total": 363,
          "pdvs": 357,
          "dn": 98.3
        },
        "locao200": {
          "total": 363,
          "pdvs": 359,
          "dn": 98.9
        }
      },
      "202602": {
        "soma": {
          "total": 363,
          "algum": 359,
          "dnAlgum": 98.9,
          "dois": 359,
          "dnDois": 98.9,
          "todos": 357,
          "dnTodos": 98.3
        },
        "kids200": {
          "total": 363,
          "pdvs": 359,
          "dn": 98.9
        },
        "spray170": {
          "total": 363,
          "pdvs": 357,
          "dn": 98.3
        },
        "locao200": {
          "total": 363,
          "pdvs": 359,
          "dn": 98.9
        }
      },
      "202603": {
        "soma": {
          "total": 363,
          "algum": 360,
          "dnAlgum": 99.2,
          "dois": 360,
          "dnDois": 99.2,
          "todos": 358,
          "dnTodos": 98.6
        },
        "kids200": {
          "total": 363,
          "pdvs": 360,
          "dn": 99.2
        },
        "spray170": {
          "total": 363,
          "pdvs": 358,
          "dn": 98.6
        },
        "locao200": {
          "total": 363,
          "pdvs": 360,
          "dn": 99.2
        }
      },
      "202604": {
        "soma": {
          "total": 363,
          "algum": 360,
          "dnAlgum": 99.2,
          "dois": 360,
          "dnDois": 99.2,
          "todos": 358,
          "dnTodos": 98.6
        },
        "kids200": {
          "total": 363,
          "pdvs": 360,
          "dn": 99.2
        },
        "spray170": {
          "total": 363,
          "pdvs": 358,
          "dn": 98.6
        },
        "locao200": {
          "total": 363,
          "pdvs": 360,
          "dn": 99.2
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 368,
          "pdvs": 305,
          "dn": 82.9
        },
        "locao200": {
          "total": 368,
          "pdvs": 322,
          "dn": 87.5
        },
        "spray170": {
          "total": 368,
          "pdvs": 257,
          "dn": 69.8
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 369,
        "pdvs": 330,
        "dn": 89.4
      },
      "locao200": {
        "total": 369,
        "pdvs": 353,
        "dn": 95.7
      },
      "spray170": {
        "total": 369,
        "pdvs": 318,
        "dn": 86.2
      }
    }
  },
  "DROGAL": {
    "fytd25": {
      "soma": {
        "total": 454,
        "algum": 403,
        "dnAlgum": 88.8,
        "dois": 403,
        "dnDois": 88.8,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 454,
        "pdvs": 403,
        "dn": 88.8
      },
      "spray170": {
        "total": 454,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 454,
        "pdvs": 403,
        "dn": 88.8
      }
    },
    "fytd26": {
      "soma": {
        "total": 454,
        "algum": 454,
        "dnAlgum": 100.0,
        "dois": 454,
        "dnDois": 100.0,
        "todos": 454,
        "dnTodos": 100.0
      },
      "kids200": {
        "total": 454,
        "pdvs": 454,
        "dn": 100.0
      },
      "spray170": {
        "total": 454,
        "pdvs": 454,
        "dn": 100.0
      },
      "locao200": {
        "total": 454,
        "pdvs": 454,
        "dn": 100.0
      }
    },
    "janabr25": {
      "soma": {
        "total": 454,
        "algum": 396,
        "dnAlgum": 87.2,
        "dois": 396,
        "dnDois": 87.2,
        "todos": 396,
        "dnTodos": 87.2
      },
      "kids200": {
        "total": 454,
        "pdvs": 396,
        "dn": 87.2
      },
      "spray170": {
        "total": 454,
        "pdvs": 396,
        "dn": 87.2
      },
      "locao200": {
        "total": 454,
        "pdvs": 396,
        "dn": 87.2
      }
    },
    "janabr26": {
      "soma": {
        "total": 454,
        "algum": 454,
        "dnAlgum": 100.0,
        "dois": 454,
        "dnDois": 100.0,
        "todos": 454,
        "dnTodos": 100.0
      },
      "kids200": {
        "total": 454,
        "pdvs": 454,
        "dn": 100.0
      },
      "spray170": {
        "total": 454,
        "pdvs": 454,
        "dn": 100.0
      },
      "locao200": {
        "total": 454,
        "pdvs": 454,
        "dn": 100.0
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 454,
          "algum": 418,
          "dnAlgum": 92.1,
          "dois": 418,
          "dnDois": 92.1,
          "todos": 418,
          "dnTodos": 92.1
        },
        "kids200": {
          "total": 454,
          "pdvs": 418,
          "dn": 92.1
        },
        "spray170": {
          "total": 454,
          "pdvs": 418,
          "dn": 92.1
        },
        "locao200": {
          "total": 454,
          "pdvs": 418,
          "dn": 92.1
        }
      },
      "202508": {
        "soma": {
          "total": 454,
          "algum": 421,
          "dnAlgum": 92.7,
          "dois": 421,
          "dnDois": 92.7,
          "todos": 421,
          "dnTodos": 92.7
        },
        "kids200": {
          "total": 454,
          "pdvs": 421,
          "dn": 92.7
        },
        "spray170": {
          "total": 454,
          "pdvs": 421,
          "dn": 92.7
        },
        "locao200": {
          "total": 454,
          "pdvs": 421,
          "dn": 92.7
        }
      },
      "202509": {
        "soma": {
          "total": 454,
          "algum": 428,
          "dnAlgum": 94.3,
          "dois": 428,
          "dnDois": 94.3,
          "todos": 428,
          "dnTodos": 94.3
        },
        "kids200": {
          "total": 454,
          "pdvs": 428,
          "dn": 94.3
        },
        "spray170": {
          "total": 454,
          "pdvs": 428,
          "dn": 94.3
        },
        "locao200": {
          "total": 454,
          "pdvs": 428,
          "dn": 94.3
        }
      },
      "202510": {
        "soma": {
          "total": 454,
          "algum": 432,
          "dnAlgum": 95.2,
          "dois": 432,
          "dnDois": 95.2,
          "todos": 432,
          "dnTodos": 95.2
        },
        "kids200": {
          "total": 454,
          "pdvs": 432,
          "dn": 95.2
        },
        "spray170": {
          "total": 454,
          "pdvs": 432,
          "dn": 95.2
        },
        "locao200": {
          "total": 454,
          "pdvs": 432,
          "dn": 95.2
        }
      },
      "202511": {
        "soma": {
          "total": 454,
          "algum": 434,
          "dnAlgum": 95.6,
          "dois": 434,
          "dnDois": 95.6,
          "todos": 434,
          "dnTodos": 95.6
        },
        "kids200": {
          "total": 454,
          "pdvs": 434,
          "dn": 95.6
        },
        "spray170": {
          "total": 454,
          "pdvs": 434,
          "dn": 95.6
        },
        "locao200": {
          "total": 454,
          "pdvs": 434,
          "dn": 95.6
        }
      },
      "202512": {
        "soma": {
          "total": 454,
          "algum": 443,
          "dnAlgum": 97.6,
          "dois": 443,
          "dnDois": 97.6,
          "todos": 443,
          "dnTodos": 97.6
        },
        "kids200": {
          "total": 454,
          "pdvs": 443,
          "dn": 97.6
        },
        "spray170": {
          "total": 454,
          "pdvs": 443,
          "dn": 97.6
        },
        "locao200": {
          "total": 454,
          "pdvs": 443,
          "dn": 97.6
        }
      },
      "202601": {
        "soma": {
          "total": 454,
          "algum": 444,
          "dnAlgum": 97.8,
          "dois": 444,
          "dnDois": 97.8,
          "todos": 444,
          "dnTodos": 97.8
        },
        "kids200": {
          "total": 454,
          "pdvs": 444,
          "dn": 97.8
        },
        "spray170": {
          "total": 454,
          "pdvs": 444,
          "dn": 97.8
        },
        "locao200": {
          "total": 454,
          "pdvs": 444,
          "dn": 97.8
        }
      },
      "202602": {
        "soma": {
          "total": 454,
          "algum": 449,
          "dnAlgum": 98.9,
          "dois": 449,
          "dnDois": 98.9,
          "todos": 449,
          "dnTodos": 98.9
        },
        "kids200": {
          "total": 454,
          "pdvs": 449,
          "dn": 98.9
        },
        "spray170": {
          "total": 454,
          "pdvs": 449,
          "dn": 98.9
        },
        "locao200": {
          "total": 454,
          "pdvs": 449,
          "dn": 98.9
        }
      },
      "202603": {
        "soma": {
          "total": 454,
          "algum": 454,
          "dnAlgum": 100.0,
          "dois": 454,
          "dnDois": 100.0,
          "todos": 454,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 454,
          "pdvs": 454,
          "dn": 100.0
        },
        "spray170": {
          "total": 454,
          "pdvs": 454,
          "dn": 100.0
        },
        "locao200": {
          "total": 454,
          "pdvs": 454,
          "dn": 100.0
        }
      },
      "202604": {
        "soma": {
          "total": 454,
          "algum": 454,
          "dnAlgum": 100.0,
          "dois": 454,
          "dnDois": 100.0,
          "todos": 454,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 454,
          "pdvs": 454,
          "dn": 100.0
        },
        "spray170": {
          "total": 454,
          "pdvs": 454,
          "dn": 100.0
        },
        "locao200": {
          "total": 454,
          "pdvs": 454,
          "dn": 100.0
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 469,
          "pdvs": 393,
          "dn": 83.8
        },
        "locao200": {
          "total": 469,
          "pdvs": 388,
          "dn": 82.7
        },
        "spray170": {
          "total": 469,
          "pdvs": 393,
          "dn": 83.8
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 469,
        "pdvs": 421,
        "dn": 89.8
      },
      "locao200": {
        "total": 469,
        "pdvs": 428,
        "dn": 91.3
      },
      "spray170": {
        "total": 469,
        "pdvs": 429,
        "dn": 91.5
      }
    }
  },
  "DROGARIA CATARINENSE": {
    "fytd25": {
      "soma": {
        "total": 77,
        "algum": 68,
        "dnAlgum": 88.3,
        "dois": 68,
        "dnDois": 88.3,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 77,
        "pdvs": 68,
        "dn": 88.3
      },
      "spray170": {
        "total": 77,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 77,
        "pdvs": 68,
        "dn": 88.3
      }
    },
    "fytd26": {
      "soma": {
        "total": 77,
        "algum": 77,
        "dnAlgum": 100.0,
        "dois": 77,
        "dnDois": 100.0,
        "todos": 75,
        "dnTodos": 97.4
      },
      "kids200": {
        "total": 77,
        "pdvs": 77,
        "dn": 100.0
      },
      "spray170": {
        "total": 77,
        "pdvs": 75,
        "dn": 97.4
      },
      "locao200": {
        "total": 77,
        "pdvs": 77,
        "dn": 100.0
      }
    },
    "janabr25": {
      "soma": {
        "total": 77,
        "algum": 68,
        "dnAlgum": 88.3,
        "dois": 68,
        "dnDois": 88.3,
        "todos": 66,
        "dnTodos": 85.7
      },
      "kids200": {
        "total": 77,
        "pdvs": 68,
        "dn": 88.3
      },
      "spray170": {
        "total": 77,
        "pdvs": 66,
        "dn": 85.7
      },
      "locao200": {
        "total": 77,
        "pdvs": 68,
        "dn": 88.3
      }
    },
    "janabr26": {
      "soma": {
        "total": 77,
        "algum": 75,
        "dnAlgum": 97.4,
        "dois": 75,
        "dnDois": 97.4,
        "todos": 75,
        "dnTodos": 97.4
      },
      "kids200": {
        "total": 77,
        "pdvs": 75,
        "dn": 97.4
      },
      "spray170": {
        "total": 77,
        "pdvs": 75,
        "dn": 97.4
      },
      "locao200": {
        "total": 77,
        "pdvs": 75,
        "dn": 97.4
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 77,
          "algum": 4,
          "dnAlgum": 5.2,
          "dois": 4,
          "dnDois": 5.2,
          "todos": 4,
          "dnTodos": 5.2
        },
        "kids200": {
          "total": 77,
          "pdvs": 4,
          "dn": 5.2
        },
        "spray170": {
          "total": 77,
          "pdvs": 4,
          "dn": 5.2
        },
        "locao200": {
          "total": 77,
          "pdvs": 4,
          "dn": 5.2
        }
      },
      "202508": {
        "soma": {
          "total": 77,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 77,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 77,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 77,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 76,
          "algum": 46,
          "dnAlgum": 60.5,
          "dois": 46,
          "dnDois": 60.5,
          "todos": 33,
          "dnTodos": 43.4
        },
        "kids200": {
          "total": 76,
          "pdvs": 46,
          "dn": 60.5
        },
        "spray170": {
          "total": 76,
          "pdvs": 36,
          "dn": 47.4
        },
        "locao200": {
          "total": 76,
          "pdvs": 33,
          "dn": 43.4
        }
      },
      "202510": {
        "soma": {
          "total": 76,
          "algum": 58,
          "dnAlgum": 76.3,
          "dois": 58,
          "dnDois": 76.3,
          "todos": 40,
          "dnTodos": 52.6
        },
        "kids200": {
          "total": 76,
          "pdvs": 58,
          "dn": 76.3
        },
        "spray170": {
          "total": 76,
          "pdvs": 40,
          "dn": 52.6
        },
        "locao200": {
          "total": 76,
          "pdvs": 44,
          "dn": 57.9
        }
      },
      "202511": {
        "soma": {
          "total": 76,
          "algum": 60,
          "dnAlgum": 78.9,
          "dois": 60,
          "dnDois": 78.9,
          "todos": 51,
          "dnTodos": 67.1
        },
        "kids200": {
          "total": 76,
          "pdvs": 60,
          "dn": 78.9
        },
        "spray170": {
          "total": 76,
          "pdvs": 51,
          "dn": 67.1
        },
        "locao200": {
          "total": 76,
          "pdvs": 55,
          "dn": 72.4
        }
      },
      "202512": {
        "soma": {
          "total": 76,
          "algum": 72,
          "dnAlgum": 94.7,
          "dois": 72,
          "dnDois": 94.7,
          "todos": 66,
          "dnTodos": 86.8
        },
        "kids200": {
          "total": 76,
          "pdvs": 72,
          "dn": 94.7
        },
        "spray170": {
          "total": 76,
          "pdvs": 66,
          "dn": 86.8
        },
        "locao200": {
          "total": 76,
          "pdvs": 68,
          "dn": 89.5
        }
      },
      "202601": {
        "soma": {
          "total": 76,
          "algum": 75,
          "dnAlgum": 98.7,
          "dois": 75,
          "dnDois": 98.7,
          "todos": 70,
          "dnTodos": 92.1
        },
        "kids200": {
          "total": 76,
          "pdvs": 75,
          "dn": 98.7
        },
        "spray170": {
          "total": 76,
          "pdvs": 70,
          "dn": 92.1
        },
        "locao200": {
          "total": 76,
          "pdvs": 70,
          "dn": 92.1
        }
      },
      "202602": {
        "soma": {
          "total": 76,
          "algum": 73,
          "dnAlgum": 96.1,
          "dois": 73,
          "dnDois": 96.1,
          "todos": 68,
          "dnTodos": 89.5
        },
        "kids200": {
          "total": 76,
          "pdvs": 73,
          "dn": 96.1
        },
        "spray170": {
          "total": 76,
          "pdvs": 68,
          "dn": 89.5
        },
        "locao200": {
          "total": 76,
          "pdvs": 68,
          "dn": 89.5
        }
      },
      "202603": {
        "soma": {
          "total": 76,
          "algum": 70,
          "dnAlgum": 92.1,
          "dois": 70,
          "dnDois": 92.1,
          "todos": 63,
          "dnTodos": 82.9
        },
        "kids200": {
          "total": 76,
          "pdvs": 70,
          "dn": 92.1
        },
        "spray170": {
          "total": 76,
          "pdvs": 66,
          "dn": 86.8
        },
        "locao200": {
          "total": 76,
          "pdvs": 63,
          "dn": 82.9
        }
      },
      "202604": {
        "soma": {
          "total": 76,
          "algum": 76,
          "dnAlgum": 100.0,
          "dois": 76,
          "dnDois": 100.0,
          "todos": 73,
          "dnTodos": 96.1
        },
        "kids200": {
          "total": 76,
          "pdvs": 76,
          "dn": 100.0
        },
        "spray170": {
          "total": 76,
          "pdvs": 73,
          "dn": 96.1
        },
        "locao200": {
          "total": 76,
          "pdvs": 76,
          "dn": 100.0
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 77,
          "pdvs": 27,
          "dn": 35.1
        },
        "locao200": {
          "total": 77,
          "pdvs": 43,
          "dn": 55.8
        },
        "spray170": {
          "total": 77,
          "pdvs": 36,
          "dn": 46.8
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 77,
        "pdvs": 35,
        "dn": 45.5
      },
      "locao200": {
        "total": 77,
        "pdvs": 53,
        "dn": 68.8
      },
      "spray170": {
        "total": 77,
        "pdvs": 45,
        "dn": 58.4
      }
    }
  },
  "DROGARIA GLOBO": {
    "fytd25": {
      "soma": {
        "total": 146,
        "algum": 145,
        "dnAlgum": 99.3,
        "dois": 145,
        "dnDois": 99.3,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 146,
        "pdvs": 145,
        "dn": 99.3
      },
      "spray170": {
        "total": 146,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 146,
        "pdvs": 145,
        "dn": 99.3
      }
    },
    "fytd26": {
      "soma": {
        "total": 146,
        "algum": 146,
        "dnAlgum": 100.0,
        "dois": 146,
        "dnDois": 100.0,
        "todos": 144,
        "dnTodos": 98.6
      },
      "kids200": {
        "total": 146,
        "pdvs": 146,
        "dn": 100.0
      },
      "spray170": {
        "total": 146,
        "pdvs": 144,
        "dn": 98.6
      },
      "locao200": {
        "total": 146,
        "pdvs": 144,
        "dn": 98.6
      }
    },
    "janabr25": {
      "soma": {
        "total": 146,
        "algum": 144,
        "dnAlgum": 98.6,
        "dois": 144,
        "dnDois": 98.6,
        "todos": 144,
        "dnTodos": 98.6
      },
      "kids200": {
        "total": 146,
        "pdvs": 144,
        "dn": 98.6
      },
      "spray170": {
        "total": 146,
        "pdvs": 144,
        "dn": 98.6
      },
      "locao200": {
        "total": 146,
        "pdvs": 144,
        "dn": 98.6
      }
    },
    "janabr26": {
      "soma": {
        "total": 146,
        "algum": 144,
        "dnAlgum": 98.6,
        "dois": 144,
        "dnDois": 98.6,
        "todos": 143,
        "dnTodos": 97.9
      },
      "kids200": {
        "total": 146,
        "pdvs": 143,
        "dn": 97.9
      },
      "spray170": {
        "total": 146,
        "pdvs": 144,
        "dn": 98.6
      },
      "locao200": {
        "total": 146,
        "pdvs": 143,
        "dn": 97.9
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 146,
          "algum": 81,
          "dnAlgum": 55.5,
          "dois": 81,
          "dnDois": 55.5,
          "todos": 81,
          "dnTodos": 55.5
        },
        "kids200": {
          "total": 146,
          "pdvs": 81,
          "dn": 55.5
        },
        "spray170": {
          "total": 146,
          "pdvs": 81,
          "dn": 55.5
        },
        "locao200": {
          "total": 146,
          "pdvs": 81,
          "dn": 55.5
        }
      },
      "202508": {
        "soma": {
          "total": 146,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 146,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 146,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 146,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 146,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 146,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 146,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 146,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202510": {
        "soma": {
          "total": 146,
          "algum": 1,
          "dnAlgum": 0.7,
          "dois": 1,
          "dnDois": 0.7,
          "todos": 1,
          "dnTodos": 0.7
        },
        "kids200": {
          "total": 146,
          "pdvs": 1,
          "dn": 0.7
        },
        "spray170": {
          "total": 146,
          "pdvs": 1,
          "dn": 0.7
        },
        "locao200": {
          "total": 146,
          "pdvs": 1,
          "dn": 0.7
        }
      },
      "202511": {
        "soma": {
          "total": 146,
          "algum": 5,
          "dnAlgum": 3.4,
          "dois": 5,
          "dnDois": 3.4,
          "todos": 5,
          "dnTodos": 3.4
        },
        "kids200": {
          "total": 146,
          "pdvs": 5,
          "dn": 3.4
        },
        "spray170": {
          "total": 146,
          "pdvs": 5,
          "dn": 3.4
        },
        "locao200": {
          "total": 146,
          "pdvs": 5,
          "dn": 3.4
        }
      },
      "202512": {
        "soma": {
          "total": 146,
          "algum": 7,
          "dnAlgum": 4.8,
          "dois": 7,
          "dnDois": 4.8,
          "todos": 7,
          "dnTodos": 4.8
        },
        "kids200": {
          "total": 146,
          "pdvs": 7,
          "dn": 4.8
        },
        "spray170": {
          "total": 146,
          "pdvs": 7,
          "dn": 4.8
        },
        "locao200": {
          "total": 146,
          "pdvs": 7,
          "dn": 4.8
        }
      },
      "202601": {
        "soma": {
          "total": 146,
          "algum": 8,
          "dnAlgum": 5.5,
          "dois": 8,
          "dnDois": 5.5,
          "todos": 8,
          "dnTodos": 5.5
        },
        "kids200": {
          "total": 146,
          "pdvs": 8,
          "dn": 5.5
        },
        "spray170": {
          "total": 146,
          "pdvs": 8,
          "dn": 5.5
        },
        "locao200": {
          "total": 146,
          "pdvs": 8,
          "dn": 5.5
        }
      },
      "202602": {
        "soma": {
          "total": 146,
          "algum": 143,
          "dnAlgum": 97.9,
          "dois": 143,
          "dnDois": 97.9,
          "todos": 143,
          "dnTodos": 97.9
        },
        "kids200": {
          "total": 146,
          "pdvs": 143,
          "dn": 97.9
        },
        "spray170": {
          "total": 146,
          "pdvs": 143,
          "dn": 97.9
        },
        "locao200": {
          "total": 146,
          "pdvs": 143,
          "dn": 97.9
        }
      },
      "202603": {
        "soma": {
          "total": 146,
          "algum": 143,
          "dnAlgum": 97.9,
          "dois": 143,
          "dnDois": 97.9,
          "todos": 143,
          "dnTodos": 97.9
        },
        "kids200": {
          "total": 146,
          "pdvs": 143,
          "dn": 97.9
        },
        "spray170": {
          "total": 146,
          "pdvs": 143,
          "dn": 97.9
        },
        "locao200": {
          "total": 146,
          "pdvs": 143,
          "dn": 97.9
        }
      },
      "202604": {
        "soma": {
          "total": 146,
          "algum": 143,
          "dnAlgum": 97.9,
          "dois": 143,
          "dnDois": 97.9,
          "todos": 143,
          "dnTodos": 97.9
        },
        "kids200": {
          "total": 146,
          "pdvs": 143,
          "dn": 97.9
        },
        "spray170": {
          "total": 146,
          "pdvs": 143,
          "dn": 97.9
        },
        "locao200": {
          "total": 146,
          "pdvs": 143,
          "dn": 97.9
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 142,
          "pdvs": 106,
          "dn": 74.6
        },
        "locao200": {
          "total": 142,
          "pdvs": 123,
          "dn": 86.6
        },
        "spray170": {
          "total": 142,
          "pdvs": 100,
          "dn": 70.4
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 142,
        "pdvs": 132,
        "dn": 93.0
      },
      "locao200": {
        "total": 142,
        "pdvs": 139,
        "dn": 97.9
      },
      "spray170": {
        "total": 142,
        "pdvs": 132,
        "dn": 93.0
      }
    }
  },
  "DROGARIA ROSARIO": {
    "fytd25": {
      "soma": {
        "total": 104,
        "algum": 92,
        "dnAlgum": 88.5,
        "dois": 92,
        "dnDois": 88.5,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 104,
        "pdvs": 92,
        "dn": 88.5
      },
      "spray170": {
        "total": 104,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 104,
        "pdvs": 92,
        "dn": 88.5
      }
    },
    "fytd26": {
      "soma": {
        "total": 104,
        "algum": 104,
        "dnAlgum": 100.0,
        "dois": 104,
        "dnDois": 100.0,
        "todos": 101,
        "dnTodos": 97.1
      },
      "kids200": {
        "total": 104,
        "pdvs": 103,
        "dn": 99.0
      },
      "spray170": {
        "total": 104,
        "pdvs": 104,
        "dn": 100.0
      },
      "locao200": {
        "total": 104,
        "pdvs": 101,
        "dn": 97.1
      }
    },
    "janabr25": {
      "soma": {
        "total": 104,
        "algum": 93,
        "dnAlgum": 89.4,
        "dois": 93,
        "dnDois": 89.4,
        "todos": 90,
        "dnTodos": 86.5
      },
      "kids200": {
        "total": 104,
        "pdvs": 90,
        "dn": 86.5
      },
      "spray170": {
        "total": 104,
        "pdvs": 93,
        "dn": 89.4
      },
      "locao200": {
        "total": 104,
        "pdvs": 90,
        "dn": 86.5
      }
    },
    "janabr26": {
      "soma": {
        "total": 104,
        "algum": 104,
        "dnAlgum": 100.0,
        "dois": 104,
        "dnDois": 100.0,
        "todos": 101,
        "dnTodos": 97.1
      },
      "kids200": {
        "total": 104,
        "pdvs": 101,
        "dn": 97.1
      },
      "spray170": {
        "total": 104,
        "pdvs": 104,
        "dn": 100.0
      },
      "locao200": {
        "total": 104,
        "pdvs": 101,
        "dn": 97.1
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 104,
          "algum": 20,
          "dnAlgum": 19.2,
          "dois": 20,
          "dnDois": 19.2,
          "todos": 19,
          "dnTodos": 18.3
        },
        "kids200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        },
        "spray170": {
          "total": 104,
          "pdvs": 20,
          "dn": 19.2
        },
        "locao200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        }
      },
      "202508": {
        "soma": {
          "total": 104,
          "algum": 20,
          "dnAlgum": 19.2,
          "dois": 20,
          "dnDois": 19.2,
          "todos": 19,
          "dnTodos": 18.3
        },
        "kids200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        },
        "spray170": {
          "total": 104,
          "pdvs": 20,
          "dn": 19.2
        },
        "locao200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        }
      },
      "202509": {
        "soma": {
          "total": 104,
          "algum": 20,
          "dnAlgum": 19.2,
          "dois": 20,
          "dnDois": 19.2,
          "todos": 19,
          "dnTodos": 18.3
        },
        "kids200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        },
        "spray170": {
          "total": 104,
          "pdvs": 20,
          "dn": 19.2
        },
        "locao200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        }
      },
      "202510": {
        "soma": {
          "total": 104,
          "algum": 20,
          "dnAlgum": 19.2,
          "dois": 20,
          "dnDois": 19.2,
          "todos": 19,
          "dnTodos": 18.3
        },
        "kids200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        },
        "spray170": {
          "total": 104,
          "pdvs": 20,
          "dn": 19.2
        },
        "locao200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        }
      },
      "202511": {
        "soma": {
          "total": 104,
          "algum": 20,
          "dnAlgum": 19.2,
          "dois": 20,
          "dnDois": 19.2,
          "todos": 19,
          "dnTodos": 18.3
        },
        "kids200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        },
        "spray170": {
          "total": 104,
          "pdvs": 20,
          "dn": 19.2
        },
        "locao200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        }
      },
      "202512": {
        "soma": {
          "total": 104,
          "algum": 20,
          "dnAlgum": 19.2,
          "dois": 20,
          "dnDois": 19.2,
          "todos": 19,
          "dnTodos": 18.3
        },
        "kids200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        },
        "spray170": {
          "total": 104,
          "pdvs": 20,
          "dn": 19.2
        },
        "locao200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        }
      },
      "202601": {
        "soma": {
          "total": 104,
          "algum": 20,
          "dnAlgum": 19.2,
          "dois": 20,
          "dnDois": 19.2,
          "todos": 19,
          "dnTodos": 18.3
        },
        "kids200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        },
        "spray170": {
          "total": 104,
          "pdvs": 20,
          "dn": 19.2
        },
        "locao200": {
          "total": 104,
          "pdvs": 19,
          "dn": 18.3
        }
      },
      "202602": {
        "soma": {
          "total": 104,
          "algum": 16,
          "dnAlgum": 15.4,
          "dois": 16,
          "dnDois": 15.4,
          "todos": 16,
          "dnTodos": 15.4
        },
        "kids200": {
          "total": 104,
          "pdvs": 16,
          "dn": 15.4
        },
        "spray170": {
          "total": 104,
          "pdvs": 16,
          "dn": 15.4
        },
        "locao200": {
          "total": 104,
          "pdvs": 16,
          "dn": 15.4
        }
      },
      "202603": {
        "soma": {
          "total": 104,
          "algum": 16,
          "dnAlgum": 15.4,
          "dois": 16,
          "dnDois": 15.4,
          "todos": 16,
          "dnTodos": 15.4
        },
        "kids200": {
          "total": 104,
          "pdvs": 16,
          "dn": 15.4
        },
        "spray170": {
          "total": 104,
          "pdvs": 16,
          "dn": 15.4
        },
        "locao200": {
          "total": 104,
          "pdvs": 16,
          "dn": 15.4
        }
      },
      "202604": {
        "soma": {
          "total": 104,
          "algum": 16,
          "dnAlgum": 15.4,
          "dois": 16,
          "dnDois": 15.4,
          "todos": 16,
          "dnTodos": 15.4
        },
        "kids200": {
          "total": 104,
          "pdvs": 16,
          "dn": 15.4
        },
        "spray170": {
          "total": 104,
          "pdvs": 16,
          "dn": 15.4
        },
        "locao200": {
          "total": 104,
          "pdvs": 16,
          "dn": 15.4
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 111,
          "pdvs": 73,
          "dn": 65.8
        },
        "locao200": {
          "total": 111,
          "pdvs": 91,
          "dn": 82.0
        },
        "spray170": {
          "total": 111,
          "pdvs": 75,
          "dn": 67.6
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 111,
        "pdvs": 93,
        "dn": 83.8
      },
      "locao200": {
        "total": 111,
        "pdvs": 101,
        "dn": 91.0
      },
      "spray170": {
        "total": 111,
        "pdvs": 96,
        "dn": 86.5
      }
    }
  },
  "DROGARIA TAMOIO": {
    "fytd25": {
      "soma": {
        "total": 98,
        "algum": 90,
        "dnAlgum": 91.8,
        "dois": 90,
        "dnDois": 91.8,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 98,
        "pdvs": 90,
        "dn": 91.8
      },
      "spray170": {
        "total": 98,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 98,
        "pdvs": 90,
        "dn": 91.8
      }
    },
    "fytd26": {
      "soma": {
        "total": 98,
        "algum": 98,
        "dnAlgum": 100.0,
        "dois": 98,
        "dnDois": 100.0,
        "todos": 96,
        "dnTodos": 98.0
      },
      "kids200": {
        "total": 98,
        "pdvs": 98,
        "dn": 100.0
      },
      "spray170": {
        "total": 98,
        "pdvs": 97,
        "dn": 99.0
      },
      "locao200": {
        "total": 98,
        "pdvs": 96,
        "dn": 98.0
      }
    },
    "janabr25": {
      "soma": {
        "total": 98,
        "algum": 91,
        "dnAlgum": 92.9,
        "dois": 91,
        "dnDois": 92.9,
        "todos": 90,
        "dnTodos": 91.8
      },
      "kids200": {
        "total": 98,
        "pdvs": 90,
        "dn": 91.8
      },
      "spray170": {
        "total": 98,
        "pdvs": 91,
        "dn": 92.9
      },
      "locao200": {
        "total": 98,
        "pdvs": 90,
        "dn": 91.8
      }
    },
    "janabr26": {
      "soma": {
        "total": 98,
        "algum": 97,
        "dnAlgum": 99.0,
        "dois": 97,
        "dnDois": 99.0,
        "todos": 96,
        "dnTodos": 98.0
      },
      "kids200": {
        "total": 98,
        "pdvs": 96,
        "dn": 98.0
      },
      "spray170": {
        "total": 98,
        "pdvs": 97,
        "dn": 99.0
      },
      "locao200": {
        "total": 98,
        "pdvs": 96,
        "dn": 98.0
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 98,
          "algum": 38,
          "dnAlgum": 38.8,
          "dois": 38,
          "dnDois": 38.8,
          "todos": 38,
          "dnTodos": 38.8
        },
        "kids200": {
          "total": 98,
          "pdvs": 38,
          "dn": 38.8
        },
        "spray170": {
          "total": 98,
          "pdvs": 38,
          "dn": 38.8
        },
        "locao200": {
          "total": 98,
          "pdvs": 38,
          "dn": 38.8
        }
      },
      "202508": {
        "soma": {
          "total": 98,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 98,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202510": {
        "soma": {
          "total": 98,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202511": {
        "soma": {
          "total": 98,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202512": {
        "soma": {
          "total": 98,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202601": {
        "soma": {
          "total": 98,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 98,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202602": {
        "soma": {
          "total": 98,
          "algum": 94,
          "dnAlgum": 95.9,
          "dois": 94,
          "dnDois": 95.9,
          "todos": 93,
          "dnTodos": 94.9
        },
        "kids200": {
          "total": 98,
          "pdvs": 93,
          "dn": 94.9
        },
        "spray170": {
          "total": 98,
          "pdvs": 94,
          "dn": 95.9
        },
        "locao200": {
          "total": 98,
          "pdvs": 93,
          "dn": 94.9
        }
      },
      "202603": {
        "soma": {
          "total": 98,
          "algum": 95,
          "dnAlgum": 96.9,
          "dois": 95,
          "dnDois": 96.9,
          "todos": 94,
          "dnTodos": 95.9
        },
        "kids200": {
          "total": 98,
          "pdvs": 94,
          "dn": 95.9
        },
        "spray170": {
          "total": 98,
          "pdvs": 95,
          "dn": 96.9
        },
        "locao200": {
          "total": 98,
          "pdvs": 94,
          "dn": 95.9
        }
      },
      "202604": {
        "soma": {
          "total": 98,
          "algum": 97,
          "dnAlgum": 99.0,
          "dois": 97,
          "dnDois": 99.0,
          "todos": 96,
          "dnTodos": 98.0
        },
        "kids200": {
          "total": 98,
          "pdvs": 96,
          "dn": 98.0
        },
        "spray170": {
          "total": 98,
          "pdvs": 97,
          "dn": 99.0
        },
        "locao200": {
          "total": 98,
          "pdvs": 96,
          "dn": 98.0
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 98,
          "pdvs": 79,
          "dn": 80.6
        },
        "locao200": {
          "total": 98,
          "pdvs": 90,
          "dn": 91.8
        },
        "spray170": {
          "total": 98,
          "pdvs": 69,
          "dn": 70.4
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 98,
        "pdvs": 93,
        "dn": 94.9
      },
      "locao200": {
        "total": 98,
        "pdvs": 93,
        "dn": 94.9
      },
      "spray170": {
        "total": 98,
        "pdvs": 84,
        "dn": 85.7
      }
    }
  },
  "DROGARIA VENANCIO": {
    "fytd25": {
      "soma": {
        "total": 151,
        "algum": 137,
        "dnAlgum": 90.7,
        "dois": 137,
        "dnDois": 90.7,
        "todos": 15,
        "dnTodos": 9.9
      },
      "kids200": {
        "total": 151,
        "pdvs": 137,
        "dn": 90.7
      },
      "spray170": {
        "total": 151,
        "pdvs": 15,
        "dn": 9.9
      },
      "locao200": {
        "total": 151,
        "pdvs": 137,
        "dn": 90.7
      }
    },
    "fytd26": {
      "soma": {
        "total": 151,
        "algum": 151,
        "dnAlgum": 100.0,
        "dois": 151,
        "dnDois": 100.0,
        "todos": 150,
        "dnTodos": 99.3
      },
      "kids200": {
        "total": 151,
        "pdvs": 150,
        "dn": 99.3
      },
      "spray170": {
        "total": 151,
        "pdvs": 150,
        "dn": 99.3
      },
      "locao200": {
        "total": 151,
        "pdvs": 151,
        "dn": 100.0
      }
    },
    "janabr25": {
      "soma": {
        "total": 151,
        "algum": 135,
        "dnAlgum": 89.4,
        "dois": 135,
        "dnDois": 89.4,
        "todos": 134,
        "dnTodos": 88.7
      },
      "kids200": {
        "total": 151,
        "pdvs": 135,
        "dn": 89.4
      },
      "spray170": {
        "total": 151,
        "pdvs": 134,
        "dn": 88.7
      },
      "locao200": {
        "total": 151,
        "pdvs": 135,
        "dn": 89.4
      }
    },
    "janabr26": {
      "soma": {
        "total": 151,
        "algum": 150,
        "dnAlgum": 99.3,
        "dois": 150,
        "dnDois": 99.3,
        "todos": 150,
        "dnTodos": 99.3
      },
      "kids200": {
        "total": 151,
        "pdvs": 150,
        "dn": 99.3
      },
      "spray170": {
        "total": 151,
        "pdvs": 150,
        "dn": 99.3
      },
      "locao200": {
        "total": 151,
        "pdvs": 150,
        "dn": 99.3
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 151,
          "algum": 139,
          "dnAlgum": 92.1,
          "dois": 139,
          "dnDois": 92.1,
          "todos": 138,
          "dnTodos": 91.4
        },
        "kids200": {
          "total": 151,
          "pdvs": 139,
          "dn": 92.1
        },
        "spray170": {
          "total": 151,
          "pdvs": 138,
          "dn": 91.4
        },
        "locao200": {
          "total": 151,
          "pdvs": 139,
          "dn": 92.1
        }
      },
      "202508": {
        "soma": {
          "total": 151,
          "algum": 143,
          "dnAlgum": 94.7,
          "dois": 143,
          "dnDois": 94.7,
          "todos": 142,
          "dnTodos": 94.0
        },
        "kids200": {
          "total": 151,
          "pdvs": 143,
          "dn": 94.7
        },
        "spray170": {
          "total": 151,
          "pdvs": 142,
          "dn": 94.0
        },
        "locao200": {
          "total": 151,
          "pdvs": 143,
          "dn": 94.7
        }
      },
      "202509": {
        "soma": {
          "total": 151,
          "algum": 144,
          "dnAlgum": 95.4,
          "dois": 144,
          "dnDois": 95.4,
          "todos": 143,
          "dnTodos": 94.7
        },
        "kids200": {
          "total": 151,
          "pdvs": 144,
          "dn": 95.4
        },
        "spray170": {
          "total": 151,
          "pdvs": 143,
          "dn": 94.7
        },
        "locao200": {
          "total": 151,
          "pdvs": 144,
          "dn": 95.4
        }
      },
      "202510": {
        "soma": {
          "total": 151,
          "algum": 143,
          "dnAlgum": 94.7,
          "dois": 143,
          "dnDois": 94.7,
          "todos": 142,
          "dnTodos": 94.0
        },
        "kids200": {
          "total": 151,
          "pdvs": 143,
          "dn": 94.7
        },
        "spray170": {
          "total": 151,
          "pdvs": 142,
          "dn": 94.0
        },
        "locao200": {
          "total": 151,
          "pdvs": 143,
          "dn": 94.7
        }
      },
      "202511": {
        "soma": {
          "total": 151,
          "algum": 145,
          "dnAlgum": 96.0,
          "dois": 145,
          "dnDois": 96.0,
          "todos": 144,
          "dnTodos": 95.4
        },
        "kids200": {
          "total": 151,
          "pdvs": 145,
          "dn": 96.0
        },
        "spray170": {
          "total": 151,
          "pdvs": 144,
          "dn": 95.4
        },
        "locao200": {
          "total": 151,
          "pdvs": 145,
          "dn": 96.0
        }
      },
      "202512": {
        "soma": {
          "total": 151,
          "algum": 146,
          "dnAlgum": 96.7,
          "dois": 146,
          "dnDois": 96.7,
          "todos": 145,
          "dnTodos": 96.0
        },
        "kids200": {
          "total": 151,
          "pdvs": 146,
          "dn": 96.7
        },
        "spray170": {
          "total": 151,
          "pdvs": 145,
          "dn": 96.0
        },
        "locao200": {
          "total": 151,
          "pdvs": 146,
          "dn": 96.7
        }
      },
      "202601": {
        "soma": {
          "total": 151,
          "algum": 147,
          "dnAlgum": 97.4,
          "dois": 147,
          "dnDois": 97.4,
          "todos": 146,
          "dnTodos": 96.7
        },
        "kids200": {
          "total": 151,
          "pdvs": 147,
          "dn": 97.4
        },
        "spray170": {
          "total": 151,
          "pdvs": 146,
          "dn": 96.7
        },
        "locao200": {
          "total": 151,
          "pdvs": 147,
          "dn": 97.4
        }
      },
      "202602": {
        "soma": {
          "total": 151,
          "algum": 147,
          "dnAlgum": 97.4,
          "dois": 147,
          "dnDois": 97.4,
          "todos": 146,
          "dnTodos": 96.7
        },
        "kids200": {
          "total": 151,
          "pdvs": 147,
          "dn": 97.4
        },
        "spray170": {
          "total": 151,
          "pdvs": 146,
          "dn": 96.7
        },
        "locao200": {
          "total": 151,
          "pdvs": 147,
          "dn": 97.4
        }
      },
      "202603": {
        "soma": {
          "total": 151,
          "algum": 149,
          "dnAlgum": 98.7,
          "dois": 149,
          "dnDois": 98.7,
          "todos": 148,
          "dnTodos": 98.0
        },
        "kids200": {
          "total": 151,
          "pdvs": 149,
          "dn": 98.7
        },
        "spray170": {
          "total": 151,
          "pdvs": 148,
          "dn": 98.0
        },
        "locao200": {
          "total": 151,
          "pdvs": 149,
          "dn": 98.7
        }
      },
      "202604": {
        "soma": {
          "total": 151,
          "algum": 149,
          "dnAlgum": 98.7,
          "dois": 149,
          "dnDois": 98.7,
          "todos": 148,
          "dnTodos": 98.0
        },
        "kids200": {
          "total": 151,
          "pdvs": 149,
          "dn": 98.7
        },
        "spray170": {
          "total": 151,
          "pdvs": 148,
          "dn": 98.0
        },
        "locao200": {
          "total": 151,
          "pdvs": 149,
          "dn": 98.7
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 150,
          "pdvs": 140,
          "dn": 93.3
        },
        "locao200": {
          "total": 150,
          "pdvs": 145,
          "dn": 96.7
        },
        "spray170": {
          "total": 150,
          "pdvs": 140,
          "dn": 93.3
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 150,
        "pdvs": 147,
        "dn": 98.0
      },
      "locao200": {
        "total": 150,
        "pdvs": 149,
        "dn": 99.3
      },
      "spray170": {
        "total": 150,
        "pdvs": 147,
        "dn": 98.0
      }
    }
  },
  "DROGASIL": {
    "fytd25": {
      "soma": {
        "total": 2137,
        "algum": 1926,
        "dnAlgum": 90.1,
        "dois": 1926,
        "dnDois": 90.1,
        "todos": 9,
        "dnTodos": 0.4
      },
      "kids200": {
        "total": 2137,
        "pdvs": 1926,
        "dn": 90.1
      },
      "spray170": {
        "total": 2137,
        "pdvs": 9,
        "dn": 0.4
      },
      "locao200": {
        "total": 2137,
        "pdvs": 1926,
        "dn": 90.1
      }
    },
    "fytd26": {
      "soma": {
        "total": 2137,
        "algum": 2132,
        "dnAlgum": 99.8,
        "dois": 2132,
        "dnDois": 99.8,
        "todos": 2117,
        "dnTodos": 99.1
      },
      "kids200": {
        "total": 2137,
        "pdvs": 2132,
        "dn": 99.8
      },
      "spray170": {
        "total": 2137,
        "pdvs": 2117,
        "dn": 99.1
      },
      "locao200": {
        "total": 2137,
        "pdvs": 2127,
        "dn": 99.5
      }
    },
    "janabr25": {
      "soma": {
        "total": 2137,
        "algum": 1907,
        "dnAlgum": 89.2,
        "dois": 1907,
        "dnDois": 89.2,
        "todos": 1898,
        "dnTodos": 88.8
      },
      "kids200": {
        "total": 2137,
        "pdvs": 1907,
        "dn": 89.2
      },
      "spray170": {
        "total": 2137,
        "pdvs": 1898,
        "dn": 88.8
      },
      "locao200": {
        "total": 2137,
        "pdvs": 1907,
        "dn": 89.2
      }
    },
    "janabr26": {
      "soma": {
        "total": 2137,
        "algum": 2119,
        "dnAlgum": 99.2,
        "dois": 2119,
        "dnDois": 99.2,
        "todos": 2117,
        "dnTodos": 99.1
      },
      "kids200": {
        "total": 2137,
        "pdvs": 2119,
        "dn": 99.2
      },
      "spray170": {
        "total": 2137,
        "pdvs": 2117,
        "dn": 99.1
      },
      "locao200": {
        "total": 2137,
        "pdvs": 2119,
        "dn": 99.2
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 2137,
          "algum": 655,
          "dnAlgum": 30.7,
          "dois": 655,
          "dnDois": 30.7,
          "todos": 652,
          "dnTodos": 30.5
        },
        "kids200": {
          "total": 2137,
          "pdvs": 655,
          "dn": 30.7
        },
        "spray170": {
          "total": 2137,
          "pdvs": 652,
          "dn": 30.5
        },
        "locao200": {
          "total": 2137,
          "pdvs": 655,
          "dn": 30.7
        }
      },
      "202508": {
        "soma": {
          "total": 2137,
          "algum": 33,
          "dnAlgum": 1.5,
          "dois": 33,
          "dnDois": 1.5,
          "todos": 33,
          "dnTodos": 1.5
        },
        "kids200": {
          "total": 2137,
          "pdvs": 33,
          "dn": 1.5
        },
        "spray170": {
          "total": 2137,
          "pdvs": 33,
          "dn": 1.5
        },
        "locao200": {
          "total": 2137,
          "pdvs": 33,
          "dn": 1.5
        }
      },
      "202509": {
        "soma": {
          "total": 2137,
          "algum": 308,
          "dnAlgum": 14.4,
          "dois": 308,
          "dnDois": 14.4,
          "todos": 307,
          "dnTodos": 14.4
        },
        "kids200": {
          "total": 2137,
          "pdvs": 308,
          "dn": 14.4
        },
        "spray170": {
          "total": 2137,
          "pdvs": 307,
          "dn": 14.4
        },
        "locao200": {
          "total": 2137,
          "pdvs": 308,
          "dn": 14.4
        }
      },
      "202510": {
        "soma": {
          "total": 2137,
          "algum": 567,
          "dnAlgum": 26.5,
          "dois": 567,
          "dnDois": 26.5,
          "todos": 564,
          "dnTodos": 26.4
        },
        "kids200": {
          "total": 2137,
          "pdvs": 567,
          "dn": 26.5
        },
        "spray170": {
          "total": 2137,
          "pdvs": 564,
          "dn": 26.4
        },
        "locao200": {
          "total": 2137,
          "pdvs": 567,
          "dn": 26.5
        }
      },
      "202511": {
        "soma": {
          "total": 2137,
          "algum": 1189,
          "dnAlgum": 55.6,
          "dois": 1189,
          "dnDois": 55.6,
          "todos": 1183,
          "dnTodos": 55.4
        },
        "kids200": {
          "total": 2137,
          "pdvs": 1189,
          "dn": 55.6
        },
        "spray170": {
          "total": 2137,
          "pdvs": 1183,
          "dn": 55.4
        },
        "locao200": {
          "total": 2137,
          "pdvs": 1189,
          "dn": 55.6
        }
      },
      "202512": {
        "soma": {
          "total": 2137,
          "algum": 1490,
          "dnAlgum": 69.7,
          "dois": 1490,
          "dnDois": 69.7,
          "todos": 1483,
          "dnTodos": 69.4
        },
        "kids200": {
          "total": 2137,
          "pdvs": 1490,
          "dn": 69.7
        },
        "spray170": {
          "total": 2137,
          "pdvs": 1483,
          "dn": 69.4
        },
        "locao200": {
          "total": 2137,
          "pdvs": 1490,
          "dn": 69.7
        }
      },
      "202601": {
        "soma": {
          "total": 2137,
          "algum": 1622,
          "dnAlgum": 75.9,
          "dois": 1622,
          "dnDois": 75.9,
          "todos": 1614,
          "dnTodos": 75.5
        },
        "kids200": {
          "total": 2137,
          "pdvs": 1622,
          "dn": 75.9
        },
        "spray170": {
          "total": 2137,
          "pdvs": 1614,
          "dn": 75.5
        },
        "locao200": {
          "total": 2137,
          "pdvs": 1622,
          "dn": 75.9
        }
      },
      "202602": {
        "soma": {
          "total": 2137,
          "algum": 2092,
          "dnAlgum": 97.9,
          "dois": 2092,
          "dnDois": 97.9,
          "todos": 2082,
          "dnTodos": 97.4
        },
        "kids200": {
          "total": 2137,
          "pdvs": 2092,
          "dn": 97.9
        },
        "spray170": {
          "total": 2137,
          "pdvs": 2082,
          "dn": 97.4
        },
        "locao200": {
          "total": 2137,
          "pdvs": 2092,
          "dn": 97.9
        }
      },
      "202603": {
        "soma": {
          "total": 2137,
          "algum": 2101,
          "dnAlgum": 98.3,
          "dois": 2101,
          "dnDois": 98.3,
          "todos": 2091,
          "dnTodos": 97.8
        },
        "kids200": {
          "total": 2137,
          "pdvs": 2101,
          "dn": 98.3
        },
        "spray170": {
          "total": 2137,
          "pdvs": 2091,
          "dn": 97.8
        },
        "locao200": {
          "total": 2137,
          "pdvs": 2101,
          "dn": 98.3
        }
      },
      "202604": {
        "soma": {
          "total": 2137,
          "algum": 2119,
          "dnAlgum": 99.2,
          "dois": 2119,
          "dnDois": 99.2,
          "todos": 2109,
          "dnTodos": 98.7
        },
        "kids200": {
          "total": 2137,
          "pdvs": 2119,
          "dn": 99.2
        },
        "spray170": {
          "total": 2137,
          "pdvs": 2109,
          "dn": 98.7
        },
        "locao200": {
          "total": 2137,
          "pdvs": 2119,
          "dn": 99.2
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 2185,
          "pdvs": 1476,
          "dn": 67.6
        },
        "locao200": {
          "total": 2185,
          "pdvs": 1691,
          "dn": 77.4
        },
        "spray170": {
          "total": 2185,
          "pdvs": 1321,
          "dn": 60.5
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 2186,
        "pdvs": 1826,
        "dn": 83.5
      },
      "locao200": {
        "total": 2186,
        "pdvs": 2016,
        "dn": 92.2
      },
      "spray170": {
        "total": 2186,
        "pdvs": 1835,
        "dn": 83.9
      }
    }
  },
  "DROGASMIL": {
    "fytd25": {
      "soma": {
        "total": 109,
        "algum": 99,
        "dnAlgum": 90.8,
        "dois": 99,
        "dnDois": 90.8,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 109,
        "pdvs": 99,
        "dn": 90.8
      },
      "spray170": {
        "total": 109,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 109,
        "pdvs": 99,
        "dn": 90.8
      }
    },
    "fytd26": {
      "soma": {
        "total": 109,
        "algum": 109,
        "dnAlgum": 100.0,
        "dois": 109,
        "dnDois": 100.0,
        "todos": 108,
        "dnTodos": 99.1
      },
      "kids200": {
        "total": 109,
        "pdvs": 109,
        "dn": 100.0
      },
      "spray170": {
        "total": 109,
        "pdvs": 108,
        "dn": 99.1
      },
      "locao200": {
        "total": 109,
        "pdvs": 108,
        "dn": 99.1
      }
    },
    "janabr25": {
      "soma": {
        "total": 109,
        "algum": 98,
        "dnAlgum": 89.9,
        "dois": 98,
        "dnDois": 89.9,
        "todos": 98,
        "dnTodos": 89.9
      },
      "kids200": {
        "total": 109,
        "pdvs": 98,
        "dn": 89.9
      },
      "spray170": {
        "total": 109,
        "pdvs": 98,
        "dn": 89.9
      },
      "locao200": {
        "total": 109,
        "pdvs": 98,
        "dn": 89.9
      }
    },
    "janabr26": {
      "soma": {
        "total": 109,
        "algum": 108,
        "dnAlgum": 99.1,
        "dois": 108,
        "dnDois": 99.1,
        "todos": 107,
        "dnTodos": 98.2
      },
      "kids200": {
        "total": 109,
        "pdvs": 107,
        "dn": 98.2
      },
      "spray170": {
        "total": 109,
        "pdvs": 108,
        "dn": 99.1
      },
      "locao200": {
        "total": 109,
        "pdvs": 107,
        "dn": 98.2
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 109,
          "algum": 48,
          "dnAlgum": 44.0,
          "dois": 48,
          "dnDois": 44.0,
          "todos": 48,
          "dnTodos": 44.0
        },
        "kids200": {
          "total": 109,
          "pdvs": 48,
          "dn": 44.0
        },
        "spray170": {
          "total": 109,
          "pdvs": 48,
          "dn": 44.0
        },
        "locao200": {
          "total": 109,
          "pdvs": 48,
          "dn": 44.0
        }
      },
      "202508": {
        "soma": {
          "total": 109,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 109,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202510": {
        "soma": {
          "total": 109,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202511": {
        "soma": {
          "total": 109,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202512": {
        "soma": {
          "total": 109,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202601": {
        "soma": {
          "total": 109,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 109,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202602": {
        "soma": {
          "total": 109,
          "algum": 106,
          "dnAlgum": 97.2,
          "dois": 106,
          "dnDois": 97.2,
          "todos": 106,
          "dnTodos": 97.2
        },
        "kids200": {
          "total": 109,
          "pdvs": 106,
          "dn": 97.2
        },
        "spray170": {
          "total": 109,
          "pdvs": 106,
          "dn": 97.2
        },
        "locao200": {
          "total": 109,
          "pdvs": 106,
          "dn": 97.2
        }
      },
      "202603": {
        "soma": {
          "total": 109,
          "algum": 106,
          "dnAlgum": 97.2,
          "dois": 106,
          "dnDois": 97.2,
          "todos": 106,
          "dnTodos": 97.2
        },
        "kids200": {
          "total": 109,
          "pdvs": 106,
          "dn": 97.2
        },
        "spray170": {
          "total": 109,
          "pdvs": 106,
          "dn": 97.2
        },
        "locao200": {
          "total": 109,
          "pdvs": 106,
          "dn": 97.2
        }
      },
      "202604": {
        "soma": {
          "total": 109,
          "algum": 107,
          "dnAlgum": 98.2,
          "dois": 107,
          "dnDois": 98.2,
          "todos": 107,
          "dnTodos": 98.2
        },
        "kids200": {
          "total": 109,
          "pdvs": 107,
          "dn": 98.2
        },
        "spray170": {
          "total": 109,
          "pdvs": 107,
          "dn": 98.2
        },
        "locao200": {
          "total": 109,
          "pdvs": 107,
          "dn": 98.2
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 110,
          "pdvs": 97,
          "dn": 88.2
        },
        "locao200": {
          "total": 110,
          "pdvs": 98,
          "dn": 89.1
        },
        "spray170": {
          "total": 110,
          "pdvs": 93,
          "dn": 84.5
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 110,
        "pdvs": 105,
        "dn": 95.5
      },
      "locao200": {
        "total": 110,
        "pdvs": 106,
        "dn": 96.4
      },
      "spray170": {
        "total": 110,
        "pdvs": 98,
        "dn": 89.1
      }
    }
  },
  "DSP": {
    "fytd25": {
      "soma": {
        "total": 1103,
        "algum": 1070,
        "dnAlgum": 97.0,
        "dois": 1070,
        "dnDois": 97.0,
        "todos": 609,
        "dnTodos": 55.2
      },
      "kids200": {
        "total": 1103,
        "pdvs": 1070,
        "dn": 97.0
      },
      "spray170": {
        "total": 1103,
        "pdvs": 609,
        "dn": 55.2
      },
      "locao200": {
        "total": 1103,
        "pdvs": 1070,
        "dn": 97.0
      }
    },
    "fytd26": {
      "soma": {
        "total": 1103,
        "algum": 1101,
        "dnAlgum": 99.8,
        "dois": 1101,
        "dnDois": 99.8,
        "todos": 1099,
        "dnTodos": 99.6
      },
      "kids200": {
        "total": 1103,
        "pdvs": 1101,
        "dn": 99.8
      },
      "spray170": {
        "total": 1103,
        "pdvs": 1099,
        "dn": 99.6
      },
      "locao200": {
        "total": 1103,
        "pdvs": 1101,
        "dn": 99.8
      }
    },
    "janabr25": {
      "soma": {
        "total": 1103,
        "algum": 1066,
        "dnAlgum": 96.6,
        "dois": 1066,
        "dnDois": 96.6,
        "todos": 1064,
        "dnTodos": 96.5
      },
      "kids200": {
        "total": 1103,
        "pdvs": 1066,
        "dn": 96.6
      },
      "spray170": {
        "total": 1103,
        "pdvs": 1064,
        "dn": 96.5
      },
      "locao200": {
        "total": 1103,
        "pdvs": 1066,
        "dn": 96.6
      }
    },
    "janabr26": {
      "soma": {
        "total": 1103,
        "algum": 1099,
        "dnAlgum": 99.6,
        "dois": 1099,
        "dnDois": 99.6,
        "todos": 1099,
        "dnTodos": 99.6
      },
      "kids200": {
        "total": 1103,
        "pdvs": 1099,
        "dn": 99.6
      },
      "spray170": {
        "total": 1103,
        "pdvs": 1099,
        "dn": 99.6
      },
      "locao200": {
        "total": 1103,
        "pdvs": 1099,
        "dn": 99.6
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 1103,
          "algum": 1066,
          "dnAlgum": 96.6,
          "dois": 1066,
          "dnDois": 96.6,
          "todos": 1064,
          "dnTodos": 96.5
        },
        "kids200": {
          "total": 1103,
          "pdvs": 1066,
          "dn": 96.6
        },
        "spray170": {
          "total": 1103,
          "pdvs": 1064,
          "dn": 96.5
        },
        "locao200": {
          "total": 1103,
          "pdvs": 1066,
          "dn": 96.6
        }
      },
      "202508": {
        "soma": {
          "total": 1103,
          "algum": 1082,
          "dnAlgum": 98.1,
          "dois": 1082,
          "dnDois": 98.1,
          "todos": 1080,
          "dnTodos": 97.9
        },
        "kids200": {
          "total": 1103,
          "pdvs": 1082,
          "dn": 98.1
        },
        "spray170": {
          "total": 1103,
          "pdvs": 1080,
          "dn": 97.9
        },
        "locao200": {
          "total": 1103,
          "pdvs": 1082,
          "dn": 98.1
        }
      },
      "202509": {
        "soma": {
          "total": 1103,
          "algum": 1087,
          "dnAlgum": 98.5,
          "dois": 1087,
          "dnDois": 98.5,
          "todos": 1085,
          "dnTodos": 98.4
        },
        "kids200": {
          "total": 1103,
          "pdvs": 1087,
          "dn": 98.5
        },
        "spray170": {
          "total": 1103,
          "pdvs": 1085,
          "dn": 98.4
        },
        "locao200": {
          "total": 1103,
          "pdvs": 1087,
          "dn": 98.5
        }
      },
      "202510": {
        "soma": {
          "total": 1103,
          "algum": 1086,
          "dnAlgum": 98.5,
          "dois": 1086,
          "dnDois": 98.5,
          "todos": 1084,
          "dnTodos": 98.3
        },
        "kids200": {
          "total": 1103,
          "pdvs": 1086,
          "dn": 98.5
        },
        "spray170": {
          "total": 1103,
          "pdvs": 1084,
          "dn": 98.3
        },
        "locao200": {
          "total": 1103,
          "pdvs": 1086,
          "dn": 98.5
        }
      },
      "202511": {
        "soma": {
          "total": 1103,
          "algum": 1087,
          "dnAlgum": 98.5,
          "dois": 1087,
          "dnDois": 98.5,
          "todos": 1085,
          "dnTodos": 98.4
        },
        "kids200": {
          "total": 1103,
          "pdvs": 1087,
          "dn": 98.5
        },
        "spray170": {
          "total": 1103,
          "pdvs": 1085,
          "dn": 98.4
        },
        "locao200": {
          "total": 1103,
          "pdvs": 1087,
          "dn": 98.5
        }
      },
      "202512": {
        "soma": {
          "total": 1103,
          "algum": 1086,
          "dnAlgum": 98.5,
          "dois": 1086,
          "dnDois": 98.5,
          "todos": 1084,
          "dnTodos": 98.3
        },
        "kids200": {
          "total": 1103,
          "pdvs": 1086,
          "dn": 98.5
        },
        "spray170": {
          "total": 1103,
          "pdvs": 1084,
          "dn": 98.3
        },
        "locao200": {
          "total": 1103,
          "pdvs": 1086,
          "dn": 98.5
        }
      },
      "202601": {
        "soma": {
          "total": 1103,
          "algum": 1084,
          "dnAlgum": 98.3,
          "dois": 1084,
          "dnDois": 98.3,
          "todos": 1082,
          "dnTodos": 98.1
        },
        "kids200": {
          "total": 1103,
          "pdvs": 1084,
          "dn": 98.3
        },
        "spray170": {
          "total": 1103,
          "pdvs": 1082,
          "dn": 98.1
        },
        "locao200": {
          "total": 1103,
          "pdvs": 1084,
          "dn": 98.3
        }
      },
      "202602": {
        "soma": {
          "total": 1103,
          "algum": 1086,
          "dnAlgum": 98.5,
          "dois": 1086,
          "dnDois": 98.5,
          "todos": 1084,
          "dnTodos": 98.3
        },
        "kids200": {
          "total": 1103,
          "pdvs": 1086,
          "dn": 98.5
        },
        "spray170": {
          "total": 1103,
          "pdvs": 1084,
          "dn": 98.3
        },
        "locao200": {
          "total": 1103,
          "pdvs": 1086,
          "dn": 98.5
        }
      },
      "202603": {
        "soma": {
          "total": 1103,
          "algum": 1088,
          "dnAlgum": 98.6,
          "dois": 1088,
          "dnDois": 98.6,
          "todos": 1086,
          "dnTodos": 98.5
        },
        "kids200": {
          "total": 1103,
          "pdvs": 1088,
          "dn": 98.6
        },
        "spray170": {
          "total": 1103,
          "pdvs": 1086,
          "dn": 98.5
        },
        "locao200": {
          "total": 1103,
          "pdvs": 1088,
          "dn": 98.6
        }
      },
      "202604": {
        "soma": {
          "total": 1103,
          "algum": 1089,
          "dnAlgum": 98.7,
          "dois": 1089,
          "dnDois": 98.7,
          "todos": 1087,
          "dnTodos": 98.5
        },
        "kids200": {
          "total": 1103,
          "pdvs": 1089,
          "dn": 98.7
        },
        "spray170": {
          "total": 1103,
          "pdvs": 1087,
          "dn": 98.5
        },
        "locao200": {
          "total": 1103,
          "pdvs": 1089,
          "dn": 98.7
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 1110,
          "pdvs": 728,
          "dn": 65.6
        },
        "locao200": {
          "total": 1110,
          "pdvs": 844,
          "dn": 76.0
        },
        "spray170": {
          "total": 1110,
          "pdvs": 699,
          "dn": 63.0
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 1110,
        "pdvs": 865,
        "dn": 77.9
      },
      "locao200": {
        "total": 1110,
        "pdvs": 987,
        "dn": 88.9
      },
      "spray170": {
        "total": 1110,
        "pdvs": 911,
        "dn": 82.1
      }
    }
  },
  "EXTRAFARMA": {
    "fytd25": {
      "soma": {
        "total": 347,
        "algum": 346,
        "dnAlgum": 99.7,
        "dois": 346,
        "dnDois": 99.7,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 347,
        "pdvs": 346,
        "dn": 99.7
      },
      "spray170": {
        "total": 347,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 347,
        "pdvs": 346,
        "dn": 99.7
      }
    },
    "fytd26": {
      "soma": {
        "total": 347,
        "algum": 347,
        "dnAlgum": 100.0,
        "dois": 347,
        "dnDois": 100.0,
        "todos": 347,
        "dnTodos": 100.0
      },
      "kids200": {
        "total": 347,
        "pdvs": 347,
        "dn": 100.0
      },
      "spray170": {
        "total": 347,
        "pdvs": 347,
        "dn": 100.0
      },
      "locao200": {
        "total": 347,
        "pdvs": 347,
        "dn": 100.0
      }
    },
    "janabr25": {
      "soma": {
        "total": 347,
        "algum": 345,
        "dnAlgum": 99.4,
        "dois": 345,
        "dnDois": 99.4,
        "todos": 345,
        "dnTodos": 99.4
      },
      "kids200": {
        "total": 347,
        "pdvs": 345,
        "dn": 99.4
      },
      "spray170": {
        "total": 347,
        "pdvs": 345,
        "dn": 99.4
      },
      "locao200": {
        "total": 347,
        "pdvs": 345,
        "dn": 99.4
      }
    },
    "janabr26": {
      "soma": {
        "total": 347,
        "algum": 347,
        "dnAlgum": 100.0,
        "dois": 347,
        "dnDois": 100.0,
        "todos": 347,
        "dnTodos": 100.0
      },
      "kids200": {
        "total": 347,
        "pdvs": 347,
        "dn": 100.0
      },
      "spray170": {
        "total": 347,
        "pdvs": 347,
        "dn": 100.0
      },
      "locao200": {
        "total": 347,
        "pdvs": 347,
        "dn": 100.0
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 347,
          "algum": 236,
          "dnAlgum": 68.0,
          "dois": 236,
          "dnDois": 68.0,
          "todos": 236,
          "dnTodos": 68.0
        },
        "kids200": {
          "total": 347,
          "pdvs": 236,
          "dn": 68.0
        },
        "spray170": {
          "total": 347,
          "pdvs": 236,
          "dn": 68.0
        },
        "locao200": {
          "total": 347,
          "pdvs": 236,
          "dn": 68.0
        }
      },
      "202508": {
        "soma": {
          "total": 347,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 347,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 347,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 347,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 347,
          "algum": 24,
          "dnAlgum": 6.9,
          "dois": 24,
          "dnDois": 6.9,
          "todos": 24,
          "dnTodos": 6.9
        },
        "kids200": {
          "total": 347,
          "pdvs": 24,
          "dn": 6.9
        },
        "spray170": {
          "total": 347,
          "pdvs": 24,
          "dn": 6.9
        },
        "locao200": {
          "total": 347,
          "pdvs": 24,
          "dn": 6.9
        }
      },
      "202510": {
        "soma": {
          "total": 347,
          "algum": 51,
          "dnAlgum": 14.7,
          "dois": 51,
          "dnDois": 14.7,
          "todos": 51,
          "dnTodos": 14.7
        },
        "kids200": {
          "total": 347,
          "pdvs": 51,
          "dn": 14.7
        },
        "spray170": {
          "total": 347,
          "pdvs": 51,
          "dn": 14.7
        },
        "locao200": {
          "total": 347,
          "pdvs": 51,
          "dn": 14.7
        }
      },
      "202511": {
        "soma": {
          "total": 347,
          "algum": 72,
          "dnAlgum": 20.7,
          "dois": 72,
          "dnDois": 20.7,
          "todos": 72,
          "dnTodos": 20.7
        },
        "kids200": {
          "total": 347,
          "pdvs": 72,
          "dn": 20.7
        },
        "spray170": {
          "total": 347,
          "pdvs": 72,
          "dn": 20.7
        },
        "locao200": {
          "total": 347,
          "pdvs": 72,
          "dn": 20.7
        }
      },
      "202512": {
        "soma": {
          "total": 347,
          "algum": 99,
          "dnAlgum": 28.5,
          "dois": 99,
          "dnDois": 28.5,
          "todos": 99,
          "dnTodos": 28.5
        },
        "kids200": {
          "total": 347,
          "pdvs": 99,
          "dn": 28.5
        },
        "spray170": {
          "total": 347,
          "pdvs": 99,
          "dn": 28.5
        },
        "locao200": {
          "total": 347,
          "pdvs": 99,
          "dn": 28.5
        }
      },
      "202601": {
        "soma": {
          "total": 347,
          "algum": 110,
          "dnAlgum": 31.7,
          "dois": 110,
          "dnDois": 31.7,
          "todos": 110,
          "dnTodos": 31.7
        },
        "kids200": {
          "total": 347,
          "pdvs": 110,
          "dn": 31.7
        },
        "spray170": {
          "total": 347,
          "pdvs": 110,
          "dn": 31.7
        },
        "locao200": {
          "total": 347,
          "pdvs": 110,
          "dn": 31.7
        }
      },
      "202602": {
        "soma": {
          "total": 347,
          "algum": 347,
          "dnAlgum": 100.0,
          "dois": 347,
          "dnDois": 100.0,
          "todos": 347,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 347,
          "pdvs": 347,
          "dn": 100.0
        },
        "spray170": {
          "total": 347,
          "pdvs": 347,
          "dn": 100.0
        },
        "locao200": {
          "total": 347,
          "pdvs": 347,
          "dn": 100.0
        }
      },
      "202603": {
        "soma": {
          "total": 347,
          "algum": 347,
          "dnAlgum": 100.0,
          "dois": 347,
          "dnDois": 100.0,
          "todos": 347,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 347,
          "pdvs": 347,
          "dn": 100.0
        },
        "spray170": {
          "total": 347,
          "pdvs": 347,
          "dn": 100.0
        },
        "locao200": {
          "total": 347,
          "pdvs": 347,
          "dn": 100.0
        }
      },
      "202604": {
        "soma": {
          "total": 347,
          "algum": 347,
          "dnAlgum": 100.0,
          "dois": 347,
          "dnDois": 100.0,
          "todos": 347,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 347,
          "pdvs": 347,
          "dn": 100.0
        },
        "spray170": {
          "total": 347,
          "pdvs": 347,
          "dn": 100.0
        },
        "locao200": {
          "total": 347,
          "pdvs": 347,
          "dn": 100.0
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 343,
          "pdvs": 270,
          "dn": 78.7
        },
        "locao200": {
          "total": 343,
          "pdvs": 295,
          "dn": 86.0
        },
        "spray170": {
          "total": 343,
          "pdvs": 208,
          "dn": 60.6
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 343,
        "pdvs": 318,
        "dn": 92.7
      },
      "locao200": {
        "total": 343,
        "pdvs": 337,
        "dn": 98.3
      },
      "spray170": {
        "total": 343,
        "pdvs": 305,
        "dn": 88.9
      }
    }
  },
  "FARMA CONDE": {
    "fytd25": {
      "soma": {
        "total": 315,
        "algum": 315,
        "dnAlgum": 100.0,
        "dois": 315,
        "dnDois": 100.0,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 315,
        "pdvs": 315,
        "dn": 100.0
      },
      "spray170": {
        "total": 315,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 315,
        "pdvs": 315,
        "dn": 100.0
      }
    },
    "fytd26": {
      "soma": {
        "total": 315,
        "algum": 312,
        "dnAlgum": 99.0,
        "dois": 312,
        "dnDois": 99.0,
        "todos": 297,
        "dnTodos": 94.3
      },
      "kids200": {
        "total": 315,
        "pdvs": 312,
        "dn": 99.0
      },
      "spray170": {
        "total": 315,
        "pdvs": 297,
        "dn": 94.3
      },
      "locao200": {
        "total": 315,
        "pdvs": 303,
        "dn": 96.2
      }
    },
    "janabr25": {
      "soma": {
        "total": 315,
        "algum": 315,
        "dnAlgum": 100.0,
        "dois": 315,
        "dnDois": 100.0,
        "todos": 315,
        "dnTodos": 100.0
      },
      "kids200": {
        "total": 315,
        "pdvs": 315,
        "dn": 100.0
      },
      "spray170": {
        "total": 315,
        "pdvs": 315,
        "dn": 100.0
      },
      "locao200": {
        "total": 315,
        "pdvs": 315,
        "dn": 100.0
      }
    },
    "janabr26": {
      "soma": {
        "total": 315,
        "algum": 297,
        "dnAlgum": 94.3,
        "dois": 297,
        "dnDois": 94.3,
        "todos": 290,
        "dnTodos": 92.1
      },
      "kids200": {
        "total": 315,
        "pdvs": 290,
        "dn": 92.1
      },
      "spray170": {
        "total": 315,
        "pdvs": 297,
        "dn": 94.3
      },
      "locao200": {
        "total": 315,
        "pdvs": 290,
        "dn": 92.1
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 315,
          "algum": 282,
          "dnAlgum": 89.5,
          "dois": 282,
          "dnDois": 89.5,
          "todos": 276,
          "dnTodos": 87.6
        },
        "kids200": {
          "total": 315,
          "pdvs": 282,
          "dn": 89.5
        },
        "spray170": {
          "total": 315,
          "pdvs": 276,
          "dn": 87.6
        },
        "locao200": {
          "total": 315,
          "pdvs": 282,
          "dn": 89.5
        }
      },
      "202508": {
        "soma": {
          "total": 315,
          "algum": 301,
          "dnAlgum": 95.6,
          "dois": 301,
          "dnDois": 95.6,
          "todos": 295,
          "dnTodos": 93.7
        },
        "kids200": {
          "total": 315,
          "pdvs": 301,
          "dn": 95.6
        },
        "spray170": {
          "total": 315,
          "pdvs": 295,
          "dn": 93.7
        },
        "locao200": {
          "total": 315,
          "pdvs": 301,
          "dn": 95.6
        }
      },
      "202509": {
        "soma": {
          "total": 315,
          "algum": 311,
          "dnAlgum": 98.7,
          "dois": 311,
          "dnDois": 98.7,
          "todos": 305,
          "dnTodos": 96.8
        },
        "kids200": {
          "total": 315,
          "pdvs": 311,
          "dn": 98.7
        },
        "spray170": {
          "total": 315,
          "pdvs": 305,
          "dn": 96.8
        },
        "locao200": {
          "total": 315,
          "pdvs": 311,
          "dn": 98.7
        }
      },
      "202510": {
        "soma": {
          "total": 315,
          "algum": 298,
          "dnAlgum": 94.6,
          "dois": 298,
          "dnDois": 94.6,
          "todos": 292,
          "dnTodos": 92.7
        },
        "kids200": {
          "total": 315,
          "pdvs": 298,
          "dn": 94.6
        },
        "spray170": {
          "total": 315,
          "pdvs": 292,
          "dn": 92.7
        },
        "locao200": {
          "total": 315,
          "pdvs": 298,
          "dn": 94.6
        }
      },
      "202511": {
        "soma": {
          "total": 315,
          "algum": 284,
          "dnAlgum": 90.2,
          "dois": 284,
          "dnDois": 90.2,
          "todos": 278,
          "dnTodos": 88.3
        },
        "kids200": {
          "total": 315,
          "pdvs": 284,
          "dn": 90.2
        },
        "spray170": {
          "total": 315,
          "pdvs": 278,
          "dn": 88.3
        },
        "locao200": {
          "total": 315,
          "pdvs": 284,
          "dn": 90.2
        }
      },
      "202512": {
        "soma": {
          "total": 315,
          "algum": 278,
          "dnAlgum": 88.3,
          "dois": 278,
          "dnDois": 88.3,
          "todos": 272,
          "dnTodos": 86.3
        },
        "kids200": {
          "total": 315,
          "pdvs": 278,
          "dn": 88.3
        },
        "spray170": {
          "total": 315,
          "pdvs": 272,
          "dn": 86.3
        },
        "locao200": {
          "total": 315,
          "pdvs": 278,
          "dn": 88.3
        }
      },
      "202601": {
        "soma": {
          "total": 315,
          "algum": 277,
          "dnAlgum": 87.9,
          "dois": 277,
          "dnDois": 87.9,
          "todos": 272,
          "dnTodos": 86.3
        },
        "kids200": {
          "total": 315,
          "pdvs": 277,
          "dn": 87.9
        },
        "spray170": {
          "total": 315,
          "pdvs": 272,
          "dn": 86.3
        },
        "locao200": {
          "total": 315,
          "pdvs": 277,
          "dn": 87.9
        }
      },
      "202602": {
        "soma": {
          "total": 315,
          "algum": 278,
          "dnAlgum": 88.3,
          "dois": 278,
          "dnDois": 88.3,
          "todos": 272,
          "dnTodos": 86.3
        },
        "kids200": {
          "total": 315,
          "pdvs": 278,
          "dn": 88.3
        },
        "spray170": {
          "total": 315,
          "pdvs": 272,
          "dn": 86.3
        },
        "locao200": {
          "total": 315,
          "pdvs": 278,
          "dn": 88.3
        }
      },
      "202603": {
        "soma": {
          "total": 315,
          "algum": 276,
          "dnAlgum": 87.6,
          "dois": 276,
          "dnDois": 87.6,
          "todos": 271,
          "dnTodos": 86.0
        },
        "kids200": {
          "total": 315,
          "pdvs": 276,
          "dn": 87.6
        },
        "spray170": {
          "total": 315,
          "pdvs": 271,
          "dn": 86.0
        },
        "locao200": {
          "total": 315,
          "pdvs": 276,
          "dn": 87.6
        }
      },
      "202604": {
        "soma": {
          "total": 315,
          "algum": 277,
          "dnAlgum": 87.9,
          "dois": 277,
          "dnDois": 87.9,
          "todos": 272,
          "dnTodos": 86.3
        },
        "kids200": {
          "total": 315,
          "pdvs": 277,
          "dn": 87.9
        },
        "spray170": {
          "total": 315,
          "pdvs": 272,
          "dn": 86.3
        },
        "locao200": {
          "total": 315,
          "pdvs": 277,
          "dn": 87.9
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 281,
          "pdvs": 172,
          "dn": 61.2
        },
        "locao200": {
          "total": 281,
          "pdvs": 197,
          "dn": 70.1
        },
        "spray170": {
          "total": 281,
          "pdvs": 165,
          "dn": 58.7
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 282,
        "pdvs": 203,
        "dn": 72.0
      },
      "locao200": {
        "total": 282,
        "pdvs": 240,
        "dn": 85.1
      },
      "spray170": {
        "total": 282,
        "pdvs": 206,
        "dn": 73.0
      }
    }
  },
  "INDIANA": {
    "fytd25": {
      "soma": {
        "total": 300,
        "algum": 261,
        "dnAlgum": 87.0,
        "dois": 261,
        "dnDois": 87.0,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 300,
        "pdvs": 261,
        "dn": 87.0
      },
      "spray170": {
        "total": 300,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 300,
        "pdvs": 261,
        "dn": 87.0
      }
    },
    "fytd26": {
      "soma": {
        "total": 300,
        "algum": 297,
        "dnAlgum": 99.0,
        "dois": 297,
        "dnDois": 99.0,
        "todos": 281,
        "dnTodos": 93.7
      },
      "kids200": {
        "total": 300,
        "pdvs": 294,
        "dn": 98.0
      },
      "spray170": {
        "total": 300,
        "pdvs": 281,
        "dn": 93.7
      },
      "locao200": {
        "total": 300,
        "pdvs": 297,
        "dn": 99.0
      }
    },
    "janabr25": {
      "soma": {
        "total": 300,
        "algum": 258,
        "dnAlgum": 86.0,
        "dois": 258,
        "dnDois": 86.0,
        "todos": 244,
        "dnTodos": 81.3
      },
      "kids200": {
        "total": 300,
        "pdvs": 258,
        "dn": 86.0
      },
      "spray170": {
        "total": 300,
        "pdvs": 244,
        "dn": 81.3
      },
      "locao200": {
        "total": 300,
        "pdvs": 258,
        "dn": 86.0
      }
    },
    "janabr26": {
      "soma": {
        "total": 300,
        "algum": 281,
        "dnAlgum": 93.7,
        "dois": 281,
        "dnDois": 93.7,
        "todos": 276,
        "dnTodos": 92.0
      },
      "kids200": {
        "total": 300,
        "pdvs": 276,
        "dn": 92.0
      },
      "spray170": {
        "total": 300,
        "pdvs": 281,
        "dn": 93.7
      },
      "locao200": {
        "total": 300,
        "pdvs": 276,
        "dn": 92.0
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 300,
          "algum": 266,
          "dnAlgum": 88.7,
          "dois": 266,
          "dnDois": 88.7,
          "todos": 252,
          "dnTodos": 84.0
        },
        "kids200": {
          "total": 300,
          "pdvs": 266,
          "dn": 88.7
        },
        "spray170": {
          "total": 300,
          "pdvs": 252,
          "dn": 84.0
        },
        "locao200": {
          "total": 300,
          "pdvs": 266,
          "dn": 88.7
        }
      },
      "202508": {
        "soma": {
          "total": 300,
          "algum": 271,
          "dnAlgum": 90.3,
          "dois": 271,
          "dnDois": 90.3,
          "todos": 256,
          "dnTodos": 85.3
        },
        "kids200": {
          "total": 300,
          "pdvs": 271,
          "dn": 90.3
        },
        "spray170": {
          "total": 300,
          "pdvs": 256,
          "dn": 85.3
        },
        "locao200": {
          "total": 300,
          "pdvs": 271,
          "dn": 90.3
        }
      },
      "202509": {
        "soma": {
          "total": 300,
          "algum": 274,
          "dnAlgum": 91.3,
          "dois": 274,
          "dnDois": 91.3,
          "todos": 259,
          "dnTodos": 86.3
        },
        "kids200": {
          "total": 300,
          "pdvs": 274,
          "dn": 91.3
        },
        "spray170": {
          "total": 300,
          "pdvs": 259,
          "dn": 86.3
        },
        "locao200": {
          "total": 300,
          "pdvs": 274,
          "dn": 91.3
        }
      },
      "202510": {
        "soma": {
          "total": 300,
          "algum": 279,
          "dnAlgum": 93.0,
          "dois": 279,
          "dnDois": 93.0,
          "todos": 264,
          "dnTodos": 88.0
        },
        "kids200": {
          "total": 300,
          "pdvs": 279,
          "dn": 93.0
        },
        "spray170": {
          "total": 300,
          "pdvs": 264,
          "dn": 88.0
        },
        "locao200": {
          "total": 300,
          "pdvs": 279,
          "dn": 93.0
        }
      },
      "202511": {
        "soma": {
          "total": 300,
          "algum": 283,
          "dnAlgum": 94.3,
          "dois": 283,
          "dnDois": 94.3,
          "todos": 268,
          "dnTodos": 89.3
        },
        "kids200": {
          "total": 300,
          "pdvs": 283,
          "dn": 94.3
        },
        "spray170": {
          "total": 300,
          "pdvs": 268,
          "dn": 89.3
        },
        "locao200": {
          "total": 300,
          "pdvs": 283,
          "dn": 94.3
        }
      },
      "202512": {
        "soma": {
          "total": 300,
          "algum": 292,
          "dnAlgum": 97.3,
          "dois": 292,
          "dnDois": 97.3,
          "todos": 276,
          "dnTodos": 92.0
        },
        "kids200": {
          "total": 300,
          "pdvs": 292,
          "dn": 97.3
        },
        "spray170": {
          "total": 300,
          "pdvs": 276,
          "dn": 92.0
        },
        "locao200": {
          "total": 300,
          "pdvs": 292,
          "dn": 97.3
        }
      },
      "202601": {
        "soma": {
          "total": 300,
          "algum": 292,
          "dnAlgum": 97.3,
          "dois": 292,
          "dnDois": 97.3,
          "todos": 276,
          "dnTodos": 92.0
        },
        "kids200": {
          "total": 300,
          "pdvs": 292,
          "dn": 97.3
        },
        "spray170": {
          "total": 300,
          "pdvs": 276,
          "dn": 92.0
        },
        "locao200": {
          "total": 300,
          "pdvs": 292,
          "dn": 97.3
        }
      },
      "202602": {
        "soma": {
          "total": 300,
          "algum": 294,
          "dnAlgum": 98.0,
          "dois": 294,
          "dnDois": 98.0,
          "todos": 278,
          "dnTodos": 92.7
        },
        "kids200": {
          "total": 300,
          "pdvs": 294,
          "dn": 98.0
        },
        "spray170": {
          "total": 300,
          "pdvs": 278,
          "dn": 92.7
        },
        "locao200": {
          "total": 300,
          "pdvs": 294,
          "dn": 98.0
        }
      },
      "202603": {
        "soma": {
          "total": 300,
          "algum": 294,
          "dnAlgum": 98.0,
          "dois": 294,
          "dnDois": 98.0,
          "todos": 278,
          "dnTodos": 92.7
        },
        "kids200": {
          "total": 300,
          "pdvs": 294,
          "dn": 98.0
        },
        "spray170": {
          "total": 300,
          "pdvs": 278,
          "dn": 92.7
        },
        "locao200": {
          "total": 300,
          "pdvs": 294,
          "dn": 98.0
        }
      },
      "202604": {
        "soma": {
          "total": 300,
          "algum": 296,
          "dnAlgum": 98.7,
          "dois": 296,
          "dnDois": 98.7,
          "todos": 280,
          "dnTodos": 93.3
        },
        "kids200": {
          "total": 300,
          "pdvs": 296,
          "dn": 98.7
        },
        "spray170": {
          "total": 300,
          "pdvs": 280,
          "dn": 93.3
        },
        "locao200": {
          "total": 300,
          "pdvs": 296,
          "dn": 98.7
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 311,
          "pdvs": 236,
          "dn": 75.9
        },
        "locao200": {
          "total": 311,
          "pdvs": 269,
          "dn": 86.5
        },
        "spray170": {
          "total": 311,
          "pdvs": 157,
          "dn": 50.5
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 311,
        "pdvs": 273,
        "dn": 87.8
      },
      "locao200": {
        "total": 311,
        "pdvs": 287,
        "dn": 92.3
      },
      "spray170": {
        "total": 311,
        "pdvs": 203,
        "dn": 65.3
      }
    }
  },
  "NISSEI": {
    "fytd25": {
      "soma": {
        "total": 470,
        "algum": 470,
        "dnAlgum": 100.0,
        "dois": 470,
        "dnDois": 100.0,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 470,
        "pdvs": 470,
        "dn": 100.0
      },
      "spray170": {
        "total": 470,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 470,
        "pdvs": 470,
        "dn": 100.0
      }
    },
    "fytd26": {
      "soma": {
        "total": 470,
        "algum": 470,
        "dnAlgum": 100.0,
        "dois": 470,
        "dnDois": 100.0,
        "todos": 469,
        "dnTodos": 99.8
      },
      "kids200": {
        "total": 470,
        "pdvs": 469,
        "dn": 99.8
      },
      "spray170": {
        "total": 470,
        "pdvs": 469,
        "dn": 99.8
      },
      "locao200": {
        "total": 470,
        "pdvs": 470,
        "dn": 100.0
      }
    },
    "janabr25": {
      "soma": {
        "total": 470,
        "algum": 470,
        "dnAlgum": 100.0,
        "dois": 470,
        "dnDois": 100.0,
        "todos": 469,
        "dnTodos": 99.8
      },
      "kids200": {
        "total": 470,
        "pdvs": 470,
        "dn": 100.0
      },
      "spray170": {
        "total": 470,
        "pdvs": 469,
        "dn": 99.8
      },
      "locao200": {
        "total": 470,
        "pdvs": 470,
        "dn": 100.0
      }
    },
    "janabr26": {
      "soma": {
        "total": 470,
        "algum": 469,
        "dnAlgum": 99.8,
        "dois": 469,
        "dnDois": 99.8,
        "todos": 469,
        "dnTodos": 99.8
      },
      "kids200": {
        "total": 470,
        "pdvs": 469,
        "dn": 99.8
      },
      "spray170": {
        "total": 470,
        "pdvs": 469,
        "dn": 99.8
      },
      "locao200": {
        "total": 470,
        "pdvs": 469,
        "dn": 99.8
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 470,
          "algum": 445,
          "dnAlgum": 94.7,
          "dois": 445,
          "dnDois": 94.7,
          "todos": 444,
          "dnTodos": 94.5
        },
        "kids200": {
          "total": 470,
          "pdvs": 445,
          "dn": 94.7
        },
        "spray170": {
          "total": 470,
          "pdvs": 444,
          "dn": 94.5
        },
        "locao200": {
          "total": 470,
          "pdvs": 445,
          "dn": 94.7
        }
      },
      "202508": {
        "soma": {
          "total": 470,
          "algum": 449,
          "dnAlgum": 95.5,
          "dois": 449,
          "dnDois": 95.5,
          "todos": 448,
          "dnTodos": 95.3
        },
        "kids200": {
          "total": 470,
          "pdvs": 449,
          "dn": 95.5
        },
        "spray170": {
          "total": 470,
          "pdvs": 448,
          "dn": 95.3
        },
        "locao200": {
          "total": 470,
          "pdvs": 449,
          "dn": 95.5
        }
      },
      "202509": {
        "soma": {
          "total": 470,
          "algum": 465,
          "dnAlgum": 98.9,
          "dois": 465,
          "dnDois": 98.9,
          "todos": 464,
          "dnTodos": 98.7
        },
        "kids200": {
          "total": 470,
          "pdvs": 465,
          "dn": 98.9
        },
        "spray170": {
          "total": 470,
          "pdvs": 464,
          "dn": 98.7
        },
        "locao200": {
          "total": 470,
          "pdvs": 465,
          "dn": 98.9
        }
      },
      "202510": {
        "soma": {
          "total": 470,
          "algum": 465,
          "dnAlgum": 98.9,
          "dois": 465,
          "dnDois": 98.9,
          "todos": 464,
          "dnTodos": 98.7
        },
        "kids200": {
          "total": 470,
          "pdvs": 465,
          "dn": 98.9
        },
        "spray170": {
          "total": 470,
          "pdvs": 464,
          "dn": 98.7
        },
        "locao200": {
          "total": 470,
          "pdvs": 465,
          "dn": 98.9
        }
      },
      "202511": {
        "soma": {
          "total": 470,
          "algum": 466,
          "dnAlgum": 99.1,
          "dois": 466,
          "dnDois": 99.1,
          "todos": 465,
          "dnTodos": 98.9
        },
        "kids200": {
          "total": 470,
          "pdvs": 466,
          "dn": 99.1
        },
        "spray170": {
          "total": 470,
          "pdvs": 465,
          "dn": 98.9
        },
        "locao200": {
          "total": 470,
          "pdvs": 466,
          "dn": 99.1
        }
      },
      "202512": {
        "soma": {
          "total": 470,
          "algum": 466,
          "dnAlgum": 99.1,
          "dois": 466,
          "dnDois": 99.1,
          "todos": 465,
          "dnTodos": 98.9
        },
        "kids200": {
          "total": 470,
          "pdvs": 466,
          "dn": 99.1
        },
        "spray170": {
          "total": 470,
          "pdvs": 465,
          "dn": 98.9
        },
        "locao200": {
          "total": 470,
          "pdvs": 466,
          "dn": 99.1
        }
      },
      "202601": {
        "soma": {
          "total": 470,
          "algum": 465,
          "dnAlgum": 98.9,
          "dois": 465,
          "dnDois": 98.9,
          "todos": 464,
          "dnTodos": 98.7
        },
        "kids200": {
          "total": 470,
          "pdvs": 465,
          "dn": 98.9
        },
        "spray170": {
          "total": 470,
          "pdvs": 464,
          "dn": 98.7
        },
        "locao200": {
          "total": 470,
          "pdvs": 465,
          "dn": 98.9
        }
      },
      "202602": {
        "soma": {
          "total": 470,
          "algum": 466,
          "dnAlgum": 99.1,
          "dois": 466,
          "dnDois": 99.1,
          "todos": 465,
          "dnTodos": 98.9
        },
        "kids200": {
          "total": 470,
          "pdvs": 466,
          "dn": 99.1
        },
        "spray170": {
          "total": 470,
          "pdvs": 465,
          "dn": 98.9
        },
        "locao200": {
          "total": 470,
          "pdvs": 466,
          "dn": 99.1
        }
      },
      "202603": {
        "soma": {
          "total": 470,
          "algum": 468,
          "dnAlgum": 99.6,
          "dois": 468,
          "dnDois": 99.6,
          "todos": 467,
          "dnTodos": 99.4
        },
        "kids200": {
          "total": 470,
          "pdvs": 468,
          "dn": 99.6
        },
        "spray170": {
          "total": 470,
          "pdvs": 467,
          "dn": 99.4
        },
        "locao200": {
          "total": 470,
          "pdvs": 468,
          "dn": 99.6
        }
      },
      "202604": {
        "soma": {
          "total": 471,
          "algum": 461,
          "dnAlgum": 97.9,
          "dois": 461,
          "dnDois": 97.9,
          "todos": 323,
          "dnTodos": 68.6
        },
        "kids200": {
          "total": 471,
          "pdvs": 323,
          "dn": 68.6
        },
        "spray170": {
          "total": 471,
          "pdvs": 380,
          "dn": 80.7
        },
        "locao200": {
          "total": 471,
          "pdvs": 461,
          "dn": 97.9
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 457,
          "pdvs": 196,
          "dn": 42.9
        },
        "locao200": {
          "total": 457,
          "pdvs": 134,
          "dn": 29.3
        },
        "spray170": {
          "total": 457,
          "pdvs": 24,
          "dn": 5.3
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 464,
        "pdvs": 235,
        "dn": 50.6
      },
      "locao200": {
        "total": 464,
        "pdvs": 155,
        "dn": 33.4
      },
      "spray170": {
        "total": 464,
        "pdvs": 49,
        "dn": 10.6
      }
    }
  },
  "PACHECO": {
    "fytd25": {
      "soma": {
        "total": 559,
        "algum": 553,
        "dnAlgum": 98.9,
        "dois": 553,
        "dnDois": 98.9,
        "todos": 119,
        "dnTodos": 21.3
      },
      "kids200": {
        "total": 559,
        "pdvs": 553,
        "dn": 98.9
      },
      "spray170": {
        "total": 559,
        "pdvs": 119,
        "dn": 21.3
      },
      "locao200": {
        "total": 559,
        "pdvs": 553,
        "dn": 98.9
      }
    },
    "fytd26": {
      "soma": {
        "total": 559,
        "algum": 559,
        "dnAlgum": 100.0,
        "dois": 559,
        "dnDois": 100.0,
        "todos": 556,
        "dnTodos": 99.5
      },
      "kids200": {
        "total": 559,
        "pdvs": 559,
        "dn": 100.0
      },
      "spray170": {
        "total": 559,
        "pdvs": 556,
        "dn": 99.5
      },
      "locao200": {
        "total": 559,
        "pdvs": 559,
        "dn": 100.0
      }
    },
    "janabr25": {
      "soma": {
        "total": 559,
        "algum": 549,
        "dnAlgum": 98.2,
        "dois": 549,
        "dnDois": 98.2,
        "todos": 546,
        "dnTodos": 97.7
      },
      "kids200": {
        "total": 559,
        "pdvs": 549,
        "dn": 98.2
      },
      "spray170": {
        "total": 559,
        "pdvs": 546,
        "dn": 97.7
      },
      "locao200": {
        "total": 559,
        "pdvs": 549,
        "dn": 98.2
      }
    },
    "janabr26": {
      "soma": {
        "total": 559,
        "algum": 557,
        "dnAlgum": 99.6,
        "dois": 557,
        "dnDois": 99.6,
        "todos": 556,
        "dnTodos": 99.5
      },
      "kids200": {
        "total": 559,
        "pdvs": 557,
        "dn": 99.6
      },
      "spray170": {
        "total": 559,
        "pdvs": 556,
        "dn": 99.5
      },
      "locao200": {
        "total": 559,
        "pdvs": 557,
        "dn": 99.6
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 559,
          "algum": 554,
          "dnAlgum": 99.1,
          "dois": 554,
          "dnDois": 99.1,
          "todos": 551,
          "dnTodos": 98.6
        },
        "kids200": {
          "total": 559,
          "pdvs": 554,
          "dn": 99.1
        },
        "spray170": {
          "total": 559,
          "pdvs": 551,
          "dn": 98.6
        },
        "locao200": {
          "total": 559,
          "pdvs": 554,
          "dn": 99.1
        }
      },
      "202508": {
        "soma": {
          "total": 559,
          "algum": 551,
          "dnAlgum": 98.6,
          "dois": 551,
          "dnDois": 98.6,
          "todos": 548,
          "dnTodos": 98.0
        },
        "kids200": {
          "total": 559,
          "pdvs": 551,
          "dn": 98.6
        },
        "spray170": {
          "total": 559,
          "pdvs": 548,
          "dn": 98.0
        },
        "locao200": {
          "total": 559,
          "pdvs": 551,
          "dn": 98.6
        }
      },
      "202509": {
        "soma": {
          "total": 559,
          "algum": 554,
          "dnAlgum": 99.1,
          "dois": 554,
          "dnDois": 99.1,
          "todos": 551,
          "dnTodos": 98.6
        },
        "kids200": {
          "total": 559,
          "pdvs": 554,
          "dn": 99.1
        },
        "spray170": {
          "total": 559,
          "pdvs": 551,
          "dn": 98.6
        },
        "locao200": {
          "total": 559,
          "pdvs": 554,
          "dn": 99.1
        }
      },
      "202510": {
        "soma": {
          "total": 559,
          "algum": 554,
          "dnAlgum": 99.1,
          "dois": 554,
          "dnDois": 99.1,
          "todos": 551,
          "dnTodos": 98.6
        },
        "kids200": {
          "total": 559,
          "pdvs": 554,
          "dn": 99.1
        },
        "spray170": {
          "total": 559,
          "pdvs": 551,
          "dn": 98.6
        },
        "locao200": {
          "total": 559,
          "pdvs": 554,
          "dn": 99.1
        }
      },
      "202511": {
        "soma": {
          "total": 559,
          "algum": 555,
          "dnAlgum": 99.3,
          "dois": 555,
          "dnDois": 99.3,
          "todos": 552,
          "dnTodos": 98.7
        },
        "kids200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        },
        "spray170": {
          "total": 559,
          "pdvs": 552,
          "dn": 98.7
        },
        "locao200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        }
      },
      "202512": {
        "soma": {
          "total": 559,
          "algum": 555,
          "dnAlgum": 99.3,
          "dois": 555,
          "dnDois": 99.3,
          "todos": 552,
          "dnTodos": 98.7
        },
        "kids200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        },
        "spray170": {
          "total": 559,
          "pdvs": 552,
          "dn": 98.7
        },
        "locao200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        }
      },
      "202601": {
        "soma": {
          "total": 559,
          "algum": 555,
          "dnAlgum": 99.3,
          "dois": 555,
          "dnDois": 99.3,
          "todos": 552,
          "dnTodos": 98.7
        },
        "kids200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        },
        "spray170": {
          "total": 559,
          "pdvs": 552,
          "dn": 98.7
        },
        "locao200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        }
      },
      "202602": {
        "soma": {
          "total": 559,
          "algum": 555,
          "dnAlgum": 99.3,
          "dois": 555,
          "dnDois": 99.3,
          "todos": 552,
          "dnTodos": 98.7
        },
        "kids200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        },
        "spray170": {
          "total": 559,
          "pdvs": 552,
          "dn": 98.7
        },
        "locao200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        }
      },
      "202603": {
        "soma": {
          "total": 559,
          "algum": 555,
          "dnAlgum": 99.3,
          "dois": 555,
          "dnDois": 99.3,
          "todos": 552,
          "dnTodos": 98.7
        },
        "kids200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        },
        "spray170": {
          "total": 559,
          "pdvs": 552,
          "dn": 98.7
        },
        "locao200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        }
      },
      "202604": {
        "soma": {
          "total": 559,
          "algum": 555,
          "dnAlgum": 99.3,
          "dois": 555,
          "dnDois": 99.3,
          "todos": 552,
          "dnTodos": 98.7
        },
        "kids200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        },
        "spray170": {
          "total": 559,
          "pdvs": 552,
          "dn": 98.7
        },
        "locao200": {
          "total": 559,
          "pdvs": 555,
          "dn": 99.3
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 558,
          "pdvs": 434,
          "dn": 77.8
        },
        "locao200": {
          "total": 558,
          "pdvs": 503,
          "dn": 90.1
        },
        "spray170": {
          "total": 558,
          "pdvs": 408,
          "dn": 73.1
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 558,
        "pdvs": 497,
        "dn": 89.1
      },
      "locao200": {
        "total": 558,
        "pdvs": 540,
        "dn": 96.8
      },
      "spray170": {
        "total": 558,
        "pdvs": 486,
        "dn": 87.1
      }
    }
  },
  "PAGUE MENOS": {
    "fytd25": {
      "soma": {
        "total": 1345,
        "algum": 1312,
        "dnAlgum": 97.5,
        "dois": 1312,
        "dnDois": 97.5,
        "todos": 2,
        "dnTodos": 0.1
      },
      "kids200": {
        "total": 1345,
        "pdvs": 1312,
        "dn": 97.5
      },
      "spray170": {
        "total": 1345,
        "pdvs": 2,
        "dn": 0.1
      },
      "locao200": {
        "total": 1345,
        "pdvs": 1312,
        "dn": 97.5
      }
    },
    "fytd26": {
      "soma": {
        "total": 1345,
        "algum": 1344,
        "dnAlgum": 99.9,
        "dois": 1344,
        "dnDois": 99.9,
        "todos": 1315,
        "dnTodos": 97.8
      },
      "kids200": {
        "total": 1345,
        "pdvs": 1344,
        "dn": 99.9
      },
      "spray170": {
        "total": 1345,
        "pdvs": 1344,
        "dn": 99.9
      },
      "locao200": {
        "total": 1345,
        "pdvs": 1315,
        "dn": 97.8
      }
    },
    "janabr25": {
      "soma": {
        "total": 1345,
        "algum": 1335,
        "dnAlgum": 99.3,
        "dois": 1335,
        "dnDois": 99.3,
        "todos": 1306,
        "dnTodos": 97.1
      },
      "kids200": {
        "total": 1345,
        "pdvs": 1306,
        "dn": 97.1
      },
      "spray170": {
        "total": 1345,
        "pdvs": 1335,
        "dn": 99.3
      },
      "locao200": {
        "total": 1345,
        "pdvs": 1306,
        "dn": 97.1
      }
    },
    "janabr26": {
      "soma": {
        "total": 1345,
        "algum": 1344,
        "dnAlgum": 99.9,
        "dois": 1344,
        "dnDois": 99.9,
        "todos": 1314,
        "dnTodos": 97.7
      },
      "kids200": {
        "total": 1345,
        "pdvs": 1314,
        "dn": 97.7
      },
      "spray170": {
        "total": 1345,
        "pdvs": 1344,
        "dn": 99.9
      },
      "locao200": {
        "total": 1345,
        "pdvs": 1314,
        "dn": 97.7
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 1345,
          "algum": 1345,
          "dnAlgum": 100.0,
          "dois": 1345,
          "dnDois": 100.0,
          "todos": 1345,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "spray170": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "locao200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        }
      },
      "202508": {
        "soma": {
          "total": 1345,
          "algum": 1345,
          "dnAlgum": 100.0,
          "dois": 1345,
          "dnDois": 100.0,
          "todos": 1345,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "spray170": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "locao200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        }
      },
      "202509": {
        "soma": {
          "total": 1345,
          "algum": 1345,
          "dnAlgum": 100.0,
          "dois": 1345,
          "dnDois": 100.0,
          "todos": 1345,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "spray170": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "locao200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        }
      },
      "202510": {
        "soma": {
          "total": 1345,
          "algum": 1345,
          "dnAlgum": 100.0,
          "dois": 1345,
          "dnDois": 100.0,
          "todos": 1345,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "spray170": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "locao200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        }
      },
      "202511": {
        "soma": {
          "total": 1345,
          "algum": 1345,
          "dnAlgum": 100.0,
          "dois": 1345,
          "dnDois": 100.0,
          "todos": 1345,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "spray170": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "locao200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        }
      },
      "202512": {
        "soma": {
          "total": 1345,
          "algum": 1345,
          "dnAlgum": 100.0,
          "dois": 1345,
          "dnDois": 100.0,
          "todos": 1345,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "spray170": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "locao200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        }
      },
      "202601": {
        "soma": {
          "total": 1345,
          "algum": 1345,
          "dnAlgum": 100.0,
          "dois": 1345,
          "dnDois": 100.0,
          "todos": 1345,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "spray170": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "locao200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        }
      },
      "202602": {
        "soma": {
          "total": 1345,
          "algum": 1345,
          "dnAlgum": 100.0,
          "dois": 1345,
          "dnDois": 100.0,
          "todos": 1345,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "spray170": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "locao200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        }
      },
      "202603": {
        "soma": {
          "total": 1345,
          "algum": 1345,
          "dnAlgum": 100.0,
          "dois": 1345,
          "dnDois": 100.0,
          "todos": 1345,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "spray170": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "locao200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        }
      },
      "202604": {
        "soma": {
          "total": 1345,
          "algum": 1345,
          "dnAlgum": 100.0,
          "dois": 1345,
          "dnDois": 100.0,
          "todos": 1345,
          "dnTodos": 100.0
        },
        "kids200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "spray170": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        },
        "locao200": {
          "total": 1345,
          "pdvs": 1345,
          "dn": 100.0
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 1357,
          "pdvs": 1068,
          "dn": 78.7
        },
        "locao200": {
          "total": 1357,
          "pdvs": 1187,
          "dn": 87.5
        },
        "spray170": {
          "total": 1357,
          "pdvs": 859,
          "dn": 63.3
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 1357,
        "pdvs": 1200,
        "dn": 88.4
      },
      "locao200": {
        "total": 1357,
        "pdvs": 1304,
        "dn": 96.1
      },
      "spray170": {
        "total": 1357,
        "pdvs": 1145,
        "dn": 84.4
      }
    }
  },
  "PANVEL": {
    "fytd25": {
      "soma": {
        "total": 662,
        "algum": 622,
        "dnAlgum": 94.0,
        "dois": 622,
        "dnDois": 94.0,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 662,
        "pdvs": 622,
        "dn": 94.0
      },
      "spray170": {
        "total": 662,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 662,
        "pdvs": 622,
        "dn": 94.0
      }
    },
    "fytd26": {
      "soma": {
        "total": 662,
        "algum": 654,
        "dnAlgum": 98.8,
        "dois": 654,
        "dnDois": 98.8,
        "todos": 649,
        "dnTodos": 98.0
      },
      "kids200": {
        "total": 662,
        "pdvs": 649,
        "dn": 98.0
      },
      "spray170": {
        "total": 662,
        "pdvs": 650,
        "dn": 98.2
      },
      "locao200": {
        "total": 662,
        "pdvs": 654,
        "dn": 98.8
      }
    },
    "janabr25": {
      "soma": {
        "total": 662,
        "algum": 621,
        "dnAlgum": 93.8,
        "dois": 621,
        "dnDois": 93.8,
        "todos": 617,
        "dnTodos": 93.2
      },
      "kids200": {
        "total": 662,
        "pdvs": 621,
        "dn": 93.8
      },
      "spray170": {
        "total": 662,
        "pdvs": 617,
        "dn": 93.2
      },
      "locao200": {
        "total": 662,
        "pdvs": 621,
        "dn": 93.8
      }
    },
    "janabr26": {
      "soma": {
        "total": 662,
        "algum": 650,
        "dnAlgum": 98.2,
        "dois": 650,
        "dnDois": 98.2,
        "todos": 645,
        "dnTodos": 97.4
      },
      "kids200": {
        "total": 662,
        "pdvs": 645,
        "dn": 97.4
      },
      "spray170": {
        "total": 662,
        "pdvs": 650,
        "dn": 98.2
      },
      "locao200": {
        "total": 662,
        "pdvs": 645,
        "dn": 97.4
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 662,
          "algum": 473,
          "dnAlgum": 71.5,
          "dois": 473,
          "dnDois": 71.5,
          "todos": 470,
          "dnTodos": 71.0
        },
        "kids200": {
          "total": 662,
          "pdvs": 473,
          "dn": 71.5
        },
        "spray170": {
          "total": 662,
          "pdvs": 470,
          "dn": 71.0
        },
        "locao200": {
          "total": 662,
          "pdvs": 473,
          "dn": 71.5
        }
      },
      "202508": {
        "soma": {
          "total": 662,
          "algum": 487,
          "dnAlgum": 73.6,
          "dois": 487,
          "dnDois": 73.6,
          "todos": 484,
          "dnTodos": 73.1
        },
        "kids200": {
          "total": 662,
          "pdvs": 487,
          "dn": 73.6
        },
        "spray170": {
          "total": 662,
          "pdvs": 484,
          "dn": 73.1
        },
        "locao200": {
          "total": 662,
          "pdvs": 487,
          "dn": 73.6
        }
      },
      "202509": {
        "soma": {
          "total": 662,
          "algum": 595,
          "dnAlgum": 89.9,
          "dois": 595,
          "dnDois": 89.9,
          "todos": 591,
          "dnTodos": 89.3
        },
        "kids200": {
          "total": 662,
          "pdvs": 595,
          "dn": 89.9
        },
        "spray170": {
          "total": 662,
          "pdvs": 591,
          "dn": 89.3
        },
        "locao200": {
          "total": 662,
          "pdvs": 595,
          "dn": 89.9
        }
      },
      "202510": {
        "soma": {
          "total": 662,
          "algum": 631,
          "dnAlgum": 95.3,
          "dois": 631,
          "dnDois": 95.3,
          "todos": 627,
          "dnTodos": 94.7
        },
        "kids200": {
          "total": 662,
          "pdvs": 631,
          "dn": 95.3
        },
        "spray170": {
          "total": 662,
          "pdvs": 627,
          "dn": 94.7
        },
        "locao200": {
          "total": 662,
          "pdvs": 631,
          "dn": 95.3
        }
      },
      "202511": {
        "soma": {
          "total": 662,
          "algum": 652,
          "dnAlgum": 98.5,
          "dois": 652,
          "dnDois": 98.5,
          "todos": 648,
          "dnTodos": 97.9
        },
        "kids200": {
          "total": 662,
          "pdvs": 652,
          "dn": 98.5
        },
        "spray170": {
          "total": 662,
          "pdvs": 648,
          "dn": 97.9
        },
        "locao200": {
          "total": 662,
          "pdvs": 652,
          "dn": 98.5
        }
      },
      "202512": {
        "soma": {
          "total": 662,
          "algum": 654,
          "dnAlgum": 98.8,
          "dois": 654,
          "dnDois": 98.8,
          "todos": 650,
          "dnTodos": 98.2
        },
        "kids200": {
          "total": 662,
          "pdvs": 654,
          "dn": 98.8
        },
        "spray170": {
          "total": 662,
          "pdvs": 650,
          "dn": 98.2
        },
        "locao200": {
          "total": 662,
          "pdvs": 654,
          "dn": 98.8
        }
      },
      "202601": {
        "soma": {
          "total": 662,
          "algum": 650,
          "dnAlgum": 98.2,
          "dois": 650,
          "dnDois": 98.2,
          "todos": 646,
          "dnTodos": 97.6
        },
        "kids200": {
          "total": 662,
          "pdvs": 650,
          "dn": 98.2
        },
        "spray170": {
          "total": 662,
          "pdvs": 646,
          "dn": 97.6
        },
        "locao200": {
          "total": 662,
          "pdvs": 650,
          "dn": 98.2
        }
      },
      "202602": {
        "soma": {
          "total": 662,
          "algum": 650,
          "dnAlgum": 98.2,
          "dois": 650,
          "dnDois": 98.2,
          "todos": 646,
          "dnTodos": 97.6
        },
        "kids200": {
          "total": 662,
          "pdvs": 650,
          "dn": 98.2
        },
        "spray170": {
          "total": 662,
          "pdvs": 646,
          "dn": 97.6
        },
        "locao200": {
          "total": 662,
          "pdvs": 650,
          "dn": 98.2
        }
      },
      "202603": {
        "soma": {
          "total": 662,
          "algum": 648,
          "dnAlgum": 97.9,
          "dois": 648,
          "dnDois": 97.9,
          "todos": 644,
          "dnTodos": 97.3
        },
        "kids200": {
          "total": 662,
          "pdvs": 648,
          "dn": 97.9
        },
        "spray170": {
          "total": 662,
          "pdvs": 644,
          "dn": 97.3
        },
        "locao200": {
          "total": 662,
          "pdvs": 648,
          "dn": 97.9
        }
      },
      "202604": {
        "soma": {
          "total": 650,
          "algum": 644,
          "dnAlgum": 99.1,
          "dois": 644,
          "dnDois": 99.1,
          "todos": 641,
          "dnTodos": 98.6
        },
        "kids200": {
          "total": 650,
          "pdvs": 641,
          "dn": 98.6
        },
        "spray170": {
          "total": 650,
          "pdvs": 643,
          "dn": 98.9
        },
        "locao200": {
          "total": 650,
          "pdvs": 644,
          "dn": 99.1
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 627,
          "pdvs": 252,
          "dn": 40.2
        },
        "locao200": {
          "total": 627,
          "pdvs": 295,
          "dn": 47.0
        },
        "spray170": {
          "total": 627,
          "pdvs": 259,
          "dn": 41.3
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 656,
        "pdvs": 320,
        "dn": 48.8
      },
      "locao200": {
        "total": 656,
        "pdvs": 379,
        "dn": 57.8
      },
      "spray170": {
        "total": 656,
        "pdvs": 351,
        "dn": 53.5
      }
    }
  },
  "PRECO POPULAR": {
    "fytd25": {
      "soma": {
        "total": 575,
        "algum": 504,
        "dnAlgum": 87.7,
        "dois": 504,
        "dnDois": 87.7,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 575,
        "pdvs": 504,
        "dn": 87.7
      },
      "spray170": {
        "total": 575,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 575,
        "pdvs": 504,
        "dn": 87.7
      }
    },
    "fytd26": {
      "soma": {
        "total": 575,
        "algum": 575,
        "dnAlgum": 100.0,
        "dois": 575,
        "dnDois": 100.0,
        "todos": 568,
        "dnTodos": 98.8
      },
      "kids200": {
        "total": 575,
        "pdvs": 575,
        "dn": 100.0
      },
      "spray170": {
        "total": 575,
        "pdvs": 568,
        "dn": 98.8
      },
      "locao200": {
        "total": 575,
        "pdvs": 573,
        "dn": 99.7
      }
    },
    "janabr25": {
      "soma": {
        "total": 575,
        "algum": 503,
        "dnAlgum": 87.5,
        "dois": 503,
        "dnDois": 87.5,
        "todos": 499,
        "dnTodos": 86.8
      },
      "kids200": {
        "total": 575,
        "pdvs": 503,
        "dn": 87.5
      },
      "spray170": {
        "total": 575,
        "pdvs": 499,
        "dn": 86.8
      },
      "locao200": {
        "total": 575,
        "pdvs": 503,
        "dn": 87.5
      }
    },
    "janabr26": {
      "soma": {
        "total": 575,
        "algum": 568,
        "dnAlgum": 98.8,
        "dois": 568,
        "dnDois": 98.8,
        "todos": 567,
        "dnTodos": 98.6
      },
      "kids200": {
        "total": 575,
        "pdvs": 567,
        "dn": 98.6
      },
      "spray170": {
        "total": 575,
        "pdvs": 568,
        "dn": 98.8
      },
      "locao200": {
        "total": 575,
        "pdvs": 567,
        "dn": 98.6
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 575,
          "algum": 9,
          "dnAlgum": 1.6,
          "dois": 9,
          "dnDois": 1.6,
          "todos": 9,
          "dnTodos": 1.6
        },
        "kids200": {
          "total": 575,
          "pdvs": 9,
          "dn": 1.6
        },
        "spray170": {
          "total": 575,
          "pdvs": 9,
          "dn": 1.6
        },
        "locao200": {
          "total": 575,
          "pdvs": 9,
          "dn": 1.6
        }
      },
      "202508": {
        "soma": {
          "total": 575,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 575,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 575,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 575,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 578,
          "algum": 311,
          "dnAlgum": 53.8,
          "dois": 311,
          "dnDois": 53.8,
          "todos": 220,
          "dnTodos": 38.1
        },
        "kids200": {
          "total": 578,
          "pdvs": 301,
          "dn": 52.1
        },
        "spray170": {
          "total": 578,
          "pdvs": 311,
          "dn": 53.8
        },
        "locao200": {
          "total": 578,
          "pdvs": 220,
          "dn": 38.1
        }
      },
      "202510": {
        "soma": {
          "total": 578,
          "algum": 455,
          "dnAlgum": 78.7,
          "dois": 455,
          "dnDois": 78.7,
          "todos": 264,
          "dnTodos": 45.7
        },
        "kids200": {
          "total": 578,
          "pdvs": 348,
          "dn": 60.2
        },
        "spray170": {
          "total": 578,
          "pdvs": 264,
          "dn": 45.7
        },
        "locao200": {
          "total": 578,
          "pdvs": 455,
          "dn": 78.7
        }
      },
      "202511": {
        "soma": {
          "total": 578,
          "algum": 454,
          "dnAlgum": 78.5,
          "dois": 454,
          "dnDois": 78.5,
          "todos": 343,
          "dnTodos": 59.3
        },
        "kids200": {
          "total": 578,
          "pdvs": 454,
          "dn": 78.5
        },
        "spray170": {
          "total": 578,
          "pdvs": 416,
          "dn": 72.0
        },
        "locao200": {
          "total": 578,
          "pdvs": 343,
          "dn": 59.3
        }
      },
      "202512": {
        "soma": {
          "total": 578,
          "algum": 543,
          "dnAlgum": 93.9,
          "dois": 543,
          "dnDois": 93.9,
          "todos": 483,
          "dnTodos": 83.6
        },
        "kids200": {
          "total": 578,
          "pdvs": 543,
          "dn": 93.9
        },
        "spray170": {
          "total": 578,
          "pdvs": 543,
          "dn": 93.9
        },
        "locao200": {
          "total": 578,
          "pdvs": 483,
          "dn": 83.6
        }
      },
      "202601": {
        "soma": {
          "total": 578,
          "algum": 537,
          "dnAlgum": 92.9,
          "dois": 537,
          "dnDois": 92.9,
          "todos": 460,
          "dnTodos": 79.6
        },
        "kids200": {
          "total": 578,
          "pdvs": 537,
          "dn": 92.9
        },
        "spray170": {
          "total": 578,
          "pdvs": 460,
          "dn": 79.6
        },
        "locao200": {
          "total": 578,
          "pdvs": 491,
          "dn": 84.9
        }
      },
      "202602": {
        "soma": {
          "total": 578,
          "algum": 529,
          "dnAlgum": 91.5,
          "dois": 529,
          "dnDois": 91.5,
          "todos": 475,
          "dnTodos": 82.2
        },
        "kids200": {
          "total": 578,
          "pdvs": 529,
          "dn": 91.5
        },
        "spray170": {
          "total": 578,
          "pdvs": 518,
          "dn": 89.6
        },
        "locao200": {
          "total": 578,
          "pdvs": 475,
          "dn": 82.2
        }
      },
      "202603": {
        "soma": {
          "total": 578,
          "algum": 502,
          "dnAlgum": 86.9,
          "dois": 502,
          "dnDois": 86.9,
          "todos": 445,
          "dnTodos": 77.0
        },
        "kids200": {
          "total": 578,
          "pdvs": 502,
          "dn": 86.9
        },
        "spray170": {
          "total": 578,
          "pdvs": 466,
          "dn": 80.6
        },
        "locao200": {
          "total": 578,
          "pdvs": 445,
          "dn": 77.0
        }
      },
      "202604": {
        "soma": {
          "total": 578,
          "algum": 571,
          "dnAlgum": 98.8,
          "dois": 571,
          "dnDois": 98.8,
          "todos": 550,
          "dnTodos": 95.2
        },
        "kids200": {
          "total": 578,
          "pdvs": 568,
          "dn": 98.3
        },
        "spray170": {
          "total": 578,
          "pdvs": 550,
          "dn": 95.2
        },
        "locao200": {
          "total": 578,
          "pdvs": 571,
          "dn": 98.8
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 544,
          "pdvs": 201,
          "dn": 36.9
        },
        "locao200": {
          "total": 544,
          "pdvs": 261,
          "dn": 48.0
        },
        "spray170": {
          "total": 544,
          "pdvs": 179,
          "dn": 32.9
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 555,
        "pdvs": 255,
        "dn": 45.9
      },
      "locao200": {
        "total": 555,
        "pdvs": 333,
        "dn": 60.0
      },
      "spray170": {
        "total": 555,
        "pdvs": 252,
        "dn": 45.4
      }
    }
  },
  "RAIA": {
    "fytd25": {
      "soma": {
        "total": 1496,
        "algum": 1374,
        "dnAlgum": 91.8,
        "dois": 1374,
        "dnDois": 91.8,
        "todos": 3,
        "dnTodos": 0.2
      },
      "kids200": {
        "total": 1496,
        "pdvs": 1374,
        "dn": 91.8
      },
      "spray170": {
        "total": 1496,
        "pdvs": 3,
        "dn": 0.2
      },
      "locao200": {
        "total": 1496,
        "pdvs": 1374,
        "dn": 91.8
      }
    },
    "fytd26": {
      "soma": {
        "total": 1496,
        "algum": 1488,
        "dnAlgum": 99.5,
        "dois": 1488,
        "dnDois": 99.5,
        "todos": 1484,
        "dnTodos": 99.2
      },
      "kids200": {
        "total": 1496,
        "pdvs": 1488,
        "dn": 99.5
      },
      "spray170": {
        "total": 1496,
        "pdvs": 1487,
        "dn": 99.4
      },
      "locao200": {
        "total": 1496,
        "pdvs": 1484,
        "dn": 99.2
      }
    },
    "janabr25": {
      "soma": {
        "total": 1496,
        "algum": 1368,
        "dnAlgum": 91.4,
        "dois": 1368,
        "dnDois": 91.4,
        "todos": 1365,
        "dnTodos": 91.2
      },
      "kids200": {
        "total": 1496,
        "pdvs": 1365,
        "dn": 91.2
      },
      "spray170": {
        "total": 1496,
        "pdvs": 1368,
        "dn": 91.4
      },
      "locao200": {
        "total": 1496,
        "pdvs": 1365,
        "dn": 91.2
      }
    },
    "janabr26": {
      "soma": {
        "total": 1496,
        "algum": 1487,
        "dnAlgum": 99.4,
        "dois": 1487,
        "dnDois": 99.4,
        "todos": 1482,
        "dnTodos": 99.1
      },
      "kids200": {
        "total": 1496,
        "pdvs": 1482,
        "dn": 99.1
      },
      "spray170": {
        "total": 1496,
        "pdvs": 1487,
        "dn": 99.4
      },
      "locao200": {
        "total": 1496,
        "pdvs": 1482,
        "dn": 99.1
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 1496,
          "algum": 268,
          "dnAlgum": 17.9,
          "dois": 268,
          "dnDois": 17.9,
          "todos": 267,
          "dnTodos": 17.8
        },
        "kids200": {
          "total": 1496,
          "pdvs": 267,
          "dn": 17.8
        },
        "spray170": {
          "total": 1496,
          "pdvs": 268,
          "dn": 17.9
        },
        "locao200": {
          "total": 1496,
          "pdvs": 267,
          "dn": 17.8
        }
      },
      "202508": {
        "soma": {
          "total": 1496,
          "algum": 32,
          "dnAlgum": 2.1,
          "dois": 32,
          "dnDois": 2.1,
          "todos": 32,
          "dnTodos": 2.1
        },
        "kids200": {
          "total": 1496,
          "pdvs": 32,
          "dn": 2.1
        },
        "spray170": {
          "total": 1496,
          "pdvs": 32,
          "dn": 2.1
        },
        "locao200": {
          "total": 1496,
          "pdvs": 32,
          "dn": 2.1
        }
      },
      "202509": {
        "soma": {
          "total": 1496,
          "algum": 207,
          "dnAlgum": 13.8,
          "dois": 207,
          "dnDois": 13.8,
          "todos": 207,
          "dnTodos": 13.8
        },
        "kids200": {
          "total": 1496,
          "pdvs": 207,
          "dn": 13.8
        },
        "spray170": {
          "total": 1496,
          "pdvs": 207,
          "dn": 13.8
        },
        "locao200": {
          "total": 1496,
          "pdvs": 207,
          "dn": 13.8
        }
      },
      "202510": {
        "soma": {
          "total": 1496,
          "algum": 406,
          "dnAlgum": 27.1,
          "dois": 406,
          "dnDois": 27.1,
          "todos": 405,
          "dnTodos": 27.1
        },
        "kids200": {
          "total": 1496,
          "pdvs": 405,
          "dn": 27.1
        },
        "spray170": {
          "total": 1496,
          "pdvs": 406,
          "dn": 27.1
        },
        "locao200": {
          "total": 1496,
          "pdvs": 405,
          "dn": 27.1
        }
      },
      "202511": {
        "soma": {
          "total": 1496,
          "algum": 903,
          "dnAlgum": 60.4,
          "dois": 903,
          "dnDois": 60.4,
          "todos": 901,
          "dnTodos": 60.2
        },
        "kids200": {
          "total": 1496,
          "pdvs": 901,
          "dn": 60.2
        },
        "spray170": {
          "total": 1496,
          "pdvs": 903,
          "dn": 60.4
        },
        "locao200": {
          "total": 1496,
          "pdvs": 901,
          "dn": 60.2
        }
      },
      "202512": {
        "soma": {
          "total": 1496,
          "algum": 1103,
          "dnAlgum": 73.7,
          "dois": 1103,
          "dnDois": 73.7,
          "todos": 1101,
          "dnTodos": 73.6
        },
        "kids200": {
          "total": 1496,
          "pdvs": 1101,
          "dn": 73.6
        },
        "spray170": {
          "total": 1496,
          "pdvs": 1103,
          "dn": 73.7
        },
        "locao200": {
          "total": 1496,
          "pdvs": 1101,
          "dn": 73.6
        }
      },
      "202601": {
        "soma": {
          "total": 1496,
          "algum": 1191,
          "dnAlgum": 79.6,
          "dois": 1191,
          "dnDois": 79.6,
          "todos": 1189,
          "dnTodos": 79.5
        },
        "kids200": {
          "total": 1496,
          "pdvs": 1189,
          "dn": 79.5
        },
        "spray170": {
          "total": 1496,
          "pdvs": 1191,
          "dn": 79.6
        },
        "locao200": {
          "total": 1496,
          "pdvs": 1189,
          "dn": 79.5
        }
      },
      "202602": {
        "soma": {
          "total": 1496,
          "algum": 1466,
          "dnAlgum": 98.0,
          "dois": 1466,
          "dnDois": 98.0,
          "todos": 1463,
          "dnTodos": 97.8
        },
        "kids200": {
          "total": 1496,
          "pdvs": 1463,
          "dn": 97.8
        },
        "spray170": {
          "total": 1496,
          "pdvs": 1466,
          "dn": 98.0
        },
        "locao200": {
          "total": 1496,
          "pdvs": 1463,
          "dn": 97.8
        }
      },
      "202603": {
        "soma": {
          "total": 1496,
          "algum": 1474,
          "dnAlgum": 98.5,
          "dois": 1474,
          "dnDois": 98.5,
          "todos": 1471,
          "dnTodos": 98.3
        },
        "kids200": {
          "total": 1496,
          "pdvs": 1471,
          "dn": 98.3
        },
        "spray170": {
          "total": 1496,
          "pdvs": 1474,
          "dn": 98.5
        },
        "locao200": {
          "total": 1496,
          "pdvs": 1471,
          "dn": 98.3
        }
      },
      "202604": {
        "soma": {
          "total": 1496,
          "algum": 1485,
          "dnAlgum": 99.3,
          "dois": 1485,
          "dnDois": 99.3,
          "todos": 1482,
          "dnTodos": 99.1
        },
        "kids200": {
          "total": 1496,
          "pdvs": 1482,
          "dn": 99.1
        },
        "spray170": {
          "total": 1496,
          "pdvs": 1485,
          "dn": 99.3
        },
        "locao200": {
          "total": 1496,
          "pdvs": 1482,
          "dn": 99.1
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 1520,
          "pdvs": 961,
          "dn": 63.2
        },
        "locao200": {
          "total": 1520,
          "pdvs": 1131,
          "dn": 74.4
        },
        "spray170": {
          "total": 1520,
          "pdvs": 936,
          "dn": 61.6
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 1534,
        "pdvs": 1155,
        "dn": 75.3
      },
      "locao200": {
        "total": 1534,
        "pdvs": 1289,
        "dn": 84.0
      },
      "spray170": {
        "total": 1534,
        "pdvs": 1164,
        "dn": 75.9
      }
    }
  },
  "REDEPHARMA": {
    "fytd25": {
      "soma": {
        "total": 106,
        "algum": 92,
        "dnAlgum": 86.8,
        "dois": 92,
        "dnDois": 86.8,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 106,
        "pdvs": 92,
        "dn": 86.8
      },
      "spray170": {
        "total": 106,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 106,
        "pdvs": 92,
        "dn": 86.8
      }
    },
    "fytd26": {
      "soma": {
        "total": 106,
        "algum": 106,
        "dnAlgum": 100.0,
        "dois": 106,
        "dnDois": 100.0,
        "todos": 104,
        "dnTodos": 98.1
      },
      "kids200": {
        "total": 106,
        "pdvs": 106,
        "dn": 100.0
      },
      "spray170": {
        "total": 106,
        "pdvs": 104,
        "dn": 98.1
      },
      "locao200": {
        "total": 106,
        "pdvs": 105,
        "dn": 99.1
      }
    },
    "janabr25": {
      "soma": {
        "total": 106,
        "algum": 90,
        "dnAlgum": 84.9,
        "dois": 90,
        "dnDois": 84.9,
        "todos": 89,
        "dnTodos": 84.0
      },
      "kids200": {
        "total": 106,
        "pdvs": 90,
        "dn": 84.9
      },
      "spray170": {
        "total": 106,
        "pdvs": 89,
        "dn": 84.0
      },
      "locao200": {
        "total": 106,
        "pdvs": 90,
        "dn": 84.9
      }
    },
    "janabr26": {
      "soma": {
        "total": 106,
        "algum": 104,
        "dnAlgum": 98.1,
        "dois": 104,
        "dnDois": 98.1,
        "todos": 104,
        "dnTodos": 98.1
      },
      "kids200": {
        "total": 106,
        "pdvs": 104,
        "dn": 98.1
      },
      "spray170": {
        "total": 106,
        "pdvs": 104,
        "dn": 98.1
      },
      "locao200": {
        "total": 106,
        "pdvs": 104,
        "dn": 98.1
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 106,
          "algum": 98,
          "dnAlgum": 92.5,
          "dois": 98,
          "dnDois": 92.5,
          "todos": 97,
          "dnTodos": 91.5
        },
        "kids200": {
          "total": 106,
          "pdvs": 98,
          "dn": 92.5
        },
        "spray170": {
          "total": 106,
          "pdvs": 97,
          "dn": 91.5
        },
        "locao200": {
          "total": 106,
          "pdvs": 98,
          "dn": 92.5
        }
      },
      "202508": {
        "soma": {
          "total": 106,
          "algum": 99,
          "dnAlgum": 93.4,
          "dois": 99,
          "dnDois": 93.4,
          "todos": 98,
          "dnTodos": 92.5
        },
        "kids200": {
          "total": 106,
          "pdvs": 99,
          "dn": 93.4
        },
        "spray170": {
          "total": 106,
          "pdvs": 98,
          "dn": 92.5
        },
        "locao200": {
          "total": 106,
          "pdvs": 99,
          "dn": 93.4
        }
      },
      "202509": {
        "soma": {
          "total": 106,
          "algum": 99,
          "dnAlgum": 93.4,
          "dois": 99,
          "dnDois": 93.4,
          "todos": 98,
          "dnTodos": 92.5
        },
        "kids200": {
          "total": 106,
          "pdvs": 99,
          "dn": 93.4
        },
        "spray170": {
          "total": 106,
          "pdvs": 98,
          "dn": 92.5
        },
        "locao200": {
          "total": 106,
          "pdvs": 99,
          "dn": 93.4
        }
      },
      "202510": {
        "soma": {
          "total": 106,
          "algum": 100,
          "dnAlgum": 94.3,
          "dois": 100,
          "dnDois": 94.3,
          "todos": 99,
          "dnTodos": 93.4
        },
        "kids200": {
          "total": 106,
          "pdvs": 100,
          "dn": 94.3
        },
        "spray170": {
          "total": 106,
          "pdvs": 99,
          "dn": 93.4
        },
        "locao200": {
          "total": 106,
          "pdvs": 100,
          "dn": 94.3
        }
      },
      "202511": {
        "soma": {
          "total": 106,
          "algum": 100,
          "dnAlgum": 94.3,
          "dois": 100,
          "dnDois": 94.3,
          "todos": 99,
          "dnTodos": 93.4
        },
        "kids200": {
          "total": 106,
          "pdvs": 100,
          "dn": 94.3
        },
        "spray170": {
          "total": 106,
          "pdvs": 99,
          "dn": 93.4
        },
        "locao200": {
          "total": 106,
          "pdvs": 100,
          "dn": 94.3
        }
      },
      "202512": {
        "soma": {
          "total": 106,
          "algum": 102,
          "dnAlgum": 96.2,
          "dois": 102,
          "dnDois": 96.2,
          "todos": 101,
          "dnTodos": 95.3
        },
        "kids200": {
          "total": 106,
          "pdvs": 102,
          "dn": 96.2
        },
        "spray170": {
          "total": 106,
          "pdvs": 101,
          "dn": 95.3
        },
        "locao200": {
          "total": 106,
          "pdvs": 102,
          "dn": 96.2
        }
      },
      "202601": {
        "soma": {
          "total": 106,
          "algum": 103,
          "dnAlgum": 97.2,
          "dois": 103,
          "dnDois": 97.2,
          "todos": 102,
          "dnTodos": 96.2
        },
        "kids200": {
          "total": 106,
          "pdvs": 103,
          "dn": 97.2
        },
        "spray170": {
          "total": 106,
          "pdvs": 102,
          "dn": 96.2
        },
        "locao200": {
          "total": 106,
          "pdvs": 103,
          "dn": 97.2
        }
      },
      "202602": {
        "soma": {
          "total": 106,
          "algum": 103,
          "dnAlgum": 97.2,
          "dois": 103,
          "dnDois": 97.2,
          "todos": 102,
          "dnTodos": 96.2
        },
        "kids200": {
          "total": 106,
          "pdvs": 103,
          "dn": 97.2
        },
        "spray170": {
          "total": 106,
          "pdvs": 102,
          "dn": 96.2
        },
        "locao200": {
          "total": 106,
          "pdvs": 103,
          "dn": 97.2
        }
      },
      "202603": {
        "soma": {
          "total": 106,
          "algum": 105,
          "dnAlgum": 99.1,
          "dois": 105,
          "dnDois": 99.1,
          "todos": 104,
          "dnTodos": 98.1
        },
        "kids200": {
          "total": 106,
          "pdvs": 105,
          "dn": 99.1
        },
        "spray170": {
          "total": 106,
          "pdvs": 104,
          "dn": 98.1
        },
        "locao200": {
          "total": 106,
          "pdvs": 105,
          "dn": 99.1
        }
      },
      "202604": {
        "soma": {
          "total": 106,
          "algum": 104,
          "dnAlgum": 98.1,
          "dois": 104,
          "dnDois": 98.1,
          "todos": 103,
          "dnTodos": 97.2
        },
        "kids200": {
          "total": 106,
          "pdvs": 104,
          "dn": 98.1
        },
        "spray170": {
          "total": 106,
          "pdvs": 103,
          "dn": 97.2
        },
        "locao200": {
          "total": 106,
          "pdvs": 104,
          "dn": 98.1
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 110,
          "pdvs": 100,
          "dn": 90.9
        },
        "locao200": {
          "total": 110,
          "pdvs": 99,
          "dn": 90.0
        },
        "spray170": {
          "total": 110,
          "pdvs": 81,
          "dn": 73.6
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 110,
        "pdvs": 105,
        "dn": 95.5
      },
      "locao200": {
        "total": 110,
        "pdvs": 105,
        "dn": 95.5
      },
      "spray170": {
        "total": 110,
        "pdvs": 103,
        "dn": 93.6
      }
    }
  },
  "SAO JOAO FARMACIAS": {
    "fytd25": {
      "soma": {
        "total": 1257,
        "algum": 1159,
        "dnAlgum": 92.2,
        "dois": 1159,
        "dnDois": 92.2,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 1257,
        "pdvs": 1159,
        "dn": 92.2
      },
      "spray170": {
        "total": 1257,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 1257,
        "pdvs": 1159,
        "dn": 92.2
      }
    },
    "fytd26": {
      "soma": {
        "total": 1257,
        "algum": 1215,
        "dnAlgum": 96.7,
        "dois": 1215,
        "dnDois": 96.7,
        "todos": 1200,
        "dnTodos": 95.5
      },
      "kids200": {
        "total": 1257,
        "pdvs": 1215,
        "dn": 96.7
      },
      "spray170": {
        "total": 1257,
        "pdvs": 1209,
        "dn": 96.2
      },
      "locao200": {
        "total": 1257,
        "pdvs": 1200,
        "dn": 95.5
      }
    },
    "janabr25": {
      "soma": {
        "total": 1257,
        "algum": 1168,
        "dnAlgum": 92.9,
        "dois": 1168,
        "dnDois": 92.9,
        "todos": 1159,
        "dnTodos": 92.2
      },
      "kids200": {
        "total": 1257,
        "pdvs": 1159,
        "dn": 92.2
      },
      "spray170": {
        "total": 1257,
        "pdvs": 1168,
        "dn": 92.9
      },
      "locao200": {
        "total": 1257,
        "pdvs": 1159,
        "dn": 92.2
      }
    },
    "janabr26": {
      "soma": {
        "total": 1257,
        "algum": 1209,
        "dnAlgum": 96.2,
        "dois": 1209,
        "dnDois": 96.2,
        "todos": 1193,
        "dnTodos": 94.9
      },
      "kids200": {
        "total": 1257,
        "pdvs": 1193,
        "dn": 94.9
      },
      "spray170": {
        "total": 1257,
        "pdvs": 1209,
        "dn": 96.2
      },
      "locao200": {
        "total": 1257,
        "pdvs": 1193,
        "dn": 94.9
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 1257,
          "algum": 1073,
          "dnAlgum": 85.4,
          "dois": 1073,
          "dnDois": 85.4,
          "todos": 1065,
          "dnTodos": 84.7
        },
        "kids200": {
          "total": 1257,
          "pdvs": 1065,
          "dn": 84.7
        },
        "spray170": {
          "total": 1257,
          "pdvs": 1073,
          "dn": 85.4
        },
        "locao200": {
          "total": 1257,
          "pdvs": 1065,
          "dn": 84.7
        }
      },
      "202508": {
        "soma": {
          "total": 1257,
          "algum": 1070,
          "dnAlgum": 85.1,
          "dois": 1070,
          "dnDois": 85.1,
          "todos": 1062,
          "dnTodos": 84.5
        },
        "kids200": {
          "total": 1257,
          "pdvs": 1062,
          "dn": 84.5
        },
        "spray170": {
          "total": 1257,
          "pdvs": 1070,
          "dn": 85.1
        },
        "locao200": {
          "total": 1257,
          "pdvs": 1062,
          "dn": 84.5
        }
      },
      "202509": {
        "soma": {
          "total": 1257,
          "algum": 1135,
          "dnAlgum": 90.3,
          "dois": 1135,
          "dnDois": 90.3,
          "todos": 1127,
          "dnTodos": 89.7
        },
        "kids200": {
          "total": 1257,
          "pdvs": 1127,
          "dn": 89.7
        },
        "spray170": {
          "total": 1257,
          "pdvs": 1135,
          "dn": 90.3
        },
        "locao200": {
          "total": 1257,
          "pdvs": 1127,
          "dn": 89.7
        }
      },
      "202510": {
        "soma": {
          "total": 1257,
          "algum": 1218,
          "dnAlgum": 96.9,
          "dois": 1218,
          "dnDois": 96.9,
          "todos": 1209,
          "dnTodos": 96.2
        },
        "kids200": {
          "total": 1257,
          "pdvs": 1209,
          "dn": 96.2
        },
        "spray170": {
          "total": 1257,
          "pdvs": 1218,
          "dn": 96.9
        },
        "locao200": {
          "total": 1257,
          "pdvs": 1209,
          "dn": 96.2
        }
      },
      "202511": {
        "soma": {
          "total": 1257,
          "algum": 1227,
          "dnAlgum": 97.6,
          "dois": 1227,
          "dnDois": 97.6,
          "todos": 1218,
          "dnTodos": 96.9
        },
        "kids200": {
          "total": 1257,
          "pdvs": 1218,
          "dn": 96.9
        },
        "spray170": {
          "total": 1257,
          "pdvs": 1227,
          "dn": 97.6
        },
        "locao200": {
          "total": 1257,
          "pdvs": 1218,
          "dn": 96.9
        }
      },
      "202512": {
        "soma": {
          "total": 1257,
          "algum": 1252,
          "dnAlgum": 99.6,
          "dois": 1252,
          "dnDois": 99.6,
          "todos": 1243,
          "dnTodos": 98.9
        },
        "kids200": {
          "total": 1257,
          "pdvs": 1243,
          "dn": 98.9
        },
        "spray170": {
          "total": 1257,
          "pdvs": 1252,
          "dn": 99.6
        },
        "locao200": {
          "total": 1257,
          "pdvs": 1243,
          "dn": 98.9
        }
      },
      "202601": {
        "soma": {
          "total": 1268,
          "algum": 1073,
          "dnAlgum": 84.6,
          "dois": 1073,
          "dnDois": 84.6,
          "todos": 1020,
          "dnTodos": 80.4
        },
        "kids200": {
          "total": 1268,
          "pdvs": 1073,
          "dn": 84.6
        },
        "spray170": {
          "total": 1268,
          "pdvs": 1051,
          "dn": 82.9
        },
        "locao200": {
          "total": 1268,
          "pdvs": 1020,
          "dn": 80.4
        }
      },
      "202602": {
        "soma": {
          "total": 1268,
          "algum": 962,
          "dnAlgum": 75.9,
          "dois": 962,
          "dnDois": 75.9,
          "todos": 821,
          "dnTodos": 64.7
        },
        "kids200": {
          "total": 1268,
          "pdvs": 962,
          "dn": 75.9
        },
        "spray170": {
          "total": 1268,
          "pdvs": 892,
          "dn": 70.3
        },
        "locao200": {
          "total": 1268,
          "pdvs": 821,
          "dn": 64.7
        }
      },
      "202603": {
        "soma": {
          "total": 1268,
          "algum": 958,
          "dnAlgum": 75.6,
          "dois": 958,
          "dnDois": 75.6,
          "todos": 724,
          "dnTodos": 57.1
        },
        "kids200": {
          "total": 1268,
          "pdvs": 791,
          "dn": 62.4
        },
        "spray170": {
          "total": 1268,
          "pdvs": 958,
          "dn": 75.6
        },
        "locao200": {
          "total": 1268,
          "pdvs": 724,
          "dn": 57.1
        }
      },
      "202604": {
        "soma": {
          "total": 1268,
          "algum": 602,
          "dnAlgum": 47.5,
          "dois": 602,
          "dnDois": 47.5,
          "todos": 415,
          "dnTodos": 32.7
        },
        "kids200": {
          "total": 1268,
          "pdvs": 415,
          "dn": 32.7
        },
        "spray170": {
          "total": 1268,
          "pdvs": 602,
          "dn": 47.5
        },
        "locao200": {
          "total": 1268,
          "pdvs": 503,
          "dn": 39.7
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 1177,
          "pdvs": 190,
          "dn": 16.1
        },
        "locao200": {
          "total": 1177,
          "pdvs": 238,
          "dn": 20.2
        },
        "spray170": {
          "total": 1177,
          "pdvs": 165,
          "dn": 14.0
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 1217,
        "pdvs": 211,
        "dn": 17.3
      },
      "locao200": {
        "total": 1217,
        "pdvs": 267,
        "dn": 21.9
      },
      "spray170": {
        "total": 1217,
        "pdvs": 185,
        "dn": 15.2
      }
    }
  },
  "OL MG": {
    "fytd25": {
      "soma": {
        "total": 2353,
        "algum": 759,
        "dnAlgum": 32.3,
        "dois": 759,
        "dnDois": 32.3,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 2353,
        "pdvs": 759,
        "dn": 32.3
      },
      "spray170": {
        "total": 2353,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 2353,
        "pdvs": 759,
        "dn": 32.3
      }
    },
    "fytd26": {
      "soma": {
        "total": 2353,
        "algum": 1611,
        "dnAlgum": 68.5,
        "dois": 1611,
        "dnDois": 68.5,
        "todos": 967,
        "dnTodos": 41.1
      },
      "kids200": {
        "total": 2353,
        "pdvs": 1611,
        "dn": 68.5
      },
      "spray170": {
        "total": 2353,
        "pdvs": 967,
        "dn": 41.1
      },
      "locao200": {
        "total": 2353,
        "pdvs": 1587,
        "dn": 67.4
      }
    },
    "janabr25": {
      "soma": {
        "total": 2353,
        "algum": 719,
        "dnAlgum": 30.6,
        "dois": 719,
        "dnDois": 30.6,
        "todos": 438,
        "dnTodos": 18.6
      },
      "kids200": {
        "total": 2353,
        "pdvs": 719,
        "dn": 30.6
      },
      "spray170": {
        "total": 2353,
        "pdvs": 438,
        "dn": 18.6
      },
      "locao200": {
        "total": 2353,
        "pdvs": 719,
        "dn": 30.6
      }
    },
    "janabr26": {
      "soma": {
        "total": 2353,
        "algum": 967,
        "dnAlgum": 41.1,
        "dois": 967,
        "dnDois": 41.1,
        "todos": 671,
        "dnTodos": 28.5
      },
      "kids200": {
        "total": 2353,
        "pdvs": 671,
        "dn": 28.5
      },
      "spray170": {
        "total": 2353,
        "pdvs": 967,
        "dn": 41.1
      },
      "locao200": {
        "total": 2353,
        "pdvs": 671,
        "dn": 28.5
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 2353,
          "algum": 6,
          "dnAlgum": 0.3,
          "dois": 6,
          "dnDois": 0.3,
          "todos": 4,
          "dnTodos": 0.2
        },
        "kids200": {
          "total": 2353,
          "pdvs": 6,
          "dn": 0.3
        },
        "spray170": {
          "total": 2353,
          "pdvs": 4,
          "dn": 0.2
        },
        "locao200": {
          "total": 2353,
          "pdvs": 6,
          "dn": 0.3
        }
      },
      "202508": {
        "soma": {
          "total": 2353,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 2353,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 2353,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 2353,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 2353,
          "algum": 11,
          "dnAlgum": 0.5,
          "dois": 11,
          "dnDois": 0.5,
          "todos": 7,
          "dnTodos": 0.3
        },
        "kids200": {
          "total": 2353,
          "pdvs": 11,
          "dn": 0.5
        },
        "spray170": {
          "total": 2353,
          "pdvs": 7,
          "dn": 0.3
        },
        "locao200": {
          "total": 2353,
          "pdvs": 11,
          "dn": 0.5
        }
      },
      "202510": {
        "soma": {
          "total": 2353,
          "algum": 14,
          "dnAlgum": 0.6,
          "dois": 14,
          "dnDois": 0.6,
          "todos": 9,
          "dnTodos": 0.4
        },
        "kids200": {
          "total": 2353,
          "pdvs": 14,
          "dn": 0.6
        },
        "spray170": {
          "total": 2353,
          "pdvs": 9,
          "dn": 0.4
        },
        "locao200": {
          "total": 2353,
          "pdvs": 14,
          "dn": 0.6
        }
      },
      "202511": {
        "soma": {
          "total": 2353,
          "algum": 15,
          "dnAlgum": 0.6,
          "dois": 15,
          "dnDois": 0.6,
          "todos": 9,
          "dnTodos": 0.4
        },
        "kids200": {
          "total": 2353,
          "pdvs": 15,
          "dn": 0.6
        },
        "spray170": {
          "total": 2353,
          "pdvs": 9,
          "dn": 0.4
        },
        "locao200": {
          "total": 2353,
          "pdvs": 15,
          "dn": 0.6
        }
      },
      "202512": {
        "soma": {
          "total": 2353,
          "algum": 30,
          "dnAlgum": 1.3,
          "dois": 30,
          "dnDois": 1.3,
          "todos": 18,
          "dnTodos": 0.8
        },
        "kids200": {
          "total": 2353,
          "pdvs": 30,
          "dn": 1.3
        },
        "spray170": {
          "total": 2353,
          "pdvs": 18,
          "dn": 0.8
        },
        "locao200": {
          "total": 2353,
          "pdvs": 30,
          "dn": 1.3
        }
      },
      "202601": {
        "soma": {
          "total": 2353,
          "algum": 43,
          "dnAlgum": 1.8,
          "dois": 43,
          "dnDois": 1.8,
          "todos": 26,
          "dnTodos": 1.1
        },
        "kids200": {
          "total": 2353,
          "pdvs": 43,
          "dn": 1.8
        },
        "spray170": {
          "total": 2353,
          "pdvs": 26,
          "dn": 1.1
        },
        "locao200": {
          "total": 2353,
          "pdvs": 43,
          "dn": 1.8
        }
      },
      "202602": {
        "soma": {
          "total": 2353,
          "algum": 522,
          "dnAlgum": 22.2,
          "dois": 522,
          "dnDois": 22.2,
          "todos": 318,
          "dnTodos": 13.5
        },
        "kids200": {
          "total": 2353,
          "pdvs": 522,
          "dn": 22.2
        },
        "spray170": {
          "total": 2353,
          "pdvs": 318,
          "dn": 13.5
        },
        "locao200": {
          "total": 2353,
          "pdvs": 522,
          "dn": 22.2
        }
      },
      "202603": {
        "soma": {
          "total": 2353,
          "algum": 599,
          "dnAlgum": 25.5,
          "dois": 599,
          "dnDois": 25.5,
          "todos": 365,
          "dnTodos": 15.5
        },
        "kids200": {
          "total": 2353,
          "pdvs": 599,
          "dn": 25.5
        },
        "spray170": {
          "total": 2353,
          "pdvs": 365,
          "dn": 15.5
        },
        "locao200": {
          "total": 2353,
          "pdvs": 599,
          "dn": 25.5
        }
      },
      "202604": {
        "soma": {
          "total": 2353,
          "algum": 671,
          "dnAlgum": 28.5,
          "dois": 671,
          "dnDois": 28.5,
          "todos": 409,
          "dnTodos": 17.4
        },
        "kids200": {
          "total": 2353,
          "pdvs": 671,
          "dn": 28.5
        },
        "spray170": {
          "total": 2353,
          "pdvs": 409,
          "dn": 17.4
        },
        "locao200": {
          "total": 2353,
          "pdvs": 671,
          "dn": 28.5
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 2286,
          "pdvs": 691,
          "dn": 30.2
        },
        "locao200": {
          "total": 2286,
          "pdvs": 691,
          "dn": 30.2
        },
        "spray170": {
          "total": 2286,
          "pdvs": 344,
          "dn": 15.0
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 3310,
        "pdvs": 1009,
        "dn": 30.5
      },
      "locao200": {
        "total": 3310,
        "pdvs": 1027,
        "dn": 31.0
      },
      "spray170": {
        "total": 3310,
        "pdvs": 503,
        "dn": 15.2
      }
    }
  },
  "OL NE": {
    "fytd25": {
      "soma": {
        "total": 1929,
        "algum": 1020,
        "dnAlgum": 52.9,
        "dois": 1020,
        "dnDois": 52.9,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 1929,
        "pdvs": 1020,
        "dn": 52.9
      },
      "spray170": {
        "total": 1929,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 1929,
        "pdvs": 1020,
        "dn": 52.9
      }
    },
    "fytd26": {
      "soma": {
        "total": 1929,
        "algum": 1666,
        "dnAlgum": 86.4,
        "dois": 1666,
        "dnDois": 86.4,
        "todos": 1061,
        "dnTodos": 55.0
      },
      "kids200": {
        "total": 1929,
        "pdvs": 1612,
        "dn": 83.6
      },
      "spray170": {
        "total": 1929,
        "pdvs": 1061,
        "dn": 55.0
      },
      "locao200": {
        "total": 1929,
        "pdvs": 1666,
        "dn": 86.4
      }
    },
    "janabr25": {
      "soma": {
        "total": 1929,
        "algum": 895,
        "dnAlgum": 46.4,
        "dois": 895,
        "dnDois": 46.4,
        "todos": 570,
        "dnTodos": 29.5
      },
      "kids200": {
        "total": 1929,
        "pdvs": 895,
        "dn": 46.4
      },
      "spray170": {
        "total": 1929,
        "pdvs": 570,
        "dn": 29.5
      },
      "locao200": {
        "total": 1929,
        "pdvs": 895,
        "dn": 46.4
      }
    },
    "janabr26": {
      "soma": {
        "total": 1929,
        "algum": 1061,
        "dnAlgum": 55.0,
        "dois": 1061,
        "dnDois": 55.0,
        "todos": 999,
        "dnTodos": 51.8
      },
      "kids200": {
        "total": 1929,
        "pdvs": 999,
        "dn": 51.8
      },
      "spray170": {
        "total": 1929,
        "pdvs": 1061,
        "dn": 55.0
      },
      "locao200": {
        "total": 1929,
        "pdvs": 999,
        "dn": 51.8
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 1929,
          "algum": 195,
          "dnAlgum": 10.1,
          "dois": 195,
          "dnDois": 10.1,
          "todos": 124,
          "dnTodos": 6.4
        },
        "kids200": {
          "total": 1929,
          "pdvs": 195,
          "dn": 10.1
        },
        "spray170": {
          "total": 1929,
          "pdvs": 124,
          "dn": 6.4
        },
        "locao200": {
          "total": 1929,
          "pdvs": 195,
          "dn": 10.1
        }
      },
      "202508": {
        "soma": {
          "total": 1929,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 1929,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 1929,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 1929,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 1929,
          "algum": 17,
          "dnAlgum": 0.9,
          "dois": 17,
          "dnDois": 0.9,
          "todos": 11,
          "dnTodos": 0.6
        },
        "kids200": {
          "total": 1929,
          "pdvs": 17,
          "dn": 0.9
        },
        "spray170": {
          "total": 1929,
          "pdvs": 11,
          "dn": 0.6
        },
        "locao200": {
          "total": 1929,
          "pdvs": 17,
          "dn": 0.9
        }
      },
      "202510": {
        "soma": {
          "total": 1929,
          "algum": 23,
          "dnAlgum": 1.2,
          "dois": 23,
          "dnDois": 1.2,
          "todos": 15,
          "dnTodos": 0.8
        },
        "kids200": {
          "total": 1929,
          "pdvs": 23,
          "dn": 1.2
        },
        "spray170": {
          "total": 1929,
          "pdvs": 15,
          "dn": 0.8
        },
        "locao200": {
          "total": 1929,
          "pdvs": 23,
          "dn": 1.2
        }
      },
      "202511": {
        "soma": {
          "total": 1929,
          "algum": 36,
          "dnAlgum": 1.9,
          "dois": 36,
          "dnDois": 1.9,
          "todos": 23,
          "dnTodos": 1.2
        },
        "kids200": {
          "total": 1929,
          "pdvs": 36,
          "dn": 1.9
        },
        "spray170": {
          "total": 1929,
          "pdvs": 23,
          "dn": 1.2
        },
        "locao200": {
          "total": 1929,
          "pdvs": 36,
          "dn": 1.9
        }
      },
      "202512": {
        "soma": {
          "total": 1929,
          "algum": 40,
          "dnAlgum": 2.1,
          "dois": 40,
          "dnDois": 2.1,
          "todos": 25,
          "dnTodos": 1.3
        },
        "kids200": {
          "total": 1929,
          "pdvs": 40,
          "dn": 2.1
        },
        "spray170": {
          "total": 1929,
          "pdvs": 25,
          "dn": 1.3
        },
        "locao200": {
          "total": 1929,
          "pdvs": 40,
          "dn": 2.1
        }
      },
      "202601": {
        "soma": {
          "total": 1929,
          "algum": 47,
          "dnAlgum": 2.4,
          "dois": 47,
          "dnDois": 2.4,
          "todos": 30,
          "dnTodos": 1.6
        },
        "kids200": {
          "total": 1929,
          "pdvs": 47,
          "dn": 2.4
        },
        "spray170": {
          "total": 1929,
          "pdvs": 30,
          "dn": 1.6
        },
        "locao200": {
          "total": 1929,
          "pdvs": 47,
          "dn": 2.4
        }
      },
      "202602": {
        "soma": {
          "total": 1929,
          "algum": 802,
          "dnAlgum": 41.6,
          "dois": 802,
          "dnDois": 41.6,
          "todos": 511,
          "dnTodos": 26.5
        },
        "kids200": {
          "total": 1929,
          "pdvs": 802,
          "dn": 41.6
        },
        "spray170": {
          "total": 1929,
          "pdvs": 511,
          "dn": 26.5
        },
        "locao200": {
          "total": 1929,
          "pdvs": 802,
          "dn": 41.6
        }
      },
      "202603": {
        "soma": {
          "total": 1929,
          "algum": 915,
          "dnAlgum": 47.4,
          "dois": 915,
          "dnDois": 47.4,
          "todos": 583,
          "dnTodos": 30.2
        },
        "kids200": {
          "total": 1929,
          "pdvs": 915,
          "dn": 47.4
        },
        "spray170": {
          "total": 1929,
          "pdvs": 583,
          "dn": 30.2
        },
        "locao200": {
          "total": 1929,
          "pdvs": 915,
          "dn": 47.4
        }
      },
      "202604": {
        "soma": {
          "total": 1929,
          "algum": 999,
          "dnAlgum": 51.8,
          "dois": 999,
          "dnDois": 51.8,
          "todos": 636,
          "dnTodos": 33.0
        },
        "kids200": {
          "total": 1929,
          "pdvs": 999,
          "dn": 51.8
        },
        "spray170": {
          "total": 1929,
          "pdvs": 636,
          "dn": 33.0
        },
        "locao200": {
          "total": 1929,
          "pdvs": 999,
          "dn": 51.8
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 4302,
          "pdvs": 1842,
          "dn": 42.8
        },
        "locao200": {
          "total": 4302,
          "pdvs": 1854,
          "dn": 43.1
        },
        "spray170": {
          "total": 4302,
          "pdvs": 897,
          "dn": 20.9
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 5689,
        "pdvs": 2828,
        "dn": 49.7
      },
      "locao200": {
        "total": 5689,
        "pdvs": 2906,
        "dn": 51.1
      },
      "spray170": {
        "total": 5689,
        "pdvs": 1555,
        "dn": 27.3
      }
    }
  },
  "OL PR/SC": {
    "fytd25": {
      "soma": {
        "total": 2329,
        "algum": 1197,
        "dnAlgum": 51.4,
        "dois": 1197,
        "dnDois": 51.4,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 2329,
        "pdvs": 1197,
        "dn": 51.4
      },
      "spray170": {
        "total": 2329,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 2329,
        "pdvs": 1197,
        "dn": 51.4
      }
    },
    "fytd26": {
      "soma": {
        "total": 2329,
        "algum": 1821,
        "dnAlgum": 78.2,
        "dois": 1821,
        "dnDois": 78.2,
        "todos": 1709,
        "dnTodos": 73.4
      },
      "kids200": {
        "total": 2329,
        "pdvs": 1709,
        "dn": 73.4
      },
      "spray170": {
        "total": 2329,
        "pdvs": 1794,
        "dn": 77.0
      },
      "locao200": {
        "total": 2329,
        "pdvs": 1821,
        "dn": 78.2
      }
    },
    "janabr25": {
      "soma": {
        "total": 2329,
        "algum": 1171,
        "dnAlgum": 50.3,
        "dois": 1171,
        "dnDois": 50.3,
        "todos": 1154,
        "dnTodos": 49.5
      },
      "kids200": {
        "total": 2329,
        "pdvs": 1171,
        "dn": 50.3
      },
      "spray170": {
        "total": 2329,
        "pdvs": 1154,
        "dn": 49.5
      },
      "locao200": {
        "total": 2329,
        "pdvs": 1171,
        "dn": 50.3
      }
    },
    "janabr26": {
      "soma": {
        "total": 2329,
        "algum": 1794,
        "dnAlgum": 77.0,
        "dois": 1794,
        "dnDois": 77.0,
        "todos": 1340,
        "dnTodos": 57.5
      },
      "kids200": {
        "total": 2329,
        "pdvs": 1340,
        "dn": 57.5
      },
      "spray170": {
        "total": 2329,
        "pdvs": 1794,
        "dn": 77.0
      },
      "locao200": {
        "total": 2329,
        "pdvs": 1340,
        "dn": 57.5
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 2329,
          "algum": 16,
          "dnAlgum": 0.7,
          "dois": 16,
          "dnDois": 0.7,
          "todos": 16,
          "dnTodos": 0.7
        },
        "kids200": {
          "total": 2329,
          "pdvs": 16,
          "dn": 0.7
        },
        "spray170": {
          "total": 2329,
          "pdvs": 16,
          "dn": 0.7
        },
        "locao200": {
          "total": 2329,
          "pdvs": 16,
          "dn": 0.7
        }
      },
      "202508": {
        "soma": {
          "total": 2329,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 2329,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 2329,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 2329,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 2329,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 2329,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 2329,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 2329,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202510": {
        "soma": {
          "total": 2329,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 2329,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 2329,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 2329,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202511": {
        "soma": {
          "total": 2329,
          "algum": 2,
          "dnAlgum": 0.1,
          "dois": 2,
          "dnDois": 0.1,
          "todos": 2,
          "dnTodos": 0.1
        },
        "kids200": {
          "total": 2329,
          "pdvs": 2,
          "dn": 0.1
        },
        "spray170": {
          "total": 2329,
          "pdvs": 2,
          "dn": 0.1
        },
        "locao200": {
          "total": 2329,
          "pdvs": 2,
          "dn": 0.1
        }
      },
      "202512": {
        "soma": {
          "total": 2329,
          "algum": 4,
          "dnAlgum": 0.2,
          "dois": 4,
          "dnDois": 0.2,
          "todos": 4,
          "dnTodos": 0.2
        },
        "kids200": {
          "total": 2329,
          "pdvs": 4,
          "dn": 0.2
        },
        "spray170": {
          "total": 2329,
          "pdvs": 4,
          "dn": 0.2
        },
        "locao200": {
          "total": 2329,
          "pdvs": 4,
          "dn": 0.2
        }
      },
      "202601": {
        "soma": {
          "total": 2329,
          "algum": 7,
          "dnAlgum": 0.3,
          "dois": 7,
          "dnDois": 0.3,
          "todos": 7,
          "dnTodos": 0.3
        },
        "kids200": {
          "total": 2329,
          "pdvs": 7,
          "dn": 0.3
        },
        "spray170": {
          "total": 2329,
          "pdvs": 7,
          "dn": 0.3
        },
        "locao200": {
          "total": 2329,
          "pdvs": 7,
          "dn": 0.3
        }
      },
      "202602": {
        "soma": {
          "total": 2329,
          "algum": 1229,
          "dnAlgum": 52.8,
          "dois": 1229,
          "dnDois": 52.8,
          "todos": 1211,
          "dnTodos": 52.0
        },
        "kids200": {
          "total": 2329,
          "pdvs": 1229,
          "dn": 52.8
        },
        "spray170": {
          "total": 2329,
          "pdvs": 1211,
          "dn": 52.0
        },
        "locao200": {
          "total": 2329,
          "pdvs": 1229,
          "dn": 52.8
        }
      },
      "202603": {
        "soma": {
          "total": 2329,
          "algum": 1286,
          "dnAlgum": 55.2,
          "dois": 1286,
          "dnDois": 55.2,
          "todos": 1267,
          "dnTodos": 54.4
        },
        "kids200": {
          "total": 2329,
          "pdvs": 1286,
          "dn": 55.2
        },
        "spray170": {
          "total": 2329,
          "pdvs": 1267,
          "dn": 54.4
        },
        "locao200": {
          "total": 2329,
          "pdvs": 1286,
          "dn": 55.2
        }
      },
      "202604": {
        "soma": {
          "total": 2329,
          "algum": 1340,
          "dnAlgum": 57.5,
          "dois": 1340,
          "dnDois": 57.5,
          "todos": 1320,
          "dnTodos": 56.7
        },
        "kids200": {
          "total": 2329,
          "pdvs": 1340,
          "dn": 57.5
        },
        "spray170": {
          "total": 2329,
          "pdvs": 1320,
          "dn": 56.7
        },
        "locao200": {
          "total": 2329,
          "pdvs": 1340,
          "dn": 57.5
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 1539,
          "pdvs": 604,
          "dn": 39.2
        },
        "locao200": {
          "total": 1539,
          "pdvs": 588,
          "dn": 38.2
        },
        "spray170": {
          "total": 1539,
          "pdvs": 561,
          "dn": 36.5
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 1867,
        "pdvs": 687,
        "dn": 36.8
      },
      "locao200": {
        "total": 1867,
        "pdvs": 714,
        "dn": 38.2
      },
      "spray170": {
        "total": 1867,
        "pdvs": 643,
        "dn": 34.4
      }
    }
  },
  "OL RJ": {
    "fytd25": {
      "soma": {
        "total": 664,
        "algum": 377,
        "dnAlgum": 56.8,
        "dois": 377,
        "dnDois": 56.8,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 664,
        "pdvs": 377,
        "dn": 56.8
      },
      "spray170": {
        "total": 664,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 664,
        "pdvs": 377,
        "dn": 56.8
      }
    },
    "fytd26": {
      "soma": {
        "total": 664,
        "algum": 595,
        "dnAlgum": 89.6,
        "dois": 595,
        "dnDois": 89.6,
        "todos": 445,
        "dnTodos": 67.0
      },
      "kids200": {
        "total": 664,
        "pdvs": 447,
        "dn": 67.3
      },
      "spray170": {
        "total": 664,
        "pdvs": 445,
        "dn": 67.0
      },
      "locao200": {
        "total": 664,
        "pdvs": 595,
        "dn": 89.6
      }
    },
    "janabr25": {
      "soma": {
        "total": 664,
        "algum": 343,
        "dnAlgum": 51.7,
        "dois": 343,
        "dnDois": 51.7,
        "todos": 257,
        "dnTodos": 38.7
      },
      "kids200": {
        "total": 664,
        "pdvs": 343,
        "dn": 51.7
      },
      "spray170": {
        "total": 664,
        "pdvs": 257,
        "dn": 38.7
      },
      "locao200": {
        "total": 664,
        "pdvs": 343,
        "dn": 51.7
      }
    },
    "janabr26": {
      "soma": {
        "total": 664,
        "algum": 445,
        "dnAlgum": 67.0,
        "dois": 445,
        "dnDois": 67.0,
        "todos": 350,
        "dnTodos": 52.7
      },
      "kids200": {
        "total": 664,
        "pdvs": 350,
        "dn": 52.7
      },
      "spray170": {
        "total": 664,
        "pdvs": 445,
        "dn": 67.0
      },
      "locao200": {
        "total": 664,
        "pdvs": 350,
        "dn": 52.7
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 664,
          "algum": 64,
          "dnAlgum": 9.6,
          "dois": 64,
          "dnDois": 9.6,
          "todos": 48,
          "dnTodos": 7.2
        },
        "kids200": {
          "total": 664,
          "pdvs": 64,
          "dn": 9.6
        },
        "spray170": {
          "total": 664,
          "pdvs": 48,
          "dn": 7.2
        },
        "locao200": {
          "total": 664,
          "pdvs": 64,
          "dn": 9.6
        }
      },
      "202508": {
        "soma": {
          "total": 664,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 664,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 664,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 664,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 664,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 664,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 664,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 664,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202510": {
        "soma": {
          "total": 664,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 664,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 664,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 664,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202511": {
        "soma": {
          "total": 664,
          "algum": 1,
          "dnAlgum": 0.2,
          "dois": 1,
          "dnDois": 0.2,
          "todos": 1,
          "dnTodos": 0.2
        },
        "kids200": {
          "total": 664,
          "pdvs": 1,
          "dn": 0.2
        },
        "spray170": {
          "total": 664,
          "pdvs": 1,
          "dn": 0.2
        },
        "locao200": {
          "total": 664,
          "pdvs": 1,
          "dn": 0.2
        }
      },
      "202512": {
        "soma": {
          "total": 664,
          "algum": 3,
          "dnAlgum": 0.5,
          "dois": 3,
          "dnDois": 0.5,
          "todos": 2,
          "dnTodos": 0.3
        },
        "kids200": {
          "total": 664,
          "pdvs": 3,
          "dn": 0.5
        },
        "spray170": {
          "total": 664,
          "pdvs": 2,
          "dn": 0.3
        },
        "locao200": {
          "total": 664,
          "pdvs": 3,
          "dn": 0.5
        }
      },
      "202601": {
        "soma": {
          "total": 664,
          "algum": 3,
          "dnAlgum": 0.5,
          "dois": 3,
          "dnDois": 0.5,
          "todos": 2,
          "dnTodos": 0.3
        },
        "kids200": {
          "total": 664,
          "pdvs": 3,
          "dn": 0.5
        },
        "spray170": {
          "total": 664,
          "pdvs": 2,
          "dn": 0.3
        },
        "locao200": {
          "total": 664,
          "pdvs": 3,
          "dn": 0.5
        }
      },
      "202602": {
        "soma": {
          "total": 664,
          "algum": 320,
          "dnAlgum": 48.2,
          "dois": 320,
          "dnDois": 48.2,
          "todos": 239,
          "dnTodos": 36.0
        },
        "kids200": {
          "total": 664,
          "pdvs": 320,
          "dn": 48.2
        },
        "spray170": {
          "total": 664,
          "pdvs": 239,
          "dn": 36.0
        },
        "locao200": {
          "total": 664,
          "pdvs": 320,
          "dn": 48.2
        }
      },
      "202603": {
        "soma": {
          "total": 664,
          "algum": 338,
          "dnAlgum": 50.9,
          "dois": 338,
          "dnDois": 50.9,
          "todos": 253,
          "dnTodos": 38.1
        },
        "kids200": {
          "total": 664,
          "pdvs": 338,
          "dn": 50.9
        },
        "spray170": {
          "total": 664,
          "pdvs": 253,
          "dn": 38.1
        },
        "locao200": {
          "total": 664,
          "pdvs": 338,
          "dn": 50.9
        }
      },
      "202604": {
        "soma": {
          "total": 664,
          "algum": 350,
          "dnAlgum": 52.7,
          "dois": 350,
          "dnDois": 52.7,
          "todos": 262,
          "dnTodos": 39.5
        },
        "kids200": {
          "total": 664,
          "pdvs": 350,
          "dn": 52.7
        },
        "spray170": {
          "total": 664,
          "pdvs": 262,
          "dn": 39.5
        },
        "locao200": {
          "total": 664,
          "pdvs": 350,
          "dn": 52.7
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 2302,
          "pdvs": 840,
          "dn": 36.5
        },
        "locao200": {
          "total": 2302,
          "pdvs": 987,
          "dn": 42.9
        },
        "spray170": {
          "total": 2302,
          "pdvs": 497,
          "dn": 21.6
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 3376,
        "pdvs": 1293,
        "dn": 38.3
      },
      "locao200": {
        "total": 3376,
        "pdvs": 1495,
        "dn": 44.3
      },
      "spray170": {
        "total": 3376,
        "pdvs": 749,
        "dn": 22.2
      }
    }
  },
  "OL RS": {
    "fytd25": {
      "soma": {
        "total": 1647,
        "algum": 855,
        "dnAlgum": 51.9,
        "dois": 855,
        "dnDois": 51.9,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 1647,
        "pdvs": 855,
        "dn": 51.9
      },
      "spray170": {
        "total": 1647,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 1647,
        "pdvs": 855,
        "dn": 51.9
      }
    },
    "fytd26": {
      "soma": {
        "total": 1647,
        "algum": 1202,
        "dnAlgum": 73.0,
        "dois": 1202,
        "dnDois": 73.0,
        "todos": 1139,
        "dnTodos": 69.2
      },
      "kids200": {
        "total": 1647,
        "pdvs": 1152,
        "dn": 69.9
      },
      "spray170": {
        "total": 1647,
        "pdvs": 1139,
        "dn": 69.2
      },
      "locao200": {
        "total": 1647,
        "pdvs": 1202,
        "dn": 73.0
      }
    },
    "janabr25": {
      "soma": {
        "total": 1647,
        "algum": 838,
        "dnAlgum": 50.9,
        "dois": 838,
        "dnDois": 50.9,
        "todos": 794,
        "dnTodos": 48.2
      },
      "kids200": {
        "total": 1647,
        "pdvs": 838,
        "dn": 50.9
      },
      "spray170": {
        "total": 1647,
        "pdvs": 794,
        "dn": 48.2
      },
      "locao200": {
        "total": 1647,
        "pdvs": 838,
        "dn": 50.9
      }
    },
    "janabr26": {
      "soma": {
        "total": 1647,
        "algum": 1139,
        "dnAlgum": 69.2,
        "dois": 1139,
        "dnDois": 69.2,
        "todos": 788,
        "dnTodos": 47.8
      },
      "kids200": {
        "total": 1647,
        "pdvs": 788,
        "dn": 47.8
      },
      "spray170": {
        "total": 1647,
        "pdvs": 1139,
        "dn": 69.2
      },
      "locao200": {
        "total": 1647,
        "pdvs": 788,
        "dn": 47.8
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 1647,
          "algum": 6,
          "dnAlgum": 0.4,
          "dois": 6,
          "dnDois": 0.4,
          "todos": 6,
          "dnTodos": 0.4
        },
        "kids200": {
          "total": 1647,
          "pdvs": 6,
          "dn": 0.4
        },
        "spray170": {
          "total": 1647,
          "pdvs": 6,
          "dn": 0.4
        },
        "locao200": {
          "total": 1647,
          "pdvs": 6,
          "dn": 0.4
        }
      },
      "202508": {
        "soma": {
          "total": 1647,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 1647,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202510": {
        "soma": {
          "total": 1647,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202511": {
        "soma": {
          "total": 1647,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 1647,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202512": {
        "soma": {
          "total": 1647,
          "algum": 2,
          "dnAlgum": 0.1,
          "dois": 2,
          "dnDois": 0.1,
          "todos": 2,
          "dnTodos": 0.1
        },
        "kids200": {
          "total": 1647,
          "pdvs": 2,
          "dn": 0.1
        },
        "spray170": {
          "total": 1647,
          "pdvs": 2,
          "dn": 0.1
        },
        "locao200": {
          "total": 1647,
          "pdvs": 2,
          "dn": 0.1
        }
      },
      "202601": {
        "soma": {
          "total": 1647,
          "algum": 2,
          "dnAlgum": 0.1,
          "dois": 2,
          "dnDois": 0.1,
          "todos": 2,
          "dnTodos": 0.1
        },
        "kids200": {
          "total": 1647,
          "pdvs": 2,
          "dn": 0.1
        },
        "spray170": {
          "total": 1647,
          "pdvs": 2,
          "dn": 0.1
        },
        "locao200": {
          "total": 1647,
          "pdvs": 2,
          "dn": 0.1
        }
      },
      "202602": {
        "soma": {
          "total": 1647,
          "algum": 714,
          "dnAlgum": 43.4,
          "dois": 714,
          "dnDois": 43.4,
          "todos": 677,
          "dnTodos": 41.1
        },
        "kids200": {
          "total": 1647,
          "pdvs": 714,
          "dn": 43.4
        },
        "spray170": {
          "total": 1647,
          "pdvs": 677,
          "dn": 41.1
        },
        "locao200": {
          "total": 1647,
          "pdvs": 714,
          "dn": 43.4
        }
      },
      "202603": {
        "soma": {
          "total": 1647,
          "algum": 756,
          "dnAlgum": 45.9,
          "dois": 756,
          "dnDois": 45.9,
          "todos": 716,
          "dnTodos": 43.5
        },
        "kids200": {
          "total": 1647,
          "pdvs": 756,
          "dn": 45.9
        },
        "spray170": {
          "total": 1647,
          "pdvs": 716,
          "dn": 43.5
        },
        "locao200": {
          "total": 1647,
          "pdvs": 756,
          "dn": 45.9
        }
      },
      "202604": {
        "soma": {
          "total": 1647,
          "algum": 788,
          "dnAlgum": 47.8,
          "dois": 788,
          "dnDois": 47.8,
          "todos": 747,
          "dnTodos": 45.4
        },
        "kids200": {
          "total": 1647,
          "pdvs": 788,
          "dn": 47.8
        },
        "spray170": {
          "total": 1647,
          "pdvs": 747,
          "dn": 45.4
        },
        "locao200": {
          "total": 1647,
          "pdvs": 788,
          "dn": 47.8
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 933,
          "pdvs": 211,
          "dn": 22.6
        },
        "locao200": {
          "total": 933,
          "pdvs": 231,
          "dn": 24.8
        },
        "spray170": {
          "total": 933,
          "pdvs": 176,
          "dn": 18.9
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 1212,
        "pdvs": 284,
        "dn": 23.4
      },
      "locao200": {
        "total": 1212,
        "pdvs": 303,
        "dn": 25.0
      },
      "spray170": {
        "total": 1212,
        "pdvs": 234,
        "dn": 19.3
      }
    }
  },
  "OL SPC": {
    "fytd25": {
      "soma": {
        "total": 1213,
        "algum": 792,
        "dnAlgum": 65.3,
        "dois": 792,
        "dnDois": 65.3,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 1213,
        "pdvs": 792,
        "dn": 65.3
      },
      "spray170": {
        "total": 1213,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 1213,
        "pdvs": 792,
        "dn": 65.3
      }
    },
    "fytd26": {
      "soma": {
        "total": 1213,
        "algum": 1044,
        "dnAlgum": 86.1,
        "dois": 1044,
        "dnDois": 86.1,
        "todos": 891,
        "dnTodos": 73.5
      },
      "kids200": {
        "total": 1213,
        "pdvs": 921,
        "dn": 75.9
      },
      "spray170": {
        "total": 1213,
        "pdvs": 891,
        "dn": 73.5
      },
      "locao200": {
        "total": 1213,
        "pdvs": 1044,
        "dn": 86.1
      }
    },
    "janabr25": {
      "soma": {
        "total": 1213,
        "algum": 775,
        "dnAlgum": 63.9,
        "dois": 775,
        "dnDois": 63.9,
        "todos": 661,
        "dnTodos": 54.5
      },
      "kids200": {
        "total": 1213,
        "pdvs": 775,
        "dn": 63.9
      },
      "spray170": {
        "total": 1213,
        "pdvs": 661,
        "dn": 54.5
      },
      "locao200": {
        "total": 1213,
        "pdvs": 775,
        "dn": 63.9
      }
    },
    "janabr26": {
      "soma": {
        "total": 1213,
        "algum": 891,
        "dnAlgum": 73.5,
        "dois": 891,
        "dnDois": 73.5,
        "todos": 730,
        "dnTodos": 60.2
      },
      "kids200": {
        "total": 1213,
        "pdvs": 730,
        "dn": 60.2
      },
      "spray170": {
        "total": 1213,
        "pdvs": 891,
        "dn": 73.5
      },
      "locao200": {
        "total": 1213,
        "pdvs": 730,
        "dn": 60.2
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 1213,
          "algum": 85,
          "dnAlgum": 7.0,
          "dois": 85,
          "dnDois": 7.0,
          "todos": 73,
          "dnTodos": 6.0
        },
        "kids200": {
          "total": 1213,
          "pdvs": 85,
          "dn": 7.0
        },
        "spray170": {
          "total": 1213,
          "pdvs": 73,
          "dn": 6.0
        },
        "locao200": {
          "total": 1213,
          "pdvs": 85,
          "dn": 7.0
        }
      },
      "202508": {
        "soma": {
          "total": 1213,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 1213,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 1213,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 1213,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 1213,
          "algum": 1,
          "dnAlgum": 0.1,
          "dois": 1,
          "dnDois": 0.1,
          "todos": 1,
          "dnTodos": 0.1
        },
        "kids200": {
          "total": 1213,
          "pdvs": 1,
          "dn": 0.1
        },
        "spray170": {
          "total": 1213,
          "pdvs": 1,
          "dn": 0.1
        },
        "locao200": {
          "total": 1213,
          "pdvs": 1,
          "dn": 0.1
        }
      },
      "202510": {
        "soma": {
          "total": 1213,
          "algum": 2,
          "dnAlgum": 0.2,
          "dois": 2,
          "dnDois": 0.2,
          "todos": 2,
          "dnTodos": 0.2
        },
        "kids200": {
          "total": 1213,
          "pdvs": 2,
          "dn": 0.2
        },
        "spray170": {
          "total": 1213,
          "pdvs": 2,
          "dn": 0.2
        },
        "locao200": {
          "total": 1213,
          "pdvs": 2,
          "dn": 0.2
        }
      },
      "202511": {
        "soma": {
          "total": 1213,
          "algum": 2,
          "dnAlgum": 0.2,
          "dois": 2,
          "dnDois": 0.2,
          "todos": 2,
          "dnTodos": 0.2
        },
        "kids200": {
          "total": 1213,
          "pdvs": 2,
          "dn": 0.2
        },
        "spray170": {
          "total": 1213,
          "pdvs": 2,
          "dn": 0.2
        },
        "locao200": {
          "total": 1213,
          "pdvs": 2,
          "dn": 0.2
        }
      },
      "202512": {
        "soma": {
          "total": 1213,
          "algum": 2,
          "dnAlgum": 0.2,
          "dois": 2,
          "dnDois": 0.2,
          "todos": 2,
          "dnTodos": 0.2
        },
        "kids200": {
          "total": 1213,
          "pdvs": 2,
          "dn": 0.2
        },
        "spray170": {
          "total": 1213,
          "pdvs": 2,
          "dn": 0.2
        },
        "locao200": {
          "total": 1213,
          "pdvs": 2,
          "dn": 0.2
        }
      },
      "202601": {
        "soma": {
          "total": 1213,
          "algum": 3,
          "dnAlgum": 0.2,
          "dois": 3,
          "dnDois": 0.2,
          "todos": 3,
          "dnTodos": 0.2
        },
        "kids200": {
          "total": 1213,
          "pdvs": 3,
          "dn": 0.2
        },
        "spray170": {
          "total": 1213,
          "pdvs": 3,
          "dn": 0.2
        },
        "locao200": {
          "total": 1213,
          "pdvs": 3,
          "dn": 0.2
        }
      },
      "202602": {
        "soma": {
          "total": 1213,
          "algum": 696,
          "dnAlgum": 57.4,
          "dois": 696,
          "dnDois": 57.4,
          "todos": 594,
          "dnTodos": 49.0
        },
        "kids200": {
          "total": 1213,
          "pdvs": 696,
          "dn": 57.4
        },
        "spray170": {
          "total": 1213,
          "pdvs": 594,
          "dn": 49.0
        },
        "locao200": {
          "total": 1213,
          "pdvs": 696,
          "dn": 57.4
        }
      },
      "202603": {
        "soma": {
          "total": 1213,
          "algum": 716,
          "dnAlgum": 59.0,
          "dois": 716,
          "dnDois": 59.0,
          "todos": 611,
          "dnTodos": 50.4
        },
        "kids200": {
          "total": 1213,
          "pdvs": 716,
          "dn": 59.0
        },
        "spray170": {
          "total": 1213,
          "pdvs": 611,
          "dn": 50.4
        },
        "locao200": {
          "total": 1213,
          "pdvs": 716,
          "dn": 59.0
        }
      },
      "202604": {
        "soma": {
          "total": 1213,
          "algum": 730,
          "dnAlgum": 60.2,
          "dois": 730,
          "dnDois": 60.2,
          "todos": 623,
          "dnTodos": 51.4
        },
        "kids200": {
          "total": 1213,
          "pdvs": 730,
          "dn": 60.2
        },
        "spray170": {
          "total": 1213,
          "pdvs": 623,
          "dn": 51.4
        },
        "locao200": {
          "total": 1213,
          "pdvs": 730,
          "dn": 60.2
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 661,
          "pdvs": 282,
          "dn": 42.7
        },
        "locao200": {
          "total": 661,
          "pdvs": 303,
          "dn": 45.8
        },
        "spray170": {
          "total": 661,
          "pdvs": 173,
          "dn": 26.2
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 808,
        "pdvs": 366,
        "dn": 45.3
      },
      "locao200": {
        "total": 808,
        "pdvs": 395,
        "dn": 48.9
      },
      "spray170": {
        "total": 808,
        "pdvs": 259,
        "dn": 32.1
      }
    }
  },
  "OL SPI": {
    "fytd25": {
      "soma": {
        "total": 1182,
        "algum": 528,
        "dnAlgum": 44.7,
        "dois": 528,
        "dnDois": 44.7,
        "todos": 0,
        "dnTodos": 0.0
      },
      "kids200": {
        "total": 1182,
        "pdvs": 528,
        "dn": 44.7
      },
      "spray170": {
        "total": 1182,
        "pdvs": 0,
        "dn": 0.0
      },
      "locao200": {
        "total": 1182,
        "pdvs": 528,
        "dn": 44.7
      }
    },
    "fytd26": {
      "soma": {
        "total": 1182,
        "algum": 878,
        "dnAlgum": 74.3,
        "dois": 878,
        "dnDois": 74.3,
        "todos": 726,
        "dnTodos": 61.4
      },
      "kids200": {
        "total": 1182,
        "pdvs": 765,
        "dn": 64.7
      },
      "spray170": {
        "total": 1182,
        "pdvs": 726,
        "dn": 61.4
      },
      "locao200": {
        "total": 1182,
        "pdvs": 878,
        "dn": 74.3
      }
    },
    "janabr25": {
      "soma": {
        "total": 1182,
        "algum": 507,
        "dnAlgum": 42.9,
        "dois": 507,
        "dnDois": 42.9,
        "todos": 419,
        "dnTodos": 35.4
      },
      "kids200": {
        "total": 1182,
        "pdvs": 507,
        "dn": 42.9
      },
      "spray170": {
        "total": 1182,
        "pdvs": 419,
        "dn": 35.4
      },
      "locao200": {
        "total": 1182,
        "pdvs": 507,
        "dn": 42.9
      }
    },
    "janabr26": {
      "soma": {
        "total": 1182,
        "algum": 726,
        "dnAlgum": 61.4,
        "dois": 726,
        "dnDois": 61.4,
        "todos": 557,
        "dnTodos": 47.1
      },
      "kids200": {
        "total": 1182,
        "pdvs": 557,
        "dn": 47.1
      },
      "spray170": {
        "total": 1182,
        "pdvs": 726,
        "dn": 61.4
      },
      "locao200": {
        "total": 1182,
        "pdvs": 557,
        "dn": 47.1
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 1182,
          "algum": 30,
          "dnAlgum": 2.5,
          "dois": 30,
          "dnDois": 2.5,
          "todos": 25,
          "dnTodos": 2.1
        },
        "kids200": {
          "total": 1182,
          "pdvs": 30,
          "dn": 2.5
        },
        "spray170": {
          "total": 1182,
          "pdvs": 25,
          "dn": 2.1
        },
        "locao200": {
          "total": 1182,
          "pdvs": 30,
          "dn": 2.5
        }
      },
      "202508": {
        "soma": {
          "total": 1182,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 1182,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 1182,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 1182,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202509": {
        "soma": {
          "total": 1182,
          "algum": 0,
          "dnAlgum": 0.0,
          "dois": 0,
          "dnDois": 0.0,
          "todos": 0,
          "dnTodos": 0.0
        },
        "kids200": {
          "total": 1182,
          "pdvs": 0,
          "dn": 0.0
        },
        "spray170": {
          "total": 1182,
          "pdvs": 0,
          "dn": 0.0
        },
        "locao200": {
          "total": 1182,
          "pdvs": 0,
          "dn": 0.0
        }
      },
      "202510": {
        "soma": {
          "total": 1182,
          "algum": 5,
          "dnAlgum": 0.4,
          "dois": 5,
          "dnDois": 0.4,
          "todos": 4,
          "dnTodos": 0.3
        },
        "kids200": {
          "total": 1182,
          "pdvs": 5,
          "dn": 0.4
        },
        "spray170": {
          "total": 1182,
          "pdvs": 4,
          "dn": 0.3
        },
        "locao200": {
          "total": 1182,
          "pdvs": 5,
          "dn": 0.4
        }
      },
      "202511": {
        "soma": {
          "total": 1182,
          "algum": 10,
          "dnAlgum": 0.8,
          "dois": 10,
          "dnDois": 0.8,
          "todos": 8,
          "dnTodos": 0.7
        },
        "kids200": {
          "total": 1182,
          "pdvs": 10,
          "dn": 0.8
        },
        "spray170": {
          "total": 1182,
          "pdvs": 8,
          "dn": 0.7
        },
        "locao200": {
          "total": 1182,
          "pdvs": 10,
          "dn": 0.8
        }
      },
      "202512": {
        "soma": {
          "total": 1182,
          "algum": 13,
          "dnAlgum": 1.1,
          "dois": 13,
          "dnDois": 1.1,
          "todos": 11,
          "dnTodos": 0.9
        },
        "kids200": {
          "total": 1182,
          "pdvs": 13,
          "dn": 1.1
        },
        "spray170": {
          "total": 1182,
          "pdvs": 11,
          "dn": 0.9
        },
        "locao200": {
          "total": 1182,
          "pdvs": 13,
          "dn": 1.1
        }
      },
      "202601": {
        "soma": {
          "total": 1182,
          "algum": 18,
          "dnAlgum": 1.5,
          "dois": 18,
          "dnDois": 1.5,
          "todos": 15,
          "dnTodos": 1.3
        },
        "kids200": {
          "total": 1182,
          "pdvs": 18,
          "dn": 1.5
        },
        "spray170": {
          "total": 1182,
          "pdvs": 15,
          "dn": 1.3
        },
        "locao200": {
          "total": 1182,
          "pdvs": 18,
          "dn": 1.5
        }
      },
      "202602": {
        "soma": {
          "total": 1182,
          "algum": 497,
          "dnAlgum": 42.0,
          "dois": 497,
          "dnDois": 42.0,
          "todos": 411,
          "dnTodos": 34.8
        },
        "kids200": {
          "total": 1182,
          "pdvs": 497,
          "dn": 42.0
        },
        "spray170": {
          "total": 1182,
          "pdvs": 411,
          "dn": 34.8
        },
        "locao200": {
          "total": 1182,
          "pdvs": 497,
          "dn": 42.0
        }
      },
      "202603": {
        "soma": {
          "total": 1182,
          "algum": 533,
          "dnAlgum": 45.1,
          "dois": 533,
          "dnDois": 45.1,
          "todos": 441,
          "dnTodos": 37.3
        },
        "kids200": {
          "total": 1182,
          "pdvs": 533,
          "dn": 45.1
        },
        "spray170": {
          "total": 1182,
          "pdvs": 441,
          "dn": 37.3
        },
        "locao200": {
          "total": 1182,
          "pdvs": 533,
          "dn": 45.1
        }
      },
      "202604": {
        "soma": {
          "total": 1182,
          "algum": 557,
          "dnAlgum": 47.1,
          "dois": 557,
          "dnDois": 47.1,
          "todos": 461,
          "dnTodos": 39.0
        },
        "kids200": {
          "total": 1182,
          "pdvs": 557,
          "dn": 47.1
        },
        "spray170": {
          "total": 1182,
          "pdvs": 461,
          "dn": 39.0
        },
        "locao200": {
          "total": 1182,
          "pdvs": 557,
          "dn": 47.1
        }
      },
      "202608": {
        "fonte": "iqvia",
        "kids200": {
          "total": 735,
          "pdvs": 249,
          "dn": 33.9
        },
        "locao200": {
          "total": 735,
          "pdvs": 262,
          "dn": 35.6
        },
        "spray170": {
          "total": 735,
          "pdvs": 200,
          "dn": 27.2
        }
      }
    },
    "fytd27": {
      "fonte": "iqvia",
      "kids200": {
        "total": 884,
        "pdvs": 303,
        "dn": 34.3
      },
      "locao200": {
        "total": 884,
        "pdvs": 325,
        "dn": 36.8
      },
      "spray170": {
        "total": 884,
        "pdvs": 262,
        "dn": 29.6
      }
    }
  },
  "GAM": {
    "fytd25": {
      "soma": {
        "total": 8466,
        "algum": 4984,
        "dnAlgum": 58.9,
        "dois": 4984,
        "dnDois": 58.9,
        "todos": 3709,
        "dnTodos": 43.8
      },
      "kids200": {
        "total": 8466,
        "pdvs": 4984,
        "dn": 58.9
      },
      "spray170": {
        "total": 8466,
        "pdvs": 4452,
        "dn": 52.6
      },
      "locao200": {
        "total": 8466,
        "pdvs": 3709,
        "dn": 43.8
      }
    },
    "fytd26": {
      "soma": {
        "total": 9524,
        "algum": 5910,
        "dnAlgum": 62.1,
        "dois": 5910,
        "dnDois": 62.1,
        "todos": 5655,
        "dnTodos": 59.4
      },
      "kids200": {
        "total": 9524,
        "pdvs": 5910,
        "dn": 62.1
      },
      "spray170": {
        "total": 9524,
        "pdvs": 5655,
        "dn": 59.4
      },
      "locao200": {
        "total": 9524,
        "pdvs": 5665,
        "dn": 59.5
      }
    },
    "janabr25": {
      "soma": {
        "total": 6619,
        "algum": 3084,
        "dnAlgum": 46.6,
        "dois": 3084,
        "dnDois": 46.6,
        "todos": 2677,
        "dnTodos": 40.4
      },
      "kids200": {
        "total": 6619,
        "pdvs": 3084,
        "dn": 46.6
      },
      "spray170": {
        "total": 6619,
        "pdvs": 3068,
        "dn": 46.4
      },
      "locao200": {
        "total": 6619,
        "pdvs": 2677,
        "dn": 40.4
      }
    },
    "janabr26": {
      "soma": {
        "total": 8038,
        "algum": 7083,
        "dnAlgum": 88.1,
        "dois": 7083,
        "dnDois": 88.1,
        "todos": 6540,
        "dnTodos": 81.4
      },
      "kids200": {
        "total": 8038,
        "pdvs": 6792,
        "dn": 84.5
      },
      "spray170": {
        "total": 8038,
        "pdvs": 7083,
        "dn": 88.1
      },
      "locao200": {
        "total": 8038,
        "pdvs": 6540,
        "dn": 81.4
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 800,
          "algum": 242,
          "dnAlgum": 30.2,
          "dois": 242,
          "dnDois": 30.2,
          "todos": 104,
          "dnTodos": 13.0
        },
        "kids200": {
          "total": 800,
          "pdvs": 242,
          "dn": 30.2
        },
        "spray170": {
          "total": 800,
          "pdvs": 164,
          "dn": 20.5
        },
        "locao200": {
          "total": 800,
          "pdvs": 104,
          "dn": 13.0
        }
      },
      "202508": {
        "soma": {
          "total": 867,
          "algum": 241,
          "dnAlgum": 27.8,
          "dois": 241,
          "dnDois": 27.8,
          "todos": 150,
          "dnTodos": 17.3
        },
        "kids200": {
          "total": 867,
          "pdvs": 241,
          "dn": 27.8
        },
        "spray170": {
          "total": 867,
          "pdvs": 186,
          "dn": 21.5
        },
        "locao200": {
          "total": 867,
          "pdvs": 150,
          "dn": 17.3
        }
      },
      "202509": {
        "soma": {
          "total": 2661,
          "algum": 1083,
          "dnAlgum": 40.7,
          "dois": 1083,
          "dnDois": 40.7,
          "todos": 734,
          "dnTodos": 27.6
        },
        "kids200": {
          "total": 2661,
          "pdvs": 1083,
          "dn": 40.7
        },
        "spray170": {
          "total": 2661,
          "pdvs": 893,
          "dn": 33.6
        },
        "locao200": {
          "total": 2661,
          "pdvs": 734,
          "dn": 27.6
        }
      },
      "202510": {
        "soma": {
          "total": 3232,
          "algum": 1405,
          "dnAlgum": 43.5,
          "dois": 1405,
          "dnDois": 43.5,
          "todos": 1205,
          "dnTodos": 37.3
        },
        "kids200": {
          "total": 3232,
          "pdvs": 1405,
          "dn": 43.5
        },
        "spray170": {
          "total": 3232,
          "pdvs": 1205,
          "dn": 37.3
        },
        "locao200": {
          "total": 3232,
          "pdvs": 1279,
          "dn": 39.6
        }
      },
      "202511": {
        "soma": {
          "total": 3660,
          "algum": 1438,
          "dnAlgum": 39.3,
          "dois": 1438,
          "dnDois": 39.3,
          "todos": 1112,
          "dnTodos": 30.4
        },
        "kids200": {
          "total": 3660,
          "pdvs": 1421,
          "dn": 38.8
        },
        "spray170": {
          "total": 3660,
          "pdvs": 1112,
          "dn": 30.4
        },
        "locao200": {
          "total": 3660,
          "pdvs": 1438,
          "dn": 39.3
        }
      },
      "202512": {
        "soma": {
          "total": 5254,
          "algum": 2563,
          "dnAlgum": 48.8,
          "dois": 2563,
          "dnDois": 48.8,
          "todos": 2055,
          "dnTodos": 39.1
        },
        "kids200": {
          "total": 5254,
          "pdvs": 2563,
          "dn": 48.8
        },
        "spray170": {
          "total": 5254,
          "pdvs": 2263,
          "dn": 43.1
        },
        "locao200": {
          "total": 5254,
          "pdvs": 2055,
          "dn": 39.1
        }
      },
      "202601": {
        "soma": {
          "total": 5512,
          "algum": 2234,
          "dnAlgum": 40.5,
          "dois": 2234,
          "dnDois": 40.5,
          "todos": 2100,
          "dnTodos": 38.1
        },
        "kids200": {
          "total": 5512,
          "pdvs": 2205,
          "dn": 40.0
        },
        "spray170": {
          "total": 5512,
          "pdvs": 2234,
          "dn": 40.5
        },
        "locao200": {
          "total": 5512,
          "pdvs": 2100,
          "dn": 38.1
        }
      },
      "202602": {
        "soma": {
          "total": 5005,
          "algum": 2142,
          "dnAlgum": 42.8,
          "dois": 2142,
          "dnDois": 42.8,
          "todos": 1887,
          "dnTodos": 37.7
        },
        "kids200": {
          "total": 5005,
          "pdvs": 1887,
          "dn": 37.7
        },
        "spray170": {
          "total": 5005,
          "pdvs": 2142,
          "dn": 42.8
        },
        "locao200": {
          "total": 5005,
          "pdvs": 2016,
          "dn": 40.3
        }
      },
      "202603": {
        "soma": {
          "total": 4079,
          "algum": 1428,
          "dnAlgum": 35.0,
          "dois": 1428,
          "dnDois": 35.0,
          "todos": 1231,
          "dnTodos": 30.2
        },
        "kids200": {
          "total": 4079,
          "pdvs": 1411,
          "dn": 34.6
        },
        "spray170": {
          "total": 4079,
          "pdvs": 1428,
          "dn": 35.0
        },
        "locao200": {
          "total": 4079,
          "pdvs": 1231,
          "dn": 30.2
        }
      },
      "202604": {
        "soma": {
          "total": 3757,
          "algum": 1289,
          "dnAlgum": 34.3,
          "dois": 1289,
          "dnDois": 34.3,
          "todos": 1193,
          "dnTodos": 31.8
        },
        "kids200": {
          "total": 3757,
          "pdvs": 1289,
          "dn": 34.3
        },
        "spray170": {
          "total": 3757,
          "pdvs": 1279,
          "dn": 34.0
        },
        "locao200": {
          "total": 3757,
          "pdvs": 1193,
          "dn": 31.8
        }
      }
    }
  },
  "GAUCHA FARMA": {
    "fytd25": {
      "soma": {
        "total": 1622,
        "algum": 822,
        "dnAlgum": 50.7,
        "dois": 822,
        "dnDois": 50.7,
        "todos": 713,
        "dnTodos": 44.0
      },
      "kids200": {
        "total": 1622,
        "pdvs": 822,
        "dn": 50.7
      },
      "spray170": {
        "total": 1622,
        "pdvs": 713,
        "dn": 44.0
      },
      "locao200": {
        "total": 1622,
        "pdvs": 763,
        "dn": 47.0
      }
    },
    "fytd26": {
      "soma": {
        "total": 1941,
        "algum": 896,
        "dnAlgum": 46.2,
        "dois": 896,
        "dnDois": 46.2,
        "todos": 720,
        "dnTodos": 37.1
      },
      "kids200": {
        "total": 1941,
        "pdvs": 896,
        "dn": 46.2
      },
      "spray170": {
        "total": 1941,
        "pdvs": 755,
        "dn": 38.9
      },
      "locao200": {
        "total": 1941,
        "pdvs": 720,
        "dn": 37.1
      }
    },
    "janabr25": {
      "soma": {
        "total": 1557,
        "algum": 567,
        "dnAlgum": 36.4,
        "dois": 567,
        "dnDois": 36.4,
        "todos": 356,
        "dnTodos": 22.9
      },
      "kids200": {
        "total": 1557,
        "pdvs": 567,
        "dn": 36.4
      },
      "spray170": {
        "total": 1557,
        "pdvs": 356,
        "dn": 22.9
      },
      "locao200": {
        "total": 1557,
        "pdvs": 442,
        "dn": 28.4
      }
    },
    "janabr26": {
      "soma": {
        "total": 1941,
        "algum": 896,
        "dnAlgum": 46.2,
        "dois": 896,
        "dnDois": 46.2,
        "todos": 720,
        "dnTodos": 37.1
      },
      "kids200": {
        "total": 1941,
        "pdvs": 896,
        "dn": 46.2
      },
      "spray170": {
        "total": 1941,
        "pdvs": 755,
        "dn": 38.9
      },
      "locao200": {
        "total": 1941,
        "pdvs": 720,
        "dn": 37.1
      }
    },
    "meses": {
      "202507": {
        "soma": {
          "total": 272,
          "algum": 21,
          "dnAlgum": 7.7,
          "dois": 21,
          "dnDois": 7.7,
          "todos": 9,
          "dnTodos": 3.3
        },
        "kids200": {
          "total": 272,
          "pdvs": 21,
          "dn": 7.7
        },
        "spray170": {
          "total": 272,
          "pdvs": 16,
          "dn": 5.9
        },
        "locao200": {
          "total": 272,
          "pdvs": 9,
          "dn": 3.3
        }
      },
      "202508": {
        "soma": {
          "total": 233,
          "algum": 25,
          "dnAlgum": 10.7,
          "dois": 25,
          "dnDois": 10.7,
          "todos": 17,
          "dnTodos": 7.3
        },
        "kids200": {
          "total": 233,
          "pdvs": 25,
          "dn": 10.7
        },
        "spray170": {
          "total": 233,
          "pdvs": 21,
          "dn": 9.0
        },
        "locao200": {
          "total": 233,
          "pdvs": 17,
          "dn": 7.3
        }
      },
      "202509": {
        "soma": {
          "total": 898,
          "algum": 280,
          "dnAlgum": 31.2,
          "dois": 280,
          "dnDois": 31.2,
          "todos": 199,
          "dnTodos": 22.2
        },
        "kids200": {
          "total": 898,
          "pdvs": 280,
          "dn": 31.2
        },
        "spray170": {
          "total": 898,
          "pdvs": 256,
          "dn": 28.5
        },
        "locao200": {
          "total": 898,
          "pdvs": 199,
          "dn": 22.2
        }
      },
      "202510": {
        "soma": {
          "total": 1333,
          "algum": 501,
          "dnAlgum": 37.6,
          "dois": 501,
          "dnDois": 37.6,
          "todos": 377,
          "dnTodos": 28.3
        },
        "kids200": {
          "total": 1333,
          "pdvs": 501,
          "dn": 37.6
        },
        "spray170": {
          "total": 1333,
          "pdvs": 417,
          "dn": 31.3
        },
        "locao200": {
          "total": 1333,
          "pdvs": 377,
          "dn": 28.3
        }
      },
      "202511": {
        "soma": {
          "total": 1414,
          "algum": 520,
          "dnAlgum": 36.8,
          "dois": 520,
          "dnDois": 36.8,
          "todos": 283,
          "dnTodos": 20.0
        },
        "kids200": {
          "total": 1414,
          "pdvs": 520,
          "dn": 36.8
        },
        "spray170": {
          "total": 1414,
          "pdvs": 469,
          "dn": 33.2
        },
        "locao200": {
          "total": 1414,
          "pdvs": 283,
          "dn": 20.0
        }
      },
      "202512": {
        "soma": {
          "total": 1587,
          "algum": 542,
          "dnAlgum": 34.2,
          "dois": 542,
          "dnDois": 34.2,
          "todos": 262,
          "dnTodos": 16.5
        },
        "kids200": {
          "total": 1587,
          "pdvs": 262,
          "dn": 16.5
        },
        "spray170": {
          "total": 1587,
          "pdvs": 542,
          "dn": 34.2
        },
        "locao200": {
          "total": 1587,
          "pdvs": 513,
          "dn": 32.3
        }
      },
      "202601": {
        "soma": {
          "total": 1514,
          "algum": 458,
          "dnAlgum": 30.3,
          "dois": 458,
          "dnDois": 30.3,
          "todos": 394,
          "dnTodos": 26.0
        },
        "kids200": {
          "total": 1514,
          "pdvs": 458,
          "dn": 30.3
        },
        "spray170": {
          "total": 1514,
          "pdvs": 437,
          "dn": 28.9
        },
        "locao200": {
          "total": 1514,
          "pdvs": 394,
          "dn": 26.0
        }
      },
      "202602": {
        "soma": {
          "total": 1137,
          "algum": 352,
          "dnAlgum": 31.0,
          "dois": 352,
          "dnDois": 31.0,
          "todos": 199,
          "dnTodos": 17.5
        },
        "kids200": {
          "total": 1137,
          "pdvs": 310,
          "dn": 27.3
        },
        "spray170": {
          "total": 1137,
          "pdvs": 352,
          "dn": 31.0
        },
        "locao200": {
          "total": 1137,
          "pdvs": 199,
          "dn": 17.5
        }
      },
      "202603": {
        "soma": {
          "total": 1658,
          "algum": 592,
          "dnAlgum": 35.7,
          "dois": 592,
          "dnDois": 35.7,
          "todos": 465,
          "dnTodos": 28.0
        },
        "kids200": {
          "total": 1658,
          "pdvs": 592,
          "dn": 35.7
        },
        "spray170": {
          "total": 1658,
          "pdvs": 495,
          "dn": 29.9
        },
        "locao200": {
          "total": 1658,
          "pdvs": 465,
          "dn": 28.0
        }
      },
      "202604": {
        "soma": {
          "total": 1941,
          "algum": 896,
          "dnAlgum": 46.2,
          "dois": 896,
          "dnDois": 46.2,
          "todos": 720,
          "dnTodos": 37.1
        },
        "kids200": {
          "total": 1941,
          "pdvs": 896,
          "dn": 46.2
        },
        "spray170": {
          "total": 1941,
          "pdvs": 755,
          "dn": 38.9
        },
        "locao200": {
          "total": 1941,
          "pdvs": 720,
          "dn": 37.1
        }
      }
    }
  }
};
