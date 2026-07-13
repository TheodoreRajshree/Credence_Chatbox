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
      
# {
#   "id": 3339,
#   "question": "Show vehicle geofence by school, branch or route",
#   "intent": "devices",
#   "function": "get_device_geofence_superadmin",
#   "fields": [
#     {
#       "name": "location_name",
#       "type": "text",
#       "label": "Enter School, Branch or Route Name",
#       "placeholder": "Example: Anandwadi"
#     },
#     {
#       "name": "vehicle_name",
#       "type": "text",
#       "label": "Enter Vehicle Name",
#       "placeholder": "Example: MH31FC7874"
#     }
#   ]
# },
{
    "id": 400,
    "question": "Show Admin ",
    "intent": "schools",
    
    "function": "find_school_superadmin",
},
{
    "id": 4000,
    "question": "Show Users",
    "intent": "schools",
    
    "function": "find_branch_superadmin",
},
{
  "id": 12293,
  "question": "Show Groups",
  "intent": "all_branchgroup_profile",
  "function": "get_all_branch_groups_profile"
},

# {
#   "id": 122011005,
#   "question": "Specific Branch Group Profile",
#   "intent": "specific_branchgroup_profile",
#   "function": "get_specific_branch_group_profile",
#   "fields": [
#     {
#       "name": "group_name",
#       "label": "Enter Branch Group Name",
#       "placeholder": "Mumbai Group"
#     }
#   ]
# },
{
        "id": 3113,
        "question":"Show Specific Users ",
      
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
        "question":"Show Specific Admin ",
      
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
    "id": 5099223333901,
    "question": "Show Specific Group ",
    "function": "get_specific_branch_group_profile",
    "fields": [
        {
            "name": "branchgroup_input",
            "type": "text",
            "label": "Enter Branch Group Name",
            "placeholder": "Example: Nagpur"
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
  "id": 21204001,
  "question": "Show vehicle KM report for a specific date",
  "function": "get_superadmin_vehicle_distance_by_date",
  "fields": [
    {
      "name": "vehicle_input",
      "type": "text",
      "label": "Enter Vehicle Name or Number",
      "placeholder": "Example: MH28BB7564"
    },
    {
      "name": "report_date",
      "type": "text",
      "label": "Enter Date",
      "placeholder": "Example: 08-02-2026"
    }
  ]
},
# {
# "id":104,
# "question":"Show all vehicle locations",
# "intent":"vehiclelastpositions",
# "function":"get_all_last_positions"
# },
{
  "id": 12209007,
  "question": "Show specific vehicle last position",
  "intent": "specific_vehicle_last_position",
  "function": "get_specific_vehicle_last_position",
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Unique ID",
      "placeholder": "MH05GA1153"
    }
  ]
}
,
# {
# "id":105,
# "question":"Show active vehicles",
# "intent":"vehiclelastpositions",
# "function":"get_active_vehicles"
# },
{
  "id": 12208008,
  "question": "Show specific active vehicle",
  "intent": "specific_active_vehicle",
  "function": "get_specific_active_vehicle",
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Unique ID",
      "placeholder": "MH05GA1153"
    }
  ]
},

# {
# "id":106,
# "question":"Show stopped vehicles",
# "intent":"vehiclelastpositions",
# "function":"get_stopped_vehicles"
# },
{
  "id": 122082009,
  "question": "Show specific stopped vehicle",
  "intent": "specific_stopped_vehicle",
  "function": "get_specific_stopped_vehicle",
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Unique ID",
      "placeholder": "MH05GA1153"
    }
  ]
},
# {
# "id":107,
# "question":"Vehicle status report",
# "intent":"report_status",
# "function":"get_all_status_reports"
# },
{
  "id": 1220822010,
  "question": "Show specific vehicle status report",
  "intent": "specific_vehicle_status_report",
  "function": "get_specific_status_report",
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Unique ID",
      "placeholder": "MH05GA1153"
    }
  ]
},
# {
# "id":108,
# "question":"Distance report",
# "intent":"distance",
# "function":"get_all_distance_reports"
# },
{
  "id": 122085011,
  "question": "Show specific vehicle distance report",
  "intent": "specific_vehicle_distance_report",
  "function": "get_specific_distance_report",
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Unique ID",
      "placeholder": "MH05GA1153"
    }
  ]
},
# {
# "id":109,
# "question":"Trip report",
# "intent":"trips",
# "function":"get_all_trips"
# },
{
  "id": 120208012,
  "question": "Show specific vehicle trip report",
  "intent": "specific_vehicle_trip_report",
  "function": "get_specific_trip_report",
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Unique ID",
      "placeholder": "MH05GA1153"
    }
  ]
},
# {
# "id":110,
# "question":"Idle report",
# "intent":"idle",
# "function":"get_all_idle_reports"
# },
{
  "id": 122208013,
  "question": "Show specific vehicle idle report",
  "intent": "specific_vehicle_idle_report",
  "function": "get_specific_idle_report",
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Unique ID",
      "placeholder": "MH05GA1153"
    }
  ]
}
,
# {
# "id":1230,
# "question":"Stoppage report",
# "intent":"stoppage",
# "function":"get_all_stoppage_reports"
# },

