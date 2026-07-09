QUESTIONS = {

"superadmin":[

{
"id":101,
"question":"Show all vehicles",
"intent":"devices",
"function":"get_all_devices"
},


{
        "id": 3111,
        "question":"Show speciifc vehicle ",
      
        "intent": "devices",
        "function": "get_superadmin_vehicle_details",
        "fields": [
          {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
          }
        ]
      },
      
{
  "id": 3339,
  "question": "Show vehicle geofence by school, branch or route",
  "intent": "devices",
  "function": "get_device_geofence_superadmin",
  "fields": [
    {
      "name": "location_name",
      "type": "text",
      "label": "Enter School, Branch or Route Name",
      "placeholder": "Example: Anandwadi"
    },
    {
      "name": "vehicle_name",
      "type": "text",
      "label": "Enter Vehicle Name",
      "placeholder": "Example: MH31FC7874"
    }
  ]
},
{
    "id": 400,
    "question": "Show Schools",
    "intent": "schools",
    
    "function": "find_school_superadmin",
},
{
    "id": 4000,
    "question": "Show branch",
    "intent": "schools",
    
    "function": "find_branch_superadmin",
},


{
        "id": 3113,
        "question":"Show specific branch ",
      
        "intent": "school",
        "function": "find_specific_branch_superadmin",
        "fields": [
          {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
          }
        ]
      },
{
        "id": 3112,
        "question":"Show specific school ",
      
        "intent": "school",
        "function": "find_specific_school_superadmin",
        "fields": [
          {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
          }
        ]
      },
{
        "id": 3119,
        "question":"all devices km report overall",
      
        "intent": "devices",
        "function": "get_superadmin_single_vehicle_km_report",
        "fields": [
          {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
          }
        ]
      },
{
"id":104,
"question":"Show all vehicle locations",
"intent":"vehiclelastpositions",
"function":"get_all_last_positions"
},

{
"id":105,
"question":"Show active vehicles",
"intent":"vehiclelastpositions",
"function":"get_active_vehicles"
},

{
"id":106,
"question":"Show stopped vehicles",
"intent":"vehiclelastpositions",
"function":"get_stopped_vehicles"
},

{
"id":107,
"question":"Vehicle status report",
"intent":"report_status",
"function":"get_all_status_reports"
},

{
"id":108,
"question":"Distance report",
"intent":"distance",
"function":"get_all_distance_reports"
},

{
"id":109,
"question":"Trip report",
"intent":"trips",
"function":"get_all_trips"
},

{
"id":110,
"question":"Idle report",
"intent":"idle",
"function":"get_all_idle_reports"
},

{
"id":1230,
"question":"Stoppage report",
"intent":"stoppage",
"function":"get_all_stoppage_reports"
},

{
"id":1220,
"question":"Travel summary report",
"intent":"travel_summary",
"function":"get_all_travel_summaries"
},





{
"id":1520,
"question":"Show routes",
"intent":"routes",
"function":"get_route_count"
},

{
"id":1620,
"question":"Show all geofences",
"intent":"geofences",
"function":"get_all_geofences"
},

{
"id":1720,
"question":"Show geofence reports",
"intent":"geofencereports",
"function":"get_all_geofence_reports"
},

{
"id":1820,
"question":"Show subscriptions",
"intent":"subscriptions",
"function":"get_all_subscriptions"
},

{
"id":1920,
"question":"Show subscription history",
"intent":"subscription_history",
"function":"get_all_subscription_history"
},

{
"id":2020,
"question":"Show tickets",
"intent":"tickets",
"function":"get_all_tickets"
},

{
"id":2120,
"question":"Show user sessions",
"intent":"sessions",
"function":"get_all_sessions"
}

],


"school": [
  {
    "id": 1,
    "question": "Show school details",
    "intent": "schools",
    "function": "get_school_profile"
  },
  
 {
    "id": 100,
    "question": "Show branch details",
    "function": "get_school_single_branch",
    "fields": [
        {
            "type": "text",
            "name": "branch_name",
            "label": "Branch Name",
            "placeholder": "Enter branch name"
        }
    ]
},
  {
    "id": 2,
    "question": "Show school vehicles",
    "intent": "devices",
    "function": "get_school_devices",
    "options": [
      {
        "id": 89,
        "label": "Show all school vehicles",
        "intent": "all_school_devices",
        "function": "get_school_devices"
      },
      {
        "id": 17,
        "label": "Show specific vehicle",
        "intent": "device",
        "function": "get_school_single_vehicle",
        "fields": [
          {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
          }
        ]
      }
    ]
  },
 {
        "id": 89,
         "question": "Show school vehicle status report",
        "intent": "all_school_devices",
        "function": "get_school_devices",
        "hidden":True,
      },
  {
    "id": 3,
    "question": "Show school vehicle status report",
    "intent": "status",
    "function": "get_school_status_report",
    "options": [
      {
        "id": 24,
        "label": "Show all vehicle status",
        "intent": "all_vehicle_status",
        "function": "get_school_status_report"
      },
      {
        "id": 18,
        "label": "Show specific vehicle status",
        "intent": "single_vehicle_status",
        "function": "get_single_school_vehicle_status",
        "fields": [
          {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
          }
        ]
      }
    ]
  },

{
  "id": 4,
  "question": "Show school vehicle distance report",
  "intent": "distance",
  "function": "get_school_distance_report",
  "options": [
    {
      "id": 25,
      "label": "Show all vehicle today distance",
      "intent": "all_vehicle_distance",
      "function": "get_school_distance_report"
    },
    {
      "id": 58,
      "label": "Show specific vehicle today distance",
      "intent": "single_vehicle_distance",
      "function": "get_school_today_accurate_distance",
      "fields": [
        {
          "name": "vehicle_input",
          "label": "Vehicle Name or Unique ID",
          "placeholder": "Enter vehicle name or unique ID"
        }
      ]
    },
    {
      "id": 32,
      "label": "Show all vehicles last active distance",
      "intent": "all_daily_distance",
      "function": "get_school_daily_distance"
    },
   
    {
      "id": 33,
      "label": "Show specific vehicle last active distance",
      "intent": "specific_vehicle_daily_distance",
      "function": "get_specific_vehicle_daily_distance",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Unique ID",
          "placeholder": "MH28BB7564 or 866221070659540"
        }
      ]
    },
    {
      "id": 31,
      "label": "Show specific vehicle overall KM report",
      "intent": "single_vehicle_km_report",
      "function": "get_school_single_vehicle_km_report",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Unique ID",
          "placeholder": "MH28BB7564 or 866221070659540"
        }
      ]
    }
  ]
}
,

  {
    "id": 6,
    "question": "Show school travel summary",
    "intent": "travel_summary",
    "function": "get_school_travel_summary",
    "options": [
      {
        "id": 26,
        "label": "Show all vehicle travel summary",
        "intent": "all_vehicle_travel_summary",
        "function": "get_school_travel_summary"
      },
      {
        "id": 20,
        "label": "Show specific vehicle travel summary",
        "intent": "single_vehicle_travel_summary",
        "function": "get_specific_vehicle_travel_summary",
        "fields": [
          {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
          }
        ]
      }
    ]
  },

  {
    "id": 7,
    "question": "Show school idle report",
    "intent": "idle",
    "function": "get_school_idle_report",
    "options": [
      {
        "id": 27,
        "label": "Show all vehicle idle report",
        "intent": "all_vehicle_idle_report",
        "function": "get_school_idle_report"
      },
      {
        "id": 21,
        "label": "Show specific vehicle idle report",
        "intent": "single_vehicle_idle_report",
        "function": "get_specific_vehicle_idle_report",
        "fields": [
          {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
          }
        ]
      }
    ]
  },

  {
    "id": 8,
    "question": "Show school vehicle locations",
    "intent": "vehiclelastpositions",
    "function": "get_all_last_positions",
    "options": [
      {
        "id": 28,
        "label": "Show all vehicle locations",
        "intent": "all_vehicle_locations",
        "function": "get_all_last_positions"
      },
      {
        "id": 29,
        "label": "Show specific vehicle location",
        "intent": "single_vehicle_location",
        "function": "get_specific_vehicle_last_position",
        "fields": [
          {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
          }
        ]
      }
    ]
  },


  {
    "id": 10,
    "question": "Show school routes",
    "intent": "routes",
    "function": "get_route_school",
    "options": [
      {
        "id": 30,
        "label": "Show all school routes",
        "intent": "all_school_routes",
        "function": "get_route_school"
      },
     
    ]
  },

  {
    "id": 11,
    "question": "Show school geofences",
    "intent": "geofences",
    "function": "get_school_geofences"
  },
    {
      "id": 58,
      "question": "Show specific vehicle today distance",
      "intent": "single_vehicle_distance",
      "function": "get_school_today_accurate_distance",
      "hidden":True,
     },

  {
    "id": 17,
    "question": "Show Specific Vehicle",
    "intent": "device",
    "function": "get_school_single_vehicle",
    "hidden":  True,
    "fields": [
      {
        "name": "school_name",
        "type": "text",
        "label": "Enter School Name",
        "placeholder": "Example: Nagpur School"
      },
      {
        "name": "vehicle_input",
        "type": "text",
        "label": "Enter Vehicle Name or Unique ID",
        "placeholder": "Example: MH31FC7874"
      }
    ]
  },

  {
    "id": 18,
    "question": "Show Specific Vehicle Status Report",
    "intent": "report_status",
    "function": "get_single_school_vehicle_status",
    "hidden":  True,
    "fields": [
      {
        "name": "vehicle_input",
        "type": "text",
        "label": "Enter Vehicle Name or Unique ID",
        "placeholder": "Example: MH31FC7874"
      }
    ]
  },

  {
    "id": 19,
    "question": "Show Specific Vehicle Distance Report",
    "intent": "report_distance",
    "function": "get_specific_school_vehicle_distance_report",
    "hidden":  True,
    "fields": [
      {
        "name": "vehicle_input",
        "type": "text",
        "label": "Enter Vehicle Name or Unique ID",
        "placeholder": "Example: MH28BB7564"
      }
    ]
  },

  {
    "id": 20,
    "question": "Show Specific Vehicle Travel Summary",
    "intent": "travel_summary",
    "function": "get_specific_vehicle_travel_summary",
    "hidden":  True,
    "fields": [
      {
        "name": "vehicle_input",
        "label": "Vehicle Name or Unique ID",
        "placeholder": "Enter Vehicle Name or Unique ID"
      }
    ]
  },

  {
    "id": 21,
    "question": "Show Specific Vehicle Idle Report",
    "intent": "idle_report",
    "function": "get_specific_vehicle_idle_report",
    "hidden":  True,
    "fields": [
      {
        "name": "vehicle_input",
        "label": "Vehicle Name or Unique ID",
        "placeholder": "Enter Vehicle Name or Unique ID"
      }
    ]
  },

  {
    "id": 29,
    "question": "Show Specific Vehicle Last Position",
    "intent": "vehicle_last_position",
    "function": "get_specific_vehicle_last_position",
    "hidden":  True,
    "fields": [
      {
        "name": "vehicle_input",
        "label": "Vehicle Name or Unique ID",
        "placeholder": "Enter Vehicle Name or Unique ID"
      }
    ]
  },

  {
    "id": 34,
    "question": "Show Specific School Geofence",
    "intent": "geofence",
    "function": "get_school_specific_geofence",
    "hidden":  True,
    "fields": [
      {
        "name": "vehicle_input",
        "label": "Enter Geofence Name",
        "placeholder": "Patheya apartment"
      }
    ]
  },

  {
    "id": 33,
    "question": "Show Specific School Vehicle Daily Distance",
    "intent": "daily_distance_cache",
    "function": "get_specific_vehicle_daily_distance",
    "hidden":  True,
    "fields": [
      {
        "name": "vehicle_input",
        "label": "Enter Vehicle Name or Unique ID",
        "placeholder": "MH28BB7564 or 866221070659540"
      }
    ]
  },

  {
    "id": 22,
    "question": "Show Specific School Vehicle Route",
    "intent": "route",
    "function": "get_route_school_specific_vehicle",
    "hidden":  True,
    "fields": [
      {
        "name": "vehicle_input",
        "type": "text",
        "label": "Enter Vehicle Name or Unique ID",
        "placeholder": "Example: MH28BB7564"
      }
    ]
  },

  {
    "id": 23,
    "question": "Show Specific School Vehicle KM Report",
    "intent": "school_km_report",
    "function": "get_school_single_vehicle_km_report",
    "hidden":  True,
    "fields": [
      {
        "name": "vehicle_input",
        "label": "Enter Vehicle Name or Unique ID",
        "placeholder": "MH28BB7564 or 866221070659540"
      }
    ]
  },

  {
    "id": 22,
    "question": "Show school vehicles",
    "intent": "devices",
    "function": "get_school_devices",
    "hidden":  True
  },

  {
    "id": 24,
    "question": "Show school vehicle status report",
    "intent": "status",
    "function": "get_school_status_report",
    "hidden":  True
  },

  {
    "id": 25,
    "question": "Show school distance report",
    "intent": "distance",
    "function": "get_school_distance_report",
    "hidden":  True
  },

  {
    "id": 26,
    "question": "Show school travel summary",
    "intent": "travel_summary",
    "function": "get_school_travel_summary",
    "hidden":  True
  },

  {
    "id": 27,
    "question": "Show school idle report",
    "intent": "idle",
    "function": "get_school_idle_report",
    "hidden":  True
  },

  {
    "id": 28,
    "question": "Show school vehicle locations",
    "intent": "vehiclelastpositions",
    "function": "get_all_last_positions",
    "hidden":  True
  },

  {
    "id": 30,
    "question": "Show school routes",
    "intent": "routes",
    "function": "get_route_school",
    "hidden":  True
  },

  {
    "id": 31,
    "question": "Show School Vehicle KM Report",
    "intent": "school_km_report",
    "function": "get_school_single_vehicle_km_report",
    "hidden":  True,
  },

  {
    "id": 32,
    "question": "Show School Daily Distance Cache",
    "intent": "daily_distance_cache",
    "function": "get_school_daily_distance",
    "hidden": True,
  }
],

