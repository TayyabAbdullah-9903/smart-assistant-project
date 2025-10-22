
    """Auto-generated UML rendering script
    Diagram type: activity
    """

    PLANTUML_SOURCE = r"""@startuml
(*) --> "Tire/Wheel Change"
--> "Enter tire details in tire settings"
--> IF "Tires with special approval?" THEN
  --> [Yes] "Reset TPMS"
  --> "Compare predefined target pressures with actual tire pressures"
  --> "Monitor tire pressure"
  --> IF "Tire pressure drops?" THEN
    --> [Yes] "Issue warning"
    --> (*)
  ELSE
    --> [No] (*)
  ENDIF
ELSE
  --> [No] "Compare predefined target pressures with actual tire pressures"
  --> "Monitor tire pressure"
  --> IF "Tire pressure drops?" THEN
    --> [Yes] "Issue warning"
    --> (*)
  ELSE
    --> [No] (*)
  ENDIF
ENDIF
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