# {
# "id":1220,
# "question":"Travel summary report",
# "intent":"travel_summary",
# "function":"get_all_travel_summaries"
# },

{
  "id": 122080134,
  "question": "Show specific vehicle travel summary",
  "intent": "specific_vehicle_travel_summary",
  "function": "get_specific_travel_summary",
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Unique ID",
      "placeholder": "MH05GA1153"
    }
  ]
},



{
"id":1520,
"question":"Show routes",
"intent":"routes",
"function":"get_superadmin_route_profile"
},

# {
# "id":1620,
# "question":"Show all geofences",
# "intent":"geofences",
# "function":"get_all_geofences"
# },
{
  "id": 122086015,
  "question": "Show specific vehicle geofences",
  "intent": "specific_vehicle_geofences",
  "function": "get_specific_vehicle_geofences",
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Unique ID",
      "placeholder": "MH05GA1153"
    }
  ]
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
    "id": 777,
    "question": "Show branch geofences ",
    "intent": "geofence",
    "function": "get_school_user_branch_geofences",
  },
  {
  "id": 777544399,
  "question": "Show Specific Branch Vehicle Geofence",
  "intent": "geofence",
  "function": "get_school_user_branch_geofences",
  
  "fields": [
    {
      "name": "branch_name",
      "label": "Enter Branch Name",
      "placeholder": "Anandwadi Branch"
    }
  ]
},

{
  "id": 778111,
  "question": "Show specific branch speciifc vehicle geofence",
  "intent": "geofence",
  "function": "get_specific_vehicle_branch_of_school_geofences",
  
  "fields": [
    {
      "name": "branch_name",
      "label": "Enter Branch Name",
      "placeholder": "Anandwadi Branch"
    },
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Unique ID",
      "placeholder": "MH28BB7564 or 866221070659540"
    }
  ]
}
,
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
    "id": 1233,
    "question": "Branchgroup Profile ",
    "function": "get_branch_group_profile_only",
  
},
{
  "id": 1220,
  "question": "Show Branch and School Profile",
  "intent": "profile",
  "function": "get_branch_school_profile",
  "options": [
    {
      "id": 1222,
      "label": "All Assigned Branches",
      "intent": "all_branch_profile",
      "function": "get_branch_group_profile"
    },
    {
      "id": 1225,
      "label": "Specific Branch Profile",
      "intent": "specific_branch_profile",
      "function": "get_branchgroup_specific_branch",
      "fields": [
        {
          "name": "branch_name",
          "type": "text",
          "label": "Enter Branch Name",
          "placeholder": "Mumbai Branch"
        }
      ]
    },
    {
      "id": 12311,
      "label": "School Profile",
      "intent": "school_profile",
      "function": "get_assigned_school_branchgroup"
    }
  ]
},






  {
    "id": 1222,
    "question": "All Assign branches",
    "function": "get_branch_group_profile",
    "hidden":True,
  },