"branch":[

{
"id":1,
"question":"Show branch details",
"intent":"branches",
"function":"get_branch_profile"
},

{
  "id": 2,
  "question": "Show branch vehicles",
  "intent": "devices",
  "function": "get_branch_devices",
  "options": [
    {
      "id": 22,
      "label": "Show all vehicles of branch",
      "intent": "all_branch_devices",
      "function": "get_branch_devices"
    },
    {
      "id": 13,
      "label": "Show specific vehicle",
      "intent": "device",
      "function": "get_branch_single_vehicle",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Unique ID",
          "placeholder": "Example: MH31FC7874"
        }
      ]
    }
  ]
}
,
# {
# "id":3,
# "question":"Show branch vehicle status",
# "intent":"status",
# "function":"get_branch_status_report"
# },
{
  "id": 3,
  "question": "Show branch vehicle status report",
  "intent": "status",
  "function": "get_branch_status_report",
  "options": [
    {
      "id": 24,
      "label": "Show all vehicles status",
      "intent": "all_vehicle_status",
      "function": "get_branch_status_report"
    },
    {
      "id": 14,
      "label": "Show specific vehicle status",
      "intent": "single_vehicle_status",
      "function": "get_single_branch_vehicle_status",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or ID",
          "placeholder": "Example: MH31FC7874"
        }
      ]
    }
  ]
},

