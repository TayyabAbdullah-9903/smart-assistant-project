from uml.utils import render_plantuml_url

p = "@startuml\nstart\n:Ensure trip meter is displayed;\n:Push and hold indicator selector knob (0);\nstop\n@enduml"


url = render_plantuml_url(p)
print("✅ Open this URL in your browser:\n", url)