{
    "id": 1225,
    "question": "Specific branch  Profile",
    "intent": "branchgroup",
    "function": "get_branchgroup_specific_branch",
     "hidden":True,

    "fields":[
        {
            "name":"branch_name",
            "label":"Enter Branch Name",
            "placeholder":"Mumbai Branch"
        }
    ]
},
 
 {
    "id": 12311,
    "question": "School Profile",
    "function": "get_assigned_school_branchgroup",
     "hidden":True,
  
},
{
    "id": 123101,
    "question": "All vehicle of Branchgroup",
    "function": "get_branchgroup_devices",
    "hidden":True,
  
},
{
  "id": 88944445,
  "question": "Specific Vehicle of branchgroup",
  "intent": "vehicle",
  "function": "get_branchgroup_specific_vehicle",
  "hidden":True,
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Number",
      "placeholder": "MH05FJ3989"
    }
  ]
},
 {
  "id": 8889,
  "question": "Specific Vehicle of Branch",
  "intent": "vehicle",
  "function": "get_branchgroup_specific_branch_vehicles",
  "hidden":True,
  "fields": [
    {
      "name": "branch_name",
      "label": "Enter Branch Name",
      "placeholder": "Mumbai Branch"
    },
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Vehicle Number",
      "placeholder": "Bus 101 / MH12AB1234"
    }
  ]
},
{
  "id": 88913,
  "question": "School Specific  vehicle ",
  "intent": "vehicle",
  "function": "get_branchgroup_school_vehicle",
  "hidden":True,
  "fields": [
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Number",
      "placeholder": "MH05FJ3989"
    }
  ]
},





{
    "id": 1234956,
    "question": "Show all branch vehicles",
    "function": "get_branchgroup_branch_vehicles_1",
    "hidden":True,
},
{
    "id": 12349057,
    "question": "Show all school vehicles",
    "function": "get_branchgroup_school_all_vehicles_1",
    "hidden":True,
},
{
  "id": 123100,
  "question": "Show All Associated Vehicles",
  "intent": "vehicle_status",
  "function": "get_associated_vehicles",
  "options": [
    {
      "id": 123101,
      "label": "All Vehicles of Branch Group",
      "intent": "all_branchgroup_vehicles",
      "function": "get_branchgroup_devices"
    },
    {
      "id": 88944445,
      "label": "Specific Vehicle of Branch Group",
      "intent": "specific_branchgroup_vehicle",
      "function": "get_branchgroup_specific_vehicle",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Number",
          "placeholder": "MH05FJ3989"
        }
      ]
    },
  
{
    "id": 1234956,
    "label": "Show all branch vehicles",
    "function": "get_branchgroup_branch_vehicles_1",
},
   
    {
      "id": 8889,
      "label": "Specific Vehicle of Branch",
      "intent": "specific_branch_vehicle",
      "function": "get_branchgroup_specific_branch_vehicles",
      "fields": [
        {
          "name": "branch_name",
          "type": "text",
          "label": "Enter Branch Name",
          "placeholder": "Mumbai Branch"
        },
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Vehicle Number",
          "placeholder": "Bus 101 / MH12AB1234"
        }
      ]
    },
    {
    "id": 12349057,
    "label": "Show all school vehicles",
    "function": "get_branchgroup_school_all_vehicles_1",
  
},
    {
      "id": 88913,
      "label": "Specific School Vehicle",
      "intent": "specific_school_vehicle",
      "function": "get_branchgroup_school_vehicle",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Number",
          "placeholder": "MH05FJ3989"
        }
      ]
    }
  ]
},
# {
#   "id": 8892236,
#   "question": "Show Geofences for a Specific Vehicle",
#   "intent": "geofence",
#   "function": "get_branchgroup_specific_vehicle_geofence",
#   "fields": [
#     {
#       "name": "vehicle_input",
#       "label": "Enter Vehicle Name or Number",
#       "placeholder": "MH05FJ3989"
#     }
#   ]
# },
{
    "id": 2119950,
    "question": "Show geofences for a specific vehicle",
    "function": "get_branchgroup_specific_vehicle_geofences",
    "hidden":True,
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
  "id": 88922137,
  "question": "Show Specific Branch Vehicle Geofence",
  "intent": "geofence",
  "function": "get_branchgroup_specific_branch_vehicle_geofence",
   "hidden":True,
  "fields": [
    {
      "name": "branch_name",
      "label": "Enter Branch Name",
      "placeholder": "Mumbai Branch"
    },
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Number",
      "placeholder": "MH05GA1153"
    }
  ]
},