{
  "id": 4,
  "question": "Show branch vehicle distance report",
  "intent": "distance",
  "function": "get_branch_distance_report",
  "options": [
    {
      "id": 25,
      "label": "All vehicle Today distance ",
      "intent": "all_vehicle_distance",
      "function": "get_branch_distance_report"
    },

    {
    "id": 58,
     "label": "specific vehicle Today  distance",
      "intent": "single_vehicle_distance",
    "function": "get_branch_today_accurate_distance",
     
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Vehicle Name or Unique ID",
            "placeholder": "Enter vehicle name or unique ID"
        }
    ]
},
    {
      "id": 30,
      "label": "all vehicles last active ",
      "intent": "all_daily_distance",
      "function": "get_branch_daily_distance"
    },
     {
      "id": 20,
      "label": "Specific vehicle last active ",
      "intent": "specific_vehicle_daily_distance",
      "function": "get_specific_vehicle_daily_distance",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Unique ID",
          "placeholder": "Example: MH28BB7564 or 866221070659540"
        }
      ]
    },
      {
      "id": 45,
      "label": "Specific vehicle overall KM report",
      "intent": "single_vehicle_km_report",
      "function": "get_single_vehicle_km_report",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Unique ID",
          "placeholder": "MH28BB7564 or 866221070659540"
        }
      ]
    }
  ]
}
,



