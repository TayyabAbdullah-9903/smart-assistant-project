
    """Auto-generated UML rendering script
    Diagram type: activity
    """

    PLANTUML_SOURCE = r"""```plantuml
@startuml
' Wheels and tires MOBILITY

start
:Tire or wheel changed?;
if (Yes) then (Yes)
  :Enter correct tire details in tire settings;
endif

:Tire Pressure Monitor monitors tire pressure;
:Warning if tire pressure drops?;
if (Yes) then (Yes)
  :Stop and check tires as soon as possible;
  :Inflate tires to proper pressure;
endif

:Driving for a few minutes?;
if (No) then (No)
  stop
endif

:Sensors measure tire pressure and temperature;
:Reset after tire/wheel replacement?;
if (Yes) then (Yes)
  :Reset with correct tire inflation pressure;
endif

:Tires with special approval?;
if (Yes) then (Yes)
  :Actively reset the system;
  :System takes actual pressures as target pressures;
endif

:Tire pressure adjusted?;
if (Yes) then (Yes)
  :Reset performed?;
  if (Yes) then (Yes)
  endif
endif

:Note information in Tire inflation pressure chapter;
:Tire sizes from vehicle/tires;
:Tire details do not need re-entry for pressure correction;
:Check tire inflation pressure of emergency wheel regularly;
:Correct if needed;
:Declaration according to NHTSA/FMVSS 138;
:Check tires monthly when cold;
:Inflate to recommended pressure;
:TPMS malfunction indicator?;
if (Yes) then (Yes)
  :Telltale flashes then remains illuminated;
  :System may not detect/signal low pressure;
  :Check TPMS malfunction telltale after replacement tires/wheels;
endif

:Sudden tire pressure loss?;
if (Yes) then (Yes)
  :System cannot indicate sudden serious tire damage;
endif

:Failure performing a reset?;
if (Yes) then (Yes)
  :System will not function correctly;
  :Flat tire may be indicated although pressures are correct;
endif

:Malfunction Message?;
if (Yes) then (Yes)
  :Yellow warning light flashes and is then illuminated;
  :Check Control message is displayed;
  :It may not be possible to identify tire pressure losses;
endif

:Measure - wheel without wheel electronics?;
if (Yes) then (Yes)
  :Have the wheels checked, if needed;
endif

:Fault caused by systems/devices with same radio frequency?;
if (Yes) then (Yes)
  :System automatically becomes active again after leaving area of interference;
endif

:Tires with special approval: unable to complete reset?;
if (Yes) then (Yes)
  :Perform a system reset again;
endif

:Tire Pressure Monitor malfunction?;
if (Yes) then (Yes)
  :Have the system checked by a manufacturer service center or another qualified service center or repair shop;
endif

:Check using tire inflation pressure specifications in the tire inflation pressure table;
:Reinitialize the Flat Tire Monitor;
:With Tire Pressure Monitor: Corrected tire inflation pressures are applied automatically;
:Make sure that the correct tire settings have been made;
:Determine the intended tire inflation pressure levels for the mounted tires;
:With tires that cannot be found in the tire pressure values on the Control Display, reset the Tire Pressure Monitor TPM;
:Check the tire inflation pressure in all four tires, using a pressure gage, for example;
:Correct the tire inflation pressure if the actual tire inflation pressure deviates from the intended tire inflation pressure;
:Check whether all valve caps are screwed onto the tire valves;
:For speeds of up to 100 mph/160 km/h and for optimum driving comfort, note the pressure values in the tire inflation pressure table and adjust as necessary;
:The tire inflation pressure specifications in the tire inflation pressure table only relate to cold tires or tires at the same temperature as the ambient temperature;
:Only check the tire inflation pressure levels when the tires are cold, i.e.:A driving distance of max. 1.25 miles/2 km has not been exceeded. If the vehicle has not moved again for at least 2 hours after a trip;
:Checking using the tire inflation pressure specifications on the Control Display;
:Do not exceed a speed of 100 mph/160 km/h;
:1. "CAR";
:2. "Vehicle status";
:3. "Tire Pressure Monitor";
:4. Check whether the current tire inflation pressure levels deviate from the intended tire pressure value;
:5. Correct the tire inflation pressure if the actual tire inflation pressure deviates from the intended tire inflation pressure;
:After correcting the tire pressure;
:With runflat tires;
stop
@enduml
```"""

    import re, networkx as nx, matplotlib.pyplot as plt
    from graphviz import Source

    def extract_edges(puml_text):
        edges = []
        for line in puml_text.splitlines():
            line = line.strip()
            m = re.match(r'"?([^"\(]+)"?\s*-+>+\s*"?([^"\)]+)"?', line)
            if m:
                edges.append(m.groups())
        return edges

    edges = extract_edges(PLANTUML_SOURCE)
    G = nx.DiGraph()
    G.add_edges_from(edges)
    nx.draw_networkx(G, with_labels=True, node_color='lightblue', node_size=2500, arrows=True)
    plt.axis('off')
    plt.show()