{
    "id": 88,
    "question": "Show school vehicle geofence",
    "function": "get_branchgroup_school_vehicle_geofence",
     "hidden":True,
    "fields":[
        {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Number",
      "placeholder": "MH05GA1153"
    }
    ]
},



{
    "id": 222306,
    "question": "Show branch group geofences",
    "intent": "branchgroup_geofence",
    "function": "get_branchgroup_geofences",
    "hidden":True,
},






 {
    "id": 211996544531,
    "question": "Show all school vehicle geofences",
    "function": "get_branchgroup_school_vehicle_geofences",
    "hidden":True,
},








{
  "id": 222300,
  "question": "Show Geofence Reports",
  "intent": "geofence_report",
  "function": "get_geofence_reports",
  "options": [
    {
      "id": 222306,
      "label": "Show Branch Group Geofences",
      "intent": "branchgroup_geofence",
      "function": "get_branchgroup_geofences"
    },
    {
    "id": 2119950,
    "label": "Show geofences of specific branchgroup vehicle",
    "function": "get_branchgroup_specific_vehicle_geofences",
    
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
      "id": 88922137,
      "label": "Show Specific Branch Vehicle Geofence",
      "intent": "specific_branch_vehicle_geofence",
      "function": "get_branchgroup_specific_branch_vehicle_geofence",
      "fields": [
        {
          "name": "branch_name",
          "type": "text",
          "label": "Enter Branch Name",
          "placeholder": "Mumbai Branch"
        },
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Number",
          "placeholder": "MH05GA1153"
        }
      ]
    },
   
     {
    "id": 211996544531,
    "label": "Show all school vehicle geofences",
    "function": "get_branchgroup_school_vehicle_geofences",
    
},
    {
      "id": 88,
      "label": "Show School Specific Vehicle Geofence",
      "intent": "school_vehicle_geofence",
      "function": "get_branchgroup_school_vehicle_geofence",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Number",
          "placeholder": "MH05GA1153"
        }
      ]
    }
  ]
},

# {
#     "id": 222299,
#     "question": "Show today's distance report for branch group vehicle",
#     "intent": "branchgroup_vehicle_distance",
#     "function": "get_branchgroup_vehicle_today_distance",
# },
{
  "id": 8845922138,
  "question": "Show specific branch vehicle today's distance",
  "function": "get_branchgroup_specific_branch_vehicle_today_distance",
   "hidden":True,
  "fields": [
    {
      "name": "branch_name",
      "label": "Enter Branch Name",
      "placeholder": "Mumbai Branch"
    },
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Number",
      "placeholder": "MH05GA1153"
    }
  ]
},

{
    "id": 59,
    "question": "Show branchgroup Today distance",
    "function": "get_branchgroup_vehicle_today_distance",
     "hidden":True,
    "fields":[
        {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Number",
      "placeholder": "MH05GA1153"
    }
    ]
},
{
 "id": 9865322,
 "question": "Show branch vehicle km distance report",
 "function": "get_branchgroup_specific_branch_vehicle_km_report",
  "hidden":True,
 "fields": [
    {
      "name": "branch_name",
      "label": "Enter Branch Name",
      "placeholder": "Mumbai Branch"
    },
    {
      "name": "vehicle_input",
      "label": "Enter Vehicle Name or Number",
      "placeholder": "MH05GA1153"
    }
  ]
},
{
    "id": 9812365323,
    "question": "Show branch group vehicle km distance report",
    "function": "get_branchgroup_vehicle_km_report",
     "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "label": "Enter Vehicle Name or Number",
            "placeholder": "MH05GA0884"
        }
    ]
},

{
    "id": 98654423,
    "question": "Show branch vehicle last active",
    "function": "get_branchgroup_specific_branch_vehicle_distance_report",
    "hidden":True,
    "fields": [
        {
            "name": "branch_name",
            "label": "Enter Branch Name",
            "placeholder": "Mumbai Branch"
        },
        {
            "name": "vehicle_input",
            "label": "Enter Vehicle Name or Number",
            "placeholder": "MH05GA1153"
        }
    ]
},