{
  "id": 6,
  "question": "Show branch travel summary",
  "intent": "travel_summary",
  "function": "get_branch_travel_summary",
  "options": [
    {
      "id": 26,
      "label": "Show all vehicles travel summary",
      "intent": "all_vehicle_travel_summary",
      "function": "get_branch_travel_summary"
    },
    {
      "id": 16,
      "label": "Show specific vehicle travel summary",
      "intent": "single_vehicle_travel_summary",
      "function": "get_specific_vehicle_travel_summary",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or ID",
          "placeholder": "Example: MH31FC7874"
        }
      ]
    }
  ]
}
,


{
  "id": 7,
  "question": "Show branch idle report",
  "intent": "idle",
  "function": "get_branch_idle_report",
  "options": [
    {
      "id": 27,
      "label": "Show all vehicles idle report",
      "intent": "all_vehicle_idle_report",
      "function": "get_branch_idle_report"
    },
    {
      "id": 17,
      "label": "Show specific vehicle idle report",
      "intent": "single_vehicle_idle_report",
      "function": "get_specific_vehicle_idle_report",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or ID",
          "placeholder": "Example: MH31FC7874"
        }
      ]
    }
  ]
},


{
  "id": 8,
  "question": "Show branch vehicle locations",
  "intent": "vehiclelastpositions",
  "function": "get_all_last_positions",
  "options": [
    {
      "id": 28,
      "label": "Show all vehicle locations",
      "intent": "all_vehicle_locations",
      "function": "get_all_last_positions"
    },
    {
      "id": 18,
      "label": "Show specific vehicle location",
      "intent": "single_vehicle_location",
      "function": "get_specific_vehicle_last_position",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or ID",
          "placeholder": "Example: MH31FC7874"
        }
      ]
    }
  ]
},

