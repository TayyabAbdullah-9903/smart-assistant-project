
    """Auto-generated UML rendering script
    Diagram type: activity
    """

    PLANTUML_SOURCE = r"""@startuml
(*) --> "Tire or wheel changed?"
if "Yes" then
  --> "Enter correct tire details in tire settings"
endif
--> "Tire Pressure Monitor monitors tire pressure"
--> "Tire pressure dropped?"
if "Yes" then
  --> "Issue warning"
endif
--> "Driving for a few minutes?"
if "Yes" then
  --> "Tire Pressure Monitor activates"
endif
--> "Tires with special approval used?"
if "Yes" then
  --> "Reset system"
  --> "System takes over actual tire inflation pressures as target pressures"
else
  --> "System automatically compares predefined target pressures with actual tire inflation pressures"
endif
--> "Tire inflation pressure adjusted to a new value?"
if "Yes" then
  --> "Reset system"
endif
--> "Determine intended tire inflation pressure levels"
--> "Check tire inflation pressure in all four tires"
--> "Correct tire inflation pressure if needed"
--> "Check valve caps"
--> "Check using tire inflation pressure specifications in the tire inflation pressure table or Control Display"
--> "Correct tire inflation pressure if needed"
--> "After correcting tire pressure"
--> "Tire pressure loss warning?"
if "Yes" then
  --> "Stop and check tires"
  --> "Inflate tires to proper pressure"
endif
--> "TPMS malfunction indicator illuminated?"
if "Yes" then
  --> "System may not be able to detect or signal low tire pressure"
endif
--> "Sudden tire pressure loss?"
if "Yes" then
  --> "System cannot indicate"
endif
--> "Failure performing a reset?"
if "Yes" then
  --> "System will not function correctly"
endif
--> "Malfunction Message?"
if "Yes" then
  --> "Check Control message displayed"
  --> "May not be possible to identify tire pressure losses"
endif
--> "Wheel without wheel electronics mounted?"
if "Yes" then
  --> "Have wheels checked"
endif
--> "Fault caused by systems or devices with the same radio frequency?"
if "Yes" then
  --> "After leaving the area of interference, the system automatically becomes active again"
endif
--> "Tires with special approval and system unable to complete reset?"
if "Yes" then
  --> "Perform a system reset again"
endif
--> "Tire Pressure Monitor malfunction?"
if "Yes" then
  --> "Have system checked by a manufacturer service center or another qualified service center or repair shop"
endif
--> (*)
@enduml
"""

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