{
    "id": 21190952,
    "question": "Show today's distance for a school vehicle",
    "function": "get_branchgroup_school_vehicle_today_distance",
    "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter School Vehicle Name or Unique ID",
            "placeholder": "Example: MH40CG0301"
        }
    ]
},
{
  "id": 98654000,
  "question": "Show Vehicle Distance Reports",
  "intent": "distance_report",
  "function": "get_vehicle_distance_reports",
  "options": [
    {
      "id": 59,
      "label": "Show Branch Group Today Distance",
      "intent": "branchgroup_today_distance",
      "function": "get_branchgroup_vehicle_today_distance",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Number",
          "placeholder": "MH05GA1153"
        }
      ]
    },
    {
      "id": 8845922138,
      "label": "Show Specific Branch Vehicle Today's Distance",
      "intent": "specific_branch_vehicle_today_distance",
      "function": "get_branchgroup_specific_branch_vehicle_today_distance",
      "fields": [
        {
          "name": "branch_name",
          "type": "text",
          "label": "Enter Branch Name",
          "placeholder": "Mumbai Branch"
        },
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Number",
          "placeholder": "MH05GA1153"
        }
      ]
    },
    {
    "id": 21190952,
    "label": "Show today's distance for a school vehicle",
    "function": "get_branchgroup_school_vehicle_today_distance",
   
    "fields": [
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter School Vehicle Name or Unique ID",
            "placeholder": "Example: MH40CG0301"
        }
    ]
},
    {
      "id": 9812365323,
      "label": "Show Branch Group Vehicle KM Distance Report",
      "intent": "branchgroup_vehicle_km_report",
      "function": "get_branchgroup_vehicle_km_report",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Number",
          "placeholder": "MH05GA0884"
        }
      ]
    },
    {
      "id": 9865322,
      "label": "Show Branch Vehicle KM Distance Report",
      "intent": "specific_branch_vehicle_km_report",
      "function": "get_branchgroup_specific_branch_vehicle_km_report",
      "fields": [
        {
          "name": "branch_name",
          "type": "text",
          "label": "Enter Branch Name",
          "placeholder": "Mumbai Branch"
        },
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Number",
          "placeholder": "MH05GA1153"
        }
      ]
    },
    {
  "id": 211993354,
  "label": "Show school specific vehicle KM report",
  "function": "get_branchgroup_school_specific_vehicle_km_report",
 
  "fields": [
    {
      "name": "vehicle_input",
      "type": "text",
      "label": "Enter School Vehicle Name or Unique ID",
      "placeholder": "Example: MH40CG0301"
    }
  ]
},
    {
      "id": 98654423,
      "label": "Show Branch Vehicle Last Active Report",
      "intent": "branch_vehicle_last_active",
      "function": "get_branchgroup_specific_branch_vehicle_distance_report",
      "fields": [
        {
          "name": "branch_name",
          "type": "text",
          "label": "Enter Branch Name",
          "placeholder": "Mumbai Branch"
        },
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Number",
          "placeholder": "MH05GA1153"
        }
      ]
    }
    ,
    {
    "id": 21199953,
    "label": "Show School specific vehicle last active report",
    "function": "get_branchgroup_school_specific_vehicle_distance_report",
    
    "fields": [
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter School Vehicle Name or Unique ID",
            "placeholder": "Example: MH40CG0301"
        }
    ]
},
    {
    "id": 21199255,
    "label": "Show Branchgroup specific vehicle last active",
    "function": "get_branchgroup_specific_vehicle_distance_report",
  
    "fields": [
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH40CG0301"
        }
    ]
}
  ]
},
{
    "id": 21199953,
    "question": "Show distance report for a school vehicle",
    "function": "get_branchgroup_school_specific_vehicle_distance_report",
    "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter School Vehicle Name or Unique ID",
            "placeholder": "Example: MH40CG0301"
        }
    ]
},
{
  "id": 211993354,
  "question": "Show school specific vehicle KM report",
  "function": "get_branchgroup_school_specific_vehicle_km_report",
  "hidden":True,
  "fields": [
    {
      "name": "vehicle_input",
      "type": "text",
      "label": "Enter School Vehicle Name or Unique ID",
      "placeholder": "Example: MH40CG0301"
    }
  ]
},

















{
    "id": 21199255,
    "question": "Show Branchgroup specific vehicle last active",
    "function": "get_branchgroup_specific_vehicle_distance_report",
    "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH40CG0301"
        }
    ]
},