{
  "id": 9,
  "question": "Show branch route details",
  "intent": "routes",
  "function": "get_route_branch",
  "options": [
    {
      "id": 29,
      "label": "Show all branch routes",
      "intent": "all_branch_routes",
      "function": "get_route_branch"
    },
   
  ]
},

{
"id":10,
"question":"Show branch geofences",
"intent":"geofences",
"function":"get_branch_geofences",
"hidden":True,
},
{
    "id": 2119430,
    "question": "Show geofences for a specific vehicle",
    "function":"get_specific_vehicle_branch_geofences",
    "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Enter Vehicle Number",
            "placeholder": "Example: MH31AB1234"
        }
    ]
},
{
  "id": 10,
  "question": "Show branch geofences",
  "intent": "geofences",
  "function": "get_branch_geofences",
  "options": [
    {
      "id": 28,
      "label": "Show all branch geofences",
      "intent": "all_branch_geofences",
      "function": "get_branch_geofences"
    },
    {
      "id": 2119430,
      "label": "Show geofences for a specific vehicle",
      "intent": "specific_vehicle_geofences",
      "function": "get_specific_vehicle_branch_geofences",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Number",
          "placeholder": "Example: MH31AB1234"
        }
      ]
    }
  ]
},
{
  "id": 11,
  "question": "Show branch daily distance report",
  "intent": "daily_distance_cache",
  "function": "get_branch_daily_distance",
  "hidden":True,
  "options": [
    {
      "id": 30,
      "label": "Show all vehicles daily distance",
      "intent": "all_daily_distance",
      "function": "get_branch_daily_distance",
      "hidden":True,
    },
    
    {
      "id": 20,
      "label": "Show specific vehicle last active distance",
      "intent": "specific_vehicle_daily_distance",
      "function": "get_specific_vehicle_daily_distance",
      "hidden":True,
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Unique ID",
          "placeholder": "Example: MH28BB7564 or 866221070659540"
        }
      ]
    }
  ]
},
# {
#   "id": 11,
#   "question": "Show branch km report",
#   "intent": "branch_km_report",
#   "function": "get_branch_vehicle_km_report"
# },