{
    "id": 2119957,
    "question": "Show status report for a specific vehicle of branchgroup",
    "function": "get_branchgroup_specific_vehicle_status",
      "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter Vehicle Name or Unique ID",
            "placeholder": "Example: MH40CG0301"
        }
    ]
},
{
    "id": 2119956,
    "question": "Show status report for a school specific vehicle",
    "function": "get_branchgroup_school_specific_vehicle_status",
      "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter School Vehicle Name or Unique ID",
            "placeholder": "Example: MH40CG0301"
        }
    ]
},
{
    "id": 9865554424,
    "question": "Show branch vehicle status report",
    "function": "get_branchgroup_specific_branch_vehicle_status",
    "hidden":True,
    "fields":[
        {
            "name":"branch_name",
            "label":"Enter Branch Name",
            "placeholder":"Mumbai Branch"
        },
        {
            "name":"vehicle_input",
            "label":"Enter Vehicle Name",
            "placeholder":"MH05GA0884"
        }
    ]
},






{
  "id": 98654001,
  "question": "Show Vehicle Status Reports",
  "intent": "vehicle_status_report",
  "function": "get_vehicle_status_reports",
  "options": [
    {
      "id": 2119957,
      "label": "Show Branch Group Vehicle Status Report",
      "intent": "branchgroup_vehicle_status",
      "function": "get_branchgroup_specific_vehicle_status",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Unique ID",
          "placeholder": "Example: MH40CG0301"
        }
      ]
    },
    {
      "id": 2119956,
      "label": "Show School Specific Vehicle Status Report",
      "intent": "school_specific_vehicle_status",
      "function": "get_branchgroup_school_specific_vehicle_status",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter School Vehicle Name or Unique ID",
          "placeholder": "Example: MH40CG0301"
        }
      ]
    },
    {
      "id": 9865554424,
      "label": "Show Branch Vehicle Status Report",
      "intent": "branch_specific_vehicle_status",
      "function": "get_branchgroup_specific_branch_vehicle_status",
      "fields": [
        {
          "name": "branch_name",
          "type": "text",
          "label": "Enter Branch Name",
          "placeholder": "Mumbai Branch"
        },
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name",
          "placeholder": "MH05GA0884"
        }
      ]
    }
  ]
},











{
  "id": 98654002,
  "question": "Show Vehicle Travel Summary Reports",
  "intent": "vehicle_travel_summary",
  "function": "get_vehicle_travel_summary_reports",
  "options": [
    {
      "id": 98655514424,
      "label": "Show Branch Vehicle Travel Summary Report",
      "intent": "branch_specific_vehicle_travel_summary",
      "function": "get_branchgroup_specific_branch_vehicle_distance_report",
      "fields": [
        {
          "name": "branch_name",
          "type": "text",
          "label": "Enter Branch Name",
          "placeholder": "Mumbai Branch"
        },
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name",
          "placeholder": "MH05GA0884"
        }
      ]
    },
    {
      "id": 21203001,
      "label": "Show School Specific Vehicle Travel Summary Report",
      "intent": "school_specific_vehicle_travel_summary",
      "function": "get_branchgroup_school_specific_vehicle_travel_summary",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter School Vehicle Name or Number",
          "placeholder": "Example: MH40CG0301"
        }
      ]
    },
    {
      "id": 212032002,
      "label": "Show Branch Group Vehicle Travel Summary Report",
      "intent": "branchgroup_specific_vehicle_travel_summary",
      "function": "get_branchgroup_specific_vehicle_travel_summary",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Number",
          "placeholder": "Example: MH40CG0301"
        }
      ]
    }
  ]
},



{
    "id": 98655514424,
    "question": "Show branch vehicle travel summary  report",
    "function": "get_branchgroup_specific_branch_vehicle_distance_report",
    "hidden":True,
    "fields":[
        {
            "name":"branch_name",
            "label":"Enter Branch Name",
            "placeholder":"Mumbai Branch"
        },
        {
            "name":"vehicle_input",
            "label":"Enter Vehicle Name",
            "placeholder":"MH05GA0884"
        }
    ]
},
{
  "id": 21203001,
  "question": "Show travel summary for a specific school vehicle",
  "function": "get_branchgroup_school_specific_vehicle_travel_summary",
    "hidden":True,
  "fields": [
    {
      "name": "vehicle_input",
      "type": "text",
      "label": "Enter School Vehicle Name or Number",
      "placeholder": "Example: MH40CG0301"
    }
  ]
},
{
  "id": 212032002,
  "question": "Show travel summary for a specific branch group vehicle",
  "function": "get_branchgroup_specific_vehicle_travel_summary",
    "hidden":True,
  "fields": [
    {
      "name": "vehicle_input",
      "type": "text",
      "label": "Enter Vehicle Name or Number",
      "placeholder": "Example: MH40CG0301"
    }
  ]
},