# {
# "id":12,
# "question":"Show branch geofences reports",
# "intent":"geofences",
# "function":"get_branch_geofences_reports"
# },
{
    "id": 13,
    "question": "Show Specific Vehicle",
    "intent": "device",
    "function": "get_branch_single_vehicle",
    "hidden":True,
    "fields": [
        {
            "name": "branch_name",
            "type": "text",
            "label": "Enter Branch Name",
            "placeholder": "Example: Nagpur Branch"
        },
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
        }
    ]
},
{
    "id": 14,
    "question": "Show Specific Vehicle Status Report",
    "intent": "report_status",
    "function": "get_single_branch_vehicle_status",
     "hidden":True,
    "fields": [
       
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH31FC7874"
        }
    ]
}
,
{
    "id": 15,
    "question": "Show Specific Vehicle Distance Report",
    "intent": "report_distance",
    "function": "get_specific_vehicle_distance_report",
     "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH28BB7564"
        }
    ]
},
{
    "id": 16,
    "question": "Show Specific Vehicle Travel Summary",
    "intent": "travel_summary",
    "function": "get_specific_vehicle_travel_summary",
     "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Vehicle Name or Unique ID",
            "placeholder": "Enter Vehicle Name or Unique ID"
        }
    ]
},
{
    "id": 17,
    "question": "Show Specific Vehicle Idle Report",
    "intent": "idle_report",
    "function": "get_specific_vehicle_idle_report",
     "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Vehicle Name or Unique ID",
            "placeholder": "Enter Vehicle Name or Unique ID"
        }
    ]
},
{
    "id": 18,
    "question": "Show Specific Vehicle Last Position",
    "intent": "vehicle_last_position",
    "function": "get_specific_vehicle_last_position",
     "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Vehicle Name or Unique ID",
            "placeholder": "Enter Vehicle Name or Unique ID"
        }
    ]
},
{
    "id": 18,
    "question": "Show Specific Branch Geofence",
    "intent": "geofence",
    "function": "get_specific_vehicle_branch_geofences",
     "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Enter Geofence Name",
            "placeholder": "Patheya apartment"
        }
    ]
},


{
    "id": 20,
    "question": "Show Specific Branch Vehicle Daily Distance",
    "intent": "daily_distance_cache",
    "function": "get_specific_vehicle_daily_distance",
     "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "MH28BB7564 or 866221070659540"
        }
    ]
},
{
    "id": 21,
    "question": "Show specific branch vehicle route",
    "intent": "Show specific branch vehicle route",
    "function": "get_route_branch_specific_vehicle",
    "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "MH28BB7564 or 866221070659540"
        }
    ]
},
{
"id":22,
 "question":"Show branch vehicles",
 "intent":"devices",
 "function":"get_branch_devices",
  "hidden":True,
 },