{
    "id": 986555141424,
    "question": "Show branch vehicle last position  report",
    "function": "get_branchgroup_specific_branch_vehicle_last_position",
    "hidden":True,
    "fields":[
        {
            "name":"branch_name",
            "label":"Enter Branch Name",
            "placeholder":"Mumbai Branch"
        },
        {
            "name":"vehicle_input",
            "label":"Enter Vehicle Name",
            "placeholder":"MH05GA0884"
        }
    ]
},
{
    "id": 21203003,
    "question": "Show last position for a specific school vehicle",
    "function": "get_branchgroup_school_specific_vehicle_last_position",
     "hidden":True,
    "fields": [
        {
            "name": "vehicle_input",
            "type": "text",
            "label": "Enter School Vehicle Name or Number",
            "placeholder": "Example: MH40CG0301"
        }
    ]
},
{
  "id": 21203004,
  "question": "Show last position for a specific branch group vehicle",
  "function": "get_branchgroup_specific_vehicle_last_position",
   "hidden":True,
  "fields": [
    {
      "name": "vehicle_input",
      "type": "text",
      "label": "Enter Vehicle Name or Vehicle Number",
      "placeholder": "Example: MH40CG0301"
    }
  ]
},
{
  "id": 98654003,
  "question": "Show Vehicle Last Position Reports",
  "intent": "vehicle_last_position",
  "function": "get_vehicle_last_position_reports",
  "options": [
    {
      "id": 986555141424,
      "label": "Show Branch Vehicle Last Position Report",
      "intent": "branch_specific_vehicle_last_position",
      "function": "get_branchgroup_specific_branch_vehicle_last_position",
      "fields": [
        {
          "name": "branch_name",
          "type": "text",
          "label": "Enter Branch Name",
          "placeholder": "Mumbai Branch"
        },
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name",
          "placeholder": "MH05GA0884"
        }
      ]
    },
    {
      "id": 21203003,
      "label": "Show School Specific Vehicle Last Position Report",
      "intent": "school_specific_vehicle_last_position",
      "function": "get_branchgroup_school_specific_vehicle_last_position",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter School Vehicle Name or Number",
          "placeholder": "Example: MH40CG0301"
        }
      ]
    },
    {
      "id": 21203004,
      "label": "Show Branch Group Vehicle Last Position Report",
      "intent": "branchgroup_specific_vehicle_last_position",
      "function": "get_branchgroup_specific_vehicle_last_position",
      "fields": [
        {
          "name": "vehicle_input",
          "type": "text",
          "label": "Enter Vehicle Name or Vehicle Number",
          "placeholder": "Example: MH40CG0301"
        }
      ]
    }
  ]
}
# {
#     "id": 4444,
#     "question": "s",
#     "intent": "branchgroup_travel_summary",
#     "function": "get_branchgroup_travel_summary"
# },
# {
#     "id": 2223011,
#     "question": "Show travel summary of branch group vehicles",
#     "intent": "branchgroup_travel_summary",
#     "function": "get_branchgroup_travel_summary"
# },
# {
#     "id": 22230344,
#     "question": "Show status report of branch group vehicles",
#     "intent": "branchgroup_vehicle_status",
#     "function": "get_branchgroup_vehicle_status_report"
# },

# {
#     "id": 22821344,
#     "question": "Show last locations",
#     "intent": "branchgroup_vehicle_status",
#     "function": "get_branchgroup_vehicle_last_positions"
# },

# {
#     "id": 11111111,
#     "question": "Show  branchgroup routes ",
#     "intent": "branchgroup routes",
#     "function": "get_branchgroup_routes"
# }






  

  
]
}