{
  "id": 24,
  "question": "Show branch vehicle status report",
  "intent": "status",
  "function": "get_branch_status_report",
   "hidden":True,
},
{
"id":25,
"question":"Show branch distance report",
"intent":"distance",
"function":"get_branch_distance_report",
 "hidden":True,
},
{
"id":26,
"question":"Show branch travel summary",
"intent":"travel_summary",
"function":"get_branch_travel_summary",
 "hidden":True,
},
{
"id":27,
"question":"Show branch idle report",
"intent":"idle",
"function":"get_branch_idle_report",
 "hidden":True,
},
{
"id":28,
"question":"Show branch vehicles location",
"intent":"vehiclelastpositions",
"function":"get_all_last_positions",
 "hidden":True,
},
{
"id":29,
"question":"Show branch routes",
"intent":"routes",
"function":"get_route_branch",
 "hidden":True,

},
{
    "id": 30,
    "question": "Show Branch Daily Distance Cache",
    "intent": "daily_distance_cache",
    "function": "get_branch_daily_distance",
     "hidden":True,
},
 {
      "id": 46,
      "label": "Show all vehicles KM report",
      "intent": "all_vehicle_km_report",
      "function": "calculate_week_month_distance",
      "hidden":True,
       "fields": [
        {
            "name": "vehicle_input",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "MH28BB7564 or 866221070659540"
        }
    ]
    },
{
    "id": 45,
    "question": "Show specific branch vehicle KM report",
    "intent": "Show specific branch vehicle KM report",
    "function": "get_branch_single_vehicle_km_report",
     "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "MH28BB7564 or 866221070659540"
        }
    ]
},
{
    "id": 58,
    "question": "Show today's accurate distance for a vehicle",
    "function": "get_branch_today_accurate_distance",
     "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Vehicle Name or Unique ID",
            "placeholder": "Enter vehicle name or unique ID"
        }
    ]
}

],


"driver":[

{
"id":1,
"question":"Show my vehicle",
"intent":"devices",
"function":"get_driver_device"
},

{
"id":2,
"question":"Show my vehicle location",
"intent":"vehiclelastpositions",
"function":"get_all_last_positions"
},


{
"id":3,
"question":"Show my distance report",
"intent":"distance",
"function":"get_driver_distance_report"
},

{
"id":4,
"question":"Show my trips",
"intent":"trips",
"function":"get_driver_trips"
},

{
"id":5,
"question":"Show my vehicle status",
"intent":"status",
"function":"get_driver_status_report"
},

{
"id":6,
"question":"Show my travel summary",
"intent":"travel_summary",
"function":"get_driver_travel_summary"
},

{
"id":7,
"question":"Show my idle report",
"intent":"idle",
"function":"get_driver_idle_report"
},

{
"id":8,
"question":"Show my stoppage report",
"intent":"stoppage",
"function":"get_driver_stoppage_report"
},

{
"id":9,
"question":"Show my geofences",
"intent":"geofences",
"function":"get_driver_geofences"
},

{
"id":10,
"question":"Show my subscription",
"intent":"subscriptions",
"function":"get_driver_subscription"
},
{
    "id":  11,
    "question": "Show My Daily Distance Cache",
    "intent": "daily_distance_cache",
    "function": "get_driver_daily_distance"
},

]
, 
"branchgroup": [
  {
    "id": 1222,
    "question": "Show branch group details",
    "function": "get_branch_group_profile",
  
}, {
    "id": 1229,
    "question": "Show branches assign",
    "function": "get_assigned_branches",
  
},
{
    "id": 1233,
    "question": "Show schools ",
    "function": "get_assigned_school_super",
  
},{
    "id": 12311,
    "question": "Show all vehicle associated ",
    "function": "get_branchgroup_devices",
  
},
    

{
    "id": 22222,
    "question": "Show vehicle devices by school or branch",
    "intent": "branchgroup_vehicle_devices",
    "function": "get_branchgroup_vehicle_school_branch",
    
},
{
    "id": 222299,
    "question": "Show today's distance report for branch group vehicle",
    "intent": "branchgroup_vehicle_distance",
    "function": "get_branchgroup_vehicle_today_distance",
    
},
{
    "id": 222306,
    "question": "Show branch group geofences",
    "intent": "branchgroup_geofence",
    "function": "get_branchgroup_geofences"
},
{
    "id": 2223011,
    "question": "Show travel summary of branch group vehicles",
    "intent": "branchgroup_travel_summary",
    "function": "get_branchgroup_travel_summary"
},
{
    "id": 22230344,
    "question": "Show status report of branch group vehicles",
    "intent": "branchgroup_vehicle_status",
    "function": "get_branchgroup_vehicle_status_report"
},

{
    "id": 22821344,
    "question": "Show last locations",
    "intent": "branchgroup_vehicle_status",
    "function": "get_branchgroup_vehicle_last_positions"
},

{
    "id": 11111111,
    "question": "Show  branchgroup routes ",
    "intent": "branchgroup routes",
    "function": "get_branchgroup_routes"
}
,





  

  
]
}